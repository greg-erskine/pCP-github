#!/bin/sh

# Version: 7.0.0 2020-06-09

. /etc/init.d/tc-functions
. pcp-functions

pcp_html_head "Write to Jivelite Tweak" "SBP"

pcp_httpd_query_string
pcp_navbar

BUILD=$(getBuild)
MIRROR="${PCP_REPO%/}/$(getMajorVer).x/$BUILD/tcz"
WGET_JL="/bin/busybox wget"
JIVELITE_TCZ="pcp-jivelite.tcz"
DEFAULT_VUMETER="VU_Meter_Kolossos_Oval.tcz"
AVAILABLE_VUMETERS=$($WGET_JL $MIRROR -q -O - | grep -ow 'VU_Meter_\w*.tcz' | sort | uniq)

# Reboot required is default, some functions turn it off.
REBOOT_REQUIRED=TRUE

#========================================================================================
# Space required for jivelite
#----------------------------------------------------------------------------------------
#  6877184   pcp-jivelite.tcz
#   192512   touchscreen-4.14.56-pcpCore_v7.tcz
#    86016   libts.tcz
#     8192   libcofi.tcz
#   212992   pcp-lua.tcz
#  2891776   pcp-jivelite_hdskins.tcz
#   471040   VU_Meter_Jstraw_Dark.tcz
#   348160   VU_Meter_Jstraw_Dark_Peak.tcz
#   434176   VU_Meter_Jstraw_Vintage.tcz
#   253952   VU_Meter_Kolossos_Oval.tcz
#   282624   VU_Meter_Logitech_Black.tcz
#   393216   VU_Meter_Logitech_White.tcz
#----------
# 12451840
#----------------------------------------------------------------------------------------
SPACE_REQUIRED=13000

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_html_end() {
	pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 10
	pcp_infoxbox_end
	pcp_footer
	pcp_copyright
	[ $REBOOT_REQUIRED ] && pcp_lirc_popup
	echo '</body>'
	echo '</html>'
	exit
}

pcp_jivelite_debug() {
	pcp_debug_variables "html" MIRROR OPTION ACTION JIVELITE VISUALISER VUMETER JIVELITE_TCZ JIVELITE_MD5 DEFAULT_VUMETER AVAILABLE_VUMETERS
}

pcp_download_jivelite() {
	JIVELITE_SUCCESS=FALSE
	if [ $(pcp_pcp_repo_accessible) -eq 0 ]; then
		[ $DEBUG -eq 1 ] && pcp_message INFO "pCP Repository available..." $MTYPE
		pcp_message INFO "Downloading Jivelite from the pCP Repository..." $MTYPE
		pcp_message INFO "Downloading will take a few minutes. Please wait..." $MTYPE
		sudo -u tc pcp-load -r $PCP_REPO -w $JIVELITE_TCZ
		if [ $? -eq 0 ]; then
			pcp_message OK "$JIVELITE_TCZ download successful." $MTYPE
			JIVELITE_SUCCESS=TRUE
		else
			pcp_message ERROR "Download unsuccessful, MD5 mismatch, try again later!" $MTYPE
		fi
	else
		pcp_message ERROR "pCP Repository NOT available..." $MTYPE
	fi
}

pcp_install_jivelite() {
	# We don't need to install extension, since we are rebooting.
	pcp_message INFO "Jivelite is installed." $MTYPE
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Jivelite is added to onboot.lst" $MTYPE
	sed -i '/pcp-jivelite.tcz/d' $ONBOOTLST
	echo 'pcp-jivelite.tcz' >> $ONBOOTLST

	# New extension still installs into /opt.
	[ $DEBUG -eq 1 ] && pcp_message INFO "Jivelite is added to .xfiletool.lst" $MTYPE
	sed -i '/^opt\/jivelite/d' /opt/.xfiletool.lst
	echo 'opt/jivelite' >> /opt/.xfiletool.lst
}

