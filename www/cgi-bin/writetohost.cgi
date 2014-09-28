#!/bin/sh
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
echo '  <title>pCP - Write Hostname</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Write Hostname" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Decode Host name using httpd
HOST=`sudo /usr/local/sbin/httpd -d \"$HOST\"`

echo '<p class="info">[ INFO ] Your HOST name is set to: '$HOST'</p>'

# Update host name in config file
sudo sed -i "s/\(HOST *=*\).*/\1$HOST/" $CONFIGCFG

# Update host name in bootsync.sh file
sudo sed -i '/sethostname/c\/usr/bin/sethostname '"$HOST" /opt/bootsync.sh

pcp_backup

[ $DEBUG = 1 ] && pcp_show_bootsync_sh
[ $DEBUG = 1 ] && pcp_show_config_cfg

pcp_go_back_button

echo '</body>'
echo '</html>'
