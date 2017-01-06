#!/bin/sh

# Version: 3.10 2017-01-06
#	Updated [Save to USB] more> help. GE.
#	Changed indicators to use pcp_green_tick, pcp_red_cross. GE.
#	Changes for Squeezelite extension. PH.

# Version: 3.00 2016-07-08
#	Moved Resize FS and Extensions to MODE_ADVANCED. GE.

# Version: 2.06 2016-05-22
#	Fixed a few typos. GE.

# Version: 2.05 2016-04-30
#	Added double quotes when comparing strings. GE.
#	Added pcp_main_update_config. GE.
#	Moved to developer mode: pcp_main_copy2fs, pcp_main_dosfsck, pcp_main_reset_all, pcp_main_restore_all. GE.
#   Changes to insitu_update section. GE.

# Version: 0.22 2016-03-10 GE
#	Added squeezelite version to more> help.
#	Added LMS indicator.

# Version: 0.21 2016-02-26 GE
#	Renamed Squeezelite [Save] button to [Install].
#	Added "Build options" to update squeezelite.
#	Changed indicators to tick and cross.

# Version: 0.20 2016-02-03 GE
#	Changed Insitu update.

# Version: 0.19 2016-01-15 GE
#	Updated "Update pCP" help text.

# Version: 0.18 2016-01-07 GE
#	Added check for version of Ralphy's squeezelite.
#	Added Shairport indicator and restart option.

# Version: 0.17 2015-12-09 SBP
#	Removed Update Triode's version of Squeezelite.
#	Updated download and update Ralphy's version of Squeezelite.

# Version: 0.16 2015-09-20 GE
#	Added fieldsets around Advanced, Beta and Developer modes.
#	Fixed pcp_main_reset_all routine.

# Version: 0.15 2015-08-29 GE
#	Revised modes.
#	Turned pcp_picoreplayers tabs on in normal mode.
#	Changed reboot, shutdown and backup messages.
#	Added warning message on reset all.

# Version: 0.14 2015-07-01 GE
#	Added pcp_mode tabs.
#	Added pcp_picoreplayers tabs.
#	Removed some unnecessary code.

# Version: 0.13 2015-05-11 GE
#	Now uses pcp_start_row_shade, pcp_start_row_shade and pcp_incr_id
#	Added Extensions, Extras, Debug and Diagnostics buttons.
#	Added Static IP to Main piCorePlayer operations.

# Version: 0.12 2015-02-20 GE
#	Moved Disable GUI, Stop Squeezelite, Backup and Shutdown to Developers operations.
#	Added Reset ALL and Restore ALL to Developers operations.

# Version: 0.11 2015-01-26 SBP
#	Added Disable GUI.

# Version: 0.10 2014-12-20 GE
#	Modified Squeezelite running indicator.

# Version: 0.09 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.08 2014-12-08 SBP
#	Revised button order.
#	Added Squeezelite running indicator.
#	Reformatted.

# Version: 0.07 2014-10-22 GE
#	Using pcp_html_head now.

# Version: 0.06 2014-10-09 GE
#	Revised uptime delay to use seconds.

# Version: 0.05 2014-10-08 GE
#	Size of input buttons controlled through input[type=submit] style.

# Version: 0.04 2014-10-02 GE
#	Added uptime delay before pcp_squeezelite_status is checked.

# Version: 0.03 2014-09-20 GE
#	Modified HTML to improve cross browser support.

# Version: 0.02 2014-08-22 GE
#	Added check for pcp_squeezelite_status.

# Version: 0.01 2014-06-25 GE
#	Original.

. pcp-lms-functions
. pcp-functions
pcp_variables

pcp_html_head "Main Page" "SBP"

[ $MODE -ge $MODE_NORMAL ] && pcp_picoreplayers
[ $MODE -ge $MODE_ADVANCED ] && pcp_controls
pcp_banner
pcp_navigation

#========================================================================================
# Padding
#----------------------------------------------------------------------------------------
pcp_main_padding() {
	pcp_toggle_row_shade
	echo '            <tr class="padding '$ROWSHADE'">'
	echo '              <td></td>'
	echo '              <td></td>'
	echo '            </tr>'
}

