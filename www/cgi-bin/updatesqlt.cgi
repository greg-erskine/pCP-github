#!/bin/sh
. pcp-functions
pcp_variables

# Version: 0.04 2016-02-10 GE
#	Added SQLT_VERSION.
#	Added free space checks.

# Version: 0.03 2015-12-09 GE
#	Remove Triode's version.
#	Update Ralphy's version.

# Version: 0.02 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.01 2014-06-24 GE
#	Original.

pcp_html_head "Updating Squeezelite" "SBP" "15" "main.cgi"

. $CONFIGCFG
OLD_SQLT_VERSION=$SQLT_VERSION

pcp_banner
pcp_running_script
pcp_squeezelite_stop
pcp_httpd_query_string

#========================================================================================
# Check for free space
#----------------------------------------------------------------------------------------
pcp_enough_free_space() {
	REQUIRED_SPACE=$1
	FREE_SPACE=$(pcp_free_space k)
	if [ $FREE_SPACE -gt $REQUIRED_SPACE ]; then
		echo '<p class="ok">[  OK  ] Free space: '$FREE_SPACE'k - Required space: '$REQUIRED_SPACE'k</p>'
		return 0
	else
		echo '<p class="error">[ ERROR ] Free space: '$FREE_SPACE'k - Required space: '$REQUIRED_SPACE'k</p>'
		echo '<p class="error">[ ERROR ] Not enough free space - try expanding your partition.</p>'
		return 1
	fi
}
#----------------------------------------------------------------------------------------

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Version: '$VERSION'</p>'

case $VERSION in
	Small*)
		MESSAGE="Updating Squeezelite to Ralphy basic version..."
		DOWNLOAD="http://ralph_irving.users.sourceforge.net/pico/squeezelite-armv6hf-noffmpeg"
		SQLT_VERSION="basic"
		SPACE_REQUIRED=1100
		;;
	Large*)
		MESSAGE="Updating Squeezelite to Ralphy ffmpeg version (will take a few minutes)..."
		DOWNLOAD="http://ralph_irving.users.sourceforge.net/pico/squeezelite-armv6hf-ffmpeg"
		SQLT_VERSION="ffmpeg"
		SPACE_REQUIRED=13000
		;;
esac

echo '<p>[ INFO ] '${MESSAGE}'</p>'
echo '<p class="info">[ INFO ] Current Squeezelite '$OLD_SQLT_VERSION' version: '$(pcp_squeezelite_version)'</p>'

pcp_enough_free_space $SPACE_REQUIRED
[ $? = 0 ] || exit

# Remove Squeezelite from /tmp
if [ -e /tmp/squeezelite-armv6hf ]; then
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Removing /tmp/squeezelite-armv6hf...</p>'
	sudo rm -f /tmp/squeezelite-armv6hf*
fi

wget -O /tmp/squeezelite-armv6hf $DOWNLOAD
result=$?
if [ $result -ne "0" ]; then
	echo '<p class="error">[ ERROR ] Download unsuccessful, try again later!'
else
	echo '<p class="ok">[ OK ] Download successful'
	sudo mv /mnt/mmcblk0p2/tce/squeezelite-armv6hf /tmp/squeezelite-armv6hf~
	sudo cp /tmp/squeezelite-armv6hf /mnt/mmcblk0p2/tce
	sudo chmod u+x /mnt/mmcblk0p2/tce/squeezelite-armv6hf
fi

[ $DEBUG = 1 ] && (echo '<p class="ok">[ OK ] '; ls -al /mnt/mmcblk0p2/tce/squeezelite-armv6hf)

pcp_save_to_config
pcp_squeezelite_start

echo '<p class="ok">[ OK ] Upgraded Squeezelite '$SQLT_VERSION' version: '$(pcp_squeezelite_version)'</p>'

echo '</body>'
echo '</html>'