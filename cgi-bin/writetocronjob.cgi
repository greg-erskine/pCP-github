#!/bin/sh

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

pcp_banner
pcp_running_script
pcp_httpd_query_string


#---------------------
#Reboot section 
#---------------------
# Decode Reboot variables using httpd, add quotes
REBOOT=`sudo /usr/local/sbin/httpd -d \"$REBOOT\"`
RB_H=`sudo /usr/local/sbin/httpd -d \"$RB_H\"`
RB_WD=`sudo /usr/local/sbin/httpd -d \"$RB_WD\"`
RB_DMONTH=`sudo /usr/local/sbin/httpd -d \"$RB_DMONTH\"`

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
RS_WD=`sudo /usr/local/sbin/httpd -d \"$RS_WD\"`
RS_DMONTH=`sudo /usr/local/sbin/httpd -d \"$RS_DMONTH\"`

sudo sed -i "s/\(RESTART *=*\).*/\1$RESTART/" $CONFIGCFG
sudo sed -i "s/\(RS_H *=*\).*/\1$RS_H/" $CONFIGCFG
sudo sed -i "s/\(RS_WD *=*\).*/\1$RS_WD/" $CONFIGCFG
sudo sed -i "s/\(RS_DMONTH *=*\).*/\1$RS_DMONTH/" $CONFIGCFG

#--------------------
#Setup cron jobs 
#--------------------
# Setup reboot con job
. /$CONFIGCFG
RB_CRON="* $RB_H $RB_DMONTH * $RB_WD $pCPHOME/reboot.sh"
RS_CRON="* $RS_H $RS_DMONTH * $RS_WD $pCPHOME/restart.sh"


#Add or remove reboot job dependent upon selection:
	if [ $REBOOT = Enabled ]; then
		echo "enabled"
		( crontab -l | grep -v "reboot" ; echo "$RB_CRON" ) | crontab -
	else
		echo "disabled"
		( crontab -l | grep -v "reboot" ) | crontab -
	fi 

#Add or remove restart job dependent upon selection:
	if [ $RESTART = Enabled ]; then
		echo "enabled"
		( crontab -l | grep -v "restart" ; echo "$RS_CRON" ) | crontab -
	else
		echo "disabled"
		( crontab -l | grep -v "restart" ) | crontab -
	fi 
	
	
	
	
#remove cronjob is reboot is disabled
#( crontab -l | grep -v "reboot" ) | crontab -

#cat < (crontab -l) |grep -v "$RB_CRON" < (echo "$RB_CRON")

# Setup restart squeezelite cron job
#RS_CRON="* '$RS_H' '$RS_DMONTH' * '$RS_WD' /restart"
#cat < (crontab -l) |grep -v "${RS_CRON}" < (echo "${RS_CRON}")
#echo "cronjob er" $RS_CRON
#( crontab -l | grep -v "$RB_CRON" ; echo "$RB_CRON" ) | crontab -




pcp_show_config_cfg
pcp_backup
pcp_go_back_button

echo '</body>'
echo '</html>'