#!/bin/sh
# Script run early in do_rebootstuff to fix issues occurring after an insitu update.

# Version: pCP2.05 0.01 2014-06-25 SBP 

. /home/tc/www/cgi-bin/pcp-functions

#--------------------------------------------------------------
# Fixes needed in order to update to pCP2.05
# Files that need to be in this folder are
#    bootfix.sh
#    pcp-load
#
mv /mnt/mmcblk0p2/tce/bootfix/pcp-load /usr/local/sbin/

# Need to fix the bootlocal problems too.
#The follwing will replace lines between #pCPstart and #cPCstop with REPLACEMENT
# We/I need to figure out how to use REPLACEMENT as a variable. It doesn't work yet

REPLACEMET=${/home/tc/www/cgi-bin/do_rebootstuff.sh | tee -a /var/log/pcp_boot.log}

sed -i -n '/#pCPstart/{p;:a;N;/#pCPstop/!ba;s/.*\n/REPLACEMENT\n/};p' /opt/bootlocal.sh

#--------------------------------------------------------------

#fixes needed in order to update to pCPversion - add below