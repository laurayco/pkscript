# the goal of this project is to create a library
# that can be used to generate script (bytecode)
# files in a consistent manner that takes advantage
# of python's higher level language features.
# think of it as a compiler with a python pre-processor.
# kind of.
import struct
import functools

def __simple_return(*a): return a

def script_func(structure,b):
	comp = functools.partial(struct.pack,structure)
	def wrap(f):
		def replace(*a,**k):
			return comp(b,*f(*a,**k))
		replace.total_size = struct.calcsize(structure)
		replace.__doc__ = f.__doc__
		return replace
	return wrap

def script_section(f):
	def wrap(func):
		def replace(*a,**k):
			r = b''
			for chunk in func(*a,**k):
				if chunk is None:
					continue
				r = r + chunk
			return r
		replace.__doc__ = func.__doc__
		return replace
	return wrap(f)

def no_args(v,help_string=""):
	def func(): return (v,)
	func.__doc__ = help_string
	return script_func('',v)(func)

def direct_arguments(structure,b,help_string=""):
	def x(*a):return a
	x.__doc__ = help_string
	return script_func(structure,b)(x)

def install_commands(cls,cmd_list):
	for cmd in cmd_list:
		m = direct_arguments(cmd['structure'],cmd['cmd'],help_string=cmd['doc_string'])
		name = cmd['name']
		m.__name__ = name
		setattr(cls,name,m)

class ScriptEngine:
	def __init__(self):
		pass
	@classmethod
	def install(cls,cmd_list):
		install_commands(cls,cmd_list)