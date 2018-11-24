#!/bin/sh

# Version: 4.1.0 2018-09-19

# Thanks to M-H for his help in debugging and testing.

. pcp-functions
. pcp-lms-functions

pcp_html_head "Cirrus Audio Card Settings" "PH"

pcp_picoreplayers_toolbar
pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_remove_query_string
pcp_httpd_query_string

CIRRUSCONF=/usr/local/etc/pcp/cirrus.conf

#---------------------------Routines-----------------------------------------------------

pcp_install_cirrus() {
	echo '[ INFO ] Downloading Cirrus Configuration extension...'
	sudo -u tc pcp-load -r $PCP_REPO -w rpi-cirrus-config.tcz
	if [ -f $TCEMNT/tce/optional/rpi-cirrus-config.tcz ]; then
		echo '[ INFO ] Installing Cirrus Configuration extension...'
		sudo -u tc pcp-load -i rpi-cirrus-config.tcz
		sudo sed -i '/rpi-cirrus-config.tcz/d' $ONBOOTLST
		sudo echo 'rpi-cirrus-config.tcz' >> $ONBOOTLST
		[ $DEBUG -eq 1 ] && echo '[ DEBUG ] rpi-cirrus-config.tcz is added to onboot.lst'
		[ $DEBUG -eq 1 ] && cat $ONBOOTLST
	fi
}

pcp_remove_cirrus() {
	sudo -u tc tce-audit builddb
	sudo -u tc tce-audit delete rpi-cirrus-config.tcz
	sudo sed -i '/rpi-cirrus-config.tcz/d' $ONBOOTLST
	echo "Removeing configuration files"
	rm -f $CIRRUSCONF
}

set_cirrus_conf() {
	[ -f /usr/local/lib/alsa/rpi-cirrus-functions.sh ] && . /usr/local/lib/alsa/rpi-cirrus-functions.sh
	if [ x"$SPEAKERS" = "x" ]; then
		echo '[ INFO ] Setting Speakers OFF'
		SPEAKERS=0
		reset_speaker_out
	else
		echo '[ INFO ] Setting Speakers ON'
		playback_to_speakers
	fi
	if [ x"$HEADSET" = "x" ]; then
		echo '[ INFO ] Setting Headset OFF'
		HEADSET=0
		reset_headset_out
	else
		echo '[ INFO ] Setting Headset ON'
		playback_to_headset
	fi
	if [ x"$LINEOUT" = "x" ]; then
		echo '[ INFO ] Setting Line Out OFF'
		LINEOUT=0
		reset_line_out
	else
		echo '[ INFO ] Setting Line Out ON'
		playback_to_lineout
	fi
	if [ x"$SPDIF" = "x" ]; then
		echo '[ INFO ] Setting Spdif OFF'
		SPDIF=0
		reset_spdif_out
	else
		echo '[ INFO ] Setting Spdif ON'
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
		pcp_table_top "Downloading rpi-cirrus-config.tcz"
		pcp_sufficient_free_space 4500
		if [ $? -eq 0 ] ; then
			echo '                <textarea class="inform" style="height:160px">'
			pcp_install_cirrus
			if [ ! -f $TCEMNT/tce/optional/rpi-cirrus-config.tcz ]; then
				echo '[ ERROR ] Error Downloading rpi-cirrus-config.tcz, please try again later.'
			fi
			echo '                </textarea>'
			pcp_table_end
		fi
	;;
	Remove)
		pcp_table_top "Removing rpi-cirrus-config.tcz"
		echo '                <textarea class="inform" style="height:120px">'
		echo 'After a reboot these extensions will be permanently deleted:'
		pcp_remove_cirrus
		echo '                </textarea>'
		pcp_table_end
		REBOOT_REQUIRED=1
	;;
	Setconfig)
		pcp_table_top "Cirrus configuration"
		echo '                <textarea class="inform" style="height:120px">'
		echo '[ INFO ] Setting Cirrus Card Configuration...'
		set_cirrus_conf
		pcp_backup "nohtml"
		echo '                </textarea>'
		pcp_table_end
	;;
	Update)
		pcp_table_top "Update"
		pcp_sufficient_free_space 4500
		echo '                <textarea class="inform" style="height:100px">'
		echo '[ INFO ] Updating rpi-cirrus-config.tcz...'
		sudo -u tc pcp-update rpi-cirrus-config.tcz
		case $? in
			0) echo '[ INFO ] Reboot Required to finish update'; REBOOT_REQUIRED=1;;
			2) echo '[ INFO ] No Update Availiable';;
			*) echo '[ ERROR] Try again later';;
		esac
		echo '                </textarea>'
		pcp_table_end
	;;
	*)
	;;
