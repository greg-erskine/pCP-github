#!/bin/sh
# Script run early in do_rebootstuff to fix issues occurring after an insitu update.

# Version: 2.06 2016-06-11 PH
#	Added Logic to determine old version.
#	Fixes for 2.06

# Version: 2.05 2016-04-17 SBP 
#	Initial Version

. /home/tc/www/cgi-bin/pcp-functions
. /usr/local/sbin/piversion.cfg
if [ -e /mnt/mmcblk0p1/oldpiversion.cfg ]; then
	. /mnt/mmcblk0p1/oldpiversion.cfg
	OLDVERS=$(echo "$OLDPIVERS" | cut -d ' ' -f2)
	OLDMAJOR=$(echo "$OLDVERS" | cut -d '.' -f1)
	OLDMINOR=$(echo "$OLDVERS" | cut -d '.' -f2)
	rm -f /mnt/mmcblk0p1/oldpiversion.cfg
else
	#just to prevent errors, if older version is being upgraded.
	OLDMAJOR=2
	OLDMINOR=4
fi
VERS=$(echo "$PIVERS" | cut -d ' ' -f2)
MAJOR=$(echo "$VERS" | cut -d '.' -f1)
MINOR=$(echo "$VERS" | cut -d '.' -f2)


# Mark with Version for the update, in case we accidentally include it in an update package when not needed for that version
#------------------------------------------------------------------------
# Fixes introduced in pCP2.05  All versions less than 2.05 need this fix
if [ $OLDMAJOR -le 2 -a $OLDMINOR -lt 5 ]; then 
	# Files that need to be in this folder are
	#    bootfix.sh
	#    pcp-load
	#
	mv /mnt/mmcblk0p2/tce/optional/pcp-load /usr/local/sbin/

	#micropython inline code, do not change indentation.
	#    Adds Trim Tags for later use
	#    Removes the extra do_rebootstuff line added by insitu_update.cgi v2.04
/usr/bin/micropython -c '
import os
import sys
infile = open("/opt/bootlocal.sh", "r")
outfile = open ("/tmp/bootlocal.sh", "w")
while True:
	ln = infile.readline()
	if ln == "":
		break
	if "do_rebootstuff" in ln:
		if "tee" in ln:
			outfile.write("#pCPstart------\n")
			outfile.write("/home/tc/www/cgi-bin/do_rebootstuff.sh | tee -a /var/log/pcp_boot.log\n")
			outfile.write("#pCPstop------\n")
	else:
		outfile.write(ln)
infile.close
outfile.close
'
	mv -f /opt/bootlocal.sh /opt/bootlocal.sh.bak
	mv -f /tmp/bootlocal.sh /opt/bootlocal.sh
	chmod 775 /opt/bootlocal.sh
	chown tc:staff /opt/bootlocal.sh
fi
#--------------------------------------------------------------
# Fixes needed for pCP2.06  All versions <= 2.05 need this fix
if [ $OLDMAJOR -le 2 -a $OLDMINOR -le 5 ]; then 
	[ "$JIVELITE" = "NO" ] && JIVELITE="no"
	[ "$JIVELITE" = "YES" ] && JIVELITE="yes"
	[ "$SCREENROTATE" = "NO" ] && SCREENROTATE="no"
	[ "$SCREENROTATE" = "YES" ] && SCREENROTATE="yes"
	pcp_save_to_config
	[ -e /mnt/mmcblk0p2/tce/optional/pcp-load ] && rm -f /mnt/mmcblk0p2/tce/optional/pcp-load
fi
#--------------------------------------------------------------
#fixes needed in order to update to pCPversion - add below
