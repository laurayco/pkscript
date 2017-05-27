import scripting
import binascii

@scripting.script_func('<BI')
def select_character(cid):
	return (0xAF,cid)

@scripting.script_section
def select_all_characters(character_list):
	for cid in character_list:
		yield select_character(cid)
	if len(character_list) < 1:
		yield None

print(binascii.hexlify(select_character(20)))
print(binascii.hexlify(select_all_characters([0xBE,0xEF,0x9A,0xCC])))