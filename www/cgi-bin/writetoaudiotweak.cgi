#!/bin/sh

# Version: 4.0.0 2018-08-04

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

WGET="/bin/busybox wget"
CAPS="caps-0.4.5"

unset VARIABLE_CHANGED
unset REBOOT_REQUIRED

pcp_html_head "Write to Audio Tweak" "SBP"

pcp_banner
pcp_running_script
pcp_httpd_query_string

pcp_table_top "Audio tweak"

#========================================================================================
# SQUEEZELITE section
#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_SQUEEZELITE" != "$SQUEEZELITE" ]; then
	VARIABLE_CHANGED=TRUE

	echo '<p class="info">[ INFO ] $SQUEEZELITE is set to: '$SQUEEZELITE'</p>'

	if [ $DEBUG -eq 1 ]; then
		echo '<p class="debug">[ DEBUG ] $ORIG_SQUEEZELITE is: '$ORIG_SQUEEZELITE'<br />'
		echo '                 [ DEBUG ] $SQUEEZELITE is: '$SQUEEZELITE'</p>'
	fi

	case "$SQUEEZELITE" in
		yes)
			echo '<p class="info">[ INFO ] Squeezelite will be enabled and start automatically.</p>'
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
else
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] $SQUEEZELITE variable unchanged.</p>'
fi

#========================================================================================
# SHAIRPORT section
#----------------------------------------------------------------------------------------
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

#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_SHAIRPORT" != "$SHAIRPORT" ]; then
	VARIABLE_CHANGED=TRUE

	echo '<p class="info">[ INFO ] $SHAIRPORT is set to: '$SHAIRPORT'</p>'

	if [ $DEBUG -eq 1 ]; then
		echo '<p class="debug">[ DEBUG ] $ORIG_SHAIRPORT is: '$ORIG_SHAIRPORT'<br />'
		echo '<p class="debug">[ DEBUG ] $SHAIRPORT is: '$SHAIRPORT'</p>'
	fi

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
			REBOOT_REQUIRED=TRUE
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
else
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] $SHAIRPORT variable unchanged.</p>'
fi

#========================================================================================
# ALSA output level section
#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_ALSAlevelout" != "$ALSAlevelout" ]; then
	VARIABLE_CHANGED=TRUE

	echo '<p class="info">[ INFO ] $ALSAlevelout is set to: '$ALSAlevelout'</p>'

	if [ $DEBUG -eq 1 ]; then
		echo '<p class="debug">[ DEBUG ] $ORIG_ALSAlevelout is: '$ORIG_ALSAlevelout'<br />'
		echo '                 [ DEBUG ] $ALSAlevelout is: '$ALSAlevelout'</p>'
	fi

else
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] $ALSAlevelout variable unchanged.</p>'
fi

#========================================================================================
# ALSA Equalizer section
#----------------------------------------------------------------------------------------
#  24576 alsaequal.tcz
# 733184 caps-0.4.5.tcz
# ------
# 757760
#----------------------------------------------------------------------------------------
pcp_download_alsaequal() {
	pcp_sufficient_free_space 800
	echo '<p class="info">[ INFO ] Downloading ALSA Equalizer from repository...</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] repo: '${PCP_REPO}'</p>'
	echo '<p class="info">[ INFO ] Download will take a few minutes. Please wait...</p>'

	sudo -u tc pcp-load -r $PCP_REPO -wi alsaequal.tcz
	if [ $? -eq 0 ]; then
		echo '<p class="ok">[ OK ] Download successful.</p>'
	else
		echo '<p class="error">[ ERROR ] Alsaequal download unsuccessful, try again!</p>'
	fi

	SPACE=$(pcp_free_space k)
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Free space: '$SPACE'k</p>'
}

pcp_remove_alsaequal() {
	echo '<p class="info">[ INFO ] Removing ALSA Equalizer...</p>'
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete alsaequal.tcz
	sudo rm -f /home/tc/.alsaequal.bin
}

