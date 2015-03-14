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


# Next we need to make a script that will do the following:
#  1. add/remove jivelite.tcz from /mnt/mmcblk0p2/tce/onboot.lst depending on JIVELITE=YES or NO in config.cfg
#  2. add/remove /opt/jivelite/bin/jivelite-sp from "user command" depending on JIVELITE=YES or NO in config.cfg  
#  3. add/remove opt/jivelite/bin/jivelite-sp to /opt/.xfiletool.lst depending on JIVELITE=YES or NO in config.cfg
#




pcp_backup
[ $DEBUG = 1 ] && pcp_show_config_cfg
pcp_go_back_button

echo '</body>'
echo '</html>'