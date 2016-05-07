#!/bin/sh
# Script run early in do_rebootstuff to fix issues occurring after an insitu update.

# Version: pCP2.05 0.01 2014-06-25 SBP 

. /home/tc/www/cgi-bin/pcp-functions

#--------------------------------------------------------------
# Fixes needed in order to update to pCP2.05
# Files that need to be in this folder are
#    bootfix.sh
#    fix_bootlocal.py
#    pcp-load
#
mv /mnt/mmcblk0p2/tce/optional/bootfix/pcp-load /usr/local/sbin/

#micropython......some things are just easier outside of shell
#    Adds Trim Tags for later use
#    Removes the extra do_rebootstuff line added by insitu_update.cgi v2.04
/usr/bin/micropython /mnt/mmcblk0p2/tce/optional/bootfix/fix_bootlocal.py
mv -f /opt/bootlocal.sh /opt/bootlocal.sh.bak
mv -f /tmp/bootlocal.sh /opt/bootlocal.sh
chmod 775 /opt/bootlocal.sh
chown tc:staff /opt/bootlocal.sh

#--------------------------------------------------------------
#fixes needed in order to update to pCPversion - add below