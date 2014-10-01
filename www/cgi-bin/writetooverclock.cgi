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
echo '  <title>pCP - Write Overclock to Config</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Write Overclock to Config" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Decode $OVERCLOCK using httpd, add quotes
OVERCLOCK=`sudo /usr/local/sbin/httpd -d \"$OVERCLOCK\"`

# Save $OVERCLOCK to config file
sudo sed -i "s/\(OVERCLOCK *=*\).*/\1$OVERCLOCK/" $CONFIGCFG

pcp_backup

# Call overclocking script
sudo ./overclock.sh

. $CONFIGCFG

echo '<p class="info">[ INFO ] Overclock is set to: '$OVERCLOCK'</p>'

[ $DEBUG = 1 ] && pcp_show_config_cfg

pcp_go_back_button

echo '</body>'
echo '</html>'
