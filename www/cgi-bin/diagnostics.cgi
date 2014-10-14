#!/bin/sh
# Diagnostics script

# Version: 0.05 2014-10-14 GE
#	Testing $LMSIP.

# Version: 0.04 2014-10-02 GE
#	Added $MODE=5 requirement.
#	Modified textarea behaviour.

# Version: 0.03 2014-09-21 GE
#	Added sound diagnostics output.

# version: 0.02 2014-07-21 GE
#	Added pcp_go_main_button.

# version: 0.01 2014-06-24 GE
#	Orignal.

. pcp-functions
pcp_variables

# Local variables
START="====================> Start <===================="
END="=====================> End <====================="

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <title>pCP - Diagnostics</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Diagnostics" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '  <script language="Javascript" src="../js/piCorePlayer.js"></script>'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_navigation
pcp_running_script
pcp_refresh_button
pcp_go_main_button

if [ $MODE -lt 5 ]; then
	echo '</body>'
	echo '</html>'
	exit 1
fi

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] wlan0: '$(pcp_wlan0_mac_address)'<br />'
	echo '                 [ DEBUG ] eth0: '$(pcp_eth0_mac_address)'<br />'
	echo '                 [ DEBUG ] config: '$(pcp_config_mac_address)'<br />'
	echo '                 [ DEBUG ] controls: '$(pcp_controls_mac_address)'</p>'
fi

#LMSDNS=$(netstat -t 2>&1 | grep 3483 | awk '{print $5}' | awk -F: '{print $1}')
#LMSIP=`nslookup $LMSDNS | grep Address | tail -1 | awk '{print $3}'`

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] LMSIP: '$(pcp_lsmip)'</p>'

#=========================================================================================
# The next 2 textareas have a test for highlighting (change to white) when selected.
#-----------------------------------------------------------------------------------------
echo '<h2>[ INFO ] piCore version: '$(pcp_picore_version)'</h2>'
echo "<textarea id=\"textbox1\" style=\"height:40px;\" onfocus=\"setbg('textbox1','white');\" onblur=\"setbg('textbox1','#d8d8d8')\">"
version
echo '</textarea>'

echo '<h2>[ INFO ] piCorePlayer version: '$(pcp_picoreplayer_version)'</h2>'
echo "<textarea id=\"textbox2\" style=\"height:80px;\" onfocus=\"setbg('textbox2','white');\" onblur=\"setbg('textbox2','#d8d8d8')\">"
echo $START
cat /usr/local/sbin/piversion.cfg
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Squeezelite version and license: '$(pcp_squeezelite_version)'</h2>'
echo "<textarea id=\"textbox3\" style=\"height:350px;\" onfocus=\"setbg('textbox3','white');\" onblur=\"setbg('textbox3','#d8d8d8')\">"
echo $START
/mnt/mmcblk0p2/tce/squeezelite-armv6hf -t
echo $END
echo '</textarea>'
#-----------------------------------------------------------------------------------------

echo '<h2>[ INFO ] ALSA output devices</h2>'
echo '<textarea name="TextBox" cols="120" rows="15">'
echo $START
/mnt/mmcblk0p2/tce/squeezelite-armv6hf -l
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Squeezelite help</h2>'
echo '<textarea name="TextBox" cols="120" rows="20">'
sudo /mnt/mmcblk0p2/tce/squeezelite-armv6hf -h
echo '</textarea>'

# Check if mmcblk0p1 is mounted otherwise mount it

pcp_mount_mmcblk0p1
dmesg | tail -1

if mount | grep $VOLUME; then
	pcp_show_config_txt
	pcp_show_cmdline_txt
	pcp_umount_mmcblk0p1
	sleep 2
	dmesg | tail -1
fi

pcp_show_config_cfg

echo '<h2>[ INFO ] Current bootsync.sh</h2>'
echo '<textarea name="TextBox4" cols="120" rows="8">'
echo $START
cat $BOOTSYNC
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Current bootlocal.sh</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
echo $START
cat $BOOTLOCAL
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Current shutdown.sh</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
echo $START
cat $SHUTDOWN
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] dmesg</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
dmesg
echo '</textarea>'

# These files are created by the backup process
#	/tmp/backup_done
#	/tmp/backup_status

echo '<h2>[ INFO ] Current /opt/.filetool.lst</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
echo $START
cat /opt/.filetool.lst
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Current /opt/.xfiletool.lst</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
echo $START
cat /opt/.xfiletool.lst
echo $END
echo '</textarea>'
 
echo '<h2>[ INFO ] Backup mydata</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
tar tzf /mnt/mmcblk0p2/tce/mydata.tgz
echo '</textarea>'

echo '<h2>[ INFO ] lsmod</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
lsmod
echo '</textarea>'

echo '<h2>[ INFO ] Directory of www/cgi-bin</h2>'
echo '<textarea name="TextBox4" cols="120" rows="12">'
ls -al
echo '</textarea>'

#=========================================================================================
# Sound diagnostics
#-----------------------------------------------------------------------------------------
echo '<h2>[ INFO ] amixer cset numid=3</h2>'
echo '<textarea name="TextBox4" cols="120" rows="5">'
sudo amixer cset numid=3
echo '</textarea>'

echo '<h2>[ INFO ] lsmod | grep snd</h2>'
echo '<textarea name="TextBox4" cols="120" rows="12">'
lsmod | grep snd
echo '</textarea>'

echo '<h2>[ INFO ] /proc/asound</h2>'
echo '<textarea name="TextBox4" cols="120" rows="10">'
ls -al /proc/asound
echo '</textarea>'

echo '<h2>[ INFO ] aplay -l</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
aplay -l
echo '</textarea>'

echo '<h2>[ INFO ] aplay -L</h2>'
echo '<textarea name="TextBox4" cols="120" rows="7">'
aplay -L
echo '</textarea>'

echo '<h2>[ INFO ] amixer</h2>'
echo '<textarea name="TextBox4" cols="120" rows="7">'
amixer
echo '</textarea>'

echo '<h2>[ INFO ] aplay -v -D hw:0,0</h2>'
echo '<textarea name="TextBox4" cols="120" rows="10">'
aplay -v -D hw:0,0 -f S16_LE -r 96000 -c 2 -t raw -d 1 
echo '</textarea>'

echo '<h2>[ INFO ] cat /etc/group</h2>'
echo '<textarea name="TextBox4" cols="120" rows="6">'
cat /etc/group
echo '</textarea>'

echo '<h2>[ INFO ] cat /etc/alsa.conf</h2>'
echo '<textarea name="TextBox4" cols="120" rows="10">'
cat /etc/alsa.conf
echo '</textarea>'

echo '<h2>[ INFO ] cat /etc/asound.conf</h2>'
echo '<textarea name="TextBox4" cols="120" rows="10">'
cat /etc/asound.conf
echo '</textarea>'

echo '<h2>[ INFO ] cat /var/lib/alsa/asound.state</h2>'
echo '<textarea name="TextBox4" cols="120" rows="80">'
cat /var/lib/alsa/asound.state
echo '</textarea>'

echo '<h2>[ INFO ] speaker test - left</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
speaker-test -t sine -f 480 -c 2 -s 1
echo '</textarea>'

echo '<h2>[ INFO ] speaker test - right</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
speaker-test -t sine -f 480 -c 2 -s 2
echo '</textarea>'

pcp_refresh_button

echo '</body>'
echo '</html>'