#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_ALSAeq" != "$ALSAeq" ]; then
	VARIABLE_CHANGED=TRUE
	REBOOT_REQUIRED=TRUE

	echo '<p class="info">[ INFO ] $ALSAeq is set to: '$ALSAeq'</p>'

	# Determination of the number of the current sound-card
	# This probably isn't necessary, as we will check at boot time, when using alsaequal
	pcp_load_card_conf

	if [ $DEBUG -eq 1 ]; then
		echo '<p class="debug">[ DEBUG ] $ORIG_ALSAeq is: '$ORIG_ALSAeq'<br />'
		echo '                 [ DEBUG ] $ALSAeq is: '$ALSAeq'<br />'
		echo '                 [ DEBUG ] $Card has number: '$CARDNO'<br />'
		echo '                 [ DEBUG ] $AUDIO is: '$AUDIO'</p>'
	fi

	case "$ALSAeq" in
		yes)
			echo '<p class="info">[ INFO ] ALSA equalizer: '$ALSAeq'</p>'
			if grep -Fxq "alsaequal.tcz" $ONBOOTLST; then
				[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ALSA equalizer modules already loaded.</p>'
			else
				pcp_download_alsaequal
				OUTPUT="equal"
			fi
			[ "$CARDNO" != "" ] && sed -i "s/plughw:.*,0/plughw:"$CARDNO",0/g" /etc/asound.conf || echo '<p class="error">[ ERROR ] Unable to determine Card Number to setup ALSAEqual</p>'
		;;
		no)
			echo '<p class="info">[ INFO ] ALSA equalizer: '$ALSAeq'</p>'
			OUTPUT=""
			sudo sed -i '/alsaequal.tcz/d' $ONBOOTLST
			sudo sed -i '/caps/d' $ONBOOTLST
			pcp_remove_alsaequal
			STRING1='You have removed ALSA equalizer. Please fill out the OUTPUT field on the Squeezelite page. Press [OK] to go back and change or [Cancel] to continue'
			SCRIPT1=squeezelite.cgi
			pcp_confirmation_required
		;;
		*)
			echo '<p class="error">[ ERROR ] ALSA equalizer invalid: '$ALSAeq'</p>'
		;;
	esac
else
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] $ALSAeq variable unchanged.</p>'
fi

#========================================================================================
# CMD section
#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_CMD" != "$CMD" ]; then
	VARIABLE_CHANGED=TRUE
	REBOOT_REQUIRED=TRUE

	echo '<p class="info">[ INFO ] $CMD is set to: '$CMD'</p>'

	if [ $DEBUG -eq 1 ]; then
		echo '<p class="debug">[ DEBUG ] $ORIG_CMD is: '$ORIG_CMD'<br />'
		echo '                 [ DEBUG ] $CMD is: '$CMD'</p>'
	fi

	case "$CMD" in
		Default)
			pcp_mount_bootpart
			if mount | grep $VOLUME >/dev/null; then
				# Remove dwc_otg_speed=1
				sed -i 's/dwc_otg.speed=1 //g' $CMDLINETXT
				[ $DEBUG -eq 1 ] && pcp_textarea_inform "Current $CMDLINETXT" "cat $CMDLINETXT" 150
				pcp_umount_bootpart
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted.</p>'
			fi
		;;
		Slow)
			pcp_mount_bootpart
			if mount | grep $VOLUME >/dev/null; then
				# Remove dwc_otg_speed=1
				sed -i 's/dwc_otg.speed=1 //g' $CMDLINETXT
				# Add dwc_otg_speed=1
				sed -i '1 s/^/dwc_otg.speed=1 /' $CMDLINETXT
				[ $DEBUG -eq 1 ] && pcp_textarea_inform "Current $CMDLINETXT" "cat $CMDLINETXT" 150
				pcp_umount_bootpart
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted.</p>'
			fi
		;;
		*)
			echo '<p class="error">[ ERROR ] $CMD invalid: '$CMD'</p>'
		;;
	esac
