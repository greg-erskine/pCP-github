#!/bin/sh

# Version: 0.04 2015-11-18 GE
#	Added code for VU Meters.

# Version: 0.03 2015-08-29 SBP
#	Changed to touch-screen version.

# Version: 0.02 2015-05-08 GE
#	Revised.

# Version: 0.01 2015-03-15 SBP
#	Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to Jivelite Tweak" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

sudo sed -i "s/\(JIVELITE *=*\).*/\1$JIVELITE/" $CONFIGCFG   #<--------------????????????????????
[ $JIVELITE = YES ] && VISUALISER="yes"
pcp_save_to_config

jivelite_tcz="jivelite_touch.tcz"
jivelite_md5="jivelite_touch.tcz.md5.txt"

dl_jivelite_tcz="http://ralph_irving.users.sourceforge.net/pico/$jivelite_tcz"
dl_jivelite_md5="http://ralph_irving.users.sourceforge.net/pico/$jivelite_md5"

vumeter_tcz="VU_Meter*.tcz"
vumeter_md5="VU_Meter*.tcz.md5.txt"
default_vumeter_tcz="VU_Meter_b.tcz"

dl_vumeter_tcz="http://ralph_irving.users.sourceforge.net/pico/$vumeter_tcz"
dl_vumeter_md5="http://ralph_irving.users.sourceforge.net/pico/$vumeter_md5"

#########################################################################################
# You are supposed to use the md5sum to verify the file was downloaded correctly. See
# sample script below.
#########################################################################################
#        echo "Downloading: $1"
#        wget -cq "$MIRROR"/"$1".md5.txt 2>/dev/null
#        wget -c "$MIRROR"/"$1"
#        md5sum -c "$1".md5.txt
#        if [ "$?" != 0 ]; then
#                echo "Error on $1"
#                abort_to_saved_dir
#        fi
#########################################################################################

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] OPTION: '$OPTION'<br />'
	echo '                 [ DEBUG ] JIVELITE: '$JIVELITE'<br />'
	echo '                 [ DEBUG ] VISUALISER: '$VISUALISER'<br />'
	echo '                 [ DEBUG ] VUMETER: '$VUMETER'</p>'
fi

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_load_jivelite() {
	echo '<p class="info">[ INFO ] Downloading Jivelite from Ralphy'\''s repository...</p>'
	wget -P /tmp $dl_jivelite_md5
	wget -P /tmp $dl_jivelite_tcz
	# The next few lines need to be changed to check md5.
	result=$?
	if [ $result -ne "0" ]; then
		echo '<p class="error">[ ERROR ] Download unsuccessful, try again later!'
	else
		echo '<p class="ok">[ OK ] Download successful'
		sudo cp /tmp/$jivelite_tcz /mnt/mmcblk0p2/tce/optional/jivelite.tcz
		sudo chown tc:staff /mnt/mmcblk0p2/tce/optional/jivelite.tcz
		sudo cp /tmp/$jivelite_md5 /mnt/mmcblk0p2/tce/optional/jivelite.tcz.md5.txt
		sudo chown tc:staff /mnt/mmcblk0p2/tce/optional/jivelite.tcz.md5.txt
	fi
}

pcp_install_jivelite() {
	echo '<p class="info">[ INFO ] Jivelite is installed in piCorePlayer.</p>'
	sudo -u tc tce-load -i jivelite.tcz
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is added to onboot.lst</p>'
	sudo sed -i '/jivelite.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo echo 'jivelite.tcz' >> /mnt/mmcblk0p2/tce/onboot.lst

	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is added to .xfiletool.lst</p>'
	sudo sed -i '/^opt\/jivelite/d' /opt/.xfiletool.lst
	sudo echo 'opt/jivelite' >> /opt/.xfiletool.lst

	# need to add this to cmdline.txt ==> consoleblank=0 
}

