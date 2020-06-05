#!/bin/sh

# Version: 7.0.0 2020-06-05

. pcp-functions
. pcp-soundcard-functions

# Store the original values so we can see if they are changed
ORIG_ALSAeq=$ALSAeq
ORIG_EQUAL_OUT_DEVICE=$EQUAL_OUT_DEVICE
ORIG_SHAIRPORT=$SHAIRPORT
ORIG_SQUEEZELITE=$SQUEEZELITE
ORIG_STREAMER=$STREAMER
ORIG_STREAMER_IN_DEVICE="$STREAMER_IN_DEVICE"
ORIG_FIQ=$FIQ
ORIG_CMD=$CMD
ORIG_FSM=$FSM

unset VARIABLE_CHANGED
unset REBOOT_REQUIRED
unset OUTPUTCONFIRM
unset RESTART_SQLT

pcp_html_head "Write to Audio Tweak" "SBP"

pcp_navbar
pcp_httpd_query_string

pcp_heading5 "Audio tweak"
pcp_infobox_begin

#========================================================================================
# SQUEEZELITE section
#----------------------------------------------------------------------------------------
if [ "$ORIG_SQUEEZELITE" != "$SQUEEZELITE" ]; then
	VARIABLE_CHANGED=TRUE

	pcp_debug_variables "text" ORIG_SQUEEZELITE SQUEEZELITE
	pcp_message INFO "\$SQUEEZELITE is set to: $SQUEEZELITE" "text"

	case "$SQUEEZELITE" in
		yes)
			pcp_message INFO "Squeezelite will be enabled and start automatically." "text"
			CLOSEOUT="15"
		;;
		no)
			pcp_message INFO "Squeezelite will be disabled and will not start after a reboot." "text"
			CLOSEOUT=""
		;;
		*)
			pcp_message ERROR "Squeezelite selection invalid: $SQUEEZELITE" "text"
		;;
	esac
else
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "\$SQUEEZELITE variable unchanged." "text"
fi

#========================================================================================
# SHAIRPORT section
#----------------------------------------------------------------------------------------
# libcofi.tcz                   8192
# pcp-shairportsync.tcz       970752
#
# Total size (bytes)          978944
#----------------------------------------------------------------------------------------
pcp_download_shairport(){
	pcp_sufficient_free_space 1000
	pcp_message INFO "Downloading Shairport-sync..." "text"
	sudo -u tc pcp-load -w pcp-shairportsync.tcz
	if [ $? -eq 0 ]; then
		pcp_message INFO "Installing Shairport-sync..." "text"
		sudo -u tc pcp-load -i pcp-shairportsync.tcz
		return 0
	else
		pcp_message ERROR "Shairport download unsuccessful, try again!" "text"
		return 1
	fi
}

pcp_remove_shairport() {
	pcp_message INFO "Removing Shairport..." "text"
	/usr/local/etc/init.d/shairport-sync stop >/dev/null 2>&1
	pcp_message INFO "" "text" "-n"
	sudo -u tc tce-audit builddb
	echo
	pcp_message INFO "After a reboot these extensions will be permanently deleted:" "text"
	sudo -u tc tce-audit delete pcp-shairportsync.tcz
	echo
}

#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_SHAIRPORT" != "$SHAIRPORT" ]; then
	VARIABLE_CHANGED=TRUE

	pcp_debug_variables "text" ORIG_SHAIRPORT SHAIRPORT	
	pcp_message INFO "\$SHAIRPORT is set to: $SHAIRPORT" "text"

	case "$SHAIRPORT" in
		yes)
			pcp_message INFO "Shairport-sync will be enabled." "text"
			if [ -f $PACKAGEDIR/pcp-shairportsync.tcz ]; then
				[ $DEBUG -eq 1 ] && pcp_message DEBUG "Shairport-sync already loaded." "text"
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
			pcp_message INFO "Shairport-sync will be disabled." "text"
			pcp_remove_shairport
			sed -i '/pcp-shairportsync.tcz/d' $ONBOOTLST
			sync
			CLOSEOUT=""
		;;
		*)
			pcp_message ERROR "Shairport selection invalid: $SHAIRPORT" "text"
		;;
	esac
else
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "$SHAIRPORT variable unchanged." "text"
fi

