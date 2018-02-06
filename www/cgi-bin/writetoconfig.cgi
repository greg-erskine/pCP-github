#!/bin/sh

# Version: 3.5.0 2018-02-04
#	Added setting of which squeezelite binary to use. PH.
#	Make sure DSDOUT is not set for regular binary. PH.
#	Utilize updated pcp_restart_required. PH.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Enhanced format. GE.
#	Removed pcp_multi_alsa_mmap. GE.

# Version: 3.02 2016-09-21
#	Fixed blanking ALSA_PARAMS issue. GE.

# Version: 2.06 2016-06-07
#	Added multi ALSA_PARAMS and FROM_PAGE. GE.
#	Added MMAP configuration. GE.
#	Added $ORG_ALSA_PARAMS4. SBP.
#	Added $CLOSEOUT $PRIORITY $POWER_GPIO check for 0. SBP.

# Version: 0.08 2016-04-25 GE
#	Added pcp_update.

# Version: 0.07 2016-03-30 SBP
#	Added warning pop-up box for setting a different output value when using ALSAeq.

# Version: 0.06 2016-01-15 SBP
#	Changed order of back button and reboot prompt.

# Version: 0.05 2015-09-21 SBP
#	Removed httpd decoding.
#	Added pcp_restart_required.

# Version: 0.04 2015-01-23 SBP
#	Added CLOSEOUT.
#	Removed debugging code.
#	Removed adding quotes when decoding variables.
#	Added pcp_reset, pcp_restore.

# Version: 0.03 2014-12-12 GE
#	HTML5 format.
#	Minor mods.

# Version: 0.02 2014-08-22 SBP
#	Changed the back button to absolute path back to Squeezelite.cgi. Otherwise we would go in circles.

# Version: 0.01 2014-06-25 GE
#	Original.

. pcp-functions
. pcp-soundcard-functions  # reset needs soundcard functions too.
#. $CONFIGCFG

# Restore sparams variable value from config.cfg so it is not overwritten with default values
PARAM1="$SPARAMS1"
PARAM2="$SPARAMS2"
PARAM3="$SPARAMS3"
PARAM4="$SPARAMS4"
PARAM5="$SPARAMS5"


# Read original mmap value, so we only do something if value is changed
ORG_ALSA_PARAMS4=$(echo $ALSA_PARAMS | cut -d':' -f4 )

RESTART_REQUIRED=TRUE
unset REBOOT_REQUIRED

pcp_html_head "Write to config.cfg" "SBP" "15" "squeezelite.cgi"

pcp_banner
pcp_running_script
pcp_remove_query_string
pcp_httpd_query_string

#========================================================================================
# Reset configuration
#----------------------------------------------------------------------------------------
pcp_reset() {
	pcp_reset_config_to_defaults
}

#========================================================================================
# Restore configuration
#
# Note: Assumes a backup onto USB stick exists.
#----------------------------------------------------------------------------------------
pcp_restore() {
	pcp_mount_device sda1
	. /mnt/sda1/newconfig.cfg
	pcp_umount_device sda1
	pcp_save_to_config
}

#========================================================================================
# Update config.cfg to the latest version
#
# This will first create the latest version of config.cfg with default values, then,
# restore original values.
#----------------------------------------------------------------------------------------
pcp_update() {
	echo '<p class="info">[ INFO ] Copying config.cfg to /tmp...</p>'
	sudo cp $CONFIGCFG /tmp/config.cfg
	[ $? -ne 0 ] && echo '<p class="error">[ ERROR ] Error copying config.cfg to /tmp...</p>'
	echo '<p class="info">[ INFO ] Setting config.cfg to defaults...</p>'
	pcp_update_config_to_defaults
	echo '<p class="info">[ INFO ] Updating config.cfg with original values...</p>'
	. $CONFIGCFG
	. /tmp/config.cfg
	pcp_save_to_config
}

#pcp_multi_alsa_mmap() {
#	pcp_mount_bootpart
#	if [ $ALSA_PARAMS4 -eq 1 ]; then
#		echo '<p class="info">[ INFO ] Adding i2s-mmap to config.txt...</p>'
#		grep dtoverlay=i2s-mmap $CONFIGTXT >/dev/null 2>&1
#		[ $? -eq 1 ] && REBOOT_REQUIRED=TRUE && unset RESTART_REQUIRED
#		sed -i '/dtoverlay=i2s-mmap/d' $CONFIGTXT
#		echo "dtoverlay=i2s-mmap" >> $CONFIGTXT
#	else
#		echo '<p class="info">[ INFO ] Deleting i2s-mmap from config.txt...</p>'
#		sed -i '/dtoverlay=i2s-mmap/d' $CONFIGTXT
#		pcp_umount_bootpart
#	fi
#}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_table_top "Write to config"

case "$SUBMIT" in
	Save)
		if [ $MODE -ge $MODE_BASIC ]; then
			ALSA_PARAMS=${ALSA_PARAMS1}:${ALSA_PARAMS2}:${ALSA_PARAMS3}:${ALSA_PARAMS4}:${ALSA_PARAMS5}
#			[ "$FROM_PAGE" = "squeezelite" ] && [ "$ORG_ALSA_PARAMS4" != "$ALSA_PARAMS4" ] && pcp_multi_alsa_mmap
			[ $CLOSEOUT -eq 0 ] && CLOSEOUT=""
			[ $PRIORITY -eq 0 ] && PRIORITY=""
			[ $POWER_GPIO -eq 0 ] && POWER_GPIO=""
		fi
		echo '<p class="info">[ INFO ] Saving config file.</p>'
		pcp_save_to_config
	;;
	Binary)
		SAVE=0
		case $SQBINARY in
			default)
				rm -f $TCEMNT/tce/squeezelite
				DSDOUT=""
				SAVE=1
			;;
			dsd)
				rm -f $TCEMNT/tce/squeezelite
				ln -s /usr/local/bin/squeezelite-dsd $TCEMNT/tce/squeezelite
				SAVE=1
			;;
			custom) 
				if [ -f $TCEMNT/tce/squeezelite-custom ]; then
					rm -f $TCEMNT/tce/squeezelite; ln -s $TCEMNT/tce/squeezelite-custom $TCEMNT/tce/squeezelite
					SAVE=1
				else
					echo '<p class="error">[ ERROR ] Custom Squeezelite not found. Copy custom binary before setting this option.</p>'
				fi
			;;
		esac
		if [ $SAVE -eq 1 ]; then
			echo '<p class="info">[ INFO ] Saving config file.</p>'
			pcp_save_to_config
		fi
	;;
	Reset*)
		pcp_reset
	;;
	Restore*)
		pcp_restore
	;;
	Update*)
		pcp_update
	;;
	*)
		echo '<p class="error">[ ERROR ] Invalid case argument.</p>'
	;;
esac

. $CONFIGCFG

if [ "$ALSAeq" = "yes" ] && [ "$OUTPUT" != "equal" ]; then
	STRING1='ALSA equalizer is enabled. In order to use it "equal" must be used in the OUTPUT box. Press OK to go back and change or Cancel to continue'
	SCRIPT1=squeezelite.cgi
	pcp_confirmation_required
fi

pcp_backup
pcp_table_middle
[ $RESTART_REQUIRED ] || pcp_go_back_button
pcp_table_end
pcp_footer
pcp_copyright

sleep 1
[ $REBOOT_REQUIRED ] && pcp_reboot_required
[ $RESTART_REQUIRED ] && pcp_restart_required $FROM_PAGE

echo '</body>'
echo '</html>'