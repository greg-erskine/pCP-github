#!/bin/sh
# Diagnostics script

# Version: 0.05 2014-10-22 GE
#	Testing $LMSIP.
#	Removed sound output to diag_snd.cgi
#	Using pcp_html_head now.

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

pcp_html_head "Diagnostics" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_refresh_button
pcp_go_main_button
pcp_footer

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

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] LMSIP: '$(pcp_lmsip)'</p>'

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

echo '<h2>[ INFO ] Squeezelite ALSA output devices</h2>'
echo '<textarea name="TextBox" rows="15">'
echo $START
/mnt/mmcblk0p2/tce/squeezelite-armv6hf -l
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Squeezelite help</h2>'
echo '<textarea name="TextBox" rows="20">'
sudo /mnt/mmcblk0p2/tce/squeezelite-armv6hf -h
echo '</textarea>'

echo '<h2>[ INFO ] Squeezelite process</h2>'
echo '<textarea name="TextBox" style="height:24px;">'
ps -o args | grep -v grep | grep squeezelite
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
echo '<textarea name="TextBox4" rows="8">'
echo $START
cat $BOOTSYNC
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Current bootlocal.sh</h2>'
echo '<textarea name="TextBox4" rows="15">'
echo $START
cat $BOOTLOCAL
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Current shutdown.sh</h2>'
echo '<textarea name="TextBox4" rows="15">'
echo $START
cat $SHUTDOWN
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] dmesg</h2>'
echo '<textarea name="TextBox4" rows="15">'
dmesg
echo '</textarea>'

# These files are created by the backup process
#	/tmp/backup_done
#	/tmp/backup_status

echo '<h2>[ INFO ] Current /opt/.filetool.lst</h2>'
echo '<textarea name="TextBox4" rows="15">'
echo $START
cat /opt/.filetool.lst
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Current /opt/.xfiletool.lst</h2>'
echo '<textarea name="TextBox4" rows="15">'
echo $START
cat /opt/.xfiletool.lst
echo $END
echo '</textarea>'
 
echo '<h2>[ INFO ] Backup mydata</h2>'
echo '<textarea name="TextBox4" rows="15">'
tar tzf /mnt/mmcblk0p2/tce/mydata.tgz
echo '</textarea>'

echo '<h2>[ INFO ] lsmod</h2>'
echo '<textarea name="TextBox4" rows="15">'
lsmod
echo '</textarea>'

echo '<h2>[ INFO ] Directory of www/cgi-bin</h2>'
echo '<textarea name="TextBox4" rows="12">'
ls -al
echo '</textarea>'

pcp_refresh_button
pcp_footer

echo '</body>'
echo '</html>'