#========================================================================================
# ALSA Equalizer section
#----------------------------------------------------------------------------------------
# alsaequal.tcz          24576
# caps.tcz              258048
# libasound.tcz         364544
#
# Total size (bytes)    647168
#----------------------------------------------------------------------------------------
pcp_download_alsaequal() {
	pcp_sufficient_free_space 700
	pcp_message INFO "Downloading ALSA Equalizer from repository..." "text"
	pcp_message INFO "Download will take a few minutes. Please wait..." "text"

	sudo -u tc pcp-load -wi alsaequal.tcz
	if [ $? -eq 0 ]; then
		pcp_message OK "Download successful." "text"
		return 0
	else
		pcp_message ERROR "ALSAequal download unsuccessful, try again!" "text"
		return 1
	fi

	SPACE=$(pcp_free_space k)
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Free space: ${SPACE}k" "text"
}

pcp_remove_alsaequal() {
	pcp_message INFO "Removing ALSA Equalizer..." "text"
	pcp_message INFO "" "text" "-n"
	sudo -u tc tce-audit builddb
	echo
	pcp_message INFO "After a reboot these extensions will be permanently deleted:" "text"
	sudo -u tc tce-audit delete alsaequal.tcz
	echo
	sudo rm -f /home/tc/.alsaequal.bin
}

pcp_set_equal_asound_output() {
	# $1 contains the hw named device.(hw:CARD=CODEC,DEV=0)
	local CNAME=$(echo $1 | awk -F'hw:CARD=' '{ print $2 }' | cut -d',' -f1)
	local DEVNO=$(echo $1 | awk -F'DEV=' '{ print $2 }')

	pcp_message INFO "$EQUAL_OUT_DEVICE is set to: $EQUAL_OUT_DEVICE" "text"
	pcp_debug_variables "text" CNAME DEVNO

	if [ "$CNAME" != "" ]; then
		sed -ir '/^pcm\.sound_device/,/\}/ s/card.*/card '$CNAME';/' $ASOUNDCONF
		sed -ir '/^pcm\.sound_device/,/\}/ s/\(^|\W\)device.*/device '$DEVNO';/' $ASOUNDCONF
	fi
}

#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_ALSAeq" != "$ALSAeq" ]; then
	VARIABLE_CHANGED=TRUE

	pcp_message INFO "$ALSAeq is set to: $ALSAeq" "text"

	# Determination of the number of the current sound-card
	# This probably isn't necessary, as we will check at boot time, when using alsaequal
	pcp_load_card_conf

	pcp_debug_variables "text" ORIG_ALSAeq ALSAeq CARDNO AUDIO

	case "$ALSAeq" in
		yes)
			pcp_message INFO "ALSA equalizer: $ALSAeq" "text"
			if grep -Fxq "alsaequal.tcz" $ONBOOTLST; then
				OUTPUT="equal"
				[ $DEBUG -eq 1 ] && pcp_message DEBUG "ALSA equalizer modules already loaded." "text"
			else
				pcp_download_alsaequal
				[ $? -eq 0 ] && OUTPUT="equal"
			fi
			if [ "$CARDNO" != "" ]; then
				# If more than one device is present on card, just set the first one.
				EQUAL_OUT_DEVICE=$(aplay -L | grep -E "^hw:" | grep $(cat /proc/asound/card${CARDNO}/id) | head -1) 
				pcp_set_equal_asound_output "$EQUAL_OUT_DEVICE"
			else
				pcp_message ERROR "Input device not selected. Select and re-save." "text"
			fi
			RESTART_SQLT=TRUE
		;;
		no)
			REBOOT_REQUIRED=TRUE
			pcp_message INFO "ALSA equalizer: $ALSAeq" "text"
			OUTPUT=""
			sudo sed -i '/alsaequal.tcz/d' $ONBOOTLST
			sudo sed -i '/caps/d' $ONBOOTLST
			pcp_remove_alsaequal
			OUTPUTCONFIRM=1
		;;
		*)
			pcp_message ERROR "ALSA equalizer invalid: $ALSAeq" "text"
		;;
	esac
else
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "$ALSAeq variable unchanged." "text"
fi

if [ "$ALSAeq" = "yes" -a "$ORIG_EQUAL_OUT_DEVICE" != "$EQUAL_OUT_DEVICE" ]; then
	VARIABLE_CHANGED=TRUE
	RESTART_SQLT=TRUE
	pcp_set_equal_asound_output "$EQUAL_OUT_DEVICE"
else
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "$EQUAL_OUT_DEVICE variable unchanged." "text"
fi

