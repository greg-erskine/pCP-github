#!/bin/sh

# Version: 3.5.0 2018-02-28
#	Fixed removal of Jivelite. SBP.
#	Cleanup. GE.
#	REMOVED. Added check that pCP Sourceforge Repository is available. GE.

# Version: 3.21 2017-05-20
#	Changed to allow booting from USB on RPI3. PH.

# Version: 3.20 2017-04-16
#	Fixed pcp-xxx-functions issues. GE.
#	Updated Jivelite to PCP_Repo. PH.
#	Changed Reboot function. PH.

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.
#	Write jivelite.tcz.dep, instead of relying on it to be in base image. PH.
#	TODO: Move Jivelite to repo with pcp-load.

# Version: 0.07 2016-05-09 GE
#	Fixed JIVELITE variable (YES/NO).

# Version: 0.06 2016-02-20 GE
#	Fixed sourceforge redirection issue.

# Version: 0.05 2015-12-19 GE
#	Added /bin/busybox to wget -s
#	Minor changes.

# Version: 0.04 2015-11-22 GE
#	Added code for VU Meters.
#	Revised Jivelite download code.

# Version: 0.03 2015-08-29 SBP
#	Changed to touch-screen version.

# Version: 0.02 2015-05-08 GE
#	Revised.

# Version: 0.01 2015-03-15 SBP
#	Original version.

. /etc/init.d/tc-functions
. pcp-functions

pcp_html_head "Write to Jivelite Tweak" "SBP" "150000" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

BUILD=$(getBuild)
MIRROR="${PCP_REPO%/}/$(getMajorVer).x/$BUILD/tcz"
WGET="/bin/busybox wget"
JIVELITE_TCZ="pcp-jivelite.tcz"
DEFAULT_VUMETER="VU_Meter_Kolossos_Oval.tcz"
AVAILABLE_VUMETERS=$($WGET $MIRROR -q -O - | grep -ow 'VU_Meter_\w*.tcz' | sort | uniq)

# Reboot is default, some functions turn it off.
REBOOT_REQUIRED=1

if [ $DEBUG -eq 1 ]; then
	echo '<p class="debug">[ DEBUG ] MIRROR: '$MIRROR'<br />'
	echo '                 [ DEBUG ] OPTION: '$OPTION'<br />'
	echo '                 [ DEBUG ] ACTION: '$ACTION'<br />'
	echo '                 [ DEBUG ] JIVELITE: '$JIVELITE'<br />'
	echo '                 [ DEBUG ] VISUALISER: '$VISUALISER'<br />'
	echo '                 [ DEBUG ] VUMETER: '$VUMETER'</p>'
	echo '                 [ DEBUG ] JIVELITE_TCZ: '$JIVELITE_TCZ'<br />'
	echo '                 [ DEBUG ] JIVELITE_MD5: '$JIVELITE_MD5'<br />'
	echo '                 [ DEBUG ] DEFAULT_VUMETER: '$DEFAULT_VUMETER'<br />'
	echo '                 [ DEBUG ] AVAILABLE_VUMETERS: '$AVAILABLE_VUMETERS'</p>'
fi

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_check_repos() {
	if [ pcp_pcp_repo_accessible -eq 0 ]; then
		echo '[ INFO ] pCP Sourceforge Repository available...'
		return 0
	else
		echo '[ ERROR ] pCP Sourceforge Repository NOT available...'
		return 1
	fi
}

pcp_download_jivelite() {
	JIVE_SUCCESS=0
#	pcp_check_repos
#	if [ $? -eq 0 ]; then
		echo '[ INFO ] Downloading Jivelite from the pCP Repository...'
		echo '[ INFO ] Downloading will take a few minutes. Please wait...'

		sudo -u tc pcp-load -r $PCP_REPO -w ${JIVELITE_TCZ}
		if [ $? -eq 0 ]; then
			echo '[ OK ] '$JIVELITE_TCZ' download successful.'
			JIVE_SUCCESS=1
		else
			echo '[ ERROR ] Download unsuccessful, MD5 mismatch, try again later!'
		fi
#	fi
}

pcp_install_jivelite() {
	# We don't need to install extension, since we are rebooting.
	echo '[ INFO ] Jivelite is installed.'
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] Jivelite is added to onboot.lst'
	sed -i '/pcp-jivelite.tcz/d' $ONBOOTLST
	echo 'pcp-jivelite.tcz' >> $ONBOOTLST

	# New extension still installs into /opt.
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] Jivelite is added to .xfiletool.lst'
	sed -i '/^opt\/jivelite/d' /opt/.xfiletool.lst
	echo 'opt/jivelite' >> /opt/.xfiletool.lst
}

pcp_delete_jivelite() {
	echo '<p class="info">[ INFO ] Jivelite is removed from piCorePlayer.</p>'
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete ${JIVELITE_TCZ}
	sudo rm -rf /home/tc/.jivelite
	sudo sed -i '/pcp-jivelite.tcz/d' $ONBOOTLST
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is removed from onboot.lst</p>'
	sudo sed -i '/^opt\/jivelite/d' /opt/.xfiletool.lst
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is removed from .xfiletool.lst</p>'
	JIVELITE="no"
	VISUALISER="no"
	pcp_save_to_config
}

pcp_download_vumeters() {
#	pcp_check_repos
#	if [ $? -eq 0 ]; then
		echo '[ INFO ] Downloading VU Meters from the pCP Sourceforge Repository...'
		for i in $AVAILABLE_VUMETERS
		do
			TCZ=${i}
			sudo -u tc pcp-load -r $PCP_REPO -w ${TCZ}
			if [ $? -eq 0 ]; then
				echo '[ OK ] '$TCZ' download successful.'
			else
				echo '[ ERROR ] Download unsuccessful, MD5 mismatch, try again later!'
			fi
		done
#	fi
}

