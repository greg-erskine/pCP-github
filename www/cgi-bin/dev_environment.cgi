#!/bin/sh

# Version: 4.0.1 2018-09-21

# Title: Print the current environment
# Description: Future, set the enviroment of busybox-httpd by launching
# env - GLOBAL=/usr/local/etc/pcp/test.cfg PATH=/usr/local/sbin:/usr/local/bin:/sbin:/usr/sbin:/bin:/usr/bin /usr/local/sbin/busybox-httpd -h /home/tc/www

printf "%s\n\n" "Content-type: text/plain"
env | sort | awk -F'=' '{ st = index($0,"="); printf "%s = \"%s\"\n" ,$1, substr($0, st+1) }'