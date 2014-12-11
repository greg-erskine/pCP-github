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
echo '  <title>pCP - Write WIFI Settings</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Write WIFI Settings" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_string
pcp_httpd_query_string

# Decode variables using httpd
SSID=`sudo /usr/local/sbin/httpd -d $SSID`
PASSWORD=`sudo /usr/local/sbin/httpd -d $PASSWORD`
ENCRYPTION=`sudo /usr/local/sbin/httpd -d $ENCRYPTION`
WIFI=`sudo /usr/local/sbin/httpd -d $WIFI`


echo '<h2>[ INFO ] You provided the following information</h2>'
echo '<p class="info">[ INFO ] WIFI is: '$WIFI'<br />'
echo '                [ INFO ] Your wifi SSID is: '$SSID'<br />'
echo '                [ INFO ] Your password is: '$PASSWORD'<br />'
echo '                [ INFO ] Encryption method is: '$ENCRYPTION'</p>'

# NEW section to save the parameters to the wifi.db
# This is a new version in order to saving space and backslash in SSID which is needed in wifi.db
# so a name like "steens wifi" should be saved as  "steens\ wifi"

# Only add backslash if not empty
if [ X"" = X"$SSID" ]; then
	break
else
	SSSID=`echo "$SSID" | sed 's/\ /\\\ /g'`
	# Change SSSID back to SSID
	SSID=$SSSID
fi

# Saves SSID either empty or with backslash
sudo chmod 766 /home/tc/wifi.db
sudo echo ${SSSID}$'\t'${PASSWORD}$'\t'${ENCRYPTION} > /home/tc/wifi.db

echo '<h2>[ INFO ] Current wifi.db</h2>'
echo '<textarea name="TextBox" cols="120" rows="2">'
cat $WIFIDB
echo '</textarea>'

# Add " " around variables
SSID="\"${SSID}"\"
PASSWORD="\"${PASSWORD}"\"
ENCRYPTION="\"${ENCRYPTION}"\"
WIFI="\"${WIFI}"\"

# Save the parameters to the config file
sudo sed -i "s/\(SSID *=*\).*/\1$SSID/" $CONFIGCFG
sudo sed -i "s/\(PASSWORD *=*\).*/\1$PASSWORD/" $CONFIGCFG
sudo sed -i "s/\(ENCRYPTION *=*\).*/\1$ENCRYPTION/" $CONFIGCFG
sudo sed -i "s/\(WIFI *=*\).*/\1$WIFI/" $CONFIGCFG

pcp_show_config_cfg
pcp_backup


##### BELOW NEEDS WORK #####

if [ $WIFI == "\"on\"" ]; then

	# Connect to the wifi
	sudo ifconfig wlan0 down
	sudo ifconfig wlan0 up

	echo "<br />"
	sudo wifi.sh -a
	echo "<br />"
	echo "<br />"
	echo "<h3>Info on the established connection:</h3>"
	echo "<br />"
echo '<textarea name="TextBox" cols="120" rows="8">'
	echo "Output from the ifconfig command:"
	ifconfig
	echo "<br />"
	echo "<br />"
	echo "Output from the iwconfig command:"
	iwconfig
echo '</textarea>'
fi

pcp_go_back_button

echo '</body>'
echo '</html>'