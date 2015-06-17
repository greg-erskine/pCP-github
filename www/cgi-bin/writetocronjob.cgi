#!/bin/sh

# Version: 0.06 2015-06-12 SBP
#	Added Custom cron command.

# Version: 0.05 2015-01-30 GE
#	Added Clear option.

# Version: 0.04 2014-12-22 SBP
#	Moved box showing "Contents of root crontab" from debug to always display.

# Version: 0.03 2014-12-16 GE
#	Using pcp_html_head now.
#	HTML5 formatting.
#	Added Reset section.

# Version: 0.02 2014-10-09 SBP
#	Fixed reboot and restart Squeezelite commands, added DEBUG.

# Version: 0.01 2014-09-09 SBP
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to crontab" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

set -f

# Decode SUBMIT variable using httpd
SUBMIT=`sudo $HTPPD -d $SUBMIT`
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] $SUBMIT: '$SUBMIT

#----------------------------------------------------------------------------------------
# Reset section
#----------------------------------------------------------------------------------------
if [ $SUBMIT = Reset ] || [ $SUBMIT = Clear ]; then
	echo '<p class="info">[ INFO ] Reset/Clear mode</p>'

	REBOOT="Disabled"
	RB_H=""
	RB_WD=""
	RB_DMONTH=""
	RESTART="Disabled"
	RS_H=""
	RS_WD=""
	RS_DMONTH=""
	CRON_COMMAND=""

	pcp_save_to_config

	( crontab -l | grep -v "reboot" ) | crontab -
	( crontab -l | grep -v "restart" ) | crontab -
	( crontab -l | grep -v "Custom" ) | crontab -
	[ $SUBMIT = Clear ] && crontab -r -u root

	pcp_textarea "Contents of root crontab" "cat /var/spool/cron/crontabs/root" 60
	pcp_show_config_cfg
	pcp_backup
	pcp_go_back_button

	echo '</body>'
	echo '</html>'
	exit
fi

#----------------------------------------------------------------------------------------
# Reboot piCorePlayer section
#----------------------------------------------------------------------------------------
# Decode Reboot variables using httpd
REBOOT=`sudo $HTPPD -d $REBOOT`
RB_H=`sudo $HTPPD -d $RB_H`
RB_WD=`sudo $HTPPD -d $RB_WD`
RB_DMONTH=`sudo $HTPPD -d $RB_DMONTH`

# Default values if not set. STEEN, ARE THESE RIGHT - GREG I DON'T THINK WE NEED THEM HERE?
#[ x"" = x"$RB_H" ] && RB_H="0"
#[ x"" = x"$RB_WD" ] && RB_WD="0"
#[ x"" = x"$RB_DMONTH" ] && RB_DMONTH="1"

#----------------------------------------------------------------------------------------
# Restart Squeezelite section
#----------------------------------------------------------------------------------------
# Decode Restart variables using httpd
RESTART=`sudo $HTPPD -d $RESTART`
RS_H=`sudo $HTPPD -d $RS_H`
RS_WD=`sudo $HTPPD -d $RS_WD`
RS_DMONTH=`sudo $HTPPD -d $RS_DMONTH`

# Default values if not set. STEEN, ARE THESE RIGHT - GREG I DON'T THINK WE NEED THEM HERE?
#[ x"" = x"$RS_H" ] && RS_H="0"
#[ x"" = x"$RS_WD" ] && RS_WD="0"
#[ x"" = x"$RS_DMONTH" ] && RS_DMONTH="1"

#----------------------------------------------------------------------------------------
# Custom cron section
#----------------------------------------------------------------------------------------
# Decode Custom cron variables using httpd
CRON_COMMAND=`sudo $HTPPD -d $CRON_COMMAND`

#---------------------------------------------------------------------------------------
# Save cron variables to config
#---------------------------------------------------------------------------------------
pcp_save_to_config

#----------------------------------------------------------------------------------------
# Setup cron jobs
#----------------------------------------------------------------------------------------
. /$CONFIGCFG
RB_CRON="0 $RB_H $RB_DMONTH * $RB_WD /sbin/reboot"
RS_CRON="0 $RS_H $RS_DMONTH * $RS_WD /usr/local/etc/init.d/squeezelite restart"

# Add or remove reboot job
if [ $REBOOT = Enabled ]; then
	( crontab -l | grep -v "reboot" ; echo "$RB_CRON" ) | crontab -
else
	( crontab -l | grep -v "reboot" ) | crontab -
fi

# Add or remove restart job
if [ $RESTART = Enabled ]; then
	( crontab -l | grep -v "restart" ; echo "$RS_CRON" ) | crontab -
else
	( crontab -l | grep -v "restart" ) | crontab -
fi

# Add or remove Custom cron command
if [ x"" = x"$CRON_COMMAND" ]; then
	( crontab -l | grep -v "Custom" ) | crontab -
else
	( crontab -l | grep -v "Custom" ; echo "$CRON_COMMAND # Custom" ) | crontab -
fi

if [ $DEBUG = 1 ]; then
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
fi

pcp_textarea "Contents of root crontab" "cat /var/spool/cron/crontabs/root" 60
pcp_show_config_cfg
pcp_backup
pcp_go_back_button

set +f

echo '</body>'
echo '</html>'