pcp_install_default_vumeter() {
	echo '[ INFO ] Installing default VU Meter...'
	sudo sed -i '/VU_Meter/d' $ONBOOTLST
	sudo echo $DEFAULT_VUMETER >> $ONBOOTLST
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] Adding default VU Meter to onboot.lst...'
}

pcp_install_vumeter() {
	echo '<p class="info">[ INFO ] Installing VU Meter...</p>'

	# Unmount all loop mounted VU_Meters (Note: should be only zero or one)
	MOUNTED_METERS=$(df | grep VU_Meter | awk '{print $6}' )
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] '$MOUNTED_METERS'</p>'

	for i in $MOUNTED_METERS
	do
		sudo umount $i
	done

	rm -f /usr/local/tce.installed/VU_Meter*
	sudo rm /opt/jivelite/share/jive/applets/JogglerSkin/images/UNOFFICIAL/VUMeter/vu_analog_25seq_w.png
	sudo -u tc tce-load -i $VUMETER >/dev/null 2>&1
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] VU Meter is added to onboot.lst</p>'
	sudo sed -i '/VU_Meter/d' $ONBOOTLST
	sudo echo $VUMETER >> $ONBOOTLST
}

pcp_delete_vumeters() {
	echo '<p class="info">[ INFO ] Removing VU Meters...</p>'
	sudo -u tc tce-audit builddb
	for i in $(ls $PACKAGEDIR/VU_Meter*.tcz); do
		sudo -u tc tce-audit delete $i
	done
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Removing VU Meter from onboot.lst...</p>'
	sudo sed -i '/VU_Meter/d' $ONBOOTLST
}

pcp_lirc_popup() {
	if [ "$IR_LIRC" = "yes" ]; then
		STRING1='INFO: LIRC is enabled; you might need to remove/install LIRC again to fix problems. But first press [OK] to reboot now.'
		SCRIPT1='reboot.cgi?RB=yes'
		pcp_confirmation_required
	else
		pcp_reboot_required
	fi
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_table_top "Jivelite"

case "$OPTION" in
	JIVELITE)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Doing OPTION: '$OPTION'<br />'
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Doing with ACTION: '$ACTION'<br />'
		case "$ACTION" in
			Install)
				# Jivelite requires about 11MB and Meters require 22MB
				pcp_sufficient_free_space 34000
				if [ $? -eq 0 ]; then
					echo '                <textarea class="inform" style="height:300px">'
					pcp_download_jivelite
					if [ $JIVE_SUCCESS -eq 1 ]; then
						pcp_install_jivelite
						JIVELITE="yes"
						VISUALISER="yes"
						pcp_download_vumeters
						pcp_install_default_vumeter
						pcp_save_to_config
						pcp_backup "nohtml"
					else
						echo '[ ERROR ] Error Downloading Jivelite, try again later.'
					fi
					echo '                </textarea>'
				fi
			;;
			Onboot)
				[ "$JIVELITE" = "yes" ] && VISUALISER="yes" || VISUALISER="no"
				pcp_save_to_config
				pcp_backup
				REBOOT_REQUIRED=0
			;;
			Remove)
				pcp_delete_jivelite
				pcp_delete_vumeters
				pcp_backup
			;;
			Reset)
				echo '<p class="info">[ INFO ] Resetting Jivelite Configuration......</p>'
				rm -f /home/tc/.jivelite/userpath/settings/*.lua
				pcp_backup
				pkill -SIGTERM jivelite
				echo '<p class="info">[ INFO ] Jivelite has been reset and restarted. Reconfigure Jivelite and then backup changes!</p>'
				REBOOT_REQUIRED=0
			;;
			Update)
				# Use full space requirement for Jivelite, incase many extensions need updated.
				pcp_sufficient_free_space 34000
				if [ $? -eq 0 ]; then
					echo '                <textarea class="inform" style="height:150px">'
					pcp-update pcp-jivelite.tcz
					CHK=$?
					if [ $CHK -eq 2 ]; then
						echo '[ INFO ] There is no update for Jivelite at this time.'
						REBOOT_REQUIRED=0
					elif [ $CHK -eq 1 ]; then
						echo '[ ERROR ] There was an error updating Jivelite, please try again later.'
						REBOOT_REQUIRED=0
					else
						REBOOT_REQUIRED=1
					fi
					for i in $(PACKAGEDIR/VU_Meter*.tcz); do
						pcp-update $i
						if [ $? -eq 0 ]; then
							echo '[ INFO ] There was an update to VU Meters.'
							REBOOT_REQUIRED=1
						fi
					done
					echo '                </textarea>'
				fi
			;;
			*)
				[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] JIVELITE: '$JIVELITE'<br />'
				echo '<p class="error">[ ERROR ] JIVELITE: '$JIVELITE', Bad ACTION:'$ACTION'<br />'
				REBOOT_REQUIRED=0
			;;
		esac
		if [ $REBOOT_REQUIRED -eq 1 ]; then
			echo '<p class="info">[ INFO ] A reboot is needed in order to finalize!</p>'
			pcp_lirc_popup
		fi
		[ $DEBUG -eq 1 ] && pcp_show_config_cfg
	;;
	VUMETER)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Doing OPTION: '$OPTION'<br />'
		case "$SUBMIT" in
			Save)
				pcp_install_vumeter
				echo '<p class="info">[ INFO ] A restart of Jivelite is needed in order to finalize!</p>'
				echo '<p class="info">[ INFO ] Jivelite will now restart!</p>'
				sudo pkill -SIGTERM jivelite
			;;
			Download)
				pcp_download_vumeters
			;;
		esac
	;;
esac

pcp_table_middle
pcp_go_back_button
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
