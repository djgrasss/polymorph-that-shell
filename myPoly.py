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
xorNotDirection = random.randint(0, 1)


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
	# XOR byte declaration
	while True:
		xorByte = random.randint(1, 255)
		if hex(xorByte) != stoppingByte:
			break
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

	# encode the shell...
	input = ""
	originalShellcodeLength = 0
	for x in bytearray(content):
		originalShellcodeLength += 1
		if xorNotDirection == 0:
			# XOR encode
			y = x^xorByte
			# NOT encode
			curValue = ~y
			curValue = hex(curValue & 0xff)
		else:
			# NOT encode
			y = ~x
			y = y & 0xff
			# XOR encode
			curValue = hex(y^xorByte)
		input += curValue
		if originalShellcodeLength == len(bytearray(content)):
			input += ", " + str(stoppingByte)
			break
		# insertion encode
		while True:
                	tmpByte = hex(random.randint(1, 255))
                        if tmpByte != stoppingByte and tmpByte != curValue:
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
	# generate garbage label
	randomString = [random.choice(string.ascii_letters) for n in xrange(10)]
	garbageLabel = "".join(randomString)
	garbageBytes = ""

###########################################################
# ToDo: Find Bug!
	numberOfGarbageBytes = random.randint(0, 0)
	for i in range(numberOfGarbageBytes):
		tmpRnd2 = random.randint(1, 255)
		garbageBytes += str(hex(tmpRnd2)) + ", "
	garbageBytes = garbageBytes[:len(garbageBytes)-2]
	garbageLabel += ": db " + garbageBytes + "\n"
##########################################################

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
        assembler += "\tlea " + shellIterator + ", [" + popRegister + " + 1 + " + str(numberOfGarbageBytes) + "]\n"
	tmpRand = random.randint(0, 1)
	tmpRegister = random.randint(0, len(commonRegisters)-1)
	if tmpRand == 0:
		assembler += "\tmov " + insertIterator + ", " + commonRegisters[tmpRegister] + "\n"
	assembler += "\txor " + insertIterator + ", " + insertIterator + "\n"
	tmpRand2 = random.randint(0, 1)
	if tmpRand2 == 0:
		tmpRand = random.randint(1, 254)
		movValue = 0x1
		permValue = movValue + tmpRand
		assembler += "\tmov " + insertIteratorLowerByte + ", " + str(hex(permValue)) + "\n"
		assembler += "\tsub " + insertIteratorLowerByte + ", " + str(hex(tmpRand)) + "\n"
	else:
		assembler += "\tmov " + insertIteratorLowerByte + ", 0x1\n"
	tmpRand = random.randint(0, 1)
        tmpRegister = random.randint(0, len(commonRegisters)-1)
        if tmpRand == 0:
                assembler += "\tmov " + tmpValue + ", " + commonRegisters[tmpRegister] + "\n"
	assembler += "\txor " + tmpValue + ", " + tmpValue + "\n"
	if xorNotDirection == 0:
		assembler += "\tnot byte [" + popRegister + " +  " + str(numberOfGarbageBytes) + "]\n"	
		assembler += "\txor byte [" + popRegister + " +  " + str(numberOfGarbageBytes) + "], " + str(hex(xorByte)) + "\n"
	else:
		assembler += "\txor byte [" + popRegister + " +  " + str(numberOfGarbageBytes) + "], " + str(hex(xorByte)) + "\n"
		assembler += "\tnot byte [" + popRegister + " +  " + str(numberOfGarbageBytes) + "]\n"
	# access decode procedure
	assembler += decode + ":\n"
	assembler += "\tmov " + tmpValueLowerByte + ", byte [" + popRegister + " + " + insertIterator + " + " + str(numberOfGarbageBytes) + "]\n"
	assembler += "\txor " + tmpValueLowerByte + ", " + stoppingByte + "\n"
	assembler += "\tjz short " + shellcodeLabel + "\n"
	assembler += "\tmov " + tmpValueLowerByte + ", byte [" + popRegister + " + " + insertIterator + " + 1 + " + str(numberOfGarbageBytes) + "]\n"
	assembler += "\tmov byte [" + shellIterator + "], " + tmpValueLowerByte + "\n"
	if xorNotDirection == 0:	
		assembler += "\tnot byte [" + shellIterator + "]\n"
		assembler += "\txor byte [" + shellIterator + "], " + str(hex(xorByte)) + "\n"
	else:
		assembler += "\txor byte [" + shellIterator + "], " + str(hex(xorByte)) + "\n"
		assembler += "\tnot byte [" + shellIterator + "]\n"
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
	if numberOfGarbageBytes > 0:
		assembler += "\t" + garbageLabel
	assembler += "\t" + shellcode
	callAfterOrders = random.randint(0, 3)     
	assembler += callPoly(callAfterOrders)

	# save the assembler file
	print "[+] Saving the black magic into an assembler file..."
	file = open("tmp.nasm", "w")
	file.write(assembler)
	file.close()