esac
[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

#========================================================================================
# Main table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Cirrus Logic Audio Card Configuration</legend>'
echo '          <table class="bggrey percent100">'

[ -f $TCEMNT/tce/optional/rpi-cirrus-config.tcz ] && DISABLE="" || DISABLE="disabled"

#------------------------------------------Install/uninstall ----------------------------
pcp_cirrus_install() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '            <form name="Install" action="'$0'">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150 center">'
	if [ ! -f $TCEMNT/tce/optional/rpi-cirrus-config.tcz ]; then
		echo '                  <input type="submit" name="ACTION" value="Install" />'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Required: Install Cirrus Logic Configuration Extension&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <p>This extension is required for the card to be properly configured for playback.</p>'
		echo '                  </div>'
	else
		echo '                  <input type="submit" name="ACTION" value="Update" />'
		echo '                </td>'
		echo '                <td class="column150 center">'
		echo '                  <input type="submit" name="ACTION" value="Remove" onclick="return confirm('\''This will remove Cirrus Logic Configuration Scripts.\n\nAre you sure?'\'')"/>'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>Update or Remove Cirrus Logic Configuration Scripts from pCP&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'

		echo '                    <p>This will remove Cirrus Logic Configuration Scripts.</p>'
		echo '                  </div>'
	fi
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_cirrus_install
#----------------------------------------------------------------------------------------

#------------------------------------------Configure ------------------------------------
SPEAKERS=$(cat $CIRRUSCONF | grep -e "^SPEAKERS=" | cut -d "=" -f2)
HEADSET=$(cat $CIRRUSCONF | grep -e "^HEADSET=" | cut -d "=" -f2)
LINEOUT=$(cat $CIRRUSCONF | grep -e "^LINEOUT=" | cut -d "=" -f2)
SPDIF=$(cat $CIRRUSCONF | grep -e "^SPDIF=" | cut -d "=" -f2)

pcp_incr_id
pcp_toggle_row_shade

COL1="column75 center"
COL2="column100"
COL3="column250"

#--------------------------------------Heading-------------------------------------------
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="'$COL1'">'
echo '                <p><b>Enabled</b></p>'
echo '              </td>'
echo '              <td class="'$COL2'">'
echo '                <p><b>Output</b></p>'
echo '              </td>'
echo '              <td class="'$COL3'">'
echo '                <p><b>Description/Help</b></p>'
echo '              </td>'
echo '            </tr>'
#----------------------------------------------------------------------------------------

#--------------------------------------configure-----------------------------------------
pcp_cirrus_configure() {
	echo '            <form name="configure" action="'$0'" method="get">'
	[ $SPEAKERS -eq 1 ] && SPEAKERSyes="checked"
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                  <input class="small1" type="checkbox" name="SPEAKERS" value="1" '$SPEAKERSyes $DISABLE'>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <p>Speakers</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Output to Speakers Port</p>'
	echo '                </td>'
	echo '              </tr>'

	[ $HEADSET -eq 1 ] && HEADSETyes="checked"
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                  <input class="small1" type="checkbox" name="HEADSET" value="1" '$HEADSETyes $DISABLE'>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <p>Headset</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Output to Headset Port</p>'
	echo '                </td>'
	echo '              </tr>'

	[ $LINEOUT -eq 1 ] && LINEOUTyes="checked"
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                  <input class="small1" type="checkbox" name="LINEOUT" value="1" '$LINEOUTyes $DISABLE'>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <p>Line Out</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Output to Line Out Port</p>'
	echo '                </td>'
	echo '              </tr>'

	[ $SPDIF -eq 1 ] && SPDIFyes="checked"
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                  <input class="small1" type="checkbox" name="SPDIF" value="1" '$SPDIFyes $DISABLE'>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <p>Spdif</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Output to Spdif Port</p>'
	echo '                </td>'
	echo '              </tr>'
#--------------------------------------Submit button-------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '                <tr class="'$ROWSHADE'">'
	echo '                  <td class="column150 center">'
	echo '                    <button type="submit" name="ACTION" value="Setconfig" '$DISABLE'>Set Outputs</button>'
	echo '                  </td>'
	echo '                  <td class="colspan=2">'
	echo '                    <p>Enable card outputs by selecting check boxes above, then press the "Set Outputs" button</p>'
	echo '                  </td>'
	echo '                </tr>'
	echo '              </form>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_cirrus_configure
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
[ $MODE -ge $MODE_NORMAL ] && pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'
