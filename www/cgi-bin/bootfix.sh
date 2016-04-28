#!/bin/sh
# Script run early in do_rebootstuff to fix issues occuring after an insitu update.

# Version: pCP2.05 0.01 2014-06-25 SBP 

. /home/tc/www/cgi-bin/pcp-functions

#--------------------------------------------------------------
# Fixes needed in order to update to pCP2.05
mv $PCPHOME/pcp-load /usr/local/sbin/
#--------------------------------------------------------------

#fixes needed in order to update to pCPversion - add below