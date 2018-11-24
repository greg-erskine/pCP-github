#!/bin/sh
# put other system startup commands here, the boot process will wait until they complete.
# Use bootlocal.sh for system startup commands that can run in the background 
# and therefore not slow down the boot process.

TCEMNT="/mnt/$(readlink /etc/sysconfig/tcedir | cut -d '/' -f3)"
[ -f /home/tc/www/cgi-bin/autoresize.sh ] && (. /home/tc/www/cgi-bin/autoresize.sh 2>&1 | tee -a ${TCEMNT}/tce/pcp_resize.log)
/usr/bin/sethostname "piCorePlayer"
/opt/bootlocal.sh &
