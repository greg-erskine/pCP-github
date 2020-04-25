#!/bin/sh

# Version: 6.0.0 2019-08-11

. pcp-functions

TCELOAD="tce-load"
REBOOT_REQUIRED=false

pcp_html_head "Write to HDMI Power" "GE"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#========================================================================================
# Check for rpi-vc.tcz, download and install.
#----------------------------------------------------------------------------------------
pcp_install_rpi_vc() {
	tce-status -i | grep rpi-vc >/dev/null 2>&1
	if [ $? -eq 0 ]; then
		echo '[  OK  ] rpi-vc.tcz already installed.'
	else
		if [ ! -f ${PACKAGEDIR}/rpi-vc.tcz ]; then
			echo -n '[ INFO ] rpi-vc.tcz downloading... '
			sudo -u tc $TCELOAD -w rpi-vc.tcz >/dev/null 2>&1
			[ $? -eq 0 ] && echo 'Done.' || echo 'Error.'
		else
			echo '[  OK  ] rpi-vc.tcz downloaded.'
		fi
		echo -n '[ INFO ] rpi-vc.tcz installing... '
		sudo -u tc $TCELOAD -i rpi-vc.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo 'Done.' || echo 'Error.'
	fi
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_table_top "Powering HDMI on/off"
echo '                <textarea class="inform" style="height:130px">'
[ $DEBUG -eq 1 ] && pcp_debug_variables "text" HDMIPOWER
echo '[ INFO ] Powering '$HDMIPOWER' HMDI...'
echo '[ INFO ] Checking for tvservice software...'

pcp_install_rpi_vc
pcp_save_to_config

echo -n '[ INFO ] '

case "$HDMIPOWER" in
	on)
		sudo tvservice --preferred
		if [ $? -eq 0 ]; then
			sed -i '/rpi-vc.tcz/d' $ONBOOTLST
			REBOOT_REQUIRED=true
		else
			echo '[ ERROR ] Error with "tvservice --preferred" command.'
		fi
	;;
	off)
		sudo tvservice --off
		if [ $? -eq 0 ]; then
			sed -i '/rpi-vc.tcz/d' $ONBOOTLST
			echo 'rpi-vc.tcz' >> $ONBOOTLST
			REBOOT_REQUIRED=true
		else
			echo '[ ERROR ] Error with "tvservice --off" command.'
		fi
	;;
	*)
		echo '[ ERROR ] Invalid value.'
	;;
esac

pcp_backup text
echo '                </textarea>'
pcp_table_middle
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 100
pcp_table_end
pcp_footer
pcp_copyright

$REBOOT_REQUIRED
[ $? -eq 0 ] && pcp_reboot_required

echo '</body>'
echo '</html>'
