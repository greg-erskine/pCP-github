#!/bin/sh

# Version: 0.02 2015-04-28 GE
#   Revised.

# Version: 0.01 2015-03-15 SBP
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to Jivelite Tweak" "SBP" "15" "tweaks.cgi"

DEBUG=1

pcp_banner
pcp_running_script
pcp_httpd_query_string

sudo sed -i "s/\(JIVELITE *=*\).*/\1$JIVELITE/" $CONFIGCFG
[ $JIVELITE = YES ] && VISUALISER="yes"
pcp_save_to_config
pcp_backup

downloadtcz="http://ralph_irving.users.sourceforge.net/pico/jivelite.tcz"
downloadmd5="http://ralph_irving.users.sourceforge.net/pico/jivelite.tcz.md5.txt"

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] JIVELITE: '$JIVELITE'<br />'
	echo '                 [ DEBUG ] VISUALISER: '$VISUALISER'</p>'
fi

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_load_jivelite() {
	echo '<p class="info">[ INFO ] Downloading Jivelite from Ralphy</p>'
	wget -P /tmp $downloadmd5
	wget -P /tmp $downloadtcz
	result=$?
	# MD5 CHECK  - look at tce-load for code
	if [ $result -ne "0" ]; then
		echo '<p class="error">[ ERROR ] Download unsuccessful, try again later!'
	else
		echo '<p class="ok">[ OK ] Download successful'
		sudo cp /tmp/jivelite.tcz /mnt/mmcblk0p2/tce/optional/jivelite.tcz
		sudo chown tc:staff /mnt/mmcblk0p2/tce/optional/jivelite.tcz
		sudo cp /tmp/jivelite.tcz.md5.txt /mnt/mmcblk0p2/tce/optional/jivelite.tcz.md5.txt
		sudo chown tc:staff /mnt/mmcblk0p2/tce/optional/jivelite.tcz.md5.txt
	fi
}

pcp_install_jivelite() {
	#tce-load -i jivelite.tcz
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is added to onboot.lst</p>'
	sudo sed -i '/jivelite.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo echo 'jivelite.tcz' >> /mnt/mmcblk0p2/tce/onboot.lst

	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is added to .xfiletool.lst</p>'
	sudo sed -i '/^opt\/jivelite/d' /opt/.xfiletool.lst
	sudo echo 'opt/jivelite' >> /opt/.xfiletool.lst
}

pcp_delete_jivelite() {
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Removing Jivelite from piCorePlayer...</p>'
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
	if [ -e /tmp/jivelite.tcz ]; then
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Removing previous downloads from tmp directory...</p>'
		sudo rm -f /tmp/jivelite.tcz
		sudo rm -f /tmp/jivelite.tcz.md5.txt
	fi
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
case $JIVELITE in
	YES)
		pcp_load_jivelite
		pcp_install_jivelite
		pcp_remove_temp
		;;
	NO)
		pcp_delete_jivelite
		pcp_remove_temp
		;;
	*)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] JIVELITE: '$JIVELITE'<br />'
		;;
esac

[ $DEBUG = 1 ] && pcp_show_config_cfg

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] A reboot is needed in order to finalize...</p>'
pcp_reboot_button
pcp_go_back_button

echo '</body>'
echo '</html>'