#========================================================================================
# pCP Streamer section
#----------------------------------------------------------------------------------------
# Total size (bytes)       3489792
# Need to download (bytes) 1466368
#----------------------------------------------------------------------------------------
pcp_download_streamer() {
	pcp_sufficient_free_space 1600
	pcp_message INFO "Downloading pCP Streamer..." "text"
	pcp_message INFO "Download will take a few minutes. Please wait..." "text"

	sudo -u tc pcp-load -wi pcp-streamer.tcz
	if [ $? -eq 0 ]; then
		pcp_message OK "Download successful." "text"
	else
		pcp_message ERROR "pCP Streamer download unsuccessful, try again!" "text"
	fi

	SPACE=$(pcp_free_space k)
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Free space: $SPACE" "text"
}

pcp_remove_streamer() {
	pcp_message INFO "Removing pCP Streamer..." "text"
	pcp_message INFO "" "text" "-n"
	sudo -u tc tce-audit builddb
	echo
	pcp_message INFO "After a reboot these extensions will be permanently deleted:" "text"
	sudo -u tc tce-audit delete pcp-streamer.tcz
	echo
}

pcp_set_streamer_asound_output() {
	# $1 contains the hw named device.(hw:CARD=CODEC,DEV=0)
	local CNAME=$(echo $1 | awk -F'hw:CARD=' '{ print $2 }' | cut -d',' -f1)
	local DEVNO=$(echo $1 | awk -F'DEV=' '{ print $2 }')

	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Card Full Name: $1" "text"
	pcp_message INFO "Setting Streamer asound to: $CNAME" "text"

	pcp_debug_variables "text" CNAME DEVNO
	if [ "$CNAME" != "" ]; then
		sed -ir '/^pcm\.pcpinput/,/\}/ s/card.*/card '$CNAME';/' $ASOUNDCONF
		sed -ir '/^pcm\.pcpinput/,/\}/ s/device.*/device '$DEVNO';/' $ASOUNDCONF
	fi
}

#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_STREAMER" != "$STREAMER" ] || [ "$STREAMER" == "yes" -a "$ORIG_STREAMER_IN_DEVICE" != "$STREAMER_IN_DEVICE" ]; then
	VARIABLE_CHANGED=TRUE

	pcp_debug_variables "text" ORIG_STREAMER STREAMER ORIG_STREAMER_IN_DEVICE STREAMER_IN_DEVICE INCARD AUDIO

	case "$STREAMER" in
		yes)
			pcp_message INFO "pCP Streamer: $STREAMER" "text"
			if grep -Fxq "pcp-streamer.tcz" $ONBOOTLST; then
				[ $DEBUG -eq 1 ] && pcp_message DEBUG "pCP Streamer module is already loaded." "text"
			else
				pcp_download_streamer
			fi
			if [ "$STREAMER_IN_DEVICE" = "" ]; then
				STREAMER_IN_DEVICE=$(arecord -L 2>/dev/null | grep -E "^hw:" | head -1)
			fi
			pcp_set_streamer_asound_output "$STREAMER_IN_DEVICE"

			/usr/local/etc/init.d/streamer restart
		;;
		no)
			REBOOT_REQUIRED=TRUE
			[ -x /usr/local/etc/init.d/streamer ] && /usr/local/etc/init.d/streamer stop
			pcp_message INFO "pCP Streamer: $STREAMER" "text"
			sudo sed -i '/pcp-streamer.tcz/d' $ONBOOTLST
			STREAMER_IN_DEVICE=""
			pcp_remove_streamer
		;;
		*)
			pcp_message ERROR "pCP Streamer invalid: $STREAMER" "text"
		;;
	esac
else
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "$STREAMER variable unchanged." "text"
fi

#========================================================================================
# CMD section
#----------------------------------------------------------------------------------------
if [ "$ORIG_CMD" != "$CMD" ]; then
	VARIABLE_CHANGED=TRUE
	REBOOT_REQUIRED=TRUE

	pcp_debug_variables "text" ORIG_CMD CMD
	pcp_message INFO "\$CMD is set to: $CMD" "text"

	case "$CMD" in
		Default)
			pcp_mount_bootpart
			if mount | grep $VOLUME >/dev/null; then
				# Remove dwc_otg_speed=1
				sed -i 's/dwc_otg.speed=1 //g' $CMDLINETXT
				[ $DEBUG -eq 1 ] && pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT"
				pcp_umount_bootpart
			else
				pcp_message ERROR "$VOLUME not mounted." "text"
			fi
		;;
		Slow)
			pcp_mount_bootpart
			if mount | grep $VOLUME >/dev/null; then
				# Remove dwc_otg_speed=1
				sed -i 's/dwc_otg.speed=1 //g' $CMDLINETXT
				# Add dwc_otg_speed=1
				sed -i '1 s/^/dwc_otg.speed=1 /' $CMDLINETXT
				[ $DEBUG -eq 1 ] && pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT" 
				pcp_umount_bootpart
			else
				pcp_message ERROR "$VOLUME not mounted." "text"
			fi
		;;
		*)
			pcp_message ERROR "\$CMD invalid: $CMD" "text"
		;;
	esac
