#!/usr/bin/python

import sys

strInput = sys.argv[1]
if strInput.find("\\x00") != -1:
    print "1"
else:
    print "0"
