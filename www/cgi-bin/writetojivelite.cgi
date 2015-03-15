#!/bin/sh

# Version: 0.03 2015-01-28 GE
#	Included changefiq.sh.

# Version: 0.02 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014-08-06 SBP
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to Jivelite Tweak" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#----------Jivelite download-----------------
# Decode $JIVELITE using httpd, add quotes
JIVELITE=`sudo /usr/local/sbin/httpd -d \"$JIVELITE\"`
sudo sed -i "s/\(JIVELITE *=*\).*/\1$JIVELITE/" $CONFIGCFG


[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] JIVELITE: '$JIVELITE'</p>'

if [ $JIVELITE == "\"YES\"" ]; then
echo '<h1>[ INFO ] Downloading Jivelite from Github</h1>'

downloadtcz="https://github.com/ralph-irving/tcz-jivelite/raw/master/jivelite.tcz"
downloadmd5="https://github.com/ralph-irving/tcz-jivelite/raw/master/jivelite.tcz.md5.txt"

# Remove Jivelite from /tmp
if [ -e /tmp/jivelite.tcz ]; then
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Removing previous downloaded versions from tmp directory...</p>'
	sudo rm -f /tmp/jivelite.tcz
	sudo rm -f /tmp/jivelite.tcz.md5.txt
fi

#Download Jivelite
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
#that is if Jivelite is "NO"
echo '<h1>[ INFO ] Removing Jivelite from piCorePlayer</h1>'
	sudo rm -f /mnt/mmcblk0p2/tce/optional/jivelite.tcz
	sudo rm -f /mnt/mmcblk0p2/tce/optional/jivelite.tcz.md5.txt
fi


if [ $JIVELITE == "\"YES\"" ]; then
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

if [ $JIVELITE == "\"YES\"" ]; then
	echo "Jivelite is added to xfiletool.lst"
		sed -i '/^opt\/jivelite\/bin\/jivelite-sp/d' /opt/.xfiletool.lst
		sudo echo 'opt/jivelite/bin/jivelite-sp' >> /opt/.xfiletool.lst
	else
	echo "Jivelite is removed from xfiletool.lst"
 		sed -i '/^opt\/jivelite\/bin\/jivelite-sp/d' /opt/.xfiletool.lst
fi

#------------END Jivelite------------------------

pcp_backup
[ $DEBUG = 1 ] && pcp_show_config_cfg
pcp_go_back_button

echo '</body>'
echo '</html>'