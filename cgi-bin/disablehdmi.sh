#!/bin/sh
# Turn HDMI output OFF in config.txt and bootlocal.sh files

. /home/tc/www/cgi-bin/pcp-functions
pcp_variables
pcp_running_script
pcp_mount_mmcblk0p1

# Remove HDMI from config.txt file
sed -i '/hdmi_drive=2/d' /mnt/mmcblk0p1/config.txt
sed -i '/hdmi_force_hotplug=1/d' /mnt/mmcblk0p1/config.txt
sed -i '/hdmi_force_edid_audio=1/d' /mnt/mmcblk0p1/config.txt
sed -i '/hdmi_ignore_edid=0xa5000080/d' /mnt/mmcblk0p1/config.txt


# Check for onboard sound card is card=0, then amixer settings is changed from HDMI to analog out
aplay -l | grep 'card 0: ALSA' &> /dev/null
if [ $? = 0 ]; then
	sudo amixer cset numid=3 1
fi

pcp_umount_mmcblk0p1
pcp_backup
