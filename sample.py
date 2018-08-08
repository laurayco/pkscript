from scripting import Build, encode_text as apply_LUT
from functools import partial

encode_text = partial(apply_LUT, {
	"ß":b"\x15",
	"é":b"\x1B",
	"0":b"\xA1",
	"1":b"\xA2",
	"2":b"\xA3",
	"3":b"\xA4",
	"4":b"\xA5",
	"5":b"\xA6",
	"6":b"\xA7",
	"7":b"\xA8",
	"8":b"\xA9",
	"9":b"\xAA",
	"!":b"\xAB",
	"-":b"\xAE",
	"«":b"\xB1",
	"»":b"\xB2",
	"<":b"\xB3",
	"'":b"\xB4",
	"$":b"\xB7",
	",":b"\xB8",
	"*":b"\xB9",
	"/":b"\xBA",
	"A":b"\xBB",
	"B":b"\xBC",
	"C":b"\xBD",
	"D":b"\xBE",
	"E":b"\xBF",
	"F":b"\xC0",
	"G":b"\xC1",
	"H":b"\xC2",
	"I":b"\xC3",
	"J":b"\xC4",
	"K":b"\xC5",
	"L":b"\xC6",
	"M":b"\xC7",
	"N":b"\xC8",
	"O":b"\xC9",
	"P":b"\xCA",
	"Q":b"\xCB",
	"R":b"\xCC",
	"S":b"\xCD",
	"T":b"\xCE",
	"U":b"\xCF",
	"V":b"\xD0",
	"W":b"\xD1",
	"X":b"\xD2",
	"Y":b"\xD3",
	"Z":b"\xD4",
	"a":b"\xD5",
	"b":b"\xD6",
	"c":b"\xD7",
	"d":b"\xD8",
	"e":b"\xD9",
	"f":b"\xDA",
	"g":b"\xDB",
	"h":b"\xDC",
	"i":b"\xDD",
	"j":b"\xDE",
	"k":b"\xDF",
	"l":b"\xE0",
	"m":b"\xE1",
	"n":b"\xE2",
	"o":b"\xE3",
	"p":b"\xE4",
	"q":b"\xE5",
	"r":b"\xE6",
	"s":b"\xE7",
	"t":b"\xE8",
	"u":b"\xE9",
	"v":b"\xEA",
	"w":b"\xEB",
	"x":b"\xEC",
	"y":b"\xED",
	"z":b"\xEE",
	":":b"\xF0",
	"Ä":b"\xF1",
	"Ö":b"\xF2",
	"Ü":b"\xF3",
	" ":b"\x00",
	"\n":b"\xFE"
})

def message(script_engine):
	yield from map(encode_text,[
		"Hello, world!"
	])
	yield b'\xFF'

def speak(script_engine):
	yield from script_engine.preparemsg(message)
	yield from script_engine.waitmsg()
	yield from script_engine.closeonkeypress()
	yield from script_engine._return()

def entry(script_engine):
	yield from script_engine.lock()
	yield from script_engine.call(speak)
	yield from script_engine.release()
	yield from script_engine.end()

with Build.build(__name__) as compile:
	compile(message)
	compile(speak)
	compile(entry)