pcp_delete_jivelite() {
	pcp_message INFO "Jivelite is removed from piCorePlayer." $MTYPE
	pcp_message INFO "" $MTYPE "-n"
	sudo -u tc tce-audit builddb
	echo
	pcp_message INFO "After a reboot these extensions will be permanently deleted:" $MTYPE
	sudo -u tc tce-audit delete $JIVELITE_TCZ
	echo
	sudo rm -rf /home/tc/.jivelite
	sudo sed -i '/pcp-jivelite.tcz/d' $ONBOOTLST
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Jivelite is removed from onboot.lst" $MTYPE
	sudo sed -i '/^opt\/jivelite/d' /opt/.xfiletool.lst
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Jivelite is removed from .xfiletool.lst" $MTYPE
	JIVELITE="no"
	VISUALISER="no"
	pcp_save_to_config
}

pcp_download_vumeters() {
	if [ $(pcp_pcp_repo_accessible) -eq 0 ]; then
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "pCP Repository available..." $MTYPE
		pcp_message INFO "Downloading VU Meters from the pCP Repository..." $MTYPE
		for METER in $AVAILABLE_VUMETERS
		do
			sudo -u tc pcp-load -r $PCP_REPO -w $METER
			if [ $? -eq 0 ]; then
				pcp_message OK "$METER download successful." $MTYPE
			else
				pcp_message ERROR "$METER download unsuccessful, MD5 mismatch, try again later!" $MTYPE
			fi
		done
	else
		pcp_message ERROR "pCP Repository NOT available..." $MTYPE
	fi
}

pcp_install_default_vumeter() {
	pcp_message INFO "Installing default VU Meter..." $MTYPE
	sudo sed -i '/VU_Meter/d' $ONBOOTLST
	sudo echo $DEFAULT_VUMETER >> $ONBOOTLST
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Adding default VU Meter to onboot.lst..." $MTYPE
}

pcp_install_vumeter() {
	pcp_message INFO "Installing VU Meter..." $MTYPE
	# Unmount all loop mounted VU_Meters.
	# There should be only one or none mounted.
	MOUNTED_METERS=$(df | grep VU_Meter | awk '{print $6}' )
	[ $DEBUG -eq 1 ] && pcp_message DEBUG $MOUNTED_METERS $MTYPE
	for METER in $MOUNTED_METERS
	do
		sudo umount $METER
	done
	rm -f /usr/local/tce.installed/VU_Meter*
	sudo rm /opt/jivelite/share/jive/applets/JogglerSkin/images/UNOFFICIAL/VUMeter/vu_analog_25seq_w.png
	sudo -u tc tce-load -i $VUMETER >/dev/null 2>&1
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "VU Meter is added to onboot.lst" $MTYPE
	sudo sed -i '/VU_Meter/d' $ONBOOTLST
	sudo echo $VUMETER >> $ONBOOTLST
}

pcp_delete_vumeters() {
	pcp_message INFO "Removing VU Meters..." $MTYPE
	pcp_message INFO "" $MTYPE "-n"
	sudo -u tc tce-audit builddb
	echo
	pcp_message INFO "After a reboot these extensions will be permanently deleted:" $MTYPE
	for METER in $(ls $PACKAGEDIR/VU_Meter*.tcz); do
		sudo -u tc tce-audit delete $METER
	done
	echo
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Removing VU Meter from onboot.lst..." $MTYPE
	sudo sed -i '/VU_Meter/d' $ONBOOTLST
}

