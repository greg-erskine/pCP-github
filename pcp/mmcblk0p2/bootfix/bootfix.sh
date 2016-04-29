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

#--------------------------------------------------------------

#fixes needed in order to update to pCPversion - add below