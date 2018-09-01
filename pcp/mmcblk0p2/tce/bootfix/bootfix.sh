#!/bin/sh
# Script run early in do_rebootstuff to fix issues occurring after an insitu update.

# Version 4.0.0 2018-06-15

. /home/tc/www/cgi-bin/pcp-functions
. /usr/local/etc/pcp/pcpversion.cfg
if [ -e $BOOTMNT/oldpcpversion.cfg ]; then
	. $BOOTMNT/oldpcpversion.cfg
	OLDVERS=$(echo "$OLDPCPVERS" | cut -d ' ' -f2)
	OLDMAJOR=$(echo "$OLDVERS" | cut -d '.' -f1)
	tt=$(echo "$OLDVERS" | cut -d '.' -f2)
	OLDMINOR=${tt:0:2}
	tt=$(echo "$OLDVERS" | cut -d '.' -f3)
	OLDPATCH=$(echo "$tt" | cut -d '-' -f1)
	rm -f $BOOTMNT/oldpcpversion.cfg
else
	#just to prevent errors, if older version is being upgraded.
	OLDMAJOR=3
	OLDMINOR=11
	OLDPATCH=0
fi
VERS=$(echo "$PCPVERS" | cut -d ' ' -f2)
MAJOR=$(echo "$VERS" | cut -d '.' -f1)
tt=$(echo "$VERS" | cut -d '.' -f2)
MINOR=${tt:0:2}
tt=$(echo "$VERS" | cut -d '.' -f3)
PATCH=$(echo "$tt" | cut -d '-' -f1)

[ $DEBUG -eq 1 ] && echo "OLDVERS=$OLDVERS"
[ $DEBUG -eq 1 ] && echo "OLDMAJOR=$OLDMAJOR"
[ $DEBUG -eq 1 ] && echo "OLDMINOR=$OLDMINOR"
[ $DEBUG -eq 1 ] && echo "OLDPATCH=$OLDPATCH"

[ $DEBUG -eq 1 ] && echo "VERS=$VERS"
[ $DEBUG -eq 1 ] && echo "MAJOR=$MAJOR"
[ $DEBUG -eq 1 ] && echo "MINOR=$MINOR"
[ $DEBUG -eq 1 ] && echo "PATCH=$PATCH"

# Mark with Version for the update, in case we accidentally include it in an update package when not needed for that version
#------------------------------------------------------------------------
case $MAJOR in
	3)
		case $MINOR in
			2*) # Fixes needed for pCP3.20  All versions <= 3.11 need this fix
				if [ $OLDMAJOR -le 3 -a $OLDMINOR -le 11 ]; then 
					. $BOOTMNT/newconfig.cfg
					[ "$SCREENROTATE" = "no" ] && SCREENROTATE="180"
					[ "$SCREENROTATE" = "yes" ] && SCREENROTATE="0"
					sed -i "s/\(SCREENROTATE=\).*/\1\"$SCREENROTATE\"/" $BOOTMNT/newconfig.cfg
				fi
			;;
			5) echo "No Boot Fixes needed for 3.5.x"
			;;
			*)
			;;
		esac
	;;
	#fixes needed in order to update to pCPversion - add below
	*);;
esac
