#!/bin/sh

# Version: 3.5.1 2018-04-08
#	Added pcp_redirect_button. GE.

# Version: 3.21 2017-05-20
#	Changed to allow booting from USB on RPi3. PH.

# Version: 3.20 2017-04-17
#	Fixed pcp-xxx-functions issues. GE.
#	Change Full Update to use pcp-update. PH.

# Version: 3.10 2017-01-04
#	Changes for Squeezelite extension. PH.
#	Formatting Changes for textareas. SBP.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions

pcp_html_head "Updating Squeezelite" "SBP"

WGET="/bin/busybox wget"

pcp_banner
pcp_running_script
pcp_httpd_query_string

unset REBOOT_REQUIRED
RESULT=0

#========================================================================================
# Routines.
#----------------------------------------------------------------------------------------
pcp_end() {
	echo '</body>'
	echo '</html>'
	exit
}

#----------------------------------------------------------------------------------------
[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ACTION='$ACTION'</p>'
case "${ACTION}" in
	update)
		pcp_table_top "Updating Squeezelite extension"
		SPACE_REQUIRED=95
		pcp_sufficient_free_space $SPACE_REQUIRED
		[ $? -eq 0 ] || pcp_end
		echo '                <textarea class="inform" style="height:180px">'
		pcp_squeezelite_stop "nohtml"
		echo '[ INFO ] Current Squeezelite version: '$(pcp_squeezelite_version)''

		echo '[ INFO ] Waiting for Squeezelite to complete shutdown...'
		CNT=0
		until ! lsof | grep -q /tmp/tcloop/pcp-squeezelite
		do
			[ $((CNT++)) -gt 10 ] && break || sleep 1
		done
		if [ $CNT -gt 10 ]; then
			echo '[ ERROR ] Squeezelite took too long to terminate, please run a full package update.'
			RESULT=1
		fi
		echo '[ INFO ] Removing old Squeezelite extension...'
		if [ $RESULT -eq 0 -a -d /tmp/tcloop/pcp-squeezelite ]; then
			umount -d /tmp/tcloop/pcp-squeezelite
			RESULT=$?
		fi
		if [ $RESULT -ne 0 ]; then
			echo '[ ERROR ] Inplace update failed, please run a full package update.'
		else
			echo '[ INFO ] Updating Squeezelite extension...'
			rm -f /usr/local/tce.installed/pcp-squeezelite
			mv -f $PACKAGEDIR/pcp-squeezelite.tcz /tmp
			mv -f $PACKAGEDIR/pcp-squeezelite.tcz.md5.txt /tmp
			if [ $DEBUG -eq 1 ]; then
				sudo -u tc pcp-load -r $PCP_REPO -w pcp-squeezelite.tcz 2>&1
			else
				sudo -u tc pcp-load -r $PCP_REPO -w pcp-squeezelite.tcz
			fi
			if [ $? -ne 0 ]; then
				DLERROR=1
				echo '[ ERROR ] Download unsuccessful, try again later!'
				mv -f /tmp/pcp-squeezelite.tcz $PACKAGEDIR
				mv -f /tmp/pcp-squeezelite.tcz.md5.txt $PACKAGEDIR
			else
				rm -f /tmp/pcp-squeezelite.tcz*
			fi
			echo '[ INFO ] Reloading Squeezelite extension...'
			sudo -u tc pcp-load -i pcp-squeezelite.tcz
			echo '[ INFO ] Current Squeezelite version: '$(pcp_squeezelite_version)''
		fi
		[ $DEBUG -eq 1 ] && (echo '[ OK ] '; ls -al ${SQLT_BIN})
		pcp_squeezelite_start "nohtml"
		echo '                </textarea>'
	;;
	full_update)
		pcp_table_top "Updating Squeezelite and any needed dependencies"
		SPACE_REQUIRED=1300
		pcp_sufficient_free_space $SPACE_REQUIRED
		[ $? -eq 0 ] || pcp_end
		echo '                <textarea class="inform" style="height:150px">'
		pcp_squeezelite_stop "nohtml"
		pcp-update pcp-squeezelite
		CHK=$?
		if [ $CHK -eq 2 ]; then
			echo '[ INFO ] There is no update for Squeezelite at this time.'
			unset REBOOT_REQUIRED
		elif [ $CHK -eq 1 ]; then
			echo '[ ERROR ] There was an error updating Squeezelite, please try again later.'
			unset REBOOT_REQUIRED
		else
			echo '[ INFO ] A [Reboot] is required to complete the update.'
			REBOOT_REQUIRED=TRUE
		fi
		pcp_squeezelite_start "nohtml"
		echo '                </textarea>'
	;;
	inst_ffmpeg)
		pcp_table_top "Installing FFMpeg extension"
		SPACE_REQUIRED=7000
		pcp_sufficient_free_space $SPACE_REQUIRED
		[ $? -eq 0 ] || pcp_end
		echo '                <textarea class="inform" style="height:100px">'
		pcp_squeezelite_stop "nohtml"
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
		pcp_squeezelite_start "nohtml"
		echo '                </textarea>'
	;;
	rem_ffmpeg)
		pcp_table_top "Removing FFMpeg extension"
		echo '                <textarea class="inform" style="height:100px">'
		pcp_squeezelite_stop "nohtml"
		echo '[ INFO ] FFMpeg extension marked for removal. Reboot required to complete.</p>'
		sudo -u tc tce-audit builddb
		sudo -u tc tce-audit delete pcp-libffmpeg.tcz
		sed -i '/pcp-libffmpeg.tcz/d' $ONBOOTLST
		REBOOT_REQUIRED=TRUE
		pcp_squeezelite_start "nohtml"
		echo '                </textarea>'
	;;
	*)
		echo '<p class="error">[ ERROR ] Option Error!</p>'
	;;
esac

pcp_table_middle
pcp_redirect_button "Go to Main Page" "main.cgi" 10
pcp_table_end
pcp_footer
pcp_copyright
[ $REBOOT_REQUIRED ] && pcp_reboot_required
pcp_end