#========================================================================================
# Main piCorePlayer operations
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Main piCorePlayer operations</legend>'
echo '          <table class="bggrey percent100">'

#------------------------------------Squeezelite/Shairport Indication--------------------
pcp_main_squeezelite_indication() {

	if [ $(pcp_squeezelite_status) -eq 0 ]; then
		pcp_green_tick "running"
	else
		pcp_red_cross "not running"
	fi

	pcp_start_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 centre">'
	echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
	echo '              </td>'
	echo '              <td>'
	if [ "$SQUEEZELITE" = "no" ]; then
		echo '                <p>Squeezelite is disabled on Tweaks page&nbsp;&nbsp;'
	else
		echo '                <p>Squeezelite is '$STATUS'&nbsp;&nbsp;'
	fi
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <ul>'
	echo '                    <li><span class="indicator_green">&#x2714;</span> = Squeezelite running.</li>'
	echo '                    <li><span class="indicator_red">&#x2718;</span> = Squeezelite not running.</li>'
	echo '                  </ul>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Squeezelite must be running for music to play.</li>'
	echo '                    <li>Squeezelite must be running for connection to LMS.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
pcp_main_squeezelite_indication && pcp_main_padding

#------------------------------------LMS Indication--------------------------------------
pcp_main_lms_indication() {

	if [ $(pcp_lms_status) -eq 0 ]; then
		pcp_green_tick "running"
	else
		pcp_red_cross "not running"
	fi

	pcp_start_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 centre">'
	echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>LMS is '$STATUS'&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <ul>'
	echo '                    <li><span class="indicator_green">&#x2714;</span> = LMS running.</li>'
	echo '                    <li><span class="indicator_red">&#x2718;</span> = LMS not running.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ "$LMSERVER" = "yes" ] && pcp_main_lms_indication && pcp_main_padding
#----------------------------------------------------------------------------------------

#------------------------------------Shairport Indication--------------------------------
pcp_main_shairport_indication() {

	if [ $(pcp_shairport_status) -eq 0 ]; then
		pcp_green_tick "running"
	else
		pcp_red_cross "not running"
	fi

	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 centre">'
	echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Shairport is '$STATUS'&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <ul>'
	echo '                    <li><span class="indicator_green">&#x2714;</span> = Shairport running.</li>'
	echo '                    <li><span class="indicator_red">&#x2718;</span> = Shairport not running.</li>'
	echo '                  </ul>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Shairport must be running for music to play from iDevices.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ "$SHAIRPORT" = "yes" ] && pcp_main_shairport_indication && pcp_main_padding
#----------------------------------------------------------------------------------------

#-------------------------------Restart - Squeezelite / Shairpoint-----------------------
pcp_main_restart_squeezelite() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Restart" action="restartsqlt.cgi" method="get">'
	echo '                  <input type="submit" value="Restart" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Restart Squeezelite with new settings&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will kill the Squeezelite process then restart it.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>A restart of Squeezelite is required after you change any of the Squeezelite settings.</li>'
	echo '                    <li>Squeezelite running indicator will turn to a green tick.</li>'
	echo '                    <li>Squeezelite in the footer will turn green.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}

pcp_main_restart_shairport() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Restart" action="restartsqlt.cgi" method="get">'
	echo '                  <input type="submit" value="Restart" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Restart Squeezelite and Shairport with new settings&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will kill the Squeezelite and Shairport processes then restart them.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>A restart of Squeezelite and Shairport is required after you change any of the Squeezelite settings.</li>'
	echo '                    <li>Squeezelite and Shairport running indicators will turn to a green tick.</li>'
	echo '                    <li>Squeezelite in the footer will turn green.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ "$SHAIRPORT" = "yes" ] && pcp_main_restart_shairport || pcp_main_restart_squeezelite
#----------------------------------------------------------------------------------------

#------------------------------------------Padding---------------------------------------
[ $MODE -le $MODE_BASIC ] && pcp_main_padding
#----------------------------------------------------------------------------------------

#------------------------------------------Update Squeezelite - Ralphy-------------------
pcp_main_update_sqlt() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <form name="updateRalphys" action="updatesqlt.cgi" method="get">'
	echo '                <td class="column150 center">'
	echo '                  <button type="submit" name="ACTION" value="update">Update</button>'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <button type="submit" name="ACTION" value="full_update">Full Update</button>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Update Squeezelite Extensions&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This will update the pCP Squeezelite extension from the pCP repository.</p>'
	echo '                    <p><b>Note:</b></p>'
	echo '                    <ul>'
	echo '                      <li>Update will attempt to update the squeezelite package in place.</li>'
	echo '                      <li>Full Update will update squeezelite and all libraries, requiring a reboot.</li>'
	echo '                      <li>Internet access is required.</li>'
	echo '                      <li>The basic version is 1.3MB which plays PCM, (WAV/AIFF), FLAC, MP3, OGG and AAC.</li>'
	echo '                      <li>If the FFMpeg library is added, can additionally play ALAC and WMA.</li>'
	echo '                      <li>Triode is the original author of Squeezelite.</li>'
	echo '                      <li>Ralphy provides Squeezelite binaries with additional features enabled.</li>'
	echo '                      <li>For more information on Squeezelite - see <a href="https://code.google.com/p/squeezelite/" target="_blank">Squeezelite Google code</a>.</li>'
	echo '                    </ul>'
	echo '                    <p><b>Version:</b> '$(pcp_squeezelite_version)'</p>'
	echo '                    <p><b>Build options:</b></p>'
	echo '                    <p>'$(sudo ${SQLT_BIN} -? | grep "Build options" | awk -F": " '{print $2}')'</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </form>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_main_update_sqlt
#----------------------------------------------------------------------------------------

#------------------------------------------Install/Remove FFMPEG-------------------------
pcp_main_ffmpeg() {

	if [ ! -f /mnt/mmcblk0p2/tce/optional/pcp-libffmpeg.tcz ]; then
		VERSIONsmall="selected"
	else
		VERSIONlarge="selected"
	fi

	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <form name="updateFFMpeg" action="updatesqlt.cgi" method="get">'
	if [ "${VERSIONsmall}" = "selected" ]; then
		echo '                <td class="column150 center">'
		echo '                  <button type="submit" name="ACTION" value="inst_ffmpeg">Install</button>'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Install FFMpeg libraries for Squeezelite&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will download and install FFMpeg Libraries from the pCP repository.</p>'
		echo '                    <p><b>Note:</b></p>'
		echo '                    <ul>'
		echo '                      <li>Internet access is required.</li>'
		echo '                      <li>The 7MB FFMpeg library adds playback of ALAC and WMA.</li>'
		echo '                    </ul>'
		echo '                  </div>'
		echo '                </td>'
	else
		echo '                <td class="column150 center">'
		echo '                  <button type="submit" name="ACTION" value="rem_ffmpeg">Remove</button>'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Remove FFMpeg libraries for Squeezelite&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This will remove the FFMpeg Libraries from the system.</p>'
		echo '                  </div>'
		echo '                </td>'
	fi
	echo '              </form>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_main_ffmpeg
#----------------------------------------------------------------------------------------

#------------------------------------------Reboot----------------------------------------
pcp_main_reboot() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Reboot" action="javascript:pcp_confirm('\''Reboot '$NAME'?'\'','\''reboot.cgi'\'')" method="get">'
	echo '                  <input type="submit" value="Reboot" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Reboot piCorePlayer after enabling or disabling HDMI output&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will reboot piCorePlayer.</p>'
	echo '                  <p><b>Note: </b>This will do the following:</p>'
	echo '                  <ul>'
	echo '                    <li>Shutdown piCorePlayer gracefully.</li>'
	echo '                    <li>Boot piCorePlayer using the latest settings.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
pcp_main_reboot
#----------------------------------------------------------------------------------------

#------------------------------------------Update pCP------------------------------------
pcp_main_update_pcp() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="InSitu" action="insitu_update_stage1.cgi" method="get">'
	echo '                  <input type="submit" value="Update pCP" />'
	echo '                  <input type="hidden" name="ACTION" value="initial" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Update piCorePlayer without removing the SD card&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This can be used when the SD card slot is not accessible.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Internet access is required.</li>'
	echo '                    <li>The current version of piCorePlayer will be completely overwritten.</li>'
	echo '                    <li>Additional extensions (ie. Jivelite, Shairport) may need to be reloaded.</li>'
	echo '                    <li>When the update has completed:</li>'
	echo '                    <ol>'
	echo '                      <li>Select [Squeezelite Settings].</li>'
	echo '                      <li>Confirm your "Audio output" settings.</li>'
	echo '                      <li>Click [Save] and [Reboot].</li>'
	echo '                    </ol>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_main_update_pcp
#----------------------------------------------------------------------------------------

#------------------------------------------Save to USB-----------------------------------
pcp_main_save_usb() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Saveconfig" action="save2usb.cgi" method="get">'
	echo '                  <input type="submit" value="Save to USB" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Save your current configuration to the USB flash drive&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will copy the current configuration file to the attached USB flash drive/device.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>If you then reboot with this USB device attached, this configuration file will be uploaded and used.</li>'
	echo '                    <li>This is handy if you update your piCorePlayer or want to setup another piCorePlayer with similar settings.</li>'
	echo '                    <li>This configuration file is named newconfig.cfg and will be automatially renamed to usedconfig.cfg after rebooting.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_main_save_usb
#----------------------------------------------------------------------------------------

#------------------------------------------Advanced mode fieldset------------------------
if [ $MODE -ge $MODE_ADVANCED ]; then
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Advanced mode operations</legend>'
	echo '          <table class="bggrey percent100">'
fi
#----------------------------------------------------------------------------------------

#------------------------------------------Stop------------------------------------------
pcp_main_stop() {
	pcp_start_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Stop" action="stop.cgi" method="get">'
	echo '                  <input type="submit" value="Stop" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Stop Squeezelite&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will kill the Squeezelite process.</p>'
	echo '                  <p>Click [Restart] to start Squeezelite again.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Squeezelite running indicator will turn to a red cross.</li>'
	echo '                    <li>Squeezelite in the footer will turn red.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_main_stop
#----------------------------------------------------------------------------------------

#------------------------------------------Backup----------------------------------------
pcp_main_backup() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="backup" action="javascript:pcp_confirm('\''Do a backup on '$NAME'?'\'','\''backup.cgi'\'')" method="get">'
	echo '                  <input type="submit" value="Backup" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Backup your changes&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will do a piCore backup to your SD card.</p>'
	echo '                  <p>piCorePlayer does a backup after it changes any setting, so this option is really just for "peace of mind"'
	echo '                     before doing a shutdown or reboot.</p>'
	echo '                  <p><b>Note: </b>This will backup the following:</p>'
	echo '                  <ul>'
	echo '                    <li>Your configuration file.</li>'
	echo '                    <li>Your home directory.</li>'
	echo '                    <li>Files and directories defined in /opt/.filetool.lst</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_main_backup
#----------------------------------------------------------------------------------------

#------------------------------------------Shutdown--------------------------------------
pcp_main_shutdown() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Shutdown" action="javascript:pcp_confirm('\''Shutdown '$NAME'?'\'','\''shutdown.cgi'\'')" method="get">'
	echo '                  <input type="submit" value="Shutdown" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Shutdown piCorePlayer&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will shutdown piCorePlayer gracefully.</p>'
	echo '                  <p>To restart piCorePlayer you will need to remove then reapply the power.</p>'
	echo '                  <p><b>Note: </b>This option is not really required - piCorePlayer can be turned off at the switch.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_main_shutdown
#----------------------------------------------------------------------------------------

#------------------------------------------Resize FS-------------------------------------
pcp_main_resize_fs() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Resize FS" action="xtras_resize.cgi" method="get">'
	echo '                  <input type="submit" value="Resize FS" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Resize file system&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This command will resize the file system to fit the SD card.</p>'
	echo '                  <p>Only required if you need to add extra extensions.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_main_resize_fs
#----------------------------------------------------------------------------------------

#------------------------------------------Extensions------------------------------------
pcp_main_extensions() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Stop" action="xtras_extensions.cgi" method="get">'
	echo '                  <input type="submit" value="Extensions" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Search, load or delete piCore extensions&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This page gives you the option to search, load or delete piCore extensions.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_main_extensions
#----------------------------------------------------------------------------------------

#------------------------------------------Beta mode fieldset----------------------------
if [ $MODE -ge $MODE_BETA ]; then
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Beta mode operations</legend>'
	echo '          <table class="bggrey percent100">'
fi
#----------------------------------------------------------------------------------------

#------------------------------------------Static IP-------------------------------------
pcp_main_static_ip(){
	pcp_start_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Static IP" action="xtras_staticip.cgi" method="get">'
	echo '                  <input type="submit" value="Static IP" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Static IP for wired networks&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This option allows you to set a static IP for wired networks (eth0).</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_static_ip
#----------------------------------------------------------------------------------------

#------------------------------------------Diagnostics-----------------------------------
pcp_main_diagnostics() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Diagnostics" action="diagnostics.cgi" method="get">'
	echo '                  <input type="submit" value="Diagnostics" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Go to Diagnostics page&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will go to the Diagnostics page.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_diagnostics
#----------------------------------------------------------------------------------------

#------------------------------------------Extras----------------------------------------
pcp_main_extras() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Extras" action="xtras.cgi" method="get">'
	echo '                  <input type="submit" value="Extras" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Go to Extras page&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will go to the Extras page.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_extras
#----------------------------------------------------------------------------------------

#------------------------------------------Developer mode fieldset-----------------------
if [ $MODE -ge $MODE_DEVELOPER ]; then
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Developer mode operations</legend>'
	echo '          <table class="bggrey percent100">'
fi
#----------------------------------------------------------------------------------------

#------------------------------------------Reset ALL-------------------------------------
pcp_main_reset_all() {
	pcp_start_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Reset ALL" action="javascript:pcp_confirm('\''WARNING:\nYou are about to RESET your configuration file.'\'','\''writetoconfig.cgi?SUBMIT=Reset'\'')" method="get">'
	echo '                  <input type="submit" name="SUBMIT" value="Reset ALL" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Reset all settings in configuration file&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This command will reset all settings in the configuration file to the defaults that'
	echo '                     are defined in pcp-functions. </p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_reset_all
#----------------------------------------------------------------------------------------

#------------------------------------------Restore ALL-----------------------------------
pcp_main_restore_all() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Restore ALL" action="writetoconfig.cgi" method="get">'
	echo '                  <input type="submit" name="SUBMIT" value="Restore ALL" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Restore all settings in configuration file&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This command will restore all settings in the configuration file to those found in'
	echo '                     newconfig.cfg on USB flash memory.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_restore_all
#----------------------------------------------------------------------------------------

#------------------------------------------Update config---------------------------------
pcp_main_update_config() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Update config" action="writetoconfig.cgi" method="get">'
	echo '                  <input type="submit" name="SUBMIT" value="Update config" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Update configuration file&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This command will update your configuration file.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_update_config
#----------------------------------------------------------------------------------------

#------------------------------------------Dosfsck---------------------------------------
pcp_main_dosfsck() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="DOS fsck" action="xtras_dosfsck.cgi" method="get">'
	echo '                  <input type="submit" value="DOS fsck" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>DOS file system check&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This option allows you to run dosfsck on the SD card.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_dosfsck
#----------------------------------------------------------------------------------------

#------------------------------------------Debug-----------------------------------------
pcp_main_debug() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="Debug" action="debug.cgi" method="get">'
	echo '                  <input type="submit" value="Debug" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Go to Debug page&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This will go to the Debug page.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_debug
#----------------------------------------------------------------------------------------

#------------------------------------------copy2fs---------------------------------------
pcp_main_copy2fs() {
	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150 center">'
	echo '                <form name="copy2fs" action="xtras_copy2fs.cgi" method="get">'
	echo '                  <input type="submit" value="copy2fs" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Set copy2fs flag&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  <p>This sets the copy2fs flag so extensions are loaded into ram.</p>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_copy2fs
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'