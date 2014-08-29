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

# Remove the line with the HDMI amixer settings in bootlocal.sh by adding #
sed -i "/amixer cset numid=/c\#amixer cset numid=3 2" /opt/bootlocal.sh

pcp_umount_mmcblk0p1
pcp_backup
