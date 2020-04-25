#!/bin/sh

# Version: 6.0.0 2020-02-23

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

pcp_banner
pcp_running_script
pcp_httpd_query_string

pcp_table_top "Audio tweak"
echo '                <textarea class="inform" style="height:160px">'
#========================================================================================
# SQUEEZELITE section
#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_SQUEEZELITE" != "$SQUEEZELITE" ]; then
	VARIABLE_CHANGED=TRUE

	echo '[ INFO ] $SQUEEZELITE is set to: '$SQUEEZELITE

	pcp_debug_variables "text" ORIG_SQUEEZELITE SQUEEZELITE

	case "$SQUEEZELITE" in
		yes)
			echo '[ INFO ] Squeezelite will be enabled and start automatically.'
			CLOSEOUT="15"
		;;
		no)
			echo '[ INFO ] Squeezelite will be disabled and will not start after a reboot.'
			CLOSEOUT=""
		;;
		*)
			echo '[ ERROR ] Squeezelite selection invalid: '$SHAIRPORT
		;;
	esac
else
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] $SQUEEZELITE variable unchanged.'
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
	echo '[ INFO ] Downloading Shairport-sync...'
	sudo -u tc pcp-load -w pcp-shairportsync.tcz
	if [ $? -eq 0 ]; then
		echo '[ INFO ] Installing Shairport-sync...'
		sudo -u tc pcp-load -i pcp-shairportsync.tcz
		return 0
	else
		echo '[ ERROR ] Shairport download unsuccessful, try again!'
		return 1
	fi
}

pcp_remove_shairport() {
	echo '[ INFO ] Removing Shairport...'
	/usr/local/etc/init.d/shairport-sync stop >/dev/null 2>&1
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete pcp-shairportsync.tcz
}

#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_SHAIRPORT" != "$SHAIRPORT" ]; then
	VARIABLE_CHANGED=TRUE

	echo '[ INFO ] $SHAIRPORT is set to: '$SHAIRPORT

	pcp_debug_variables "text" ORIG_SHAIRPORT SHAIRPORT

	case "$SHAIRPORT" in
		yes)
			echo '[ INFO ] Shairport-sync will be enabled.'
			if [ -f $PACKAGEDIR/pcp-shairportsync.tcz ]; then
				[ $DEBUG -eq 1 ] && echo '[ DEBUG ] Shairport-sync already loaded.'
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
			echo '[ INFO ] Shairport-sync will be disabled.'
			pcp_remove_shairport
			sed -i '/pcp-shairportsync.tcz/d' $ONBOOTLST
			sync
			CLOSEOUT=""
		;;
		*)
			echo '[ ERROR ] Shairport selection invalid: '$SHAIRPORT
		;;
	esac
else
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] $SHAIRPORT variable unchanged.'
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
	echo '[ INFO ] Downloading ALSA Equalizer from repository...'
	echo '[ INFO ] Download will take a few minutes. Please wait...'

	sudo -u tc pcp-load -wi alsaequal.tcz
	if [ $? -eq 0 ]; then
		echo '[ OK ] Download successful.'
		return 0
	else
		echo '[ ERROR ] Alsaequal download unsuccessful, try again!'
		return 1
	fi

	SPACE=$(pcp_free_space k)
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] Free space: '$SPACE'k'
}

pcp_remove_alsaequal() {
	echo '[ INFO ] Removing ALSA Equalizer...'
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete alsaequal.tcz
	sudo rm -f /home/tc/.alsaequal.bin
}

