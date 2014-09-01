#!/bin/bash

echo " "
countValue=0
while true
do
	# load shellcode directly or from a file
	if [ "$1" = "-f" ]; then
		./myPoly.py "-f" $2
	else
		./myPoly.py $1
	fi

	# use nasm and ld to compile and link the assembler program
	echo "[+] Compiling and linking..."
	nasm -f elf32 -o tmp.o tmp.nasm
	ld -o tmp tmp.o

	# check if bad characters are in there
	countValue=$((countValue+1))

	# count length (number of characters) of the extracted shellcode
	shellString=$(objdump -d tmp | grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-7 -d' '|tr -s ' '|tr '\t' ' '|sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s |sed 's/^/"/'|sed 's/$/"/g')

	echo "[+] Checking for bad characters: $countValue iteration..." 
	badchars=$(./badchars.py ${shellString})
	if [ $badchars == "0" ]; then
		echo "[+] No bad characters found"
		break
	else
		echo "[-] Bad characters found!"
	fi
done

# divide length by four to determine the exact shellcode length
charCount=${#shellString}
charCount=$(($charCount/4))
shellOutput="[+] Extracting polymorphed shellcode ($charCount Bytes) from executable..."
echo " "
echo $shellOutput
echo $shellString
echo " "

echo "[+] Removing temporary files..."
rm tmp tmp.o tmp.nasm

echo "[+] Done!"
echo " "
