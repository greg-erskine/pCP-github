#!/bin/sh

# Version: 4.0.0 2018-04-17
#	Major changes. GE.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 0.01 2014-09-09
#	Original. SBP.

set -f
. pcp-functions

unset REBOOT_REQUIRED

pcp_html_head "Write to crontab" "SBP"
pcp_banner
pcp_running_script
pcp_httpd_query_string

#DEBUG=1
#----------------------------------------------------------------------------------------
# Routines.
#----------------------------------------------------------------------------------------
pcp_cron_initialise() {
	/etc/init.d/services/crond status >/dev/null 2>&1
	if [ $? -eq 0 ]; then
		echo '<p class="info">[ INFO ] crond running.</p>'
	else
		echo '<p class="WARN">[ WARN ] crond not running.</p>'
		if [ "$REBOOT" = "Enabled" ] || [ "$RESTART" = "Enabled" ] || [ x"" != x"$CRON_COMMAND" ]; then
			echo '<p class="INFO">[ INFO ] Starting crond...</p>'
			sudo /etc/init.d/services/crond start
		fi
	fi
}

pcp_cron_config() {
	REBOOT_REQUIRED=TRUE
	MESSAGE='<p class="info">[ INFO ] cron added to '$CMDLINETXT'.</p>'
	pcp_mount_bootpart >/dev/null 2>&1
	sed -i 's/cron[ ]*//g' $CMDLINETXT
	[ "$1" = "add" ] && ( sed -i '1 s/^/cron /' $CMDLINETXT; echo $MESSAGE )
	pcp_umount_bootpart >/dev/null 2>&1
}

# cat /proc/cmdline

pcp_cron_reset() {
	REBOOT="Disabled"
	RB_H="2"
	RB_WD="*"
	RB_DMONTH="*"
	RESTART="Disabled"
	RS_H="2"
	RS_WD="*"
	RS_DMONTH="*"
	CRON_COMMAND=""

	( crontab -l | grep -v "reboot" ) | crontab -
	( crontab -l | grep -v "restart" ) | crontab -
	( crontab -l | grep -v "Custom" ) | crontab -
}

pcp_cron_debug() {
	if [ $DEBUG -eq 1 ]; then
		echo '<p class="debug">[ DEBUG ] $REBOOT: '$REBOOT'<br />'
		echo '                 [ DEBUG ] $RESTART: '$RESTART'<br  />'
		echo '                 [ DEBUG ] $RESTART_Y: '$RESTART_Y'<br />'
		echo '                 [ DEBUG ] $RESTART_N: '$RESTART_N'<br />'
		echo '                 [ DEBUG ] $RB_H: '$RB_H'<br />'
		echo '                 [ DEBUG ] $RB_WD: '$RB_WD'<br />'
		echo '                 [ DEBUG ] $RB_DMONTH: '$RB_DMONTH'<br />'
		echo '                 [ DEBUG ] $RS_H: '$RS_H'<br />'
		echo '                 [ DEBUG ] $RS_WD: '$RS_WD'<br />'
		echo '                 [ DEBUG ] $RS_DMONTH: '$RS_DMONTH'<br />'
		echo '                 [ DEBUG ] $RB_CRON: '$RB_CRON'<br />'
		echo '                 [ DEBUG ] $RS_CRON: '$RS_CRON'<br />'
		echo '                 [ DEBUG ] $CRON_COMMAND: '$CRON_COMMAND'</p>'

		pcp_textarea_inform "Contents of root crontab" "cat /var/spool/cron/crontabs/root" 60
		pcp_textarea_inform "Current config.cfg" "grep -C 4 RESTART= /usr/local/sbin/config.cfg" 150
	fi
}

#----------------------------------------------------------------------------------------
# Main.
#----------------------------------------------------------------------------------------
pcp_table_top "Schedule cronjobs"
pcp_cron_debug

case $SUBMIT in
	Reset)
		echo '<p class="info">[ INFO ] Resetting cronjobs to default...</p>'
		pcp_cron_reset
		pcp_cron_config delete
		;;
	Clear)
		echo '<p class="info">[ INFO ] Clearing all cronjobs...</p>'
		pcp_cron_reset
		crontab -r -u root
	;;
	Save)
		echo '<p class="info">[ INFO ] Saving current cronjob settings...</p>'

		pcp_cron_initialise

		RB_CRON="0 $RB_H $RB_DMONTH * $RB_WD /sbin/reboot"
		RS_CRON="0 $RS_H $RS_DMONTH * $RS_WD /usr/local/etc/init.d/squeezelite restart"

		# Add or remove reboot cron job
		#--------------------------------------------------------------------------------
		if [ "$REBOOT" = "Enabled" ]; then
			( crontab -l | grep -v "reboot"; echo "$RB_CRON" ) | crontab -
		else
			( crontab -l | grep -v "reboot" ) | crontab -
		fi

		# Add or remove restart cron job
		#--------------------------------------------------------------------------------
		if [ "$RESTART" = "Enabled" ]; then
			( crontab -l | grep -v "restart"; echo "$RS_CRON" ) | crontab -
		else
			( crontab -l | grep -v "restart" ) | crontab -
		fi

		# Add or remove Custom cron command
		#--------------------------------------------------------------------------------
		if [ x"" = x"$CRON_COMMAND" ]; then
			( crontab -l | grep -v "Custom" ) | crontab -
		else
			( crontab -l | grep -v "Custom"; echo "$CRON_COMMAND # Custom" ) | crontab -
		fi

		[ "$REBOOT" = "Enabled" ] || [ "$RESTART" = "Enabled" ] || [ x"" != x"$CRON_COMMAND" ] && pcp_cron_config add
	;;
esac

pcp_save_to_config
pcp_backup
pcp_cron_debug
pcp_table_middle
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 15
pcp_table_end
pcp_footer
pcp_copyright
[ $REBOOT_REQUIRED ] && pcp_reboot_required

set +f
echo '</body>'
echo '</html>'