else
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] $CMD variable unchanged.</p>'
fi

#========================================================================================
# USB_FIQ FSM section
#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_FSM" != "$FSM" ]; then
	VARIABLE_CHANGED=TRUE
	REBOOT_REQUIRED=TRUE

	echo '<p class="info">[ INFO ] $FSM is set to: '$FSM'</p>'

	if [ $DEBUG -eq 1 ]; then
		echo '<p class="debug">[ DEBUG ] $ORIG_FSM is: '$ORIG_FSM'<br />'
		echo '                 [ DEBUG ] $FSM is: '$FSM'</p>'
	fi

	case "$FSM" in
		Default)
			pcp_mount_bootpart
			if mount | grep $VOLUME >/dev/null; then
				# dwc_otg.fiq_fsm_enable=0
				sed -i 's/dwc_otg.fiq_fsm_enable=0 \+//g' $CMDLINETXT
				[ $DEBUG -eq 1 ] && pcp_textarea_inform "Current $CMDLINETXT" "cat $CMDLINETXT" 150
				pcp_umount_bootpart
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
			fi
		;;
		Disabled)
			pcp_mount_bootpart
			if mount | grep $VOLUME >/dev/null; then
				# Remove dwc_otg.fiq_fsm_enable=0
				sed -i 's/dwc_otg.fiq_fsm_enable=0 \+//g' $CMDLINETXT
				# Add dwc_otg.fiq_fsm_enable=0
				sed -i '1 s/^/dwc_otg.fiq_fsm_enable=0 /' $CMDLINETXT
				[ $DEBUG -eq 1 ] && pcp_textarea_inform "Current $CMDLINETXT" "cat $CMDLINETXT" 150
				pcp_umount_bootpart
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
			fi
		;;
	esac
else
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] $FSM variable unchanged.</p>'
fi

#========================================================================================
# FIQ split section
#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_FIQ" != "$FIQ" ]; then
	VARIABLE_CHANGED=TRUE
	REBOOT_REQUIRED=TRUE

	echo '<p class="info">[ INFO ] $FIQ is set to: '$FIQ'</p>'

	if [ $DEBUG -eq 1 ]; then
		echo '<p class="debug">[ DEBUG ] $ORIG_FIG is: '$ORIG_FIQ'<br />'
		echo '                 [ DEBUG ] $FIQ is: '$FIQ'</p>'
	fi

	pcp_mount_bootpart
	if mount | grep $VOLUME >/dev/null; then
		# Remove fiq settings
		sed -i 's/dwc_otg.fiq_fsm_mask=0x[1-8F] \+//g' $CMDLINETXT
		# Add FIQ settings from config file
		sed -i '1 s/^/dwc_otg.fiq_fsm_mask='$FIQ' /' $CMDLINETXT
		[ $DEBUG -eq 1 ] && pcp_textarea_inform "Current $CMDLINETXT" "cat $CMDLINETXT" 150
		pcp_umount_bootpart
	else
		echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
	fi
else
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] $FIQ variable unchanged.</p>'
fi
#----------------------------------------------------------------------------------------

if [ $VARIABLE_CHANGED ]; then
	pcp_save_to_config
	pcp_backup
	if [ $DEBUG -eq 1 ]; then
		pcp_table_middle
		pcp_textarea_inform "Current $ASOUNDCONF" "cat $ASOUNDCONF" 150
		pcp_textarea_inform "Current $ONBOOTLST" "cat $ONBOOTLST" 150
		pcp_textarea_inform "Current $PCPCFG" "cat $PCPCFG" 150
	fi
	[ $REBOOT_REQUIRED ] && pcp_reboot_required
else
	echo '<p class="info">[ INFO ] Variables unchanged.</p>'
	echo '<p class="info">[ INFO ] Nothing to do.</p>'
fi

pcp_table_middle
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 15
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
