#!/bin/sh

# Version: 7.0.0 2020-05-11

. pcp-functions
. pcp-lms-functions

pcp_html_head "Main Page" "SBP"

pcp_controls
pcp_navbar
pcp_httpd_query_string

COLUMN2_1="col-sm-2 text-md-right"
COLUMN2_2="col-10"

BUTTON="btn btn-primary w-100"
COLLAPSE="collapse bg-white border shadow rounded border-secondary px-3 pt-2"

#========================================================================================
# Reboot page.
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "reboot" ]; then
	. pcp-rpi-functions
	pcp_rpi_details
	echo '<p>'$NAME' is rebooting...</p>'
	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		pcp_debug_variables "html" MODEL RB_DELAY
		echo '<!-- End of debug info -->'
	fi
	echo '<div>'
	pcp_redirect_button "Refresh Main Page" "main.cgi" $RB_DELAY
	echo '</div>'
	pcp_remove_query_string
	pcp_html_end
	pcp_reboot "none"
#	sudo reboot
	exit
fi

#========================================================================================
# Shutdown page.
#----------------------------------------------------------------------------------------
if [ "$ACTION" = "shutdown" ]; then
	. pcp-rpi-functions
	pcp_rpi_details
	echo '<p>'$NAME' is shutting down...</p>'
	echo '<p><b>Note:</b> You need to reapply power to restart after a shutdown.</p>'
	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		pcp_debug_variables "html" MODEL RB_DELAY
		echo '<!-- End of debug info -->'
	fi
	echo '<div>'
	pcp_redirect_button "Refresh Main Page" "main.cgi" 15
	echo '</div>'
	pcp_remove_query_string
	pcp_html_end
	pcp_shutdown "none"
#	exitcheck.sh
	exit
fi

#========================================================================================
# Main piCorePlayer operations
#----------------------------------------------------------------------------------------

