from scripting import script_func, script_section, no_args, direct_arguments

nop = no_args(0x00)
nop1 = no_args(0x01)
end = no_args(0x02)
script_return = no_args(0x03)

@script_func('I',0x04)
def call(ref,mgr=None):
	if mgr is not None:
		ref = mgr.get_location(ref)
	return (ref,)

@script_func('I',0x05)
def goto(ref,mgr=None):
	if mgr is not None:
		ref = mgr.get_location(ref)
	return (ref,)

@script_func('BI',0x06):
def cmp_jump(condition,ref,mgr=None):
	if mgr is not None:
		ref = mgr.get_location(ref)
	return (condition,ref)

@script_func('BI',0x07):
def cmp_jump(condition,ref,mgr=None):
	if mgr is not None:
		ref = mgr.get_location(ref)
	return (condition,ref)

goto_std_function = direct_arguments('B',0x08)
call_std_function = direct_arguments('B',0x09)
conditional_goto_std_function = direct_arguments('BB',0x0A)
conditional_call_std_function = direct_arguments('BB',0x0B)

jump_ram = no_args(0x0C)
kill = no_args(0x0D)

set_byte = direct_arguments('B',0x0E)
load_pointer = direct_arguments('BI',0x0F)
set_bank_byte = direct_arguments('BB',0x10)
set_pointer_byte = direct_arguments('BI',0x11)
get_pointer_byte = direct_arguments('BI',0x12)
set_far_byte = direct_arguments('BI',0x13)
copy_bank = direct_arguments('BB',0x14)
copy_byte = direct_arguments('II',0x15)
set_variable = direct_arguments('HH',0x16)
add_variable = direct_arguments('HH',0x17)
subtract_variable = direct_arguments('HH',0x18)
copy_variable = direct_arguments('HH',0x19)
copy_var_or_value = direct_arguments('HH',0x1A)
compare_banks = direct_arguments('BB',0x1B)
compare_bank_to_byte = direct_arguments('BB',0x1C)
compare_bank_to_far_byte = direct_arguments('BI',0x1D)
compare_far_byte_to_bank = direct_arguments('IB',0x1E)
compare_far_byte_to_byte = direct_arguments('IB',0x1f)
compare_far_bytes = direct_arguments('II',0x20)
compare_variable_to_byte = direct_arguments('HB',0x21)
compare_variables = direct_arguments('HH',0x22)

call_asm_routine = direct_arguments('I',0x23)
cmd_24 = direct_arguments('I',0x24)
call_special_func = direct_arguments('H',0x25)
assign_from_special_func = direct_arguments('HH',0x26)

wait_state = no_args(0x27)
pause = direct_arguments('H',0x28)

set_flag = direct_arguments('H',0x29)
clear_flag = direct_arguments('H',0x2A)
check_flag = direct_arguments('H',0x2B)
nop_2c = no_args(0x2C)
check_daily_flag = no_args(0x2D)
reset_flags = no_args(0x2E)

sound = direct_arguments('H',0x2F)
wait_sound = no_args(0x30)