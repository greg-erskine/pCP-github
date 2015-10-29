#!/bin/sh

# Version: 0.03 2015-29-08 SBP
#   Changed to touch-screen version.

# Version: 0.02 2015-05-08 GE
#   Revised.

# Version: 0.01 2015-03-15 SBP
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to Jivelite Tweak" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

sudo sed -i "s/\(JIVELITE *=*\).*/\1$JIVELITE/" $CONFIGCFG
[ $JIVELITE = YES ] && VISUALISER="yes"
pcp_save_to_config

jivelite_tcz="jivelite_touch.tcz"
jivelite_md5="jivelite_touch.tcz.md5.txt"

downloadtcz="http://ralph_irving.users.sourceforge.net/pico/$jivelite_tcz"
downloadmd5="http://ralph_irving.users.sourceforge.net/pico/$jivelite_md5"



#########################################################################################
# Steen, this md5 file is WRONG. It has no use in its current form. Also, this script
# currently doesn't even try to use the the md5 file. The standard Tinycore md5 check
# routines will also fail. Ralphy needs to fix it!
#
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
	echo '<p class="debug">[ DEBUG ] JIVELITE: '$JIVELITE'<br />'
	echo '                 [ DEBUG ] VISUALISER: '$VISUALISER'</p>'
fi

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_load_jivelite() {
	echo '<p class="info">[ INFO ] Downloading Jivelite from Ralphy'\''s repository...</p>'
	wget -P /tmp $downloadmd5
	wget -P /tmp $downloadtcz
	# The next few lines need to be changed to check md5 when it is FIXED.
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
	#tce-load -i jivelite.tcz
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is added to onboot.lst</p>'
	sudo sed -i '/jivelite.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo echo 'jivelite.tcz' >> /mnt/mmcblk0p2/tce/onboot.lst

	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is added to .xfiletool.lst</p>'
	sudo sed -i '/^opt\/jivelite/d' /opt/.xfiletool.lst
	sudo echo 'opt/jivelite' >> /opt/.xfiletool.lst
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
	if [ -e /tmp/jivelite.tcz ]; then
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Removing previous downloads from tmp directory.</p>'
		sudo rm -f /tmp/$jivelite_tcz
		sudo rm -f /tmp/$jivelite_md5
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

pcp_backup
[ $DEBUG = 1 ] && pcp_show_config_cfg

echo '<p class="info">[ INFO ] A reboot is needed in order to finalize!</p>'
pcp_reboot_button
pcp_go_back_button

echo '</body>'
echo '</html>'