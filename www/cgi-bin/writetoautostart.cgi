#!/bin/sh

# Version: 0.01 2015-01-15 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to Autostart" "GE" "5" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

DEBUG=1

pcp_set_austostart_lms() {
	if [ "$SUBMIT" == "Clear" ]; then
		AUTOSTARTLMS=""
	fi

	# Save the encoded parameter to the config file, with quotes
	sudo sed -i "s/\(AUTOSTARTLMS=\).*/\1\"$AUTOSTARTLMS\"/" $CONFIGCFG
	echo '<p class="info">[ INFO ] Autostart LMS is set to: '$AUTOSTARTLMS'</p>'

	pcp_backup

	if [ "$SUBMIT" == "Test" ]; then
		echo '<p class="info">[ INFO ] Submit: '$SUBMIT'</p>'
		pcp_auto_start_lms
	fi
}

pcp_set_austostart_fav() {
	if [ "$SUBMIT" == "Clear" ]; then
		AUTOSTARTFAV=""
	fi

	# Save the encoded parameter to the config file, with quotes
	sudo sed -i "s/\(AUTOSTARTFAV=\).*/\1\"$AUTOSTARTFAV\"/" $CONFIGCFG
	echo '<p class="info">[ INFO ] Autostart favorite is set to: '$AUTOSTARTFAV'</p>'

	pcp_backup

	if [ "$SUBMIT" == "Test" ]; then
		echo '<p class="info">[ INFO ] Submit: '$SUBMIT'</p>'
		pcp_auto_start_fav
	fi
}

case "$AUTOSTART" in
	LMS)
		pcp_set_austostart_lms
		;;
	FAV)
		pcp_set_austostart_fav
		;;
esac

[ $DEBUG = 1 ] && pcp_show_config_cfg
pcp_go_back_button

echo '</body>'
echo '</html>'