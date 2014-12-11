#!/bin/sh
# change FIQ settings in cmdline.txt file

. pcp-functions
pcp_variables
pcp_running_script
pcp_mount_mmcblk0p1

if mount | grep $VOLUME; then
	# Remove fiq settings
	sed -i 's/dwc_otg.fiq_fsm_mask=0x1 //g' /mnt/mmcblk0p1/cmdline.txt
	sed -i 's/dwc_otg.fiq_fsm_mask=0x2 //g' /mnt/mmcblk0p1/cmdline.txt
	sed -i 's/dwc_otg.fiq_fsm_mask=0x3 //g' /mnt/mmcblk0p1/cmdline.txt
	sed -i 's/dwc_otg.fiq_fsm_mask=0x4 //g' /mnt/mmcblk0p1/cmdline.txt
	sed -i 's/dwc_otg.fiq_fsm_mask=0x7 //g' /mnt/mmcblk0p1/cmdline.txt
	sed -i 's/dwc_otg.fiq_fsm_mask=0x8 //g' /mnt/mmcblk0p1/cmdline.txt

	# Add FIQ settings from config file
	sed -i '1 s/^/dwc_otg.fiq_fsm_mask='$FIQ' /' /mnt/mmcblk0p1/cmdline.txt

	[ $DEBUG = 1 ] && pcp_show_cmdline_txt
	pcp_umount_mmcblk0p1
else
	echo '<p class="error">[ ERROR ] '$VOLUME' not mounted</p>'
fi