pcp_lirc_popup() {
	if [ "$IR_LIRC" = "yes" ]; then
		STRING1='INFO: LIRC is enabled; you might need to remove/install LIRC again to fix problems. But first press [OK] to reboot now.'
		SCRIPT1='main.cgi?ACTION=reboot'
		pcp_confirmation_required
	else
		pcp_reboot_required
	fi
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_jivelite_debug

case "$OPTION" in
	JIVELITE)
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "Doing OPTION: $OPTION" $MTYPE
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "Doing with ACTION: $ACTION" $MTYPE
		case "$ACTION" in
			Install)
				MTYPE="text"
				pcp_heading5 "Install Jivelite"
				pcp_infobox_begin
				pcp_sufficient_free_space $SPACE_REQUIRED "text"
				if [ $? -eq 0 ]; then
					pcp_download_jivelite
					if [ $JIVELITE_SUCCESS ]; then
						pcp_install_jivelite
						JIVELITE="yes"
						VISUALISER="yes"
						pcp_download_vumeters
						pcp_install_default_vumeter
						pcp_save_to_config
						pcp_backup "text"
					else
						pcp_message ERROR "Error Downloading Jivelite, try again later." $MTYPE
					fi
				fi
				pcp_infobox_end
			;;
			Onboot)
				MTYPE="text"
				pcp_heading5 "Setting Jivelite onboot behaviour"
				pcp_infobox_begin
				if [ "$JIVELITE" = "yes" ]; then
					VISUALISER="yes"
					pcp_message INFO "Setting Jivelite to automatically start during boot..." $MTYPE
				else
					VISUALISER="no"
					pcp_message INFO "Setting Jivelite to not start during boot..." $MTYPE
				fi
				pcp_save_to_config
				pcp_backup "text"
				pcp_infobox_end
				unset REBOOT_REQUIRED
			;;
			Remove)
				MTYPE="text"
				pcp_heading5 "Removing Jivelite"
				pcp_infobox_begin
				pcp_delete_jivelite
				pcp_delete_vumeters
				pcp_backup "text"
				pcp_infobox_end
				REBOOT_REQUIRED=TRUE
			;;
			Reset)
				unset REBOOT_REQUIRED
				MTYPE="text"
				pcp_heading5 "Resetting Jivelite"
				pcp_infobox_begin
				pcp_message INFO "Resetting Jivelite Configuration..." $MTYPE
				rm -f /home/tc/.jivelite/userpath/settings/*.lua
				pcp_backup "text"

				sudo kill -SIGTERM `pidof jivelite`

				if [ $? -ne 0 ]; then
					pcp_message ERROR "Jivelite not killed..." $MTYPE
				else
					pcp_message OK "Jivelite killed..." $MTYPE
				fi

				pcp_message INFO "Jivelite has been reset and restarted." $MTYPE
				pcp_message INFO "Reconfigure Jivelite and then backup changes!" $MTYPE
				pcp_infobox_end
			;;
			Update)
				MTYPE="text"
				pcp_heading5 "Updating Jivelite"
				pcp_infobox_begin
				pcp_sufficient_free_space $SPACE_REQUIRED "text"
				if [ $? -eq 0 ]; then
					pcp-update pcp-jivelite.tcz
					CHK=$?
					if [ $CHK -eq 2 ]; then
						pcp_message INFO "There is no update for Jivelite at this time." $MTYPE
						unset REBOOT_REQUIRED
					elif [ $CHK -eq 1 ]; then
						pcp_message ERROR "'There was an error updating Jivelite, please try again later." $MTYPE
						unset REBOOT_REQUIRED
					else
						REBOOT_REQUIRED=TRUE
					fi
					for METER in $(PACKAGEDIR/VU_Meter*.tcz); do
						pcp-update $METER
						if [ $? -eq 0 ]; then
							pcp_message INFO "There was an update to VU Meters." $MTYPE
							REBOOT_REQUIRED=TRUE
						fi
					done
				fi
				pcp_infobox_end
			;;
			*)
				MTYPE="text"
				[ $DEBUG -eq 1 ] && pcp_message DEBUG "JIVELITE: $JIVELITE" $MTYPE
				pcp_message ERROR "JIVELITE: $JIVELITE, Bad ACTION: $ACTION" $MTYPE
				unset REBOOT_REQUIRED
			;;
		esac
	;;
	VUMETER)
		MTYPE="text"
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "Doing OPTION: $OPTION" $MTYPE
		case "$SUBMIT" in
			Save)
				pcp_install_vumeter
				pcp_message INFO "A restart of Jivelite is needed in order to finalize!" $MTYPE
				pcp_message INFO "Jivelite will now restart!" $MTYPE
				sudo kill -SIGTERM `pidof jivelite`
				unset REBOOT_REQUIRED
			;;
			Download)
				pcp_download_vumeters
			;;
		esac
	;;
esac

pcp_html_end