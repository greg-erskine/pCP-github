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

# Decode $CMD using httpd, add quotes
CMD=`sudo /usr/local/sbin/httpd -d \"$CMD\"`

sudo sed -i "s/\(CMD *=*\).*/\1$CMD/" $CONFIGCFG

case "$CMD" in 
	\"Default\")
		echo '<p class="info">[ INFO ] $CMD: '$CMD'</p>'
		sudo ./disableotg.sh
		;;
	\"Slow\")
		echo '<p class="info">[ INFO ] $CMD: '$CMD'</p>'
		sudo ./enableotg.sh
		;;
	*)
		echo '<p class="error">[ ERROR ] $CMD invalid: '$CMD'</p>'
		;;
esac

pcp_show_config_cfg
pcp_backup
pcp_go_back_button

echo '</body>'
echo '</html>'
