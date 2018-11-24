#!/bin/sh

# Version: 4.1.0 2018-09-19

. pcp-functions

TCELOAD="tce-load"
unset REBOOT_REQUIRED

pcp_html_head "Write to HDMI Power" "GE"

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
			REBOOT_REQUIRED=TRUE
		else
			echo '[ ERROR ] Error with "tvservice -p" command.'
		fi
	;;
	off)
		tvservice -o
		if [ $? -eq 0 ]; then
			echo '[  OK  ] Done.'
			echo 'rpi-vc.tcz' >> $ONBOOTLST
			REBOOT_REQUIRED=TRUE
		else
			echo '[ ERROR ] Error with "tvservice -o" command.'
		fi
	;;
	*)
		echo '[ ERROR ] Invalid value.'
	;;
esac

pcp_backup_nohtml
echo '                </textarea>'
pcp_table_middle
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 10
pcp_table_end
pcp_footer
pcp_copyright

[ $REBOOT_REQUIRED ] && pcp_reboot_required

echo '</body>'
echo '</html>'