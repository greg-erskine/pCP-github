#!/bin/sh

# Version: 4.1.0 2018-10-07

. pcp-functions
. pcp-lms-functions

pcp_html_head "Write to Autostart" "GE"

pcp_banner
pcp_running_script
pcp_httpd_query_string

pcp_debug_variables "html" SUBMIT AUTOSTART A_S_LMS AUTOSTARTLMS A_S_FAV AUTOSTARTFAV USER_COMMAND_1 USER_COMMAND_2 USER_COMMAND_3

#========================================================================================
# Auto start Favorite.
#----------------------------------------------------------------------------------------
pcp_set_austostart_fav() {
	if [ "$SUBMIT" = "Clear" ]; then
		AUTOSTARTFAV=""
		A_S_FAV="Disabled"
	fi

	if [ "$A_S_FAV" = "Enabled" ]; then
		A_S_LMS="Disabled"
	fi

	pcp_save_to_config

	echo '<p class="info">[ INFO ] Auto start favorite is: '$A_S_FAV'</p>'
	echo '<p class="info">[ INFO ] Auto start favorite is set to: '$AUTOSTARTFAV'</p>'

	pcp_backup

	if [ "$SUBMIT" = "Test" ]; then
		pcp_lms_auto_start_fav
	fi
}

#========================================================================================
# Auto start LMS command.
#----------------------------------------------------------------------------------------
pcp_set_austostart_lms() {
	if [ "$SUBMIT" = "Clear" ]; then
		AUTOSTARTLMS=""
		A_S_LMS="Disabled"
	fi

	if [ "$A_S_LMS" = "Enabled" ]; then
		A_S_FAV="Disabled"
	fi

	pcp_save_to_config

	echo '<p class="info">[ INFO ] Auto start LMS command is: '$A_S_LMS'</p>'
	echo '<p class="info">[ INFO ] Auto start LMS command is set to: '$AUTOSTARTLMS'</p>'

	pcp_backup

	if [ "$SUBMIT" = "Test" ]; then
		pcp_lms_auto_start_lms
	fi
}

#========================================================================================
# Save user commands.
#----------------------------------------------------------------------------------------
pcp_set_user_commands() {
	if [ "$SUBMIT" = "Clear" ]; then
		USER_COMMAND_1=""
		USER_COMMAND_2=""
		USER_COMMAND_3=""
	fi

	pcp_save_to_config

	echo '<p class="info">[ INFO ] User command #1 is set to: '$USER_COMMAND_1'</p>'
	echo '<p class="info">[ INFO ] User command #2 is set to: '$USER_COMMAND_2'</p>'
	echo '<p class="info">[ INFO ] User command #3 is set to: '$USER_COMMAND_3'</p>'

	pcp_backup
}

#========================================================================================
# Main routine
#----------------------------------------------------------------------------------------
case "$AUTOSTART" in
	FAV)
		pcp_table_top "Auto Start Favorite"
		pcp_httpd_query_string
		pcp_set_austostart_fav
	;;
	LMS)
		pcp_table_top "Auto Start LMS Command"
		pcp_httpd_query_string_no_decode
		pcp_set_austostart_lms
	;;
	CMD)
		pcp_table_top "User Commands"
		pcp_httpd_query_string_no_decode
		pcp_set_user_commands
	;;
	*)
		echo '<p class="error">[ ERROR ] Invalid AUTOSTART option: '$AUTOSTART'</p>'
	;;
esac
#----------------------------------------------------------------------------------------

pcp_table_middle
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 5
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'