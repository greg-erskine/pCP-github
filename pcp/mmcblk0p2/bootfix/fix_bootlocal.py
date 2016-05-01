#!/usr/bin/micropython

import os
import sys

infile = open("/opt/bootlocal.sh", "r")
outfile = open ("/tmp/bootlocal.sh", "w")

while True:
	ln = infile.readline()
	if ln == '':
		break

	if "do_rebootstuff" in ln:
		if "tee" in ln:
			outfile.write('#pCPstart------\n')
			outfile.write(ln)
			outfile.write('#pCPstop------\n')
	else:
		outfile.write(ln)

infile.close
outfile.close
