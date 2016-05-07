#!/bin/sh

# Version: 0.01 2016-05-07 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG
TCELOAD="tce-load"
REBOOT_REQUIRED=0

pcp_html_head "Write to HDMI Power" "GE" "5" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#========================================================================================
# Check for rpi-vc.tcz, download and install.
#----------------------------------------------------------------------------------------
pcp_install_rpi_vc() {
	which tvservice >/dev/null
	if [ $? -eq 0 ]; then
		echo '[  OK  ] rpi-vc.tcz already installed.'
	else
		if [ ! -f /mnt/mmcblk0p2/tce/optional/rpi-vc.tcz ]; then
			echo -n '[ INFO ] rpi-vc.tcz downloading... '
			sudo -u tc $TCELOAD -w rpi-vc.tcz 2>&1 >/dev/null
			[ $? -eq 0 ] && echo 'Done.' || echo 'Error.'
		else
			echo '[  OK  ] rpi-vc.tcz downloaded.'
		fi
		echo -n '[ INFO ] rpi-vc.tcz installing... '
		sudo -u tc $TCELOAD -i rpi-vc.tcz 2>&1 >/dev/null
		[ $? -eq 0 ] && echo 'Done.' || echo 'Error.'
	fi
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
echo '<textarea rows="11">'
echo '[ INFO ] Powering '$HDMIPOWER' HMDI...'
echo '[ INFO ] Checking for tvservice software...'

pcp_install_rpi_vc
pcp_save_to_config

echo -n '[ INFO ] '

case "$HDMIPOWER" in
	on)
		tvservice -p
		if [ $? -eq 0 ]; then
			echo '[  OK  ] Done.'
			sed -i '/rpi-vc.tcz/d' $ONBOOTLST
			REBOOT_REQUIRED=1
		else
			echo '[ ERROR ] Error.'
		fi
		;;
	off)
		tvservice -o
		if [ $? -eq 0 ]; then
			echo '[  OK  ] Done.'
			echo "rpi-vc.tcz" >> $ONBOOTLST
			REBOOT_REQUIRED=1
		else
			echo '[ ERROR ] Error.'
		fi
		;;
	*)
		echo '[ ERROR ] Invalid case argument.'
		;;
esac

pcp_backup_nohtml

echo '</textarea>'

pcp_footer
pcp_copyright

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

echo '</body>'
echo '</html>'