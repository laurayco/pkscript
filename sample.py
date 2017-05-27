import frlg
from scripting import script_section

@script_section
def sample_text_display(text_location):
	yield frlg.lock()
	yield frlg.faceplayer()
	yield frlg.preparemsg(text_location)
	yield frlg.closeonkeypress()
	yield frlg.release()
	yield frlg.end()

if __name__=="__main__":
	import sys
	# I don't actually know of any text locations off the top of my head lol
	TEXT_LOCATION = 0x08123456
	if len(sys.argv) > 1:
		TEXT_LOCATION = int(sys.argv[1])
	sys.stdout.buffer.write(sample_text_display(TEXT_LOCATION))