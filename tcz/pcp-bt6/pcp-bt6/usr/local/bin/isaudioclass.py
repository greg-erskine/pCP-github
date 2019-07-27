#!/usr/bin/micropython

# Small script to convert bluetooth COD to binary string

import os
import sys

def hextobin(hexval):
        '''
        Takes a string representation of hex data with
        arbitrary length and converts to string representation
        of binary.  Includes padding 0s
        '''
        thelen = len(hexval)*4
        binval = bin(int(hexval, 16))[2:]
        while ((len(binval)) < thelen):
            binval = '0' + binval
        return binval

def reverse(s):
	if len(s) == 0:
		return s
	else:
		return reverse(s[1:]) + s[0]

bin = hextobin(sys.argv[1])
# Reverse the bits so we just can address like a string.
rev = reverse(bin)
# Looking at the major class Audio Device bit 10, and print the bit
print ("%d" % int(rev[10]))