else
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "\$CMD variable unchanged." "text"
fi

#========================================================================================
# USB_FIQ FSM section
#----------------------------------------------------------------------------------------
if [ "$ORIG_FSM" != "$FSM" ]; then
	VARIABLE_CHANGED=TRUE
	REBOOT_REQUIRED=TRUE

	pcp_debug_variables "text" ORIG_FSM FSM
	pcp_message INFO "$FSM is set to: $FSM" "text"

	case "$FSM" in
		Default)
			pcp_mount_bootpart
			if mount | grep $VOLUME >/dev/null; then
				# dwc_otg.fiq_fsm_enable=0
				sed -i 's/dwc_otg.fiq_fsm_enable=0 \+//g' $CMDLINETXT
				[ $DEBUG -eq 1 ] && pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT"
				pcp_umount_bootpart
			else
				pcp_message ERROR "$VOLUME not mounted" "text"
			fi
		;;
		Disabled)
			pcp_mount_bootpart
			if mount | grep $VOLUME >/dev/null; then
				# Remove dwc_otg.fiq_fsm_enable=0
				sed -i 's/dwc_otg.fiq_fsm_enable=0 \+//g' $CMDLINETXT
				# Add dwc_otg.fiq_fsm_enable=0
				sed -i '1 s/^/dwc_otg.fiq_fsm_enable=0 /' $CMDLINETXT
				[ $DEBUG -eq 1 ] && pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT"
				pcp_umount_bootpart
			else
				pcp_message ERROR "$VOLUME not mounted" "text"
			fi
		;;
	esac
else
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "\$FSM variable unchanged." "text"
fi

#========================================================================================
# FIQ split section
#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_FIQ" != "$FIQ" ]; then
	VARIABLE_CHANGED=TRUE
	REBOOT_REQUIRED=TRUE

	pcp_debug_variables "text" ORIG_FIG FIQ
	pcp_message INFO "\$FIQ is set to: $FIQ" "text"

	pcp_mount_bootpart
	if mount | grep $VOLUME >/dev/null; then
		# Remove fiq settings
		sed -i 's/dwc_otg.fiq_fsm_mask=0x[1-8F] \+//g' $CMDLINETXT
		# Add FIQ settings from config file
		sed -i '1 s/^/dwc_otg.fiq_fsm_mask='$FIQ' /' $CMDLINETXT
		[ $DEBUG -eq 1 ] && pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT"
		pcp_umount_bootpart
	else
		pcp_message ERROR "$VOLUME not mounted" "text"
	fi
else
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "\$FIQ variable unchanged." "text"
fi

if [ $OUTPUTCONFIRM ]; then
	STRING1='You have removed ALSA equalizer. Please fill out the OUTPUT field on the Squeezelite page. Press [OK] to go back and change or [Cancel] to continue'
	SCRIPT1=squeezelite.cgi
	pcp_confirmation_required
fi

#----------------------------------------------------------------------------------------
if [ $VARIABLE_CHANGED ]; then
	pcp_save_to_config
	pcp_backup "text"
	if [ $DEBUG -eq 1 ]; then
		pcp_textarea "Current $ASOUNDCONF" "cat $ASOUNDCONF" 15
		pcp_textarea "Current $ONBOOTLST" "cat $ONBOOTLST" 15
		pcp_textarea "Current $PCPCFG" "cat $PCPCFG" 15
	fi
	[ $REBOOT_REQUIRED ] && pcp_reboot_required
else
	pcp_message INFO "Variables unchanged." "text"
	pcp_message INFO "Nothing to do." "text"
fi

[ $RESTART_SQLT ] && pcp_squeezelite_restart

pcp_infobox_end
#----------------------------------------------------------------------------------------
[ $DEBUG -eq 0 ] && DELAY=15 || DELAY=9999
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" "$DELAY"

pcp_html_end
exit
