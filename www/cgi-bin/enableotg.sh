#!/bin/sh
# Add dwc_otg_speed=1 to cmdline.txt file

. pcp-functions
pcp_variables
pcp_running_script
pcp_mount_mmcblk0p1

if mount | grep $VOLUME; then
	# Remove dwc_otg_speed=1
	sed -i 's/dwc_otg.speed=1 //g' /mnt/mmcblk0p1/cmdline.txt
	
	# Add dwc_otg_speed=1
	sed -i '1 s/^/dwc_otg.speed=1 /' /mnt/mmcblk0p1/cmdline.txt
	pcp_umount_mmcblk0p1
else
	echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
fi