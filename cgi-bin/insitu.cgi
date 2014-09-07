#!/bin/sh

# Version: 0.05 2014-09-05 GE
#	Added INSITU_DOWNLOAD variable.

# Version: 0.04 2014-08-12 GE
#	Added sudo to wget.

# Version: 0.03 2014-07-21 GE
#	Improved error checking.
#	Added pcp_go_main_button and pcp_navigation.

# Version: 0.02 2014-06-24 GE
#	Rewritten.

# Version: 0.01 2014 SBP
#	Orignal.

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
echo '  <title>pCP - InSitu upgrade</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="InSitu upgrade" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

# Decode variables using httpd
INSITU=`sudo /usr/local/sbin/httpd -d $INSITU`

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] QUERY_STRING: '$QUERY_STRING'<br />'
	echo '                 [ DEBUG ] INSITU: '$INSITU'<br />'
	echo '                 [ DEBUG ] UPD_PCP: '$UPD_PCP'<br />'
	echo '                 [ DEBUG ] INSITU_DOWNLOAD: '$INSITU_DOWNLOAD'</p>'
fi

#=========================================================================================
# This should be passed to do_updatepicoreplayer.cgi via hidden input field.
#-----------------------------------------------------------------------------------------
echo "INSITU="$INSITU > $UPD_PCP/version.cfg
#-----------------------------------------------------------------------------------------

echo '<h2>[ INFO ] You are going from piCorePlayer'$(pcp_picoreplayer_version)' to '$INSITU'</h2>'

# Make directories
sudo mkdir $UPD_PCP/boot
sudo mkdir $UPD_PCP/tce

# Download the boot files and the tce files and Break if errors in downloading boot files
echo '<p class="info">[ INFO ] Downloading '$INSITU'_boot.tar.gz...</p>'
sudo wget -P "$UPD_PCP"/boot "$INSITU_DOWNLOAD"/"$INSITU"/"$INSITU"_boot.tar.gz
result_boot=$?
if [ $result_boot = 0 ]; then
	echo '<p class="ok">[ OK ] Success downloading boot files</p>'
else
	echo '<p class="error">[ ERROR: '$result_boot' ] Error downloading boot files</p>'
	pcp_go_main_button
fi

if [ $result_boot = 0 ]; then
	# Break if error in downloading tce files
	echo '<p class="info">[ INFO ] Downloading '$INSITU'_tce.tar.gz...</p>'
	sudo wget -P "$UPD_PCP"/tce "$INSITU_DOWNLOAD"/"$INSITU"/"$INSITU"_tce.tar.gz
	result_tce=$?
	if [ $result_tce = 0 ]; then
		echo '<p class="ok">[ OK ] Success downloading tce files</p>'
		echo '<form name="do_update" action= "do_updatepicoreplayer.cgi" method="get">'
		echo '<p><input type="submit" value="Update piCorePlayer" />&nbsp;&nbsp;When you press the button, you will make the actual update with the downloaded files.</p></form>'
	else
		echo '<p class="error">[ ERROR: '$result_tce' ] Error downloading tce files.</p>'
	fi
fi

pcp_go_main_button

echo '</body>'
echo '</html>'
