#!/bin/sh

# Version: 3.21 2017-07-08
#	Changed to allow booting from USB on RPI3. PH.
#	Updates for Alsaequal cardnumber

# Version: 3.20 2017-03-08
#	Changed pcp_picoreplayers_toolbar and pcp_controls. GE.
#	Fixed pcp-xxx-functions issues. GE.
#	Fixed remove alsaeq function. SBP.

# Version: 3.11 2017-01-24
#	Set CLOSEOUT empty when removing Shairport. PH.

# Version: 3.10 2016-12-23
#	Changes for pcp-shairportsync.tcz. PH.
#	Changes for sourceforge repo, also moved alsaequal to armv5&7 repos and changed install. PH.

# Version: 3.02 2016-09-05
#	Updated FIQ-split. SBP.

# Version: 0.01 2014-08-06 SBP
#	Original version.

. pcp-functions
. pcp-soundcard-functions

# Store the original values so we can see if they are changed
ORIG_ALSAeq=$ALSAeq
ORIG_SHAIRPORT=$SHAIRPORT
ORIG_SQUEEZELITE=$SQUEEZELITE
ORIG_ALSAlevelout=$ALSAlevelout
ORIG_FIQ=$FIQ
ORIG_CMD=$CMD
ORIG_FSM=$FSM

pcp_html_head "Write to Audio Tweak" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

WGET="/bin/busybox wget"
#EQREPOSITORY="https://sourceforge.net/projects/picoreplayer/files/tce/7.x/ALSAequal"
CAPS="caps-0.4.5"

# Only offer reboot option if needed
REBOOT_REQUIRED=0

#========================================================================================================
# Routines
#--------------------------------------------------------------------------------------------------------
pcp_download_shairport(){
	pcp_sufficient_free_space 500
	echo '<p class="info">[ INFO ] Downloading Shairport-sync...</p>'
	sudo -u tc pcp-load -r ${PCP_REPO} -w pcp-shairportsync.tcz
	if [ $? -eq 0 ]; then
		echo '<p class="info">[ INFO ] Installing Shairport-sync...</p>'
		sudo -u tc pcp-load -i pcp-shairportsync.tcz
		return 0
	else
		echo '<p class="error">[ ERROR ] Shairport download unsuccessful, try again!</p>'
		return 1
	fi
}

pcp_remove_shairport() {
	echo '<p class="info">[ INFO ] Removing Shairport...'
	/usr/local/etc/init.d/shairport-sync stop >/dev/null 2>&1
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete pcp-shairportsync.tcz
}

#========================================================================================
# ALSA output level section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ "$ORIG_ALSAlevelout" != "$ALSAlevelout" ]; then
	echo '<hr>'
	echo '<p class="info">[ INFO ] ALSAlevelout is set to: '$ALSAlevelout'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_ALSAlevelout is: '$ORIG_ALSAlevelout'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ALSAlevelout is: '$ALSAlevelout'</p>'
	echo '<hr>'
else
	echo '<p class="info">[ INFO ] ALSAlevelout variable unchanged.</p>'
fi

#========================================================================================
# ALSA Equalizer section
#
#  24576 alsaequal.tcz
# 733184 caps-0.4.5.tcz
# ------
# 757760
#----------------------------------------------------------------------------------------
#Routines
pcp_download_alsaequal() {
	pcp_sufficient_free_space 800
	echo '<p class="info">[ INFO ] Downloading ALSA Equalizer from repository...</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] repo: '${PCP_REPO}'</p>'
	echo '<p class="info">[ INFO ] Download will take a few minutes. Please wait...</p>'

	sudo -u tc pcp-load -r $PCP_REPO -wi alsaequal.tcz
	if [ $? -eq 0 ]; then
		echo '<p class="ok">[ OK ] Download successful.</p>'
	else
		echo '<p class="error">[ ERROR ] Alsaequalizer download unsuccessful, try again!</p>'
	fi

	SPACE=$(pcp_free_space k)
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Free space: '$SPACE'k</p>'
}

pcp_remove_alsaequal() {
	echo '<p class="info">[ INFO ] Removing ALSA Equalizer...</p>'
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete alsaequal.tcz
	sudo rm -f /home/tc/.alsaequal.bin
	REBOOT_REQUIRED=1
}

