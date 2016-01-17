#!/bin/sh

# version: 0.01 2016-01-16 GE
#	Original - Combined upd_picoreplayer.cgi, insitu.cgi and do_updatepicoreplayer.cgi

. pcp-functions
pcp_variables

pcp_html_head "Update pCP" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

DEBUG=1 ################

WGET="/bin/busybox wget"

# As all the insitu upgrade is done in one file, it may be better to define this here
UPD_PCP=/tmp/upd_picoreplayer
INSITU_DOWNLOAD="http://sourceforge.net/projects/picoreplayer/files/insitu"

#========================================================================================
# DEBUG info
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	echo '<p class="debug">[ DEBUG ] QUERY_STRING: '$QUERY_STRING'<br />'
	echo '                 [ DEBUG ] ACTION: '$ACTION'<br />'
	echo '                 [ DEBUG ] VERSION: '$VERSION'<br />'
	echo '                 [ DEBUG ] UPD_PCP: '$UPD_PCP'<br />'
	echo '                 [ DEBUG ] INSITU_DOWNLOAD: '$INSITU_DOWNLOAD'</p>'
}

#========================================================================================
# Prepare download directories
#----------------------------------------------------------------------------------------
pcp_create_upd_directory() {
	sudo rm -rf $UPD_PCP
	sudo mkdir -m 755 $UPD_PCP
	sudo mkdir $UPD_PCP/boot
	sudo mkdir $UPD_PCP/tce
}

#========================================================================================
# Download a list of available piCorePlayer versions from Sourceforge
#----------------------------------------------------------------------------------------
pcp_get_insitu_cfg() {
	echo '[ INFO ] STEP 1. Downloading insitu.cfg...'
	$WGET -P $UPD_PCP $INSITU_DOWNLOAD/insitu.cfg
	if [ $? = 0 ]; then
		echo '[ OK ] Success downloading insitu.cfg'
	else
		echo '[ ERROR ] Error downloading insitu.cfg'
	fi
}

#========================================================================================
# Main routine
#----------------------------------------------------------------------------------------
case $ACTION in
	initial)
		STEP="Step 1 - Downloading available version"
		pcp_create_upd_directory
#		pcp_get_insitu_cfg
		;;
	download)
		STEP="Step 2 - Downloading files"
		echo
		;;
	install)
		STEP="Step 3 - Installing files"
		echo
		;;
	*)
		echo '<p class="error">[ ERROR ] Invalid ACTION: "'$ACTION'"</p>'
		;;
esac

#========================================================================================
# 
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>'$STEP'</legend>'
echo '          <table class="bggrey percent100">'

pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <p>[ INFO ] You are currently using piCorePlayer'$(pcp_picoreplayer_version)'</p>'
[ $ACTION = "download" ] &&
echo '                  <p>[ INFO ] You are loading piCorePlayer'$VERSION'</p>'
echo '                </td>'
echo '              </tr>'

if [ $ACTION = "initial" ]; then
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	                    if [ $(pcp_internet_accessible) = 0 ]; then
	                      IMAGE="green.png"
	                      STATUS="Internet accessible..."
	                    else
	                      IMAGE="red.png"
	                      STATUS="Internet not accessible!!"
	                    fi
	echo '              <td class="small3">'
	echo '                <p class="centre"><img src="../images/'$IMAGE'" alt="'$STATUS'"></p>'
	echo '              </td>'
	echo '              <td class="column300">'
	echo '                <p>'$STATUS'</p>'
	echo '              </td>'
	                    if [ $(pcp_sourceforge_accessible) = 0 ]; then
	                      IMAGE="green.png"
	                      STATUS="Sourceforge repository accessible..."
	                    else
	                      IMAGE="red.png"
	                      STATUS="Sourceforge repository not accessible!!"
	                    fi
	echo '              <td class="small3">'
	echo '                <p class="centre"><img src="../images/'$IMAGE'" alt="'$STATUS'"></p>'
	echo '              </td>'
	echo '              <td class="column300">'
	echo '                <p>'$STATUS'</p>'
	echo '              </td>'
	echo '            </tr>'

	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <textarea class="inform" style="height:80px">'
	                          pcp_get_insitu_cfg
	echo '                  </textarea>'
	echo '                </td>'
	echo '              </tr>'
fi

if [ $DEBUG = 1 ]; then
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_debug_info
	echo '                </td>'
	echo '              </tr>'
fi

echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# 
#----------------------------------------------------------------------------------------
if [ $ACTION = "initial" ]; then
	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>piCorePlayer insitu upgrade</legend>'
	echo '          <table class="bggrey percent100">'

	echo '            <form name="insitu" action= "'$0'" method="get">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18">'
	echo '                  <select name="VERSION">'
	                          awk '{ print "<option value=\""$1"\">" $1"</option>" }' $UPD_PCP/insitu.cfg
	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Choose version of piCorePlayer from Drop-Down list you require.</p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="large18 center">'
	echo '                  <input class="large12" type="submit" value="Update piCorePlayer">'
	echo '                  <input type="hidden" name="ACTION" value="download">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Update may take a few minutes... please be patient. When the download has finished a new page will load.</p>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'

	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

pcp_footer
pcp_copyright
pcp_go_main_button

echo '</body>'
echo '</html>'

exit

############################################################

# Download the boot files and the tce files and Break if errors in downloading boot files
echo '<p class="info">[ INFO ] Downloading '$INSITU'_boot.tar.gz...Please wait</p>'
$WGET -P "$UPD_PCP"/boot "$INSITU_DOWNLOAD"/"$INSITU"/"$INSITU"_boot.tar.gz

