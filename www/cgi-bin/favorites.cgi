#!/bin/sh

# Version: 0.01 2015-01-13 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Favorites" "GE"

#====================================Fix=================================================

#echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
#echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
#echo ''
#echo '<head>'
#echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
#echo '  <meta http-equiv="Pragma" content="no-cache" />'
#echo '  <meta http-equiv="Expires" content="0" />'
#echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
#echo '  <title>pCP - Controls</title>'
#echo '  <meta name="author" content="Steen" />'
#echo '  <meta name="description" content="Controls" />'
#echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
#echo '  <script language="Javascript" src="../js/piCorePlayer.js"></script>'
#echo '</head>'
#echo ''

[ $DEBUG = 1 ] && echo '<body>' || echo '<body onload="javascript:location.href=document.referrer;">'

#====================================Fix=================================================

[ $DEBUG = 1 ] && pcp_controls && pcp_banner && pcp_navigation && pcp_running_script

pcp_httpd_query_string

pcp_start_fav $STARTFAV

[ $DEBUG = 1 ] && pcp_footer

echo '</body>'
echo '</html>'