#------------------------------------Squeezelite Indication------------------------------
pcp_main_squeezelite_indication() {

	if [ $(pcp_squeezelite_status) -eq 0 ]; then
		pcp_green_tick "running"
	else
		pcp_red_cross "not running"
	fi

	pcp_incr_id
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'$INDICATOR'</div>'
	echo '    <div class="'$COLUMN2_2'">'

	if [ "$SQUEEZELITE" = "no" ]; then
		echo '      <p>Squeezelite is disabled on Tweaks page&nbsp;&nbsp;'
	else
		echo '      <p>Squeezelite is '$STATUS'&nbsp;&nbsp;'
	fi

	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <ul>'
	echo '          <li>'$(pcp_bi_check)' = Squeezelite running.</li>'
	echo '          <li>'$(pcp_bi_x)' = Squeezelite not running.</li>'
	echo '        </ul>'
	echo '        <p><b>Note:</b></p>'
	echo '        <ul>'
	echo '          <li>Squeezelite must be running for music to play.</li>'
	echo '          <li>Squeezelite must be running for connection to LMS.</li>'
	echo '        </ul>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
pcp_main_squeezelite_indication
#----------------------------------------------------------------------------------------

#------------------------------------LMS Indication--------------------------------------
pcp_main_lms_indication() {

	if [ $(pcp_lms_status) -eq 0 ]; then
		pcp_green_tick "running"
	else
		pcp_red_cross "not running"
	fi

	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'$INDICATOR'</div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>LMS is '$STATUS'&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <ul>'
	echo '          <li>'$(pcp_bi_check)' = LMS running.</li>'
	echo '          <li>'$(pcp_bi_x)' = LMS not running.</li>'
	echo '        </ul>'
	echo '    </div>'
	echo '  </div>'
}
[ "$LMSERVER" = "yes" ] && pcp_main_lms_indication
#----------------------------------------------------------------------------------------

#------------------------------------Shairport Indication--------------------------------
pcp_main_shairport_indication() {

	if [ $(pcp_shairport_status) -eq 0 ]; then
		pcp_green_tick "running"
	else
		pcp_red_cross "not running"
	fi

	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'$INDICATOR'</div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Shairport is '$STATUS'&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <ul>'
	echo '          <li>'$(pcp_bi_check)' = Shairport running.</li>'
	echo '          <li>'$(pcp_bi_x)' = Shairport not running.</li>'
	echo '        </ul>'
	echo '        <p><b>Note:</b></p>'
	echo '        <ul>'
	echo '          <li>Shairport must be running for music to play from iDevices.</li>'
	echo '        </ul>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ "$SHAIRPORT" = "yes" ] && pcp_main_shairport_indication
#----------------------------------------------------------------------------------------

#-------------------------------------Main Tab-------------------------------------------
echo '<hr>'
pcp_heading5 "Main page"
#----------------------------------------------------------------------------------------

#-------------------------------Restart - Squeezelite / Shairpoint-----------------------
pcp_main_restart_squeezelite() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Restart" action="restartsqlt.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Restart">Restart</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Restart Squeezelite with new settings&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will kill the Squeezelite process then restart it.</p>'
	echo '        <p><b>Note:</b></p>'
	echo '        <ul>'
	echo '          <li>A restart of Squeezelite is required after you change any of the Squeezelite settings.</li>'
	echo '          <li>Squeezelite running indicator will turn to a green tick.</li>'
	echo '          <li>Squeezelite in the footer will turn green.</li>'
	echo '        </ul>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}

pcp_main_restart_shairport() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Restart" action="restartsqlt.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Restart">Restart</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Restart Squeezelite and Shairport with new settings&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will kill the Squeezelite and Shairport processes then restart them.</p>'
	echo '        <p><b>Note:</b></p>'
	echo '        <ul>'
	echo '          <li>A restart of Squeezelite and Shairport is required after you change any of the Squeezelite settings.</li>'
	echo '          <li>Squeezelite and Shairport running indicators will turn to a green tick.</li>'
	echo '          <li>Squeezelite in the footer will turn green.</li>'
	echo '        </ul>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}

if [ "$SHAIRPORT" = "yes" ]; then
	pcp_main_restart_shairport
else
	pcp_main_restart_squeezelite
fi
#----------------------------------------------------------------------------------------

#------------------------------------------Update Squeezelite----------------------------
pcp_main_update_sqlt() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="updateRalphys" action="updatesqlt.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON' mb-1" name="ACTION" value="update">Update</button>'
	echo '        <button type="submit" class="'$BUTTON'" name="ACTION" value="full_update">Full Update</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Update Squeezelite Extensions&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will update the pCP Squeezelite extension from the pCP repository.</p>'
	echo '        <p><b>Note:</b></p>'
	echo '        <ul>'
	echo '          <li>Update will attempt to update the squeezelite package in place.</li>'
	echo '          <li>Full Update will update squeezelite and all libraries, requiring a reboot.</li>'
	echo '          <li>Internet access is required.</li>'
	echo '          <li>The basic version is 1.3MB which plays PCM, (WAV/AIFF), FLAC, MP3, OGG and AAC.</li>'
	echo '          <li>If the FFMpeg library is added, can additionally play ALAC and WMA.</li>'
	echo '          <li>Triode is the original author of Squeezelite.</li>'
	echo '          <li>Ralphy provides Squeezelite binaries with additional features enabled.</li>'
	echo '          <li>For more information on Squeezelite - see <a href="https://code.google.com/p/squeezelite/" target="_blank">Squeezelite Google code</a>.</li>'
	echo '        </ul>'
	echo '        <p><b>Version:</b> '$(pcp_squeezelite_version)'</p>'
	echo '        <p><b>Build options:</b></p>'
	echo '        <p>'$(sudo ${SQLT_BIN} -? | grep "Build options" | awk -F": " '{print $2}')'</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_main_update_sqlt
#----------------------------------------------------------------------------------------

#------------------------------------------Install/Remove FFMPEG-------------------------
pcp_main_ffmpeg() {

	if [ ! -f /$TCEMNT/tce/optional/pcp-libffmpeg.tcz ]; then
		VERSIONsmall="selected"
	else
		VERSIONlarge="selected"
	fi

	if [ "${VERSIONsmall}" = "selected" ]; then
		echo '  <div class="form-group row">'
		echo '    <div class="'$COLUMN2_1'">'
		echo '      <form name="updateFFMpeg" action="updatesqlt.cgi" method="get">'
		echo '        <button type="submit" class="'$BUTTON'" name="ACTION" value="inst_ffmpeg">Install</button>'
		echo '      </form>'
		echo '    </div>'
		pcp_incr_id
		echo '    <div class="'$COLUMN2_2'">'
		echo '      <p>Install FFMpeg libraries for Squeezelite&nbsp;&nbsp;'
		echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
		echo '      </p>'
		echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '        <p>This will download and install FFMpeg Libraries from the pCP repository.</p>'
		echo '        <p><b>Note:</b></p>'
		echo '        <ul>'
		echo '          <li>Internet access is required.</li>'
		echo '          <li>The 7MB FFMpeg library adds playback of ALAC and WMA.</li>'
		echo '        </ul>'
		echo '      </div>'
		echo '    </div>'
		echo '  </div>'
	else
		echo '  <div class="form-group row">'
		echo '    <div class="'$COLUMN2_1'">'
		echo '      <form name="updateFFMpeg" action="updatesqlt.cgi" method="get">'
		echo '        <button type="submit" class="'$BUTTON'" name="ACTION" value="rem_ffmpeg">Remove</button>'
		echo '      </form>'
		echo '    </div>'
		pcp_incr_id
		echo '    <div class="'$COLUMN2_2'">'
		echo '      <p>Remove FFMpeg libraries for Squeezelite&nbsp;&nbsp;'
		echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
		echo '      </p>'
		echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '        <p>This will remove the FFMpeg Libraries from the system.</p>'
		echo '      </div>'
		echo '    </div>'
		echo '  </div>'
	fi
}
[ $MODE -ge $MODE_PLAYER ] && pcp_main_ffmpeg
#----------------------------------------------------------------------------------------

#------------------------------------------Bluetooth-------------------------------------
pcp_main_bluetooth() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Bluetooth" action="bluetooth.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Bluetooth">Bluetooth</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Go to Bluetooth page&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will go to the Bluetooth page.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[[ $MODE -ge $MODE_PLAYER ] && pcp_main_bluetooth
#----------------------------------------------------------------------------------------

#------------------------------------------Reboot----------------------------------------
pcp_main_reboot() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Reboot" action="javascript:pcp_confirm('\''Reboot '$NAME'?'\'','\''main.cgi?ACTION=reboot'\'')" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Reboot">Reboot</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Reboot piCorePlayer&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will reboot piCorePlayer.</p>'
	echo '        <p><b>Note: </b>This will do the following:</p>'
	echo '        <ul>'
	echo '          <li>Shutdown piCorePlayer gracefully.</li>'
	echo '          <li>Boot piCorePlayer using the latest settings.</li>'
	echo '        </ul>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
pcp_main_reboot
#----------------------------------------------------------------------------------------

#------------------------------------------Diagnostics-----------------------------------
pcp_main_diagnostics() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Diagnostics" action="diagnostics.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Diagnostics">Diagnostics</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Go to Diagnostics page&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will go to the Diagnostics page.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_main_diagnostics
#----------------------------------------------------------------------------------------

#------------------------------------------Save to USB-----------------------------------
pcp_main_save_usb() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Saveconfig" action="save2usb.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Save to USB">Save to USB</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Save your current configuration to the USB flash drive&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will copy the current configuration file to the attached USB flash drive/device.</p>'
	echo '        <p><b>Note:</b></p>'
	echo '        <ul>'
	echo '          <li>If you reboot with this USB device attached, this configuration file will be uploaded and used.</li>'
	echo '          <li>This is handy if you update your piCorePlayer or want to setup another piCorePlayer with similar settings.</li>'
	echo '          <li>This configuration file (newpcp.cfg) will be automatically renamed to usedpcp.cfg after rebooting.</li>'
	echo '          <li>This method will only work on basic piCorePlayer setups.</li>'
	echo '        </ul>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_save_usb
#----------------------------------------------------------------------------------------

#--------------------------------------Advanced mode-------------------------------------
echo '<hr>'
pcp_heading5 "Advanced mode"
#----------------------------------------------------------------------------------------

#------------------------------------------Stop------------------------------------------
pcp_main_stop() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Stop" action="stop.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Stop">Stop</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Stop Squeezelite&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will kill the Squeezelite process.</p>'
	echo '        <p>Click [Restart] to start Squeezelite again.</p>'
	echo '        <p><b>Note:</b></p>'
	echo '        <ul>'
	echo '          <li>Squeezelite running indicator will turn to a red cross.</li>'
	echo '          <li>Squeezelite start at boot can be changed in Tweaks.</li>'
	echo '        </ul>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_main_stop
#----------------------------------------------------------------------------------------

#------------------------------------------Backup----------------------------------------
pcp_main_backup() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="backup" action="javascript:pcp_confirm('\''Do a backup on '$NAME'?'\'','\''backup.cgi'\'')" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Backup">Backup</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Backup your changes&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will do a piCore backup to your SD card.</p>'
	echo '        <p>piCorePlayer does a backup after it changes any setting, so this option is really just for "peace of mind"'
	echo '           before doing a shutdown or reboot.</p>'
	echo '        <p><b>Note: </b>This will backup the following:</p>'
	echo '        <ul>'
	echo '          <li>Your configuration file.</li>'
	echo '          <li>Your home directory.</li>'
	echo '          <li>Files and directories defined in /opt/.filetool.lst</li>'
	echo '        </ul>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_main_backup
#----------------------------------------------------------------------------------------

#------------------------------------------Shutdown--------------------------------------
pcp_main_shutdown() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Shutdown" action="javascript:pcp_confirm('\''Shutdown '$NAME'?'\'','\''main.cgi?ACTION=shutdown'\'')" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Shutdown">Shutdown</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Shutdown piCorePlayer&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will shutdown piCorePlayer gracefully.</p>'
	echo '        <p>To restart piCorePlayer you will need to remove then reapply the power.</p>'
	echo '        <p><b>Note: </b>This option is not really required - piCorePlayer can be turned off at the switch.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_main_shutdown
#----------------------------------------------------------------------------------------

#------------------------------------------Resize FS-------------------------------------
pcp_main_resize_fs() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Resize FS" action="xtras_resize.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Resize FS">Resize FS</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Resize file system&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This command will resize the file system on the SD card.</p>'
	echo '        <p><b>Note:</b> Only required if you need to add extra extensions.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_main_resize_fs
#----------------------------------------------------------------------------------------

#------------------------------------------Extensions------------------------------------
pcp_main_extensions() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Stop" action="xtras_extensions.cgi" method="get">'
	echo '        <input type="submit" class="'$BUTTON'" value="Extensions">'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Search, load or delete piCore extensions&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This page gives you the option to search, load or delete piCore extensions.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_main_extensions
#----------------------------------------------------------------------------------------

#--------------------------------------------Update------t-------------------------------
echo '<hr>'
pcp_heading5 "Update"
#----------------------------------------------------------------------------------------

#-------------------------------------Update pcp web and base----------------------------
pcp_main_update_pcpbase() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Update" action="updatebase.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" name="ACTION" value="Update">Patch Update</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Patch pCP current version extensions&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will check for updated pcp extensions and update if needed.</p>'
	echo '        <p>pCP Version will remain unchanged.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_main_update_pcpbase
#----------------------------------------------------------------------------------------

#------------------------------------------HotFix----------------------------------------
pcp_main_minor_update() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Minor" action="minor_update.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" name="ACTION value="initial">Minor Update</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Check for minor pCP update&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will check for a pCP minor upgrade.</p>'
	echo '        <p>This will change the pCP verion.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_main_minor_update
#----------------------------------------------------------------------------------------

#------------------------------------------Update pCP------------------------------------
pcp_main_update_pcp() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="InSitu" action="insitu_update_stage1.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Full Update">Full Update</button>'
	echo '        <input type="hidden" name="ACTION" value="initial">'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Insitu Update piCorePlayer without removing the SD card&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This can be used when the SD card slot is not accessible.</p>'
	echo '        <p><b>Note:</b></p>'
	echo '        <ul>'
	echo '          <li>Internet access is required.</li>'
	echo '          <li>The current version of piCorePlayer will be completely overwritten.</li>'
	echo '          <li>Additional extensions (ie. Jivelite, Shairport) may need to be reloaded.</li>'
	echo '          <li>When the update has completed:'
	echo '            <ol>'
	echo '              <li>Select [Squeezelite Settings].</li>'
	echo '              <li>Confirm your "Audio output" settings.</li>'
	echo '              <li>Click [Save] and [Reboot].</li>'
	echo '            </ol>'
	echo '          </li>'
	echo '        </ul>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_main_update_pcp
#----------------------------------------------------------------------------------------

#------------------------------------------Beta mode-------------------------------------
[ $MODE -ge $MODE_BETA ] && echo '<hr>'
[ $MODE -ge $MODE_BETA ] && pcp_heading5 "Beta"
#----------------------------------------------------------------------------------------

#------------------------------------------Static IP-------------------------------------
pcp_main_static_ip() {

	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Static IP" action="xtras_staticip.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Static IP">Static IP</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Static IP for network interface&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>The recommended method to set a static IP address is to map the MAC address to an IP address in your router.</p>'
	echo '        <p>This option allows you to set a static IP for network interface.</p>'
	echo '        <p>You will need to re-install static IP after an insitu update.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_static_ip
#----------------------------------------------------------------------------------------

#------------------------------------------Extras----------------------------------------
pcp_main_extras() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Extras" action="xtras.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Extras">Extras</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Go to Extras page&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will go to the Extras page.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_extras
#----------------------------------------------------------------------------------------

#------------------------------------------Security--------------------------------------
pcp_main_security() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Security" action="security.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Security">Security</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Go to Security page&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will go to the Security page.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_security
#----------------------------------------------------------------------------------------

#------------------------------------------Dosfsck---------------------------------------
pcp_main_dosfsck() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="DOS fsck" action="xtras_dosfsck.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="DOS fsck">DOS fsck</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>DOS file system check&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This option allows you to run dosfsck on the SD card.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_BETA ] && pcp_main_dosfsck
#----------------------------------------------------------------------------------------

#----------------------------------------Developer mode ---------------------------------
[ $MODE -ge $MODE_DEVELOPER ] && echo '<hr>'
[ $MODE -ge $MODE_DEVELOPER ] && pcp_heading5 "developer"
#----------------------------------------------------------------------------------------

#------------------------------------------Reset ALL-------------------------------------
pcp_main_reset_all() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Reset ALL" action="javascript:pcp_confirm('\''WARNING:\nYou are about to RESET your configuration file.'\'','\''writetoconfig.cgi?SUBMIT=Reset'\'')" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" name="SUBMIT" value="Reset ALL">Reset ALL</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Reset all settings in configuration file&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This command will reset all settings in the configuration file to the defaults that'
	echo '           are defined in pcp-functions. </p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_reset_all
#----------------------------------------------------------------------------------------

#------------------------------------------Restore ALL-----------------------------------
pcp_main_restore_all() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Restore ALL" action="writetoconfig.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" name="SUBMIT" value="Restore ALL">Restore ALL</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Restore all settings in configuration file&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This command will restore all settings in the configuration file to those found in'
	echo '           newconfig.cfg on USB flash memory.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_restore_allx
#----------------------------------------------------------------------------------------

#------------------------------------------Update config---------------------------------
pcp_main_update_config() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Update config" action="writetoconfig.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" name="SUBMIT" value="Update config">Update config</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Update configuration file&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This command will update your configuration file.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_update_config
#----------------------------------------------------------------------------------------

#------------------------------------------Debug-----------------------------------------
pcp_main_debug() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="Debug" action="debug.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="Debug">Debug</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Go to Debug page&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This will go to the Debug page.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_debug
#----------------------------------------------------------------------------------------

#------------------------------------------copy2fs---------------------------------------
pcp_main_copy2fs() {
	echo '  <div class="form-group row">'
	echo '    <div class="'$COLUMN2_1'">'
	echo '      <form name="copy2fs" action="xtras_copy2fs.cgi" method="get">'
	echo '        <button type="submit" class="'$BUTTON'" value="copy2fs">copy2fs</button>'
	echo '      </form>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="'$COLUMN2_2'">'
	echo '      <p>Set copy2fs flag&nbsp;&nbsp;'
	echo '        <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '      </p>'
	echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '        <p>This sets the copy2fs flag so extensions are loaded into ram.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_main_copy2fs
#----------------------------------------------------------------------------------------

#pcp_html_end
#exit

pcp_footer
pcp_mode
pcp_copyright

echo '</div>'
echo '</body>'
echo '</html>'
exit