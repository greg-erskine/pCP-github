#!/bin/bash

if [ ! -d squeezelite ]; then
	exit 1
fi

cd squeezelite
make -f Makefile.pcp clean
make -f Makefile.pcp

if [ -f find_servers ]; then
	rm find_servers
fi

gcc -O2 -s -o find_servers tools/find_servers.c
