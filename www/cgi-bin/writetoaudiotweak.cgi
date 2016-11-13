#!/bin/sh

# Version 3.03 2016-11-13
#	Changes for pcp-shairportsync.tcz. PH

# Version: 3.02 2016-09-05
#	Updated FIQ-split. SBP.

# Version: 0.13 2016-03-30 SBP
#	Added warning pop-up box for setting output value when removing ALSAeq.

# Version: 0.12 2016-03-25 SBP
#	Added 0xf FIQ-Split acceleration.

# Version: 0.11 2016-03-19 SBP
#	Added dwc_otg.fiq_fsm_enable.

# Version: 0.10 2016-02-26 SBP
#	Added SQUEEZELITE section.

# Version: 0.09 2016-02-20 GE
#	Fixed sourceforge redirection issue.

# Version: 0.08 2016-02-09 SBP
#	Updated CARDNO.

# Version: 0.07 2016-01-29 SBP
#	Activated ALSA Equalizer.

# Version: 0.06 2016-01-07 SBP
#	Added ALSA Equalizer.
#	Added Shairport-sync.

# Version: 0.05 2015-09-19 SBP
#	Removed httpd decoding.

# Version: 0.04 2015-06-06 GE
#	Remove multiple spaces from CONFIGCFG.
#	Removed duplicate ALSA output level section.

# Version: 0.03 2015-01-28 GE
#	Included changefiq.sh.

# Version: 0.02 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014-08-06 SBP
#	Original version.

. pcp-functions
pcp_variables

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
EQREPOSITORY="https://sourceforge.net/projects/picoreplayer/files/tce/7.x/ALSAequal"
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
	cd /tmp
	sudo rm -f /tmp/alsaequal.tcz
	sudo rm -f /tmp/caps*
	echo '<p class="info">[ INFO ] Downloading ALSA Equalizer from repository...</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] repo: '${EQREPOSITORY}'</p>'
	echo '<p class="info">[ INFO ] Download will take a few minutes. Please wait...</p>'

	$WGET -s ${EQREPOSITORY}/alsaequal.tcz
	if [ $? -eq 0 ]; then
		RESULT=0
		echo '<p class="info">[ INFO ] Downloading ALSA Equalizer and packages...'
		$WGET ${EQREPOSITORY}/alsaequal.tcz/download -O /tmp/alsaequal.tcz
		[ $? -eq 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET ${EQREPOSITORY}/${CAPS}.tcz/download -O /tmp/${CAPS}.tcz
		[ $? -eq 0 ] && echo -n . || (echo $?; RESULT=1)
		if [ $RESULT -eq 0 ]; then
			echo '<p class="ok">[ OK ] Download successful.</p>'
			sudo cp /tmp/alsaequal.tcz /mnt/mmcblk0p2/tce/optional/alsaequal.tcz
			sudo chown tc:staff /mnt/mmcblk0p2/tce/optional/alsaequal.tcz
			sudo chmod 644 /mnt/mmcblk0p2/tce/optional/alsaequal.tcz
			sudo cp /tmp/${CAPS}.tcz /mnt/mmcblk0p2/tce/optional/${CAPS}.tcz
			sudo chown tc:staff /mnt/mmcblk0p2/tce/optional/${CAPS}.tcz
			sudo chmod 644 /mnt/mmcblk0p2/tce/optional/${CAPS}.tcz
			sudo rm -f /tmp/alsaequal.tcz
			sudo rm -f /tmp/caps*
		else
			echo '<p class="error">[ ERROR ] Alsaequalizer download unsuccessful, try again!</p>'
		fi
	else
		echo '<p class="error">[ ERROR ] Alsaequalizer not available in repository, try again later!</p>'
	fi

	SPACE=$(pcp_free_space k)
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Free space: '$SPACE'k</p>'
}

pcp_remove_alsaequal() {
	echo '<p class="info">[ INFO ] Removing ALSA Equalizer...</p>'
	sudo rm -f /mnt/mmcblk0p2/tce/optional/alsaequal.tcz
	sudo rm -f /mnt/mmcblk0p2/tce/optional/${CAPS}.tcz
	sudo rm -f /home/tc/.alsaequal.bin
}

