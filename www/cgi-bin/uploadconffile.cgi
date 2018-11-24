#!/bin/sh

# Version: 4.1.0 2018-11-17

. pcp-functions

pcp_html_head "Upload Configuration File" "PH" 

# This is not to upload executable files, the user rights and file mod should be set to be secure.
# For other files, add the file variable to the case statement.  The lines below the case statement
# should be common.

pcp_banner
pcp_running_script

RESTART_LMS=0

pcp_table_top "Uploading File..."
echo '<textarea class="inform" style="height:200px">'
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
		esac
	done
	#strip the next two lines....still part of the header
	read line
	read line
	cat - >$TMPOUT
	file $TMPOUT | grep -q "text"
	if [ $? -eq 0 ]; then
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
		pcp_backup "nohtml"
	else
		echo "[ ERROR ] Invalid file format, must be a text file."
		RESTART_LMS=0
		rm -f $TMPOUT
	fi
else
	echo "[ ERROR ] Script error! This routine only accepts form POST...."
fi

if [ $RESTART_LMS -eq 1 ]; then
	echo "[ INFO ] Restarting LMS"
	/usr/local/etc/init.d/slimserver stop
	/usr/local/etc/init.d/slimserver start
fi

[ $BACKUP_REQUIRED -eq 1 ] && pcp_backup "nohtml"
echo '</textarea>'

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required
pcp_table_middle
pcp_redirect_button "Go Back" $FROM_PAGE 5
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