#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ "$ORIG_ALSAeq" != "$ALSAeq" ]; then
	REBOOT_REQUIRED=1
	echo '<hr>'
	echo '<p class="info">[ INFO ] ALSAeq is set to: '$ALSAeq'</p>'

	# Determination of the number of the current sound-card
	pcp_find_card_number   #This probably isn't necessary, as we will check at boot time, when using alsaequal

	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_ALSAeq is: '$ORIG_ALSAeq'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ALSAeq is: '$ALSAeq'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Card has number: '$CARDNO'.</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] AUDIO is: '$AUDIO'</p>'

	case "$ALSAeq" in
		yes)
			echo '<p class="info">[ INFO ] ALSA equalizer: '$ALSAeq'</p>'
			if grep -Fxq "alsaequal.tcz" $ONBOOTLST; then
				[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ALSA equalizer modules already loaded.</p>'
			else
				pcp_download_alsaequal
				OUTPUT="equal"
			fi
			sed -i "s/plughw:.*,0/plughw:"$CARDNO",0/g" /etc/asound.conf
		;;
		no)
			echo '<p class="info">[ INFO ] ALSA equalizer: '$ALSAeq'</p>'
			OUTPUT=""
			sudo sed -i '/alsaequal.tcz/d' $ONBOOTLST
			sudo sed -i '/caps/d' $ONBOOTLST
			pcp_remove_alsaequal
			STRING1='You have removed ALSA equalizer. Please fill out the OUTPUT field on the Squeezelite page. Press OK to go back and change or Cancel to continue'
			SCRIPT1=squeezelite.cgi
			pcp_confirmation_required
		;;
		*)
			echo '<p class="error">[ ERROR ] ALSA equalizer invalid: '$ALSAeq'</p>'
		;;
	esac
	echo '<hr>'
else
	echo '<p class="info">[ INFO ] ALSAeq variable unchanged.</p>'
fi

#========================================================================================
# CMD section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ "$ORIG_CMD" != "$CMD" ]; then
	REBOOT_REQUIRED=1
	echo '<hr>'
	echo '<p class="info">[ INFO ] CMD is set to: '$CMD'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_CMD is: '$ORIG_CMD'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] CMD is: '$CMD'</p>'

	case "$CMD" in
		Default)
			echo '<p class="info">[ INFO ] CMD: '$CMD'</p>'
			#sudo ./disableotg.sh

			pcp_mount_bootpart

			if mount | grep $VOLUME; then
				# Remove dwc_otg_speed=1
				sed -i 's/dwc_otg.speed=1 //g' $CMDLINETXT
				pcp_umount_bootpart
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
			fi
		;;
		Slow)
			echo '<p class="info">[ INFO ] CMD: '$CMD'</p>'
			#sudo ./enableotg.sh

			pcp_mount_bootpart

			if mount | grep $VOLUME; then
				# Remove dwc_otg_speed=1
				sed -i 's/dwc_otg.speed=1 //g' $CMDLINETXT

				# Add dwc_otg_speed=1
				sed -i '1 s/^/dwc_otg.speed=1 /' $CMDLINETXT
				pcp_umount_bootpart
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
			fi
		;;
		*)
			echo '<p class="error">[ ERROR ] CMD invalid: '$CMD'</p>'
		;;
	esac
	echo '<hr>'
else
	echo '<p class="info">[ INFO ] CMD variable unchanged.</p>'
fi

#========================================================================================
# USB_FIQ FSM section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ "$ORIG_FSM" != "$FSM" ]; then
	REBOOT_REQUIRED=1
	echo '<hr>'
	echo '<p class="info">[ INFO ] FSM is set to: '$FSM'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_FSM is: '$ORIG_FSM'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] FSM is: '$FSM'</p>'

	case "$FSM" in
		Default)
			echo '<p class="info">[ INFO ] FSM: '$FSM'</p>'

			pcp_mount_bootpart

			if mount | grep $VOLUME; then
				# dwc_otg.fiq_fsm_enable=0
				sed -i 's/dwc_otg.fiq_fsm_enable=0 \+//g' $CMDLINETXT
				[ $DEBUG -eq 1 ] && pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT" 150
				pcp_umount_bootpart
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
			fi
		;;
		Disabled)
			echo '<p class="info">[ INFO ] FSM: '$FSM'</p>'

			pcp_mount_bootpart

			if mount | grep $VOLUME; then
				# Remove dwc_otg.fiq_fsm_enable=0
				sed -i 's/dwc_otg.fiq_fsm_enable=0 \+//g' $CMDLINETXT

				# Add dwc_otg.fiq_fsm_enable=0
				sed -i '1 s/^/dwc_otg.fiq_fsm_enable=0 /' $CMDLINETXT
				[ $DEBUG -eq 1 ] && pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT" 150
				pcp_umount_bootpart
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
			fi
		;;
	esac
