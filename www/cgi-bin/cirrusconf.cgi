#!/bin/sh

# Version: 7.0.0 2020-05-17

# Thanks to M-H for his help in debugging and testing.

. pcp-functions
. pcp-lms-functions

pcp_html_head "Cirrus Audio Card Settings" "PH"

pcp_controls
pcp_navbar
pcp_httpd_query_string
pcp_remove_query_string

CIRRUSCONF="/usr/local/etc/pcp/cirrus.conf"

COLUMN3_1="col-2 text-md-center"
COLUMN3_2="col-2"
COLUMN3_3="col-8"

#---------------------------Routines-----------------------------------------------------

pcp_install_cirrus() {
	pcp_message INFO "Downloading Cirrus Configuration extension..." "text"
	sudo -u tc pcp-load -r $PCP_REPO -w rpi-cirrus-config.tcz
	if [ -f $TCEMNT/tce/optional/rpi-cirrus-config.tcz ]; then
		pcp_message INFO "Installing Cirrus Configuration extension..." "text"
		sudo -u tc pcp-load -i rpi-cirrus-config.tcz
		sudo sed -i '/rpi-cirrus-config.tcz/d' $ONBOOTLST
		sudo echo 'rpi-cirrus-config.tcz' >> $ONBOOTLST
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "rpi-cirrus-config.tcz is added to onboot.lst" "text"
		[ $DEBUG -eq 1 ] && cat $ONBOOTLST
	fi
}

pcp_remove_cirrus() {
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete rpi-cirrus-config.tcz
	sudo sed -i '/rpi-cirrus-config.tcz/d' $ONBOOTLST
	echo "Removing configuration files" "text"
	rm -f $CIRRUSCONF
}

set_cirrus_conf() {
	[ -f /usr/local/lib/alsa/rpi-cirrus-functions.sh ] && . /usr/local/lib/alsa/rpi-cirrus-functions.sh
	if [ x"$SPEAKERS" = x"" ]; then
		pcp_message INFO "Setting Speakers OFF" "text"
		SPEAKERS=0
		reset_speaker_out
	else
		pcp_message INFO "Setting Speakers ON" "text"
		playback_to_speakers
	fi
	if [ x"$HEADSET" = x"" ]; then
		pcp_message INFO "Setting Headset OFF" "text"
		HEADSET=0
		reset_headset_out
	else
		pcp_message INFO "Setting Headset ON" "text"
		playback_to_headset
	fi
	if [ x"$LINEOUT" = x"" ]; then
		pcp_message INFO "Setting Line Out OFF" "text"
		LINEOUT=0
		reset_line_out
	else
		pcp_message INFO "Setting Line Out ON" "text"
		playback_to_lineout
	fi
	if [ x"$SPDIF" = x"" ]; then
		pcp_message INFO "Setting Spdif OFF" "text"
		SPDIF=0
		reset_spdif_out
	else
		pcp_message INFO "Setting Spdif ON" "text"
		playback_to_spdif
	fi

	sudo sed -i "s/\(^SPEAKERS=\).*/\1$SPEAKERS/" $CIRRUSCONF
	sudo sed -i "s/\(^HEADSET=\).*/\1$HEADSET/" $CIRRUSCONF
	sudo sed -i "s/\(^LINEOUT=\).*/\1$LINEOUT/" $CIRRUSCONF
	sudo sed -i "s/\(^SPDIF=\).*/\1$SPDIF/" $CIRRUSCONF
}

REBOOT_REQUIRED=0
case "$ACTION" in
	Install)
		pcp_textarea_begin "" 9
		pcp_sufficient_free_space 4500
		if [ $? -eq 0 ] ; then
			pcp_install_cirrus
			if [ ! -f $TCEMNT/tce/optional/rpi-cirrus-config.tcz ]; then
				pcp_message ERROR "Error Downloading rpi-cirrus-config.tcz, please try again later." "text"
			fi
		fi
		pcp_textarea_end
		pcp_hr
	;;
	Remove)
		pcp_textarea_begin "" 9
		pcp_message INFO "After a reboot these extensions will be permanently deleted:" "text"
		pcp_remove_cirrus
		pcp_textarea_end
		REBOOT_REQUIRED=1
		pcp_hr
	;;
	Setconfig)
		pcp_textarea_begin "" 9
		pcp_message INFO "Setting Cirrus Card configuration..." "text"
		set_cirrus_conf
		pcp_backup "text"
		pcp_textarea_end
		pcp_hr
	;;
	Update)
		pcp_textarea_begin "" 9
		pcp_sufficient_free_space 4500
		pcp_message INFO "Updating rpi-cirrus-config.tcz..." "text"
		sudo -u tc pcp-update rpi-cirrus-config.tcz
		case $? in
			0) pcp_message INFO "Reboot required to finish update" "text"; REBOOT_REQUIRED=1;;
			2) pcp_message INFO "No update available" "text";;
			*) pcp_message ERROR "Try again later" "text";;
		esac
		pcp_textarea_end
		pcp_hr
	;;
	*)
	;;
