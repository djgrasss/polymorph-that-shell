#!/bin/bash

echo -n $1 | grep '[0-9a-f]' | sed 's/\\x/, 0x/g' | xargs -I{} ./myPoly.py "{}"

echo '[+] Assembling with Nasm ... '
nasm -f elf32 -o tmp.o tmp.nasm

echo '[+] Linking ...'
ld -o tmp tmp.o
echo ' '

echo '[+] Extracting polymorphed shellcode ...'
objdump -d tmp | grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-7 -d' '|tr -s ' '|tr '\t' ' '|sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s |sed 's/^/"/'|sed 's/$/"/g'
echo ' '

echo '[+] Removing temporary files ...'
rm tmp tmp.o tmp.nasm

echo '[+] Done!'

