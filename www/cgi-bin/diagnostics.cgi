#!/bin/sh
# Diagnostics script

# Version: 0.06 2014-12-11 GE
#	Added logging to log file.

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
#	Original.

. pcp-functions
pcp_variables

# Local variables
START="====================> Start <===================="
END="=====================> End <====================="
LOG="/tmp/diagnostics.log"
(echo $0; date) > $LOG

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
	echo '                 [ DEBUG ] controls: '$(pcp_controls_mac_address)'<br />'
	echo '                 [ DEBUG ] LMSIP: '$(pcp_lmsip)'</p>'
fi

pcp_textarea "piCore version: $(pcp_picore_version)" "version" 60 log
pcp_textarea "piCorePlayer version: $(pcp_picoreplayer_version)" "cat /usr/local/sbin/piversion.cfg" 60 log
pcp_textarea "Squeezelite version and license: $(pcp_squeezelite_version)" "/mnt/mmcblk0p2/tce/squeezelite-armv6hf -t" 300 log
pcp_textarea "Squeezelite ALSA output devices" "/mnt/mmcblk0p2/tce/squeezelite-armv6hf -l" 150 log
pcp_textarea "Squeezelite help" "/mnt/mmcblk0p2/tce/squeezelite-armv6hf -h" 300 log

#================================Problem=================================================
pcp_textarea "Squeezelite process" "ps -o args | grep -v grep | grep squeezelite" 60 log

echo '<h2>[ INFO ] Squeezelite process</h2>'
echo '<textarea name="TextBox" style="height:24px;">'
ps -o args | grep -v grep | grep squeezelite
echo '</textarea>'
#================================Problem=================================================

pcp_mount_mmcblk0p1
dmesg | tail -1

if mount | grep $VOLUME; then
	pcp_textarea "Current config.txt" "cat $CONFIGTXT" 150 log
	pcp_textarea "Current cmdline.txt" "cat $CMDLINETXT" 150 log
	pcp_umount_mmcblk0p1
	sleep 2
	#=========Fix============
	dmesg | tail -1
fi

pcp_textarea "Current config.cfg" "cat $CONFIGCFG" 150 log
pcp_textarea "Current bootsync.sh" "cat $BOOTSYNC" 150 log
pcp_textarea "Current bootlocal.sh" "cat $BOOTLOCAL" 150 log
pcp_textarea "Current shutdown.sh" "cat $SHUTDOWN" 150 log
pcp_textarea "" "dmesg" 300 log
pcp_textarea "Current /opt/.filetool.lst" "cat /opt/.filetool.lst" 300 log
pcp_textarea "Current /opt/.xfiletool.lst" "cat /opt/.xfiletool.lst" 300 log
pcp_textarea "Backup mydata" "tar tzf /mnt/mmcblk0p2/tce/mydata.tgz" 300 log
pcp_textarea "lsmod" "lsmod" 300 log
pcp_textarea "Directory of www/cgi-bin" "ls -al" 300 log

pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'