result_boot=$?
if [ $result_boot = 0 ]; then
	echo '<p class="ok">[ OK ] Success downloading boot files</p>'
else
	echo '<p class="error">[ ERROR: '$result_boot' ] Error downloading boot files</p>'
	pcp_go_main_button
fi

if [ $result_boot = 0 ]; then
	# Break if error in downloading tce files
	echo '<p class="info">[ INFO ] Downloading '$INSITU'_tce.tar.gz...Please wait.</p>'
	sudo wget -P "$UPD_PCP"/tce "$INSITU_DOWNLOAD"/"$INSITU"/"$INSITU"_tce.tar.gz 

	result_tce=$? 
	if [ $result_tce = 0 ]; then
		echo '<p class="ok">[ OK ] Success downloading tce files</p>'
		echo '<form name="do_update" action= "do_updatepicoreplayer.cgi" method="get">'
		echo '<p><input class="large12" type="submit" value="Update piCorePlayer" />&nbsp;&nbsp;When you press the button, you will make the actual update with the downloaded files.</p></form>'
	else
		echo '<p class="error">[ ERROR: '$result_tce' ] Error downloading tce files.</p>'
	fi
fi

############################################################


#=========================================================================================
# Check for sufficient free space to untar to partition mmcblk0p2
#-----------------------------------------------------------------------------------------
FREE_SPACE=$(df | grep mmcblk0p2 | awk '{ print ($2-$3) }')
TAR_FILE_SIZE=$(ls -s "$UPD_PCP"/tce/"$INSITU"_tce.tar.gz | awk '{ print $1 }')
CONTINUE=`expr $FREE_SPACE - $TAR_FILE_SIZE`

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] free space on mmcblk0p2: '$FREE_SPACE'<br />'
	echo '                 [ DEBUG ] file size              : '$TAR_FILE_SIZE'<br />'
	echo '                 [ DEBUG ] Continue               : '$CONTINUE'</p>'

	if [ $CONTINUE -lt 0 ]; then
		echo '<p class="error">[ ERROR ] Not enough free space on mmcblk0p2</p>'
		pcp_go_main_button
		echo '</body>'
		echo '</html>'
		exit
	fi
	echo '<p>Continue</p>'
fi
#-----------------------------------------------------------------------------------------

pcp_mount_mmcblk0p1

# Delete all files from the boot partition
sudo rm -rf /mnt/mmcblk0p1/* 

#=========================================================================================
# Copy ALSA settings so they are avaiable after an update
#-----------------------------------------------------------------------------------------
if [ ALSAlevelout="Custom" ]; then
sudo cp /etc/asound.conf /mnt/mmcblk0p1/
sudo cp /var/lib/alsa/asound.state /mnt/mmcblk0p1/
fi
#-----------------------------------------------------------------------------------------


# Copy the config file to boot partition
sudo cp -f /usr/local/sbin/config.cfg /mnt/mmcblk0p1/newconfig.cfg 
sudo dos2unix -u /mnt/mmcblk0p1/newconfig.cfg
echo '<p class="info">[ INFO ] Your config has been saved so your current settings will used be after updating piCorePlayer.</p>'

# Untar and overwrite the boot files
echo '<p class="info">[ INFO ] Untarring '$INSITU'_boot.tar.gz...</p>'
echo '<textarea name="TextBox" cols="120" rows="8">'
sudo tar -zxvf $UPD_PCP/boot/"$INSITU"_boot.tar.gz -C /
result_boot=$?
echo '</textarea>'

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] boot tar result: '$result_boot'</p>'

pcp_umount_mmcblk0p1

if [ $result_boot = 0 ]; then
	# Delete all the kernel specific files in the optional directory - so no stray files are left
	sudo rm -rf /mnt/mmcblk0p2/tce/optional/*piCore*.*

	# Untar and overwrite the tce files
	echo '<p class="info">[ INFO ] Untarring '$INSITU'_tce.tar.gz...</p>'
	echo '<textarea name="TextBox" cols="120" rows="8">'
	sudo tar -zxvf $UPD_PCP/tce/"$INSITU"_tce.tar.gz -C /
	result_tce=$?
	echo '</textarea>'

	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] tce tar result: '$result_tce'</p>'

	if [ $result_tce = 0 ]; then
		echo '<h2>[ INFO ] piCorePlayer has been updated, please reboot now. And then you should have: '$INSITU'</h2>'
		pcp_reboot_button
	else
		echo '<p class="error">[ ERROR ] piCorePlayer has NOT been updated.</p>'
	fi
else
	echo '<p class="error">[ ERROR ] piCorePlayer has NOT been updated.</p>'
fi

# Add eventual missing packages to onboot.lst. It is important if different versions of piCorePlayer have different needs.
fgrep -vxf /mnt/mmcblk0p2/tce/onboot.lst /mnt/mmcblk0p2/tce/piCorePlayer.dep >> /mnt/mmcblk0p2/tce/onboot.lst

#Remove wifi firmware from onboot.lst if wifi is off so that pCP will boot faster
if [ $WIFI = off ]; then
sleep 1
	sudo sed -i '/firmware-ralinkwifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/firmware-rtlwifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/firmware-atheros.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/wireless/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo sed -i '/wifi.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
fi


pcp_go_main_button

echo '</body>'
echo '</html>'