else
	echo '<p class="info">[ INFO ] USB FSM FIQ variable unchanged.</p>'
fi

#========================================================================================
# SQUEEZELITE section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ "$ORIG_SQUEEZELITE" != "$SQUEEZELITE" ]; then
	REBOOT_REQUIRED=1
	echo '<hr>'
	echo '<p class="info">[ INFO ] SQUEEZELITE is set to: '$SQUEEZELITE'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_SQUEEZELITE is: '$ORIG_SQUEEZELITE'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] SQUEEZELITE is: '$SQUEEZELITE'</p>'

	case "$SQUEEZELITE" in
		yes)
			echo '<p class="info">[ INFO ] Squeezelite will be enabled and start automatically when pCP is started.</p>'
			CLOSEOUT="15"
		;;
		no)
			echo '<p class="info">[ INFO ] Squeezelite will be disabled and will not start after a reboot.</p>'
			CLOSEOUT=""
		;;
		*)
			echo '<p class="error">[ ERROR ] Squeezelite selection invalid: '$SHAIRPORT'</p>'
		;;
	esac
	echo '<hr>'
else
	echo '<p class="info">[ INFO ] SQUEEZELITE variable unchanged.</p>'
fi

#========================================================================================
# SHAIRPORT section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ "$ORIG_SHAIRPORT" != "$SHAIRPORT" ]; then
	echo '<hr>'
	echo '<p class="info">[ INFO ] SHAIRPORT is set to: '$SHAIRPORT'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_SHAIRPORT is: '$ORIG_SHAIRPORT'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] SHAIRPORT is: '$SHAIRPORT'</p>'

	case "$SHAIRPORT" in
		yes)
			echo '<p class="info">[ INFO ] Shairport-sync will be enabled.</p>'
			if [ -f $PACKAGEDIR/pcp-shairportsync.tcz ]; then
				[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Shairport-sync already loaded.</p>'
				echo "pcp-shairportsync.tcz" >> $ONBOOTLST
			else
				pcp_download_shairport
				if [ $? -eq 0 ]; then
					echo "pcp-shairportsync.tcz" >> $ONBOOTLST
					/usr/local/etc/init.d/shairport-sync start
				fi
			fi
			CLOSEOUT="15"
		;;
		no)
			REBOOT_REQUIRED=1
			echo '<p class="info">[ INFO ] Shairport-sync will be disabled.</p>'
			pcp_remove_shairport
			sed -i '/pcp-shairportsync.tcz/d' $ONBOOTLST
			sync
			CLOSEOUT=""
		;;
		*)
			echo '<p class="error">[ ERROR ] Shairport selection invalid: '$SHAIRPORT'</p>'
		;;
	esac
	echo '<hr>'
else
	echo '<p class="info">[ INFO ] SHAIRPORT variable unchanged.</p>'
fi

#========================================================================================
# FIQ spilt section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ "$ORIG_FIQ" != "$FIQ" ]; then
	REBOOT_REQUIRED=1
	echo '<hr>'
	echo '<p class="info">[ INFO ] FIQ is set to: '$FIQ'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_FIG is: '$ORIG_FIQ'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] FIQ is: '$FIQ'</p>'

	pcp_mount_bootpart

	if mount | grep $VOLUME; then
		# Remove fiq settings
		sed -i 's/dwc_otg.fiq_fsm_mask=0x[1-8F] \+//g' $CMDLINETXT
		# Add FIQ settings from config file
		sed -i '1 s/^/dwc_otg.fiq_fsm_mask='$FIQ' /' $CMDLINETXT

		[ $DEBUG -eq 1 ] && pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT" 150
		pcp_umount_bootpart
	else
		echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
	fi
	echo '<hr>'
else
	echo '<p class="info">[ INFO ] FIQ variable unchanged.</p>'
fi
#----------------------------------------------------------------------------------------

echo '<hr>'
pcp_save_to_config
pcp_backup
[ $DEBUG -eq 1 ] && pcp_textarea "Current $ASOUNDCONF" "cat $ASOUNDCONF" 150
[ $DEBUG -eq 1 ] && pcp_textarea "Current $ONBOOTLST" "cat $ONBOOTLST" 150
[ $DEBUG -eq 1 ] && pcp_textarea "Current $CONFIGCFG" "cat $CONFIGCFG" 150

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required
pcp_go_back_button

echo '</body>'
echo '</html>'