esac
[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required
#----------------------------------------------------------------------------------------
# tc@pCPScreen1:~/www/cgi-bin$ pcp-update rpi-cirrus-config.tcz | sed -e "s/\[ INFO \]/<div>\[ INFO \]/ g" -e "/^$/d" -e "s/$/<\/div>/
#========================================================================================
pcp_heading5 "Cirrus Logic Audio Card Configuration"

[ -f $TCEMNT/tce/optional/rpi-cirrus-config.tcz ] && DISABLE="" || DISABLE="disabled"

#------------------------------------------Install/uninstall ----------------------------
pcp_cirrus_install() {
	pcp_incr_id
	echo '  <form name="Install" action="'$0'">'
	echo '    <div class="row">'

	if [ ! -f $TCEMNT/tce/optional/rpi-cirrus-config.tcz ]; then
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Install" />'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '        <p>Required: Install Cirrus Logic Configuration Extension&nbsp;&nbsp;'
		echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>This extension is required for the card to be properly configured for playback.</p>'
		echo '        </div>'
		echo '      </div>'
	else
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Update" />'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Remove" onclick="return confirm('\''This will remove Cirrus Logic Configuration Scripts.\n\nAre you sure?'\'')"/>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_3'">'
		echo '        <p>Update or Remove Cirrus Logic Configuration Scripts from pCP&nbsp;&nbsp;'
		echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>This will remove Cirrus Logic Configuration Scripts.</p>'
		echo '        </div>'
		echo '      </div>'
	fi
	echo '    </div>'
	echo '  </form>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_cirrus_install
#----------------------------------------------------------------------------------------

#------------------------------------------Configure ------------------------------------
SPEAKERS=$(cat $CIRRUSCONF | grep -e "^SPEAKERS=" | cut -d "=" -f2)
HEADSET=$(cat $CIRRUSCONF | grep -e "^HEADSET=" | cut -d "=" -f2)
LINEOUT=$(cat $CIRRUSCONF | grep -e "^LINEOUT=" | cut -d "=" -f2)
SPDIF=$(cat $CIRRUSCONF | grep -e "^SPDIF=" | cut -d "=" -f2)

#--------------------------------------Heading-------------------------------------------
echo '  <div class="row">'
echo '    <div class="'$COLUMN3_1'">'
echo '      <p><b>Enabled</b></p>'
echo '    </div>'
echo '    <div class="'$COLUMN3_2'">'
echo '      <p><b>Output</b></p>'
echo '    </div>'
echo '    <div class="'$COLUMN3_3'">'
echo '      <p><b>Description/Help</b></p>'
echo '    </div>'
echo '  </div>'
#----------------------------------------------------------------------------------------

#--------------------------------------configure-----------------------------------------
pcp_cirrus_configure() {
	echo '  <form name="configure" action="'$0'" method="get">'
	#------------------------------------------------------------------------------------
	[ $SPEAKERS -eq 1 ] && SPEAKERSyes="checked"
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input id="cb1" type="checkbox" name="SPEAKERS" value="1" '$SPEAKERSyes $DISABLE'>'
	echo '        <label for="cb1">&#8239;</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <p>Speakers</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Output to Speakers Port</p>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	[ $HEADSET -eq 1 ] && HEADSETyes="checked"
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input id="cb2" type="checkbox" name="HEADSET" value="1" '$HEADSETyes $DISABLE'>'
#	echo '        <label for="cb2">&#8239;</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <p>Headset</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Output to Headset Port</p>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	[ $LINEOUT -eq 1 ] && LINEOUTyes="checked"
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input id="cb3" type="checkbox" name="LINEOUT" value="1" '$LINEOUTyes $DISABLE'>'
#	echo '        <label for="cb3">&#8239;</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <p>Line Out</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Output to Line Out Port</p>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	[ $SPDIF -eq 1 ] && SPDIFyes="checked"
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input id="cb4" type="checkbox" name="SPDIF" value="1" '$SPDIFyes $DISABLE'>'
#	echo '        <label for="cb4">&#8239;</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <p>Spdif</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Output to Spdif Port</p>'
	echo '      </div>'
	echo '    </div>'
	#--------------------------------------Submit button---------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Setconfig" '$DISABLE'>Set Outputs</button>'
	echo '      </div>'
	echo '      <div class="col-10">'
	echo '        <p>Enable card outputs by selecting check boxes above, then press the "Set Outputs" button</p>'
	echo '      </div>'
	echo '    </div>'
#----------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_cirrus_configure
#----------------------------------------------------------------------------------------

pcp_html_end
