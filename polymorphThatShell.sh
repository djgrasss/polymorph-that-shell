#!/bin/bash

echo " "
if [ "$1" = "-f" ]; then
	./myPoly.py "-f" $2
else
	./myPoly.py $1
fi

echo "[+] Compiling and linking..."
nasm -f elf32 -o tmp.o tmp.nasm

ld -o tmp tmp.o
echo " "

shellString=$(objdump -d tmp | grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-7 -d' '|tr -s ' '|tr '\t' ' '|sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s |sed 's/^/"/'|sed 's/$/"/g')
charCount=${#shellString}
charCount=$(($charCount/4))
shellOutput="[+] Extracting polymorphed shellcode ($charCount Bytes) from executable..."
echo $shellOutput
echo $shellString
echo " "

echo "[+] Removing temporary files..."
rm tmp tmp.o tmp.nasm

echo "[+] Done!"
echo " "
