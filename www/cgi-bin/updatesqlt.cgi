#!/bin/sh

# Version: 7.0.0 2020-05-26

. pcp-functions

pcp_html_head "Updating Squeezelite" "SBP"

WGET="/bin/busybox wget"

pcp_navbar
pcp_httpd_query_string

unset REBOOT_REQUIRED
RESULT=0

pcp_debug_variables "html" ACTION

case "${ACTION}" in
	update)
		SPACE_REQUIRED=95
		pcp_heading5 "Updating Squeezelite extension"
		pcp_infobox_begin
		pcp_sufficient_free_space $SPACE_REQUIRED "text"
		if [ $? -eq 0 ]; then
			pcp_squeezelite_stop "text"
			pcp_message INFO "Current Squeezelite version: $(pcp_squeezelite_version)" "text"
			pcp_message INFO "Waiting for Squeezelite to complete shutdown..." "text"
			CNT=0
			until ! lsof | grep -q /tmp/tcloop/pcp-squeezelite
			do
				[ $((CNT++)) -gt 10 ] && break || sleep 1
			done
			if [ $CNT -gt 10 ]; then
				pcp_message ERROR "Squeezelite took too long to terminate, please run a full package update." "text"
				RESULT=1
			fi
			pcp_message INFO "Removing old Squeezelite extension..." "text"
			if [ $RESULT -eq 0 -a -d /tmp/tcloop/pcp-squeezelite ]; then
				umount -d /tmp/tcloop/pcp-squeezelite
				RESULT=$?
			fi
			if [ $RESULT -ne 0 ]; then
				pcp_message ERROR "In place update failed, please run a full package update." "text"
			else
				pcp_message INFO "Updating Squeezelite extension..." "text"
				rm -f /usr/local/tce.installed/pcp-squeezelite
				mv -f ${PACKAGEDIR}/pcp-squeezelite.tcz /tmp
				mv -f ${PACKAGEDIR}/pcp-squeezelite.tcz.md5.txt /tmp
				if [ $DEBUG -eq 1 ]; then
					sudo -u tc pcp-load -r $PCP_REPO -w pcp-squeezelite.tcz 2>&1
				else
					sudo -u tc pcp-load -r $PCP_REPO -w pcp-squeezelite.tcz
				fi
				if [ $? -ne 0 ]; then
					DLERROR=1
					pcp_message ERROR "Download unsuccessful, try again later!" "text"
					mv -f /tmp/pcp-squeezelite.tcz $PACKAGEDIR
					mv -f /tmp/pcp-squeezelite.tcz.md5.txt $PACKAGEDIR
				else
					rm -f /tmp/pcp-squeezelite.tcz*
				fi
				pcp_message INFO "Reloading Squeezelite extension..." "text"
				sudo -u tc pcp-load -i pcp-squeezelite.tcz
				pcp_message INFO "Current Squeezelite version: $(pcp_squeezelite_version)" "text"
			fi
			[ $DEBUG -eq 1 ] && (echo '[ OK ] '; ls -al ${SQLT_BIN})
			pcp_squeezelite_start "text"
		fi
		pcp_infobox_end
	;;
	full_update)
		SPACE_REQUIRED=1300
		pcp_heading5 "Updating Squeezelite and any needed dependencies"
		pcp_infobox_begin
		pcp_sufficient_free_space $SPACE_REQUIRED "text"
		if [ $? -eq 0 ]; then
			pcp_squeezelite_stop "text"
			pcp-update pcp-squeezelite
			CHK=$?
			if [ $CHK -eq 2 ]; then
				pcp_message INFO "There is no update for Squeezelite at this time." "text"
				unset REBOOT_REQUIRED
			elif [ $CHK -eq 1 ]; then
				pcp_message ERROR "There was an error updating Squeezelite, please try again later." "text"
				unset REBOOT_REQUIRED
			else
				pcp_message INFO "[Reboot] is required to complete the update." "text"
				REBOOT_REQUIRED=TRUE
			fi
			pcp_squeezelite_start "text"
		fi
		pcp_infobox_end
	;;
	inst_ffmpeg)
		SPACE_REQUIRED=7000
		pcp_heading5 "Installing FFMpeg extension"
		pcp_infobox_begin
		pcp_sufficient_free_space $SPACE_REQUIRED "text"
		if [ $? -eq 0 ]; then
			pcp_squeezelite_stop "text"
			if [ $DEBUG -eq 1 ]; then
				sudo -u tc pcp-load -r $PCP_REPO -w pcp-libffmpeg.tcz 2>&1
				[ $? -eq 0 ] && FAIL=0 || FAIL=1
			else
				sudo -u tc pcp-load -r $PCP_REPO -w pcp-libffmpeg.tcz
				[ $? -eq 0 ] && FAIL=0 || FAIL=1
			fi
			if [ $FAIL -eq 0 ]; then
				sudo -u tc pcp-load -i pcp-libffmpeg.tcz
				echo "pcp-libffmpeg.tcz" >> $ONBOOTLST
			fi
			pcp_squeezelite_start "text"
		fi
		pcp_infobox_end
	;;
	rem_ffmpeg)
		pcp_heading5 "Removing FFMpeg extension"
		pcp_infobox_begin
		pcp_squeezelite_stop "text"
		pcp_message INFO "FFMpeg extension marked for removal. Reboot required to complete." "text"
		sudo -u tc tce-audit builddb
		sudo -u tc tce-audit delete pcp-libffmpeg.tcz
		sed -i '/pcp-libffmpeg.tcz/d' $ONBOOTLST
		REBOOT_REQUIRED=TRUE
		pcp_squeezelite_start "text"
		pcp_infobox_end
	;;
	*)
		pcp_infobox_begin
		pcp_message ERROR "Option Error!" "text"
		pcp_infobox_end
	;;
esac

pcp_redirect_button "Go to Main Page" "main.cgi" 10

[ $REBOOT_REQUIRED ] && pcp_reboot_required
pcp_html_end