pcp_set_equal_asound_output() {
	# $1 contains the hw named device.(hw:CARD=CODEC,DEV=0)
	local CNAME=$(echo $1 | awk -F'hw:CARD=' '{ print $2 }' | cut -d',' -f1)
	local DEVNO=$(echo $1 | awk -F'DEV=' '{ print $2 }')

	echo '[ INFO ] $EQUAL_OUT_DEVICE is set to:'$EQUAL_OUT_DEVICE
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

	echo '[ INFO ] $ALSAeq is set to: '$ALSAeq

	# Determination of the number of the current sound-card
	# This probably isn't necessary, as we will check at boot time, when using alsaequal
	pcp_load_card_conf

	pcp_debug_variables "text" ORIG_ALSAeq ALSAeq CARDNO AUDIO

	case "$ALSAeq" in
		yes)
			echo '[ INFO ] ALSA equalizer: '$ALSAeq
			if grep -Fxq "alsaequal.tcz" $ONBOOTLST; then
				OUTPUT="equal"
				[ $DEBUG -eq 1 ] && echo '[ DEBUG ] ALSA equalizer modules already loaded.'
			else
				pcp_download_alsaequal
				[ $? -eq 0 ] && OUTPUT="equal"
			fi
			if [ "$CARDNO" != "" ]; then
				# If more than one device is present on card, just set the first one.
				EQUAL_OUT_DEVICE=$(aplay -L | grep -E "^hw:" | grep $(cat /proc/asound/card${CARDNO}/id) | head -1) 
				pcp_set_equal_asound_output "$EQUAL_OUT_DEVICE"
			else
				echo '[ ERROR ] Input device not selected. Select and re-save.'
			fi
			RESTART_SQLT=TRUE
		;;
		no)
			REBOOT_REQUIRED=TRUE
			echo '[ INFO ] ALSA equalizer: '$ALSAeq
			OUTPUT=""
			sudo sed -i '/alsaequal.tcz/d' $ONBOOTLST
			sudo sed -i '/caps/d' $ONBOOTLST
			pcp_remove_alsaequal
			OUTPUTCONFIRM=1
		;;
		*)
			echo '[ ERROR ] ALSA equalizer invalid: '$ALSAeq
		;;
	esac
else
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] $ALSAeq variable unchanged.'
fi

if [ "$ALSAeq" = "yes" -a "$ORIG_EQUAL_OUT_DEVICE" != "$EQUAL_OUT_DEVICE" ]; then
	VARIABLE_CHANGED=TRUE
	RESTART_SQLT=TRUE
	pcp_set_equal_asound_output "$EQUAL_OUT_DEVICE"
else
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] $EQUAL_OUT_DEVICE variable unchanged.'
fi

#========================================================================================
# pCP Streamer section
#----------------------------------------------------------------------------------------
# Total size (bytes)       3489792
# Need to download (bytes) 1466368
#----------------------------------------------------------------------------------------
pcp_download_streamer() {
	pcp_sufficient_free_space 1600
	echo '[ INFO ] Downloading pCP Streamer...'
	echo '[ INFO ] Download will take a few minutes. Please wait...'

	sudo -u tc pcp-load -wi pcp-streamer.tcz
	if [ $? -eq 0 ]; then
		echo '[ OK ] Download successful.'
	else
		echo '[ ERROR ] pCP Stremer download unsuccessful, try again!'
	fi

	SPACE=$(pcp_free_space k)
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] Free space: '$SPACE
}

pcp_remove_streamer() {
	echo '[ INFO ] Removing pCP Streamer...'
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete pcp-streamer.tcz
}

pcp_set_streamer_asound_output() {
	# $1 contains the hw named device.(hw:CARD=CODEC,DEV=0)
	local CNAME=$(echo $1 | awk -F'hw:CARD=' '{ print $2 }' | cut -d',' -f1)
	local DEVNO=$(echo $1 | awk -F'DEV=' '{ print $2 }')

	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] Card Full Name:'$1
	echo '[ INFO ] Setting Streamer asound to:'$CNAME

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
			echo '[ INFO ] pCP Streamer: '$STREAMER
			if grep -Fxq "pcp-streamer.tcz" $ONBOOTLST; then
				[ $DEBUG -eq 1 ] && echo '[ DEBUG ] pCP Streamer module is already loaded.'
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
			echo '[ INFO ] pCP Streamer: '$STREAMER
			sudo sed -i '/pcp-streamer.tcz/d' $ONBOOTLST
			STREAMER_IN_DEVICE=""
			pcp_remove_streamer
		;;
		*)
			echo '[ ERROR ] pCP Streamer invalid: '$STREAMER
		;;
	esac
else
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] $STREAMER variable unchanged.'
fi

