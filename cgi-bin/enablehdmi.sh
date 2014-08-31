#!/bin/sh
# Turn HDMI output ON in config.txt and bootlocal.sh files

. /home/tc/www/cgi-bin/pcp-functions
pcp_variables
pcp_running_script
pcp_mount_mmcblk0p1

if mount | grep $VOLUME; then
	# Remove HDMI settings
	sed -i '/hdmi_drive=2/d' /mnt/mmcblk0p1/config.txt
	sed -i '/hdmi_force_hotplug=1/d' /mnt/mmcblk0p1/config.txt                                                           
	sed -i '/hdmi_force_edid_audio=1/d' /mnt/mmcblk0p1/config.txt                                                        
	sed -i '/hdmi_ignore_edid=0xa5000080/d' /mnt/mmcblk0p1/config.txt

	# Insert HDMI setting to enable HDMI out
	sudo echo hdmi_drive=2 >> /mnt/mmcblk0p1/config.txt
	sudo echo hdmi_force_hotplug=1 >> /mnt/mmcblk0p1/config.txt                                                           
	sudo echo hdmi_force_edid_audio=1 >> /mnt/mmcblk0p1/config.txt                                                        
	sudo echo hdmi_ignore_edid=0xa5000080 >> /mnt/mmcblk0p1/config.txt

	if [ $DEBUG = 1 ]; then	
		pcp_show_config_txt
	fi
	
	# Check for onboard sound card is card=0, so HDMI amixer settings is only used here
	aplay -l | grep 'card 0: ALSA' &> /dev/null
	if [ $? == 0 ] && [ $AUDIO = HDMI ]; then
	    sudo amixer cset numid=3 2
	fi 
 

	if [ $DEBUG = 1 ]; then	
		pcp_show_bootlocal_sh
	fi
	
	pcp_umount_mmcblk0p1
	pcp_backup
fi


