#!/bin/sh

# Version: 7.0.0 2020-06-04

. pcp-functions
. pcp-lms-functions

pcp_html_head "Write to Autostart" "GE"

pcp_httpd_query_string

pcp_navbar

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

	pcp_message INFO "Auto start favorite is: $A_S_FAV" "text"
	pcp_message INFO "Auto start favorite is set to: $AUTOSTARTFAV" "text"

	pcp_backup "text"

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

	pcp_message INFO "Auto start LMS command is: $A_S_LMS" "text"
	pcp_message INFO "Auto start LMS command is set to: $AUTOSTARTLMS" "text"

	pcp_backup "text"

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

	pcp_message INFO "User command #1 is set to: $USER_COMMAND_1" "text"
	pcp_message INFO "User command #2 is set to: $USER_COMMAND_2" "text"
	pcp_message INFO "User command #3 is set to: $USER_COMMAND_3" "text"

	pcp_backup "text"
}

#========================================================================================
# Main routine
#----------------------------------------------------------------------------------------
case "$AUTOSTART" in
	FAV)
		pcp_heading5 "Auto Start Favorite"
		pcp_infobox_begin
		pcp_httpd_query_string
		pcp_set_austostart_fav
		pcp_infobox_end
	;;
	LMS)
		pcp_heading5 "Auto Start LMS Command"
		pcp_infobox_begin
		pcp_httpd_query_string_no_decode
		pcp_set_austostart_lms
		pcp_infobox_end
	;;
	CMD)
		pcp_heading5 "User Commands"
		pcp_infobox_begin
		pcp_httpd_query_string_no_decode
		pcp_set_user_commands
		pcp_infobox_end
	;;
	*)
		pcp_infobox_begin
		pcp_message ERROR "Invalid AUTOSTART option: $AUTOSTART" "text"
		pcp_infobox_end
	;;
esac
#----------------------------------------------------------------------------------------

pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 5

pcp_html_end
exit