#========================================================================================
# CMD section
#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_CMD" != "$CMD" ]; then
	VARIABLE_CHANGED=TRUE
	REBOOT_REQUIRED=TRUE

	echo '[ INFO ] $CMD is set to: '$CMD

	pcp_debug_variables "text" ORIG_CMD CMD

	case "$CMD" in
		Default)
			pcp_mount_bootpart
			if mount | grep $VOLUME >/dev/null; then
				# Remove dwc_otg_speed=1
				sed -i 's/dwc_otg.speed=1 //g' $CMDLINETXT
				[ $DEBUG -eq 1 ] && "Current $CMDLINETXT" "cat $CMDLINETXT"
				pcp_umount_bootpart
			else
				echo '[ ERROR ] '$VOLUME' not mounted.'
			fi
		;;
		Slow)
			pcp_mount_bootpart
			if mount | grep $VOLUME >/dev/null; then
				# Remove dwc_otg_speed=1
				sed -i 's/dwc_otg.speed=1 //g' $CMDLINETXT
				# Add dwc_otg_speed=1
				sed -i '1 s/^/dwc_otg.speed=1 /' $CMDLINETXT
				[ $DEBUG -eq 1 ] && "Current $CMDLINETXT" "cat $CMDLINETXT" 
				pcp_umount_bootpart
			else
				echo '[ ERROR ] '$VOLUME' not mounted.'
			fi
		;;
		*)
			echo '[ ERROR ] $CMD invalid: '$CMD
		;;
	esac
else
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] $CMD variable unchanged.'
fi

#========================================================================================
# USB_FIQ FSM section
#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_FSM" != "$FSM" ]; then
	VARIABLE_CHANGED=TRUE
	REBOOT_REQUIRED=TRUE

	echo '[ INFO ] $FSM is set to: '$FSM

	pcp_debug_variables "text" ORIG_FSM FSM

	case "$FSM" in
		Default)
			pcp_mount_bootpart
			if mount | grep $VOLUME >/dev/null; then
				# dwc_otg.fiq_fsm_enable=0
				sed -i 's/dwc_otg.fiq_fsm_enable=0 \+//g' $CMDLINETXT
				[ $DEBUG -eq 1 ] && "Current $CMDLINETXT" "cat $CMDLINETXT"
				pcp_umount_bootpart
			else
				echo '[ ERROR ] '$VOLUME' not mounted'
			fi
		;;
		Disabled)
			pcp_mount_bootpart
			if mount | grep $VOLUME >/dev/null; then
				# Remove dwc_otg.fiq_fsm_enable=0
				sed -i 's/dwc_otg.fiq_fsm_enable=0 \+//g' $CMDLINETXT
				# Add dwc_otg.fiq_fsm_enable=0
				sed -i '1 s/^/dwc_otg.fiq_fsm_enable=0 /' $CMDLINETXT
				[ $DEBUG -eq 1 ] && "Current $CMDLINETXT" "cat $CMDLINETXT"
				pcp_umount_bootpart
			else
				echo '[ ERROR ] '$VOLUME' not mounted'
			fi
		;;
	esac
else
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] $FSM variable unchanged.'
fi

#========================================================================================
# FIQ split section
#----------------------------------------------------------------------------------------
# Only do something if variable has changed.
#----------------------------------------------------------------------------------------
if [ "$ORIG_FIQ" != "$FIQ" ]; then
	VARIABLE_CHANGED=TRUE
	REBOOT_REQUIRED=TRUE

	echo '[ INFO ] $FIQ is set to: '$FIQ

	pcp_debug_variables "text" ORIG_FIG FIQ

	pcp_mount_bootpart
	if mount | grep $VOLUME >/dev/null; then
		# Remove fiq settings
		sed -i 's/dwc_otg.fiq_fsm_mask=0x[1-8F] \+//g' $CMDLINETXT
		# Add FIQ settings from config file
		sed -i '1 s/^/dwc_otg.fiq_fsm_mask='$FIQ' /' $CMDLINETXT
		[ $DEBUG -eq 1 ] && "Current $CMDLINETXT" "cat $CMDLINETXT"
		pcp_umount_bootpart
	else
		echo '[ ERROR ] '$VOLUME' not mounted'
	fi
else
	[ $DEBUG -eq 1 ] && echo '[ DEBUG ] $FIQ variable unchanged.'
fi

echo '                </textarea>'

if [ $OUTPUTCONFIRM ]; then
	STRING1='You have removed ALSA equalizer. Please fill out the OUTPUT field on the Squeezelite page. Press [OK] to go back and change or [Cancel] to continue'
	SCRIPT1=squeezelite.cgi
	pcp_confirmation_required
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

[ $RESTART_SQLT ] && pcp_squeezelite_restart

[ $DEBUG -eq 0 ] && DELAY=15 || DELAY=9999

pcp_table_middle
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" "$DELAY"
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
