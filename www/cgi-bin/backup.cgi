#!/bin/sh

# Version: 0.03 2014-08-29 GE
#	Added pcp_go_main_button.

# Version: 0.02 2014-07-18 GE
#	Added pcp_running_script.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <meta http-equiv="Refresh" content="5; url=main.cgi">'
echo '  <title>pCP - Backup mydata</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Backup mydata" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_script
pcp_backup
pcp_go_main_button

echo '</body>'
echo '</html>'