pcp_delete_jivelite() {
	echo '<p class="info">[ INFO ] Jivelite is removed from piCorePlayer.</p>'
	sudo rm -f /mnt/mmcblk0p2/tce/optional/jivelite.tcz
	sudo rm -f /mnt/mmcblk0p2/tce/optional/jivelite.tcz.md5.txt
	sudo rm -rf /home/tc/.jivelite
	sudo rm -rf /opt/jivelite

	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is removed from onboot.lst</p>'
	sudo sed -i '/jivelite.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst

	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is removed from .xfiletool.lst</p>'
	sudo sed -i '/^opt\/jivelite/d' /opt/.xfiletool.lst
}

pcp_remove_temp() {
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Removing previous downloads from tmp directory.</p>'
	sudo rm -f /tmp/$jivelite_tcz
	sudo rm -f /tmp/$jivelite_md5
	sudo rm -f /tmp/$vumeter_tcz
	sudo rm -f /tmp/$vumeter_md5
}

pcp_load_vumeters() {
	echo '<p class="info">[ INFO ] Downloading VU Meters from Ralphy'\''s repository...</p>'
	wget -P /tmp $dl_jivelite_md5
	wget -P /tmp $dl_jivelite_tcz 
	# The next few lines need to be changed to check md5.
	result=$?
	if [ $result -ne "0" ]; then
		echo '<p class="error">[ ERROR ] Download unsuccessful, try again later!'
	else
		echo '<p class="ok">[ OK ] Download successful'
		sudo cp /tmp/$vumeter_tcz /mnt/mmcblk0p2/tce/optional/
		sudo chown tc:staff /mnt/mmcblk0p2/tce/optional/$vumeter_tcz
		sudo cp /tmp/$vumeter_md5 /mnt/mmcblk0p2/tce/optional/
		sudo chown tc:staff /mnt/mmcblk0p2/tce/optional/$vumeter_md5
	fi
}

pcp_install_default_vumeter() {
	echo '<p class="info">[ INFO ] Default VU Meter is installed.</p>'
	sudo -u tc tce-load -i $default_vumeter_tcz
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Default VU Meter is added to onboot.lst</p>'
	sudo sed -i '/VU_Meters/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo echo $default_vumeter_tcz >> /mnt/mmcblk0p2/tce/onboot.lst
}

pcp_install_vumeter() {
	echo '<p class="info">[ INFO ] Installing VU Meter...</p>'

	# Unmount all loop mounted VU_Meters (Note: should be only zero or one)
	MOUNTED_METERS=$(df | grep VU_Meter | awk '{print $6}' )
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] '$MOUNTED_METERS'</p>'

	for i in $MOUNTED_METERS
	do
		sudo umount $i
	done

	rm -f /usr/local/tce.installed/VU_Meter*
	sudo -u tc tce-load -i $VUMETER >/dev/null 2>&1
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] VU Meters is added to onboot.lst</p>'
	sudo sed -i '/VU_Meter/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo echo $VUMETER >> /mnt/mmcblk0p2/tce/onboot.lst
}

pcp_delete_vumeters() {
	echo '<p class="info">[ INFO ] VU Meters are removed.</p>'
	sudo rm -f /mnt/mmcblk0p2/tce/optional/VU_Meter*.tcz
	sudo rm -f /mnt/mmcblk0p2/tce/optional/VU_Meter*.tcz.md5.txt

	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] VU Meters are removed from onboot.lst</p>'
	sudo sed -i '/VU_Meter/d' /mnt/mmcblk0p2/tce/onboot.lst
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
case $OPTION in

	JIVELITE)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Doing OPTION: '$OPTION'<br />'
		case $JIVELITE in
			YES)
				#pcp_load_jivelite
				pcp_install_jivelite
				#pcp_load_vumeters
				pcp_install_default_vumeter
				pcp_remove_temp
				;;
			NO)
				#pcp_delete_jivelite
				#pcp_delete_vumeters
				pcp_remove_temp
				;;
			*)
				[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] JIVELITE: '$JIVELITE'<br />'
				;;
		esac

		pcp_backup
		[ $DEBUG = 1 ] && pcp_show_config_cfg

		echo '<p class="info">[ INFO ] A reboot is needed in order to finalize!</p>'
		pcp_reboot_button
		;;

	VUMETER)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Doing OPTION: '$OPTION'<br />'
		pcp_install_vumeter
		;;
esac

pcp_go_back_button

echo '</body>'
echo '</html>'