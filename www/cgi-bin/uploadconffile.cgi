#!/bin/sh

# Version: 7.0.0 2020-06-03

. pcp-functions

pcp_html_head "Upload Configuration File" "PH"

# For other files, add the file variable to the case statement.  The lines below the case statement
# should be common.

RESTART_LMS=0

pcp_infobox_begin
if [ "$REQUEST_METHOD" = "POST" ]; then
	echo -n "[ INFO ] Uploading: "
	TMPOUT=$(mktemp)
	# POST does not send QUERY_STRING, variables are in the post header.
	# Read Header, until the file variable is found.
	while read HEADER; do
		case $HEADER in
			*CUSTOMCONVERT*)
				FROM_PAGE=lms.cgi
				echo "custom_convert.conf"
				UPLOADED_FILE="/usr/local/slimserver/custom-convert.conf"
				RESTART_LMS=1
				BACKUP_REQUIRED=0
				REBOOT_REQUIRED=0
				break
			;;
			*LIRCCONF*)
				FROM_PAGE=lirc.cgi
				echo "lirc.conf"
				UPLOADED_FILE="/usr/local/etc/lirc/lircd.conf"
				BACKUP_REQUIRED=1
				REBOOT_REQUIRED=1
				break
			;;
			*LIRCRC*)
				FROM_PAGE=lirc.cgi
				echo "lircrc"
				UPLOADED_FILE="/home/tc/.lircrc"
				BACKUP_REQUIRED=1
				REBOOT_REQUIRED=1
				break
			;;
			*KEYTABLE*)
				FROM_PAGE=lirc.cgi
				BACKUP_REQUIRED=1
				RELOAD_KEYTABLE=1
				break
			;;
		esac
	done
	# Strip the next two lines....still part of the header
	read line
	read line
	# Pass content through strings to remove potential binary content.
	cat - | strings >$TMPOUT
	# Get the line count
	LINES=$(wc -l $TMPOUT | cut -d ' ' -f 1)
	# Remove the last line
	head -$((LINES - 1)) $TMPOUT >$TMPOUT.1
	dos2unix $TMPOUT.1
	chmod 664 $TMPOUT.1
	chown tc.staff ${UPLOADED_FILE}
	cp -f $TMPOUT.1 ${UPLOADED_FILE}
	chown nobody.nogroup ${UPLOADED_FILE}
	rm -f $TMPOUT*
	sed -i '/'$(echo ${UPLOADED_FILE##/} | sed 's|\/|\\\/|g')'/d' $FILETOOLLST
	if [ -f "${UPLOADED_FILE}" ]; then
		echo "${UPLOADED_FILE##/}" >> $FILETOOLLST
	fi
	pcp_backup "text"
else
	echo "[ ERROR ] Script error! This routine only accepts form POST...."
fi

if [ $RESTART_LMS -eq 1 ]; then
	echo "[ INFO ] Restarting LMS"
	/usr/local/etc/init.d/slimserver stop
	/usr/local/etc/init.d/slimserver start
fi

if [ $RELOAD_KEYTABLE -eq 1 ]; then
	echo ???
fi

[ $BACKUP_REQUIRED -eq 1 ] && pcp_backup "text"
pcp_infobox_end

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

pcp_redirect_button "Go Back" $FROM_PAGE 5

pcp_html_end
exit