#----------------------------------------------------------------------------------------
# Only do something if variable is changed
if [ "$ORIG_ALSAeq" != "$ALSAeq" ]; then
	REBOOT_REQUIRED=1
	echo '<hr>'
	echo '<p class="info">[ INFO ] ALSAeq is set to: '$ALSAeq'</p>'

	# Determination of the number of the current sound-card

	# If output is analog or HDMI then find the number of the used ALSA-card
	if [ "$AUDIO" = "Analog" ] || [ "$AUDIO" = "HDMI" ]; then
		CARDNO=$(sudo cat /proc/asound/cards | grep '\[' | grep 'ALSA' | awk '{print $1}')
	fi
	
	#-- Code below need improving as I2S DACs and USB-DAC at the same time possibly gets wrong card number-----	
	if [ "$AUDIO" != "Analog" ] && [ "$AUDIO" != "HDMI" ]; then
		CARDNO=1
	fi

	# If output is different from analog or HDMI then find the number of the non-ALSA card
	#	aplay -l | grep 'card 0: ALSA'  >/dev/null 2>&1
	#-- Code below is not fully working as I2S DACs needs a reboot to show up ---------------------------------	
	#	if [ $? = 0 ]; then
	#		if [ $AUDIO != Analog ] && [ $AUDIO != HDMI ]; then
	#			CARDNO=$(sudo cat /proc/asound/cards | sed '/ALSA/d' | grep '\[' | awk '{print $1}')
	#		fi
	#	else
	#		if [ $AUDIO != Analog ] && [ $AUDIO != HDMI ]; then
	#			CARDNO=$(sudo cat /proc/asound/cards | grep '\[' | awk '{print $1}')
	#		fi
	#	fi
	# ---------------------------------------------------------------------------------------------------------

	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_ALSAeq is: '$ORIG_ALSAeq'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ALSAeq is: '$ALSAeq'</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Card has number: '$CARDNO'.</p>'
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] AUDIO is: '$AUDIO'</p>'

	case "$ALSAeq" in
		yes)
			echo '<p class="info">[ INFO ] ALSA equalizer: '$ALSAeq'</p>'
			if grep -Fxq "alsaequal.tcz" /mnt/mmcblk0p2/tce/onboot.lst; then
				[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] ALSA equalizer modules already loaded.</p>'
			else
				sudo sed -i '/alsaequal.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
				sudo echo "alsaequal.tcz" >> /mnt/mmcblk0p2/tce/onboot.lst
				sudo sed -i '/caps/d' /mnt/mmcblk0p2/tce/onboot.lst
				sudo echo "caps-0.4.5.tcz" >> /mnt/mmcblk0p2/tce/onboot.lst
				pcp_download_alsaequal
				OUTPUT="equal"
			fi
			sed -i "s/plughw:.*,0/plughw:"$CARDNO",0/g" /etc/asound.conf
		;;
		no)
			echo '<p class="info">[ INFO ] ALSA equalizer: '$ALSAeq'</p>'
			OUTPUT=""
			sudo sed -i '/alsaequal.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
			sudo sed -i '/caps/d' /mnt/mmcblk0p2/tce/onboot.lst
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

			pcp_mount_mmcblk0p1

			if mount | grep $VOLUME; then
				# Remove dwc_otg_speed=1
				sed -i 's/dwc_otg.speed=1 //g' /mnt/mmcblk0p1/cmdline.txt
				pcp_umount_mmcblk0p1
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
			fi
		;;
		Slow)
			echo '<p class="info">[ INFO ] CMD: '$CMD'</p>'
			#sudo ./enableotg.sh

			pcp_mount_mmcblk0p1

			if mount | grep $VOLUME; then
				# Remove dwc_otg_speed=1
				sed -i 's/dwc_otg.speed=1 //g' /mnt/mmcblk0p1/cmdline.txt

				# Add dwc_otg_speed=1
				sed -i '1 s/^/dwc_otg.speed=1 /' /mnt/mmcblk0p1/cmdline.txt
				pcp_umount_mmcblk0p1
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

			pcp_mount_mmcblk0p1

			if mount | grep $VOLUME; then
				# dwc_otg.fiq_fsm_enable=0
				sed -i 's/dwc_otg.fiq_fsm_enable=0 \+//g' /mnt/mmcblk0p1/cmdline.txt
				[ $DEBUG -eq 1 ] && pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT" 150
				pcp_umount_mmcblk0p1
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
			fi
		;;
		Disabled)
			echo '<p class="info">[ INFO ] FSM: '$FSM'</p>'

			pcp_mount_mmcblk0p1

			if mount | grep $VOLUME; then
				# Remove dwc_otg.fiq_fsm_enable=0
				sed -i 's/dwc_otg.fiq_fsm_enable=0 \+//g' /mnt/mmcblk0p1/cmdline.txt

				# Add dwc_otg.fiq_fsm_enable=0
				sed -i '1 s/^/dwc_otg.fiq_fsm_enable=0 /' /mnt/mmcblk0p1/cmdline.txt
				[ $DEBUG -eq 1 ] && pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT" 150
				pcp_umount_mmcblk0p1
			else
				echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
			fi
		;;
	esac
else
	echo '<p class="info">[ INFO ] USB FSM FIQ variable unchanged.</p>'
fi
#----------------------------------------------------------------------------------------

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
			if [ -f /mnt/mmcblk0p2/tce/optional/pcp-shairportsync.tcz ]; then
				[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Shairport-sync already loaded.</p>'
				echo "pcp-shairportsync.tcz" >> /mnt/mmcblk0p2/tce/onboot.lst
			else
				pcp_download_shairport
				if [ $? -eq 0 ]; then
					echo "pcp-shairportsync.tcz" >> /mnt/mmcblk0p2/tce/onboot.lst
					/usr/local/etc/init.d/shairport-sync start
				fi
			fi
#			I think this should be in the audiocard setup, not here
#			[ "$OUTPUT" = "hw:CARD=sndrpihifiberry" ] && pcp_disable_analog
			CLOSEOUT="15"
		;;
		no)
			REBOOT_REQUIRED=1
			echo '<p class="info">[ INFO ] Shairport-sync will be disabled.</p>'
			pcp_remove_shairport
			sed -i '/pcp-shairportsync.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
			sync
#			I think this should be in the audiocard setup, not here
#			[ "$OUTPUT" = "hw:CARD=sndrpihifiberry" ] && pcp_re_enable_analog
			CLOSEOUT="2"
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

	pcp_mount_mmcblk0p1

	if mount | grep $VOLUME; then
		# Remove fiq settings
		sed -i 's/dwc_otg.fiq_fsm_mask=0x[1-8F] \+//g' /mnt/mmcblk0p1/cmdline.txt
		# Add FIQ settings from config file
		sed -i '1 s/^/dwc_otg.fiq_fsm_mask='$FIQ' /' /mnt/mmcblk0p1/cmdline.txt

		[ $DEBUG -eq 1 ] && pcp_textarea "Current $CMDLINETXT" "cat $CMDLINETXT" 150
		pcp_umount_mmcblk0p1
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