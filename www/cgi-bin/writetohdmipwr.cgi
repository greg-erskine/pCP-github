#!/bin/sh

# Version: 7.0.0 2020-05-12

. pcp-functions

TCELOAD="tce-load"
REBOOT_REQUIRED=false

pcp_html_head "Write to HDMI Power" "GE"

pcp_navbar
pcp_httpd_query_string

#========================================================================================
# Check for rpi-vc.tcz, download and install.
#----------------------------------------------------------------------------------------
pcp_install_rpi_vc() {
	tce-status -i | grep rpi-vc >/dev/null 2>&1
	if [ $? -eq 0 ]; then
		pcp_message OK "rpi-vc.tcz already installed." "html"
	else
		if [ ! -f ${PACKAGEDIR}/rpi-vc.tcz ]; then
			ppc_message INFO "rpi-vc.tcz downloading... " "html" "-n"
			sudo -u tc $TCELOAD -w rpi-vc.tcz >/dev/null 2>&1
			[ $? -eq 0 ] && echo 'Done.</div>' || echo 'Error.</div>'
		else
			pcp_message OK "rpi-vc.tcz downloaded." "html"
		fi
		pcp_message INFO "rpi-vc.tcz installing... " "html" "-n"
		sudo -u tc $TCELOAD -i rpi-vc.tcz >/dev/null 2>&1
		[ $? -eq 0 ] && echo 'Done.</div>' || echo 'Error.</div>'
	fi
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_heading5 "Powering HDMI on/off"
pcp_infobox_begin

pcp_message INFO "Powering $HDMIPOWER HMDI..." "html"
pcp_message INFO "Checking for tvservice software..." "html"

pcp_install_rpi_vc
pcp_save_to_config

pcp_message INFO "" "html" "-n"

case "$HDMIPOWER" in
	on)
		sudo tvservice --preferred
		if [ $? -eq 0 ]; then
			sed -i '/rpi-vc.tcz/d' $ONBOOTLST
			REBOOT_REQUIRED=true
		else
			pcp_message ERROR "Error with \"tvservice --preferred\" command." "html"
		fi
	;;
	off)
		sudo tvservice --off
		if [ $? -eq 0 ]; then
			sed -i '/rpi-vc.tcz/d' $ONBOOTLST
			echo 'rpi-vc.tcz' >> $ONBOOTLST
			REBOOT_REQUIRED=true
		else
			pcp_message ERROR "Error with \"tvservice --off\" command." "html"
		fi
	;;
	*)
		pcp_message ERROR "Invalid value." "html"
	;;
esac

pcp_backup
pcp_infobox_end

pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 100

$REBOOT_REQUIRED
[ $? -eq 0 ] && pcp_reboot_required

pcp_html_end
