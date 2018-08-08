from struct import pack, calcsize
from functools import partial
from sys import stdout
from json import load
from io import TextIOWrapper
import argparse

class Compiler:
	REF_FMT = '<I'
	def __init__(self,engine):
		self.engine = engine
		self.compiled = {} # func_name: bytes
		self.references = {} # func_name: [ (position, reference)]
	def compile(self, f, *a, **k):
		funcname = f.__name__
		self.compiled[funcname] = b''
		for chunk in f(self.engine,*a,**k):
			if isinstance(chunk,bytes):
				self.compiled[funcname] = self.compiled[funcname] + chunk
			elif callable(chunk):
				pos = len(self.compiled[funcname])
				self.compiled[funcname] = self.compiled[funcname] + pack(self.REF_FMT,0)
				ref = chunk.__name__
				self.references[funcname] = self.references.get(funcname,[])
				self.references[funcname].append((pos,ref))
		return f

class Knower:
	def __init__(self, src):
		self.data = src
	def find_space(self,size,used=None,byte=0xFF,start=0x000000, align=0x02):
		used = (used or [])[:]
		cursor, scan = start, start
		data = self.data
		dlen = len(data)
		print(dlen)
		while (scan - cursor) < size and scan < dlen:
			if len(used):
				if scan in used[0]:
					cursor = scan = used[0].stop + 1
					used = used[1:]
					continue
			if data[scan]!=byte:
				scan += 1
				while scan % align != 0:
					scan += 1
				cursor = scan
			else:
				scan += 1
		if scan - cursor >= size:
			return cursor
		raise Exception("Could not find {} bytes = {} aligned to {} after position 0x{:06X} of 0x{:06X} (cursor: 0x{:06X})".format(size, byte, align, start, dlen, cursor))

 
class Linker:
	def __init__(self,knower, compiler):
		self.knower = knower
		self.compiler = compiler
	def replace_references(self, data, references, positions):
		ref_fmt = self.compiler.REF_FMT
		ref_sz = calcsize(ref_fmt)
		for (position, ref) in references:
			data_L = data[:position]
			ref = positions[ref] | 0x08000000
			data_ref = pack(ref_fmt, ref)
			data_R = data[position+ref_sz:]
			data = data_L + data_ref + data_R
		return data
	def compile(self, freespace_starts = 0x000000, freespace_align = 0x02, freespace_byte=0xFF):
		compiled = self.compiler.compiled
		sections = compiled.items()
		positions = {}
		used = []
		for func_name, bytecode in sections:
			sz = len(bytecode)
			pos = positions[func_name] = self.knower.find_space(sz, used,start=freespace_starts, align=freespace_align, byte=freespace_byte)
			used.append(range(pos,pos+sz))
		return {
			func_name: {
				"data": self.replace_references(bytecode, self.compiler.references.get(func_name,[]), positions),
				"position": positions[func_name]
			}
			for func_name, bytecode in sections
		}

class PatchMaker:
	def __init__(self, data, bulk = None, truncate = None):
		self.data = data
		self.bulk_records = bulk or []
		self._truncate = truncate
	@classmethod
	def make_addr(cls,addr):
		return pack(">I",addr)[1:]
	@property
	def truncate(self):
		return self.make_addr(self._truncate) if self._truncate else b''
	def compile(self):
		return b'PATCH' + b''.join([
			self.make_addr(record['position']) + pack('>H',len(record['data'])) + record['data']
			for record in self.data
		]) + b''.join([
			self.make_addr(record['position']) + b'\x00\x00' + pack(">HB",record['count'],record['value'])
			for record in self.bulk_records
		]) + b'EOF' + self.truncate

class ScriptEngine:
	def __init__(self):
		pass
	def install(self,cmd_list):
		def script_func(cmd,*args):
			args = [cmd['cmd']] + list(args)
			fmt = cmd["structure"]
			order = fmt[0] if fmt[0] in "@<>=!" else '<'
			structure = fmt[1:] if fmt[0] in "@<>=!" else fmt[:]
			for segment, val in zip(structure,args):
				if callable(val):
					assert segment=='I'
					yield val
				else:
					segment = order + segment
					yield pack(segment,val)

		for cmd in cmd_list:
			m = partial(script_func, cmd)
			m.__doc__ = cmd['doc_string']
			m.__name__ = cmd['name']
			setattr(self,cmd['name'],m)

def encode_text(LUT,text):
	return b''.join(LUT.get(c,c) for c in text)

def build_argparser():
	parser = argparse.ArgumentParser(description='Compiles the script into an IPS patch.')
	parser.add_argument("-target","--t",type=argparse.FileType(mode='rb'),dest='target')
	parser.add_argument("-output","--o",type=argparse.FileType(mode='wb'),dest='output')
	parser.add_argument("-engine","--e",type=argparse.FileType(mode='r',encoding='utf-8'),dest='engine')
	return parser

class DummyContextManager:
	def __init__(self):
		pass
	def __enter__(self):
		return self
	def __exit__(self, etype, exception, tb):
		pass

class DummyCompileContext(DummyContextManager):
	def __call__(self,*a,**k):
		pass

class Build:
	def __init__(self, target, output, engine, freespace_start=0x740000):
		data = target.read()
		self.knower = Knower(data)
		self.freespace_start=freespace_start

		self.engine = ScriptEngine()
		engine = load(engine)
		self.engine.install(engine)

		self.compiler = Compiler(self.engine)

		self.linker = Linker(self.knower, self.compiler)

		self.output = output.buffer if isinstance(output,TextIOWrapper) else output
		
	def __enter__(self):
		return self.compiler.compile
	def __exit__(self, etype, exception, tb):
		if etype is None and exception is None and tb is None:
			linked = self.linker.compile(freespace_starts=self.freespace_start)
			pm = PatchMaker(linked.values())
			self.output.write(pm.compile())
			if self.output is not stdout.buffer:
				for func_name, record in linked:
					print("{: 20}: inserted at 0x{:06X} is {} bytes long.".format(func_name, record['position'], len(record['data'])))
	@classmethod
	def build(cls,name):
		if name=="__main__":
			argparser = build_argparser()
			args = argparser.parse_args()
			return cls(args.target, args.output, args.engine)
		else:
			return DummyCompileContext()
