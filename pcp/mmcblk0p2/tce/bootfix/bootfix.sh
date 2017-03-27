#!/bin/sh
# Script run early in do_rebootstuff to fix issues occurring after an insitu update.

# Version: 3.20 2017-03-25 PH
#	Added SCREENROTATE fix for 3.20
#	Removed changes for <3.00, since those would never see an insitu 3.20 upgrade

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
	tt=$(echo "$OLDVERS" | cut -d '.' -f2)
	OLDMINOR=${tt:0:2}
	rm -f /mnt/mmcblk0p1/oldpiversion.cfg
else
	#just to prevent errors, if older version is being upgraded.
	OLDMAJOR=3
	OLDMINOR=11
fi
VERS=$(echo "$PIVERS" | cut -d ' ' -f2)
MAJOR=$(echo "$VERS" | cut -d '.' -f1)
tt=$(echo "$VERS" | cut -d '.' -f2)
MINOR=${tt:0:2}

# Mark with Version for the update, in case we accidentally include it in an update package when not needed for that version
#------------------------------------------------------------------------
# Fixes needed for pCP3.20  All versions <= 3.11 need this fix
if [ $OLDMAJOR -le 3 -a $OLDMINOR -le 11 ]; then 
	. /mnt/mmcblk0p1/newconfig.cfg
	[ "$SCREENROTATE" = "no" ] && SCREENROTATE="180"
	[ "$SCREENROTATE" = "yes" ] && SCREENROTATE="0"
	sed -i "s/\(SCREENROTATE=\).*/\1\"$SCREENROTATE\"/" /mnt/mmcblk0p1/newconfig.cfg
fi
#fixes needed in order to update to pCPversion - add below
