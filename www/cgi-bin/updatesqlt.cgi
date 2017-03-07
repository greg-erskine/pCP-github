#!/bin/sh

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-04
#	Changes for Squeezelite extension. PH.
#	Formatting Changes for textareas. SBP.

# Version: 0.05 2016-02-20 GE
#	Fixed sourceforge redirection issue.

# Version: 0.04 2016-02-10 GE
#	Added SQLT_VERSION.
#	Added free space checks.

# Version: 0.03 2015-12-09 GE
#	Remove Triode's version.
#	Update Ralphy's version.

# Version: 0.02 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
#. $CONFIGCFG

pcp_html_head "Updating Squeezelite" "SBP" "5" "main.cgi"

WGET="/bin/busybox wget"
#OLD_SQLT_VERSION=$SQLT_VERSION

pcp_banner
pcp_running_script
pcp_squeezelite_stop
pcp_httpd_query_string
REBOOT_REQUIRED=0
RESULT=0

#========================================================================================
# Check for free space
#----------------------------------------------------------------------------------------

pcp_end() {
	pcp_squeezelite_start
	echo '</body>'
	echo '</html>'
	exit
}
#----------------------------------------------------------------------------------------
[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ACTION='$ACTION'</p>'
case "${ACTION}" in
	update)
		SPACE_REQUIRED=95
		pcp_sufficient_free_space $SPACE_REQUIRED
		[ $? -eq 0 ] || pcp_end
		pcp_table_top "Updating Squeezelite extension"
		echo '                <textarea class="inform" style="height:150px">'
		echo '[ INFO ] Current Squeezelite version: '$(pcp_squeezelite_version)''

		echo '[ INFO ] Waiting for Squeezelite to complete shutdown.'
		CNT=0
		until ! lsof | grep -q /tmp/tcloop/pcp-squeezelite
		do
			[ $((CNT++)) -gt 10 ] && break || sleep 1
		done
		if [ $CNT -gt 10 ]; then
			echo '[ ERROR ] Squeezelite took too long to terminate, please run a full package update.'
		 	RESULT=1
		fi		
		echo '[ INFO ] Removing old Squeezelite extension'
		if [ $RESULT -eq 0 -a -d /tmp/tcloop/pcp-squeezelite ]; then
			umount -d /tmp/tcloop/pcp-squeezelite
			RESULT=$?
		fi
		if [ $RESULT -ne 0 ]; then
			echo '[ ERROR ] Inplace update failed, please run a full package update.'
		else
			echo '[ INFO ] Updating Squeezelite extension'
			rm -f /usr/local/tce.installed/pcp-squeezelite
			mv -f /mnt/mmcblk0p2/tce/optional/pcp-squeezelite.tcz /tmp
			mv -f /mnt/mmcblk0p2/tce/optional/pcp-squeezelite.tcz.md5.txt /tmp
			if [ $DEBUG -eq 1 ]; then
				sudo -u tc pcp-load -r $PCP_REPO -w pcp-squeezelite.tcz 2>&1
			else
				sudo -u tc pcp-load -r $PCP_REPO -w pcp-squeezelite.tcz
			fi

			if [ $? -ne 0 ]; then
				DLERROR=1
				echo '[ ERROR ] Download unsuccessful, try again later!'
				mv -f /tmp/pcp-squeezelite.tcz /mnt/mmcblk0p2/tce/optional
				mv -f /tmp/pcp-squeezelite.tcz.md5.txt /mnt/mmcblk0p2/tce/optional
			else
				rm -f /tmp/pcp-squeezelite.tcz*
			fi
			echo '[ INFO ] Reloading squeezelite extension'
			sudo -u tc pcp-load -i pcp-squeezelite.tcz
			echo '[ OK ] Current Squeezelite version: '$(pcp_squeezelite_version)''
		fi
		[ $DEBUG -eq 1 ] && (echo '[ OK ] '; ls -al ${SQLT_BIN})
		echo '                </textarea>'
		pcp_table_end
	;;
	full_update)
		SPACE_REQUIRED=1300
		pcp_sufficient_free_space $SPACE_REQUIRED
		[ $? -eq 0 ] || pcp_end

		pcp_table_top "Updating Squeezelite and all libraries"
		echo '                <textarea class="inform" style="height:150px">'
		echo '[ INFO ] Updating Squeezelite extension.'
		echo '[ INFO ] a reboot will be required to complete.'

		TMP_UPG="/tmp/upgrade"
		rm -rf ${TMP_UPG}
		mkdir ${TMP_UPG}
		chown tc.staff ${TMP_UPG}

		if [ $DEBUG -eq 1 ]; then
			sudo -u tc pcp-load -r $PCP_REPO -w ${TMP_UPG}/pcp-squeezelite.tcz 2>&1
			[ $? -eq 0 ] && FAIL=0 || FAIL=1
		else
			sudo -u tc pcp-load -r $PCP_REPO -w ${TMP_UPG}/pcp-squeezelite.tcz
			[ $? -eq 0 ] && FAIL=0 || FAIL=1
		fi
		if [ $FAIL -eq 0 ]; then
			mkdir -p ${PACKAGEDIR}/upgrade
			mv ${TMP_UPG}/* ${PACKAGEDIR}/upgrade
			chown -R tc.staff ${PACKAGEDIR}/upgrade
			sync
			REBOOT_REQUIRED=1
		else
			echo '[ INFO ] Reloading old squeezelite extension'
		fi
		echo '                </textarea>'
		pcp_table_end
	;;
	inst_ffmpeg)
		pcp_table_top "Installing FFMpeg extension"
		SPACE_REQUIRED=7000
		pcp_sufficient_free_space $SPACE_REQUIRED
		[ $? -eq 0 ] || pcp_end
		echo '                <textarea class="inform" style="height:100px">'
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
		echo '                </textarea>'
		pcp_table_end
	;;
	rem_ffmpeg)
		pcp_table_top "Removing FFMpeg extension"
		echo '                <textarea class="inform" style="height:100px">'
		echo '[ INFO ] FFMpeg extension marked for removal. Reboot Required to complete.</p>'
		sudo -u tc tce-audit builddb
		sudo -u tc tce-audit delete pcp-libffmpeg.tcz
		sed -i '/pcp-libffmpeg.tcz/d' $ONBOOTLST
		REBOOT_REQUIRED=1
		echo '                </textarea>'
		pcp_table_end
	;;
	*) echo '<p class="error">[ ERROR ] Option Error!'
	;;
esac

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

pcp_end