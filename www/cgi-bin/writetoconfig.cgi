#!/bin/sh

# Version 2.06: 0.09 2016-05-17 GE
#	Added multi ALSA_PARAMS and FROM_PAGE.
#	Added MMAP configuration.

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
pcp_variables
. $CONFIGCFG

RESTART=1
REBOOT=0

pcp_html_head "Write to config.cfg" "SBP" "15" "squeezelite.cgi"

pcp_banner
pcp_running_script
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

pcp_multi_alsa_mmap() {
	ALSA_PARAMS=${ALSA_PARAMS1}:${ALSA_PARAMS2}:${ALSA_PARAMS3}:${ALSA_PARAMS4}:${ALSA_PARAMS5}
	pcp_mount_mmcblk0p1
	if [ $ALSA_PARAMS4 -eq 1 ]; then
		echo '<p class="info">[ INFO ] Adding i2s-mmap to config.txt...</p>'
		grep dtoverlay=i2s-mmap $CONFIGTXT >/dev/null 2>&1
		[ $? -eq 1 ] && REBOOT=1 && RESTART=0
		sed -i '/dtoverlay=i2s-mmap/d' $CONFIGTXT
		echo "dtoverlay=i2s-mmap" >> $CONFIGTXT
	else
		echo '<p class="info">[ INFO ] Deleting i2s-mmap from config.txt...</p>'
		sed -i '/dtoverlay=i2s-mmap/d' $CONFIGTXT
	fi
	pcp_umount_mmcblk0p1
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
case "$SUBMIT" in
	Save)
		[ "$FROM_PAGE" = "squeezelite" ] && pcp_multi_alsa_mmap
		[ "$CLOSEOUT" = "0" ] && CLOSEOUT=""
		[ "$PRIORITY" = "0" ] && PRIORITY=""
		[ "$POWER_GPIO" = 0 ] && POWER_GPIO=""
		pcp_save_to_config
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

pcp_show_config_cfg
pcp_backup
sleep 1
[ $REBOOT -eq 1 ] && pcp_reboot_required
[ $RESTART -eq 1 ] && pcp_restart_required
pcp_go_back_button

echo '</body>'
echo '</html>'