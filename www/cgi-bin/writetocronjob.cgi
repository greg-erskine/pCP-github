#!/bin/sh

# Version: 0.02 2014-10-09 SBP
#	Fixed reboot and restart Squeezelite commands, added DEBUG.

# Version: 0.01 2014-09-09 SBP
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <title>pCP - Write to CMD</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Write to CMD" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string




#---------------------
#Reboot section 
#---------------------
# Decode Reboot variables using httpd, add quotes
REBOOT=`sudo /usr/local/sbin/httpd -d \"$REBOOT\"`
RB_H=`sudo /usr/local/sbin/httpd -d \"$RB_H\"`
if [[ X'""' = X"$RB_H" ]]; then  RB_H='"0"'; else break; fi
RB_WD=`sudo /usr/local/sbin/httpd -d \"$RB_WD\"`
if [[ X'""' = X"$RB_WD" ]]; then  RB_WD='"0"'; else break; fi
RB_DMONTH=`sudo /usr/local/sbin/httpd -d \"$RB_DMONTH\"`
if [[ X'""' = X"$RB_DMONTH" ]]; then  RB_DMONTH='"1"'; else break; fi

sudo sed -i "s/\(REBOOT *=*\).*/\1$REBOOT/" $CONFIGCFG
sudo sed -i "s/\(RB_H *=*\).*/\1$RB_H/" $CONFIGCFG
sudo sed -i "s/\(RB_WD *=*\).*/\1$RB_WD/" $CONFIGCFG
sudo sed -i "s/\(RB_DMONTH *=*\).*/\1$RB_DMONTH/" $CONFIGCFG

#---------------------
#Restart Squeezelite section
#---------------------
# Decode Reboot variables using httpd, add quotes
RESTART=`sudo /usr/local/sbin/httpd -d \"$RESTART\"`
RS_H=`sudo /usr/local/sbin/httpd -d \"$RS_H\"`
if [[ X'""' = X"$RS_H" ]]; then  RS_H='"0"'; else break; fi
RS_WD=`sudo /usr/local/sbin/httpd -d \"$RS_WD\"`
if [[ X'""' = X"$RS_WD" ]]; then  RS_WD='"0"'; else break; fi
RS_DMONTH=`sudo /usr/local/sbin/httpd -d \"$RS_DMONTH\"`
if [[ X'""' = X"$RS_DMONTH" ]]; then  RS_DMONTH='"1"'; else break; fi

sudo sed -i "s/\(RESTART *=*\).*/\1$RESTART/" $CONFIGCFG
sudo sed -i "s/\(RS_H *=*\).*/\1$RS_H/" $CONFIGCFG
sudo sed -i "s/\(RS_WD *=*\).*/\1$RS_WD/" $CONFIGCFG
sudo sed -i "s/\(RS_DMONTH *=*\).*/\1$RS_DMONTH/" $CONFIGCFG

#--------------------
#Setup cron jobs 
#--------------------
# Setup reboot cron job
. /$CONFIGCFG
RB_CRON="0 $RB_H $RB_DMONTH * $RB_WD /sbin/reboot"
RS_CRON="0 $RS_H $RS_DMONTH * $RS_WD /usr/local/etc/init.d/squeezelite restart"

#Add or remove reboot job dependent upon selection:
	if [ $REBOOT = Enabled ]; then
		( crontab -l | grep -v "reboot" ; echo "$RB_CRON" ) | crontab -
	else
		( crontab -l | grep -v "reboot" ) | crontab -
	fi 

#Add or remove restart job dependent upon selection:
	if [ $RESTART = Enabled ]; then
		( crontab -l | grep -v "restart" ; echo "$RS_CRON" ) | crontab -
	else
		( crontab -l | grep -v "restart" ) | crontab -
	fi 
	

if [ $DEBUG = 1 ]; then 
	echo '<p class="debug">[ DEBUG ] $REBOOT: '$REBOOT'<br />'
	echo '                 [ DEBUG ] $RESTART: '$RESTART'<br  />'
	echo '                 [ DEBUG ] $RESTART_Y: '$RESTART_Y' <br />'
	echo '                 [ DEBUG ] $RESTART_N: '$RESTART_N' <br />'
	echo '                 [ DEBUG ] $RB_H: '$RB_H' <br />'
	echo '                 [ DEBUG ] $RB_WD: '$RB_WD' <br />'
	echo '                 [ DEBUG ] $RB_DMONTH: '$RB_DMONTH' <br />'
	echo '                 [ DEBUG ] $RS_H: '$RS_H' <br />'
	echo '                 [ DEBUG ] $RS_WD: '$RS_WD' <br />'
	echo '                 [ DEBUG ] $RS_DMONTH: '$RS_DMONTH' <br />'
	echo '                 [ DEBUG ] $RB_CRON: "$RB_CRON" <br />'
	echo '                 [ DEBUG ] $RS_CRON: "$RS_CRON" <br />'
	echo '      <textarea name="TextBox" cols="120" rows="7">'
	echo '			Content of crontab file:'
					sudo cat /var/spool/cron/crontabs/root
	echo '      </textarea>'
fi


pcp_show_config_cfg
pcp_backup
pcp_go_back_button

echo '</body>'
echo '</html>'