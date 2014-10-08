#!/bin/sh
# Turn HDMI output OFF in config.txt

# Version: 0.03 2014-10-07 SBP
#	Added pcp_mount_mmcblk0p1_nohtml and pcp_umount_mmcblk0p1_nohtml.
#	Added echos for booting debugging purposes.

# Version: 0.02 2014-09-02 SBP
#	Added Check for onboard sound card is card=0.

# Version: 0.01 2014-06-25 SBP
#	Original.

echo "[ INFO ] Running $0..."

. /home/tc/www/cgi-bin/pcp-functions
pcp_variables
pcp_mount_mmcblk0p1_nohtml

# Remove HDMI from config.txt file
sed -i '/hdmi_drive=2/d' /mnt/mmcblk0p1/config.txt
sed -i '/hdmi_force_hotplug=1/d' /mnt/mmcblk0p1/config.txt
sed -i '/hdmi_force_edid_audio=1/d' /mnt/mmcblk0p1/config.txt
sed -i '/hdmi_ignore_edid=0xa5000080/d' /mnt/mmcblk0p1/config.txt

pcp_umount_mmcblk0p1_nohtml
pcp_backup_nohtml

# Check for onboard sound card is card=0, then amixer settings is changed from HDMI to analog out
aplay -l | grep 'card 0: ALSA' &> /dev/null
if [ $? = 0 ]; then
	sudo amixer cset numid=3 1
fi

echo "[ INFO ] End $0"
