#!/bin/sh

# Version: 0.02 2014-08-28 GE
#	Changed refresh time from 30 to 20 seconds.
#	Added pcp_go_main_button.
#	Added textarea with listing of *config.cfg on USB

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables

# First location
VOLUME_A=/mnt/sda1
DEVICE_A=/dev/sda1

#=========================================================================================
# Alternative locations. NOT USED.
#-----------------------------------------------------------------------------------------
# Second location
#VOLUME_B=/mnt/sdb1
#DEVICE_B=/dev/sdb1

# Third location
# Defined in pcp-functions
#VOLUME=/mnt/mmcblk0p1
#DEVICE=/dev/mmcblk0p1

#=========================================================================================
# is_mounted routine, used later in the script
#-----------------------------------------------------------------------------------------
is_mounted() {
	echo '<p class="info">[ INFO ] '$VOLUME_A' is mounted.</p>'
	echo '<p class="info">[ INFO ] Copying config.cfg to USB...</p>'
	sudo /bin/cp -f /usr/local/sbin/config.cfg /mnt/sda1/newconfig.cfg
	if [ -f /mnt/sda1/newconfig.cfg ]; then
		echo '<h2>Your config file (config.cfg) has been saved to your USB stick as newconfig.cfg.</h2>'
		echo '<p>Note: If you boot with this USB-stick attached then this file will be copied by piCorePlayer and used as config file.<br>
				 This is handy if you update your piCorePlayer or want to setup another piCorePlayer with similar settings.</p>'
				 echo '<textarea name="TextBox" cols="120" rows="3">'
				 ls -al /mnt/sda1/*config.cfg
				 echo '</textarea>'
	else
		echo '<h2>Something went wrong! Your config file (config.cfg) was NOT saved - reboot with your USB attached and then try to save your config file again.</h2>'
	fi
	sync
	echo '<p class="info">[ INFO ] Unmounting '$VOLUME_A'</p>'
	sudo umount $DEVICE_A
}

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <meta http-equiv="Refresh" content="20; url=main.cgi">'
echo '  <title>pCP - Save config.cfg to USB</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Save config.cfg to USB" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_script

if mount | grep $VOLUME_A; then
	echo '<p class="info">[ INFO ] '$VOLUME_A' is mounted...</p>'
else
	echo '<p class="info">[ INFO ] Mounting '$VOLUME_A'...</p>'
	echo '<p style="font-size:10px">'
	sudo mount $DEVICE_A;
	sleep 1
fi

if mount | grep $VOLUME_A; then
	is_mounted
else
	echo '<p class="error">[ ERROR ] '$VOLUME_A' has NOT mounted.</p>'
	echo '<p class="error">[ ERROR ] Insert USB stick and try again.</p>'
fi

pcp_go_main_button

echo '</body>'
echo '</html>'
