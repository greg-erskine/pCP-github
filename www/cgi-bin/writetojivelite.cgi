#!/bin/sh

# Version: 0.01 2015-15-03 SBP
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to Jivelite Tweak" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

pcp_squeezelite_stop

#----------Jivelite download and adding -v to squeezelite string-----------------
#-----decode string via httpd and save to config----- 
JIVELITE=`sudo $HTPPD -d $JIVELITE`
sudo sed -i "s/\(JIVELITE *=*\).*/\1$JIVELITE/" $CONFIGCFG
. $CONFIGCFG

	if [ $JIVELITE = YES ]; then
		VISUALISER="yes"
	fi
pcp_save_to_config

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] JIVELITE: '$JIVELITE'</p>'

if [ $JIVELITE = YES ]; then
		sudo tce-load -i wget.tcz     # needed to load wget in order to download from https
			echo '<h1>[ INFO ] Downloading Jivelite from Github</h1>'
			downloadtcz="https://github.com/ralph-irving/tcz-jivelite/raw/master/jivelite.tcz"
			downloadmd5="https://github.com/ralph-irving/tcz-jivelite/raw/master/jivelite.tcz.md5.txt"
			# Remove old version of Jivelite from /tmp
		if [ -e /tmp/jivelite.tcz ]; then
			[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Removing previous downloaded versions from tmp directory...</p>'
			sudo rm -f /tmp/jivelite.tcz
			sudo rm -f /tmp/jivelite.tcz.md5.txt
		fi

	#----Download Jivelite
	wget -P /tmp $downloadmd5
	wget -P /tmp $downloadtcz
	result=$?
	if [ $result -ne "0" ]; then
		echo '<p class="error">[ ERROR ] Download unsuccessful, try again later!'
		else
		echo '<p class="ok">[ OK ] Download successful'
		sudo cp /tmp/jivelite.tcz /mnt/mmcblk0p2/tce/optional/jivelite.tcz
		sudo chmod u+x /mnt/mmcblk0p2/tce/optional/jivelite.tcz

		sudo cp /tmp/jivelite.tcz.md5.txt /mnt/mmcblk0p2/tce/optional/jivelite.tcz.md5.txt
		sudo chmod u+x /mnt/mmcblk0p2/tce/optional/jivelite.tcz.md5.txt
	fi

else
#----that is if Jivelite is "NO"
	echo '<h1>[ INFO ] Removing Jivelite from piCorePlayer</h1>'
	sudo rm -f /mnt/mmcblk0p2/tce/optional/jivelite.tcz
	sudo rm -f /mnt/mmcblk0p2/tce/optional/jivelite.tcz.md5.txt
	sudo rm -rf /home/tc/.jivelite
	sudo rm -rf /opt/jivelite	
fi


if [ $JIVELITE = YES ]; then
	if grep -Fxq "jivelite.tcz" /mnt/mmcblk0p2/tce/onboot.lst
	then
		echo "Jivelite already present in onboot.lst"
	else
		echo "Jivelite is added to onboot.lst"
		sudo sed -i '/jivelite.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
		sudo echo 'jivelite.tcz' >> /mnt/mmcblk0p2/tce/onboot.lst

	fi
else
		echo "Jivelite is removed from onboot.lst"
		sudo sed -i '/jivelite.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
fi

if [ $JIVELITE = YES ]; then
	echo "Jivelite is added to xfiletool.lst"
		sudo sed -i '/^opt\/jivelite/d' /opt/.xfiletool.lst
		sudo echo 'opt/jivelite' >> /opt/.xfiletool.lst
	else
	echo "Jivelite is removed from xfiletool.lst"
 		sudo sed -i '/^opt\/jivelite/d' /opt/.xfiletool.lst
fi

#-------------Cleanup---------------------------
	sudo rm -f /tmp/jivelite.tcz
	sudo rm -f /tmp/jivelite.tcz.md5.txt
#------------END Jivelite------------------------

pcp_squeezelite_start

pcp_backup
[ $DEBUG = 1 ] && pcp_show_config_cfg

pcp_reboot_button
pcp_go_back_button

echo '</body>'
echo '</html>'