#!/bin/sh

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

# Decode SUBMIT variable using httpd
SUBMIT=`sudo /usr/local/sbin/httpd -d $SUBMIT`
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] $SUBMIT: '$SUBMIT

#----------------------------------------------------------------------------------------
# Reset section 
#----------------------------------------------------------------------------------------
if [ $SUBMIT = Reset ]; then
	echo '<p class="info">[ INFO ] Reset mode</p>'

	sudo sed -i "s/\(REBOOT *=*\).*/\1\"Disabled\"/" $CONFIGCFG
	sudo sed -i "s/\(RB_H *=*\).*/\1\"0\"/" $CONFIGCFG
	sudo sed -i "s/\(RB_WD *=*\).*/\1\"0\"/" $CONFIGCFG
	sudo sed -i "s/\(RB_DMONTH *=*\).*/\1\"0\"/" $CONFIGCFG
	sudo sed -i "s/\(RESTART *=*\).*/\1\"Disabled\"/" $CONFIGCFG
	sudo sed -i "s/\(RS_H *=*\).*/\1\"0\"/" $CONFIGCFG
	sudo sed -i "s/\(RS_WD *=*\).*/\1\"0\"/" $CONFIGCFG
	sudo sed -i "s/\(RS_DMONTH *=*\).*/\1\"0\"/" $CONFIGCFG

	( crontab -l | grep -v "reboot" ) | crontab -
	( crontab -l | grep -v "restart" ) | crontab -

	pcp_textarea "Contents of root crontab" "cat /var/spool/cron/crontabs/root" 60
	pcp_show_config_cfg
	pcp_backup
	pcp_go_back_button

	echo '</body>'
	echo '</html>'
	exit
fi

#----------------------------------------------------------------------------------------
# Reboot section 
#----------------------------------------------------------------------------------------
# Decode Reboot variables using httpd, add quotes
REBOOT=`sudo /usr/local/sbin/httpd -d \"$REBOOT\"`
RB_H=`sudo /usr/local/sbin/httpd -d \"$RB_H\"`
if [[ x'""' = x"$RB_H" ]]; then  RB_H='"0"'; else break; fi
RB_WD=`sudo /usr/local/sbin/httpd -d \"$RB_WD\"`
if [[ x'""' = x"$RB_WD" ]]; then  RB_WD='"0"'; else break; fi
RB_DMONTH=`sudo /usr/local/sbin/httpd -d \"$RB_DMONTH\"`
if [[ x'""' = x"$RB_DMONTH" ]]; then  RB_DMONTH='"1"'; else break; fi

sudo sed -i "s/\(REBOOT *=*\).*/\1$REBOOT/" $CONFIGCFG
sudo sed -i "s/\(RB_H *=*\).*/\1$RB_H/" $CONFIGCFG
sudo sed -i "s/\(RB_WD *=*\).*/\1$RB_WD/" $CONFIGCFG
sudo sed -i "s/\(RB_DMONTH *=*\).*/\1$RB_DMONTH/" $CONFIGCFG

#----------------------------------------------------------------------------------------
# Restart Squeezelite section
#----------------------------------------------------------------------------------------
# Decode Reboot variables using httpd, add quotes
RESTART=`sudo /usr/local/sbin/httpd -d \"$RESTART\"`
RS_H=`sudo /usr/local/sbin/httpd -d \"$RS_H\"`
if [[ x'""' = x"$RS_H" ]]; then  RS_H='"0"'; else break; fi
RS_WD=`sudo /usr/local/sbin/httpd -d \"$RS_WD\"`
if [[ x'""' = x"$RS_WD" ]]; then  RS_WD='"0"'; else break; fi
RS_DMONTH=`sudo /usr/local/sbin/httpd -d \"$RS_DMONTH\"`
if [[ x'""' = x"$RS_DMONTH" ]]; then  RS_DMONTH='"1"'; else break; fi

sudo sed -i "s/\(RESTART *=*\).*/\1$RESTART/" $CONFIGCFG
sudo sed -i "s/\(RS_H *=*\).*/\1$RS_H/" $CONFIGCFG
sudo sed -i "s/\(RS_WD *=*\).*/\1$RS_WD/" $CONFIGCFG
sudo sed -i "s/\(RS_DMONTH *=*\).*/\1$RS_DMONTH/" $CONFIGCFG

#----------------------------------------------------------------------------------------
# Setup cron jobs 
#----------------------------------------------------------------------------------------
# Setup reboot cron job
. /$CONFIGCFG
RB_CRON="0 $RB_H $RB_DMONTH * $RB_WD /sbin/reboot"
RS_CRON="0 $RS_H $RS_DMONTH * $RS_WD /usr/local/etc/init.d/squeezelite restart"

# Add or remove reboot job dependent upon selection:
if [ $REBOOT = Enabled ]; then
	( crontab -l | grep -v "reboot" ; echo "$RB_CRON" ) | crontab -
else
	( crontab -l | grep -v "reboot" ) | crontab -
fi 

# Add or remove restart job dependent upon selection:
if [ $RESTART = Enabled ]; then
	( crontab -l | grep -v "restart" ; echo "$RS_CRON" ) | crontab -
else
	( crontab -l | grep -v "restart" ) | crontab -
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
	echo '                 [ DEBUG ] $RB_CRON: 'echo "$RB_CRON"'<br />'
	echo '                 [ DEBUG ] $RS_CRON: 'echo "$RS_CRON"'</p>'

	pcp_textarea "Contents of root crontab" "cat /var/spool/cron/crontabs/root" 60
fi

pcp_textarea "Contents of root crontab" "cat /var/spool/cron/crontabs/root" 60
pcp_show_config_cfg
pcp_backup
pcp_go_back_button

echo '</body>'
echo '</html>'