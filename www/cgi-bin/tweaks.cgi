#!/bin/sh

# Version: 3.00 2016-07-31
#	Added LIRC IR remote controls. SBP.
#	Reorganized order. PH. GE.
#	Created USB Audio tweaks fieldset. GE.
#	Modified User commands. GE.
#	Added WOL interface. GE.

# Version: 0.26 2016-05-30
#	Added pcp_tweaks_hdmipower. GE.
#	Added Reset Jivelite configuration. PH.
#	Changed overclock to enable only for RPi1. GE.
#	Fixed JIVELITE, SCREENROTATE variables (YES/NO). GE.
#	Renamed variable HTPPD to HTTPD. GE.

# Version: 0.25 2016-04-23 GE
#	Added pcp_tweaks_playertabs and pcp_tweaks_lmscontrols.

# Version: 0.24 2016-03-27 SBP
#	Added 0xf FIQ-Split acceleration.
#	Changed LMS Web Port to Advanced mode.

# Version: 0.23 2016-03-10 GE
#	Fixed Auto start favorite pull-down list.
#	Added LMS Web Port.
#	Added dwc_otg.fiq_fsm_enable.

# Version: 0.22 2016-02-26 GE
#	Increased size of Custom Cron Command field.
#	Increased size of User Command fields.
#	Added Clear button to User commands.
#	Added squeezelite autostart option.

# Version: 0.21 2016-01-29 SBP
#	Activated alsaeqaual feature.
#	Added configure button to xtras_alsaequal.cgi

# Version: 0.20 2016-01-18 GE
#	Minor update to alsaequal.

# Version: 0.19 2016-01-04 SBP
#	Added ALSA Equalizer.
#	Added Shairport-sync.

# Version: 0.18 2015-11-23 GE
#	Fixed auto favorites for decode $HTTPD change and LMS 7.9
#	Fixed Autostart LMS and User commands.
#	Added VU Meters.

# Version: 0.17 2015-10-06 SBP
#	Added Screen rotate routine.

# Version: 0.16 2015-08-29 GE
#	Revised modes.
#	Turned pcp_picoreplayers tabs on in normal mode.
#	Turned overclocking on for RPI2B if in beta mode.
#	Updated some help messages.
#	Revised initial mode settings.

# Version: 0.15 2015-07-01 GE
#	Added pcp_mode tabs.
#	Added pcp_picoreplayers tabs.

# Version: 0.14 2015-06-25 SBP
#	Added Custom cron command.

# Version: 0.13 2015-06-08 GE
#	Started adding HTML5 input field validation.
#	Removed some unnecessary code.
#	Added more help to custom ALSA.

# Version: 0.12 2015-05-11 GE
#	Removed shairport option.
#	Added debug code for auto start favorite.

# Version: 0.11 2015-03-29 GE
#	Added shairport (mode = 99).
#	Added $ROWSHADE variable. Thought it would be easier.
#	Added pcp_incr_id and pcp_start_row_shade.

# Version: 0.10 2015-03-24 SBP
#	Added jivelite support.

# Version: 0.09 2015-02-27 SBP
#	Removed overclock option for RPi2 boards.
#	Removed mode = 4 for User command feature.

# Version: 0.08 2015-02-19 GE
#	Updated Auto start favorite.
#	Added User commands.
#	Minor html updates through out.
#	Added more/less help to Schedule CRON jobs.
#	Added copyright.

# Version: 0.07 2015-01-04 GE
#	Updated Auto start LMS.

# Version: 0.06 2014-12-14 GE
#	Using pcp_html_head now.
#	HTML5 formatting.
#	Major reformatting.
#	Moved debug information to appropriate locations.

# Version: 0.05 2014-10-02 GE
#	Activated $MODE = 5 for AUTOSTARTLMS.

# Version: 0.04 2014-09-10 GE
#	Reformatted html.

# Version: 0.03 2014-09-09 GE
#	Added Auto start LMS command.

# Version: 0.02 2014-09-06 SBP
#	Added cronjob.

# Version: 0.01 2014-08-06 GE
#	Original version.

set -f
. pcp-lms-functions
. pcp-functions
. pcp-rpi-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Tweaks" "SBP"

[ $MODE -ge $MODE_NORMAL ] && pcp_picoreplayers
[ $MODE -ge $MODE_ADVANCED ] && pcp_controls
pcp_banner
pcp_navigation

#========================================================================================
# pCP System Tweaks
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>pCP System Tweaks</legend>'

#----------------------------------------------Hostname---------------------------------
pcp_tweaks_hostname() {
	echo '          <table class="bggrey percent100">'
	echo '            <form name="squeeze" action="writetohost.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">Host name</td>'
	echo '                <td class="column210">'
	echo '                  <input class="large16"'
	echo '                         type="text"'
	echo '                         name="HOST"'
	echo '                         value="'$HOST'"'
	echo '                         maxlength="26"'
	echo '                         title="Only alphanumeric and hyphen allowed."'
	echo '                         pattern="[a-zA-Z0-9-]*"'
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Provide a host name, so the player is easier to identify on your LAN&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Note:</b> This is the linux hostname, not the piCorePlayer name used by LMS.</p>'
	echo '                    <p>The Internet standards for protocols mandate that component hostname labels may '
	echo '                       contain only the ASCII letters "a" through "z" (in a case-insensitive manner), '
	echo '                       the digits "0" through "9", and the hyphen ("-"). No other symbols, punctuation '
	echo '                       characters, or white space are permitted.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'" >'
	echo '                <td colspan=3>'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'
}
[ $MODE -ge $MODE_INITIAL ] && pcp_tweaks_hostname
#----------------------------------------------------------------------------------------

#----------------------------------------------Timezone----------------------------------
pcp_tweaks_timezone() {
	echo '          <table class="bggrey percent100">'
	echo '            <form name="tzone" action="writetotimezone.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">Timezone</td>'
	echo '                <td class="column210">'
	echo '                  <input class="large16"'
	echo '                         type="text"'
	echo '                         name="TIMEZONE"'
	echo '                         value="'$TIMEZONE'"'
	echo '                         maxlength="28"'
	echo '                         pattern="[a-zA-Z0-9-,./]*"'
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Add or change your timezone&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Format:</b> EST-10EST,M10.1.0,M4.1.0/3</p>'
	echo '                    <p>Your timezone should be automatically populated.</p>'
	echo '                    <p>Delete and reboot to force piCorePlayer to automatically populate timezone.</p>'
	echo '                    <p>If not, cut and paste your timezone from your favourite timezone location.</p>'
	echo '                    <p><b>Examples here:</b></p>'
	echo '                    <ul>'
	echo '                      <li><a href="http://wiki.openwrt.org/doc/uci/system#time.zones" target="_blank">Openwrt</a></li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="2">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'
}
[ $MODE -ge $MODE_INITIAL ] && pcp_tweaks_timezone
#----------------------------------------------------------------------------------------

#----------------------------------------------Password----------------------------------
# Note: changing passwords through a script over html is not very secure.
#----------------------------------------------------------------------------------------
pcp_tweaks_password() {
	echo '          <table class="bggrey percent100">'
	echo '            <form name="password" action="changepassword.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">Password for "'$(pcp_tc_user)'"</td>'
	echo '                <td class="column210">'
	echo '                  <input class="large16" type="password" name="NEWPASSWORD" maxlength="26">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter new password&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> piCore</p>'
	echo '                    <p class="error"><b>Warning: </b>Changing passwords through a script over html is not very secure.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150"></td>'
	echo '                <td class="column210">'
	echo '                  <input class="large16" type="password" name="CONFIRMPASSWORD" maxlength="26">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Confirm new password.</p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'" >'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'
}
[ $MODE -ge $MODE_BASIC ] && pcp_tweaks_password
#----------------------------------------------------------------------------------------

#---------------------------------------Overclock----------------------------------------
pcp_tweaks_overclock() {
	case "$OVERCLOCK" in
		NONE) OCnone="selected" ;;
		MILD) OCmild="selected" ;;
		MODERATE) OCmoderate="selected" ;;
	esac

	# Only works for Raspberry Pi Model 1, disable for the others.
	case "$(pcp_rpi_type)" in
		1)     DISABLED="" ;;
		0|2|3) DISABLED="disabled" ;;
	esac

	echo '          <table class="bggrey percent100">'
	echo '            <form name="overclock" action= "writetooverclock.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Overclock</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <select class="large16" name="OVERCLOCK" '$DISABLED'>'
	echo '                    <option value="NONE" '$OCnone'>No overclocking</option>'
	echo '                    <option value="MILD" '$OCmild'>Mild overclocking</option>'
	echo '                    <option value="MODERATE" '$OCmoderate'>Moderate overclocking</option>'
	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Change Raspberry Pi overclocking&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;No overclocking|Mild overclocking|Moderate overclocking&gt;</p>'
	echo '                    <p><b>Note:</b> Only suitable for Raspberry Pi Model 1.</p>'
	echo '                    <p>Reboot is needed.<p>'
	echo '                    <p><b>Note:</b> If Raspberry Pi fails to boot:</p>'
	echo '                    <ul>'
	echo '                      <li>hold down the shift key during booting, or</li>'
	echo '                      <li>edit the config.txt file manually</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Save" '$DISABLED'>'
	[ $MODE -ge $MODE_BETA ] &&
	echo '                  <input class="large16" type="button" name="ADVANCED_OVERCLOCK" onClick="location.href='\'''xtras_overclock.cgi''\''" value="Advanced Overclock">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<p class="debug">[ DEBUG ] $OVERCLOCK: '$OVERCLOCK'<br />'
		echo '                 [ DEBUG ] $OCnone: '$OCnone'<br />'
		echo '                 [ DEBUG ] $OCmild: '$OCmild'<br />'
		echo '                 [ DEBUG ] $OCmoderate: '$OCmoderate'</p>'
		echo '<!-- End of debug info -->'
	fi
}
[ $MODE -ge $MODE_NORMAL ] && pcp_tweaks_overclock
#----------------------------------------------------------------------------------------

#----------------------------------------------Player Tabs-------------------------------
pcp_tweaks_playertabs() {
	case "$PLAYERTABS" in
		yes) PLAYERTABSyes="checked" ;;
		no)  PLAYERTABSno="checked" ;;
	esac

	echo '          <table class="bggrey percent100">'
	echo '            <form name="playertabs" action="writetoconfig.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>piCorePlayer Tabs</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="PLAYERTABS" value="yes" '$PLAYERTABSyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="PLAYERTABS" value="no" '$PLAYERTABSno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Display piCorePlayer Tabs&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Sometimes it might be useful to turn off the piCorePlayer Tabs.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'
}
[ $MODE -ge $MODE_BETA ] && pcp_tweaks_playertabs
#----------------------------------------------------------------------------------------

#----------------------------------------------LMS Control Toolbar-----------------------
pcp_tweaks_lmscontrols() {
	case "$LMSCONTROLS" in
		yes) LMSCONTROLSyes="checked" ;;
		no)  LMSCONTROLSno="checked" ;;
	esac

	echo '          <table class="bggrey percent100">'
	echo '            <form name="playertabs" action="writetoconfig.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>LMS Controls Toolbar</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="LMSCONTROLS" value="yes" '$LMSCONTROLSyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="LMSCONTROLS" value="no" '$LMSCONTROLSno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Display LMS Controls Toolbar&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Sometimes it might be useful to turn off the LMS Controls Toolbar.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'
}
[ $MODE -ge $MODE_BETA ] && pcp_tweaks_lmscontrols
#----------------------------------------------------------------------------------------

#----------------------------------------------HDMI Power--------------------------------
pcp_tweaks_hdmipower() {
	case "$HDMIPOWER" in
		on) HDMIPOWERyes="checked" ;;
		off) HDMIPOWERno="checked" ;;
	esac

	echo '          <table class="bggrey percent100">'
	echo '            <form name="hdmipower" action="writetohdmipwr.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>HDMI power</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="HDMIPOWER" value="on" '$HDMIPOWERyes'>On&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="HDMIPOWER" value="off" '$HDMIPOWERno'>Off'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>HDMI power&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Power off HDMI to save some power.</p>'
	echo '                    <p>Using this option will download and install rpi-vc.tcz.</p>'
	echo '                    <p>Reboot required.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'
}
[ $MODE -ge $MODE_BETA ] && pcp_tweaks_hdmipower
#----------------------------------------------------------------------------------------

#----------------------------------------------LMS Web Port------------------------------
pcp_tweaks_lmswebport() {
	echo '          <table class="bggrey percent100">'
	echo '            <form name="tzone" action="writetoconfig.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>LMS Web Port</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large16" type="number" name="LMSWEBPORT" value="'$LMSWEBPORT'" min="9001" max="9999">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter non-default LMS Web Port number&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;number&gt;</p>'
	echo '                    <p><b>Default:</b> 9000</p>'
	echo '                    <p><b>Range:</b> 9001:9999</p>'
	echo '                    <p><b>Note:</b> Only add this if you have changed from the default LMS Web Port value.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="2">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_tweaks_lmswebport
#----------------------------------------------------------------------------------------
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
# Wake-on-LAN table
#----------------------------------------------------------------------------------------
pcp_tweaks_wol() {

	case "$WOL" in
		yes)
			WOLyes="checked"
		;;
		no)
			WOLno="checked"
			WOLDISABLED="disabled"
		;;
	esac

	set -- $(arp $LMSIP)

	if [ $DEBUG -eq 1 ]; then
		[ "$WOL_NIC" = "" ] && WOL_NIC=$7
		[ "$WOL_LMSMACADDRESS" = "" ] && WOL_LMSMACADDRESS=$4
	fi

	#----------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Wake-on-LAN (WOL)</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="tzone" action="writetoconfig.cgi" method="get">'
	#----------------------------------------------------------------------------------------
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>WOL</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="WOL" value="yes" '$WOLyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="WOL" value="no" '$WOLno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>LMS Wake-on-LAN&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Transmits a Wake-On-LAN (WOL) "Magic Packet", used for restarting machines that have been soft-powered-down.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>LMS NIC</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input id="input'$ID'"'
	echo '                         class="large16"'
	echo '                         type="text"'
	echo '                         name="WOL_NIC"'
	echo '                         value="'$WOL_NIC'"'
	echo '                         title="LMS NIC: ( eth0 | eth1 | wlan0 | wlan1 )"'
	echo '                         pattern="(eth0|eth1|wlan0|wlan1)"'
	echo '                         '$WOLDISABLED
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>LMS Network Interface Card&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;eth0|eth1|wlan0|wlan1&gt;</p>'
	echo '                    <p onclick="myFunction'$ID'()"><b>Example:</b> <span id="example'$ID'">'$7'</span></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '              <script>'
	echo '                function myFunction'$ID'() {'
	echo '                  document.getElementById("input'$ID'").value = document.getElementById("example'$ID'").innerHTML;'
	echo '                }'
	echo '              </script>'
	#----------------------------------------------------------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>LMS MAC address</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input id="input'$ID'"'
	echo '                         class="large16"'
	echo '                         type="text"'
	echo '                         name="WOL_LMSMACADDRESS"'
	echo '                         value="'$WOL_LMSMACADDRESS'"'
	echo '                         title="01:23:45:67:ab:cd:ef"'
	echo '                         pattern="([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"'
	echo '                         '$WOLDISABLED
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>LMS MAC address&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;01:23:45:67:ab:cd:ef&gt;</p>'
	echo '                    <p onclick="pcpFunction'$ID'()"><b>Example:</b> <span id="example'$ID'">'$4'</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '              <script>'
	echo '                function pcpFunction'$ID'() {'
	echo '                  document.getElementById("input'$ID'").value = document.getElementById("example'$ID'").innerHTML;'
	echo '                }'
	echo '              </script>'
	#----------------------------------------------------------------------------------------
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="2">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'
	#----------------------------------------------------------------------------------------
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_BETA ] && pcp_tweaks_wol

#========================================================================================
# Auto start tweaks
#----------------------------------------------------------------------------------------
pcp_tweaks_auto_start() {
	# Function to check the A_S_LMS radio button according to config file
	case "$A_S_LMS" in
		Enabled) A_S_LMS_Y="checked" ;;
		Disabled) A_S_LMS_N="checked" ;;
	esac

	# Function to check the A_S_FAV radio button according to config file
	case "$A_S_FAV" in
		Enabled) A_S_FAV_Y="checked" ;;
		Disabled) A_S_FAV_N="checked" ;;
	esac

	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Auto start tweaks</legend>'

	#----------------------------------------------Auto start favorite-----------------------------
	#b8:27:eb:b8:7d:33 favorites items 0 100 title:Favorites id:0 name:702 ABC Sydney | (Public Radio) type:audio isaudio:1 hasitems:0 id:1 name:ABC Grandstand (Sports Talk and News) type:audio
	#isaudio:1 hasitems:0 id:2 name:Elephant type:playlist isaudio:1 hasitems:1 id:3 name:ABC NewsRadio 630 (National News) type:audio isaudio:1 hasitems:0 id:4 name:16 Of Their Greatest Hits
	#type:playlist isaudio:1 hasitems:1 id:5 name:greg isaudio:0 hasitems:1 count:6
	#----------------------------------------------------------------------------------------------

	echo '          <table class="bggrey percent100">'
	echo '            <form name="autostartfav" action="writetoautostart.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">Auto start favorite</td>'
	echo '                <td class="column420">'
	echo '                  <select class="large30" name="AUTOSTARTFAV">'

	# Generate a list of options
	FAVLIST=`( echo "$(pcp_controls_mac_address) favorites items 0 100"; echo "exit" ) | nc $(pcp_lmsip) 9090 | sed 's/ /\+/g'`
	FAVLIST=$(sudo $HTTPD -d $FAVLIST)
	echo $FAVLIST | awk -v autostartfav="$AUTOSTARTFAV" '
	BEGIN {
		RS="id:"
		FS=":"
		i = 0
	}
	# Main
	{
		i++
		name[i]=$2
		gsub(" type","",name[i])
		sel[i]=""
		if ( name[i] == autostartfav ) {
			sel[i]="selected"
		}
		isaudio[i]=$3
		gsub(" hasitems","",isaudio[i])
		if ( isaudio[i] == "0" ) {
			i--
		}
		isfavorite[i]=$6
		gsub(" title","",isfavorite[i])
		if ( isfavorite[i] == "33 favorites items 0 100" ) {
			i--
		}
	}
	END {
		for (j=1; j<=i; j++) {
			printf "                    <option value=\"%s\" %s>%s</option>\n",name[j],sel[j],name[j]
		}
	} '

	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <input class="small1" type="radio" name="A_S_FAV" value="Enabled" '$A_S_FAV_Y'>Enabled'
	echo '                  <input class="small1" type="radio" name="A_S_FAV" value="Disabled" '$A_S_FAV_N'>Disabled'
	echo '                </td>'
	echo '              </tr>'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                </td>'
	echo '                <td colspan="2">'
	echo '                  <p>Select your auto start favorite from list&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Allows you to set an auto start favorite command that is run after'
	echo '                       a "hard" power on. '
	echo '                       This could be handy for people building Internet radios.<p>'
	echo '                    <p><b>Note:</b></p>'
	echo '                    <ul>'
	echo '                      <li>Squeezelite must be running.</li>'
	echo '                      <li>LMS IP address is auto-discovered.</li>'
	echo '                      <li>Favorites must exist in LMS.</li>'
	echo '                      <li>Favorites must be at the top level.</li>'
	echo '                      <li>Folders will not be navigated.</li>'
	echo '                      <li>Maximum of 100 favorites.</li>'
	echo '                      <li>Favorite name can not have an "&" - Rename using LMS.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="'$ROWSHADE'">'
		echo '  <td colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $AUTOSTARTFAV: '$AUTOSTARTFAV'<br />'
		echo '                     [ DEBUG ] Controls MAC: '$(pcp_controls_mac_address)'<br />'
		echo '                     [ DEBUG ] LMS IP: '$(pcp_lmsip)'<br />'
		echo '                     [ DEBUG ] $FAVLIST: '$FAVLIST'</p>'
		echo '  </td>'
		echo '</tr>'
		echo '<!-- End of debug info -->'
	fi

	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="hidden" name="AUTOSTART" value="FAV"/>'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="submit" name="SUBMIT" value="Test">'
	[ $MODE -ge $MODE_BETA ] &&
	echo '                  <input type="submit" name="SUBMIT" value="Clear">'
	echo '                </td>'
	echo '              </tr>'

	echo '            </form>'
	echo '          </table>'

	#----------------------------------------------Autostart LMS-----------------------------
	# Decode variables using httpd, no quotes
	AUTOSTARTLMS=`sudo $HTTPD -d $AUTOSTARTLMS`

	echo '          <table class="bggrey percent100">'
	echo '            <form name="autostartlms" action="writetoautostart.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">Auto start LMS</td>'
	echo '                <td class="column420">'
	echo '                  <input class="large30" type="text" name="AUTOSTARTLMS" maxlength="254" value="'$AUTOSTARTLMS'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <input class="small1" type="radio" name="A_S_LMS" value="Enabled" '$A_S_LMS_Y'>Enabled'
	echo '                  <input class="small1" type="radio" name="A_S_LMS" value="Disabled" '$A_S_LMS_N'>Disabled'
	echo '                </td>'
	echo '              </tr>'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                </td>'
	echo '                <td colspan="2">'
	echo '                  <p>Cut and paste your auto start LMS command&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Allows you to set an auto start LMS command that is run after'
	echo '                       a "hard" power on. This field can contain any valid LMS CLI command.'
	echo '                       This could be handy for people building Internet radios.<p>'
	echo '                    <p><b>Example:</b></p>'
	echo '                    <ul>'
	echo '                      <li>randomplay tracks</li>'
	echo '                      <li>playlist play http://stream-tx1.radioparadise.com/aac-32</li>'
	echo '                      <li>playlist play http://radioparadise.com/m3u/aac-128.m3u</li>'
	echo '                    </ul>'
	echo '                    <p><b>Note:</b></p>'
	echo '                    <ul>'
	echo '                      <li>Squeezelite must be running.</li>'
	echo '                      <li>LMS IP address is auto-discovered.</li>'
	echo '                      <li>Do not include MAC address in CLI command.</li>'
	echo '                      <li>Maximum number of characters 254.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="'$ROWSHADE'">'
		echo '  <td colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $AUTOSTARTLMS: '$AUTOSTARTLMS'<br />'
		echo '                     [ DEBUG ] $A_S_LMS_Y: '$A_S_LMS_Y'<br />'
		echo '                     [ DEBUG ] $A_S_LMS_N: '$A_S_LMS_N'</p>'
		echo '  </td>'
		echo '</tr>'
		echo '<!-- End of debug info -->'
	fi

	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="hidden" name="AUTOSTART" value="LMS"/>'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="submit" name="SUBMIT" value="Test">'
	[ $MODE -ge $MODE_BETA ] &&
	echo '                  <input type="submit" name="SUBMIT" value="Clear">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'

	#----------------------------------------------------------------------------------------
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'

	[ $DEBUG -eq 1 ] && pcp_favorites
}
[ $MODE -ge $MODE_NORMAL ] && pcp_tweaks_auto_start

#========================================================================================
# Jivelite/Screen functions
#----------------------------------------------------------------------------------------
if [ $MODE -ge $MODE_NORMAL ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Jivelite Setup</legend>'
fi

#---------------------------------------Jivelite-----------------------------------------
# Function to download/install/delete Jivelite
#----------------------------------------------------------------------------------------
pcp_tweaks_jivelite() {
	case "$JIVELITE" in
		yes) JIVEyes="selected" ;;
		no) JIVEno="selected" ;;
	esac

	echo '          <table class="bggrey percent100">'
	echo '            <form name="jivelite" action= "writetojivelite.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Jivelite</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <select class="large16" name="JIVELITE">'
	echo '                    <option value="yes" '$JIVEyes'>Jivelite enabled</option>'
	echo '                    <option value="no" '$JIVEno'>Jivelite disabled</option>'
	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enable/disable Jivelite&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Allows to view and control piCorePlayer via Jivelite on an attached screen.</p>'
	echo '                    <p>Jivelite for piCorePlayer is add-on extension developed by Ralphy.<p>'
	echo '                    <p>A reboot after installation is needed.<p>'
	echo '                    <p><b>Note:</b> For the first configuration of Jivelite an attached keyboard or touch screen is needed.</p>'
	echo '                    <ul>'
	echo '                      <li>Jivelite enabled - Downloads and installs Jivelite.</li>'
	echo '                      <li>Jivelite disabled - Removes all traces of Jivelite.</li>'
	echo '                    </ul>'
	echo '                    <p>Jivelite may use all the free space which will prevent insitu upgrade from working.<p>'
	echo '                    <p>Installing Jivelite will also install the VU Meters.<p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="hidden" name="OPTION" value="JIVELITE">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	[ $MODE -ge $MODE_ADVANCED -a "$JIVELITE" = "yes" ] &&
	echo '                  <input type="submit" name="SUBMIT" value="Reset">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<p class="debug">[ DEBUG ] $JIVELITE: '$JIVELITE'<br />'
		echo '                 [ DEBUG ] $JIVEyes: '$JIVEyes'<br />'
		echo '                 [ DEBUG ] $JIVEno: '$JIVEno'</p>'
		echo '<!-- End of debug info -->'
	fi
}
[ $MODE -ge $MODE_NORMAL ] && pcp_tweaks_jivelite

#---------------------------------------VU Meters----------------------------------------
# Function to download/install/delete Jivelite VU Meters
#----------------------------------------------------------------------------------------
pcp_tweaks_vumeter() {

	LOADED_VU_METER=$( cat /mnt/mmcblk0p2/tce/onboot.lst | grep VU_Meter )

	echo '          <table class="bggrey percent100">'
	echo '            <form name="vumeter" action= "writetojivelite.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Jivelite VU Meter</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <select class="large16" name="VUMETER">'

	                          VUMETERS=$(ls /mnt/mmcblk0p2/tce/optional/ | grep VU_Meter | grep .tcz$ )
	                          for i in $VUMETERS
	                          do
	                            [ "$i" = "$LOADED_VU_METER" ] && SEL="selected" || SEL=""
	                            DISPLAY=$( echo $i | sed -e 's/^VU_Meter_//' -e 's/.tcz$//' -e 's/_/ /g' )
	                            echo '                    <option value="'$i'" '$SEL'>'$DISPLAY'</option>'
	                          done

	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Select Jivelite VU Meter (Joggler Skin only)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Allows you to select VU Meters from a dropdown list.</p>'
	echo '                    <p>Jivelite will restart after changing VU Meter.<p>'
	echo '                    <p>VU Meters have been sourced from various community members. Thank you.<p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="hidden" name="OPTION" value="VUMETER">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="submit" name="SUBMIT" value="Download">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'

	if [ $DEBUG -eq 1 ]; then
		#========================================================================================
		# Display debug information
		#----------------------------------------------------------------------------------------
		echo '<!-- Start of debug info -->'
		pcp_start_row_shade
		pcp_toggle_row_shade
		echo '           <table class="bggrey percent100">'
		echo '             <tr class="'$ROWSHADE'">'
		echo '               <td>'
		echo '                 <p class="debug">[ DEBUG ] Loop mounted extensions</p>'
		echo '               </td>'
		echo '             </tr>'
		pcp_toggle_row_shade
		echo '             <tr class="'$ROWSHADE'">'
		echo '               <td>'
		                       pcp_textarea_inform "none" "df | grep /dev/loop " 200
		echo '               </td>'
		echo '             </tr>'
		pcp_toggle_row_shade
		echo '             <tr class="'$ROWSHADE'">'
		echo '               <td>'
		echo '                 <p class="debug">[ DEBUG ] Installed extensions</p>'
		echo '               <td>'
		echo '             </tr>'
		pcp_toggle_row_shade
		echo '             <tr class="'$ROWSHADE'">'
		echo '               <td>'
		                       ls /usr/local/tce.installed >/tmp/installed.lst
		                       pcp_textarea_inform "none" "cat /tmp/installed.lst" 100
		echo '               </td>'
		echo '             </tr>'
		echo '           </table>'

		echo '<p class="debug">[ DEBUG ] $LOADED_VU_METER: '$LOADED_VU_METER'<br />'
		echo '                 [ DEBUG ] $DISPLAY: '$DISPLAY'<br />'
		echo '                 [ DEBUG ] $VUMETERS: '$VUMETERS'</p>'
		echo '<!-- End of debug info -->'
	fi
}
[ $MODE -ge $MODE_NORMAL ] && [ "$JIVELITE" = "yes" ] && pcp_tweaks_vumeter
#----------------------------------------------------------------------------------------

#---------------------------------------Screen rotate------------------------------------
pcp_tweaks_screenrotate() {
	case "$SCREENROTATE" in
		yes) SCREENyes="selected" ;;
		no) SCREENno="selected" ;;
	esac

	echo '          <table class="bggrey percent100">'
	echo '            <form name="screen_rotate" action="writetoscreenrotate.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Rotate screen</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <select class="large16" name="SCREENROTATE">'
	echo '                    <option value="yes" '$SCREENyes'>Rotate screen</option>'
	echo '                    <option value="no" '$SCREENno'>Default screen rotation</option>'
	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Rotate screen if upside down&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Allows to rotate piCorePlayer if upside down.</p>'
	echo '                    <p>A reboot after any change is needed.<p>'
	echo '                    <p><b>Note:</b> For some screen mounts piCorePlayer is shown upside down.</p>'
	echo '                    <ul>'
	echo '                      <li>Rotate screen - will flip the view 180 degrees.</li>'
	echo '                      <li>Default screen orientation.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<p class="debug">[ DEBUG ] $SCREENROTATE: '$SCREENROTATE'<br />'
		echo '                 [ DEBUG ] $SCREENyes: '$SCREENyes'<br />'
		echo '                 [ DEBUG ] $SCREENno: '$SCREENno'</p>'
		echo '<!-- End of debug info -->'
	fi
}
[ $MODE -ge $MODE_NORMAL ] && pcp_tweaks_screenrotate
#----------------------------------------------------------------------------------------

if [ $MODE -ge $MODE_NORMAL ]; then
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# IR Remote table
#----------------------------------------------------------------------------------------
pcp_tweaks_lirc() {
	pgrep lircd > /dev/null && IR_RUN=0

	if [ $IR_RUN -eq 0 ]; then
		IR_INDICATOR=$HEAVY_CHECK_MARK
		CLASS="indicator_green"
		STATUS="running"
	else
		IR_INDICATOR=$HEAVY_BALLOT_X
		CLASS="indicator_red"
		STATUS="not running"
	fi

	#----------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>LIRC remote control</legend>'

	#----------------------------------------------------------------------------------------
	# Function to check the IR_LIRC radio button according to config file
	#----------------------------------------------------------------------------------------
	case "$IR_LIRC" in
		yes) IR_LIRC_Y="checked" ;;
		no) IR_LIRC_N="checked" ;;
	esac

	echo '          <table class="bggrey percent100">'
	echo '            <form name="LIRC" action="lirc.cgi" method="get">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>IR remote control</p>'
	echo '                </td>'
	echo '                <td class="column100">'
	echo '                 <p class="'$CLASS'">'$IR_INDICATOR'</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>LIRC IR remote control is '$STATUS' &nbsp;&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Go to LIRC page to...</p>'
	echo '                    <p>Install/remove LIRC.</p>'
	echo '                    <p>Configure LIRC.</p>'
	echo '                    <p>Change GPIO number.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="LIRC page">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
	echo '          </table>'
	#----------------------------------------------------------------------------------------
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_BETA ] && pcp_tweaks_lirc
#----------------------------------------------------------------------------------------

#========================================================================================
# Audio tweaks
#----------------------------------------------------------------------------------------
pcp_tweaks_audio_tweaks() {
	# Function to check the SQUEEZELITE radio button according to config file
	case "$SQUEEZELITE" in
		yes) SQUEEZELITEyes="checked" ;;
		no) SQUEEZELITEno="checked" ;;
	esac

	# Function to check the SHAIRPORT radio button according to config file
	case "$SHAIRPORT" in
		yes) SHAIRPORTyes="checked" ;;
		no) SHAIRPORTno="checked" ;;
	esac

	# Function to check the ALSA radio button according to config file
	case "$ALSAlevelout" in
		Default) ALSAdefault="checked" ;;
		Custom) ALSAcustom="checked" ;;
	esac

	# Function to check the ALSA-EQ radio button according to config file
	case "$ALSAeq" in
		yes) ALSAeqyes="checked" ;;
		no) ALSAeqno="checked" ;;
	esac

	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="setaudiotweaks" action="writetoaudiotweak.cgi" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Audio tweaks</legend>'
	echo '            <table class="bggrey percent100">'

	#-------------------------------------------Squeezelite--------------------------------
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Squeezelite</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="SQUEEZELITE" value="yes" '$SQUEEZELITEyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="SQUEEZELITE" value="no" '$SQUEEZELITEno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Automatically start Squeezelite when pCP starts&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Enable or disable that Squeezelite starts automatically.</p>'
	echo '                    <p>If pCP is used as a LMS server or touch controler for other players it is not needed that Squeezelite starts.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="'$ROWSHADE'">'
		echo '  <td colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $SQUEEZELITE: '$SQUEEZELITE'<br />'
		echo '                     [ DEBUG ] $SQUEEZELITEyes: '$SQUEEZELITEyes'<br />'
		echo '                     [ DEBUG ] $SQUEEZELITEno: '$SQUEEZELITEno'</p>'
		echo '  </td>'
		echo '</tr>'
		echo '<!-- End of debug info -->'
	fi

	#-------------------------------------------Shairport--------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Shairport-sync</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="SHAIRPORT" value="yes" '$SHAIRPORTyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="SHAIRPORT" value="no" '$SHAIRPORTno'>No'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Use Shairport-sync to stream from iDevices&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Automatically start Shairport when pCP starts to stream audio from your iDevice.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="'$ROWSHADE'">'
		echo '  <td colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $SHAIRPORT: '$SHAIRPORT'<br />'
		echo '                     [ DEBUG ] $SHAIRPORTyes: '$SHAIRPORTyes'<br />'
		echo '                     [ DEBUG ] $SHAIRPORTno: '$SHAIRPORTno'</p>'
		echo '  </td>'
		echo '</tr>'
		echo '<!-- End of debug info -->'
	fi

	#-------------------------------------------ALSAlevelout---------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>ALSA output level</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="ALSAlevelout" value="Default" '$ALSAdefault'>Default'
	echo '                  <input class="small1" type="radio" name="ALSAlevelout" value="Custom" '$ALSAcustom'>Custom'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Custom option allows the ALSA output level to be restored after reboot&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Note: </b>Only necessary if you have changed the ALSA output level.</p>'
	echo '                    <p><b>Step:</b></p>'
	echo '                    <ol>'
	echo '                      <li>Login via ssh.</li>'
	echo '                      <li>Use "alsamixer" to set the ALSA output level.</li>'
	echo '                      <li>Save ALSA settings by typing "sudo alsactl store".</li>'
	echo '                      <li>Backup ALSA settings by typing "sudo filetool.sh -b".</li>'
	echo '                      <li>Select Custom option on this Tweak page.</li>'
	echo '                    <ol>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="'$ROWSHADE'">'
		echo '  <td colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $ALSAlevelout: '$ALSAlevelout'<br />'
		echo '                     [ DEBUG ] $ALSAdefault: '$ALSAdefault'<br />'
		echo '                     [ DEBUG ] $ALSAcustom: '$ALSAcustom'</p>'
		echo '  </td>'
		echo '</tr>'
		echo '<!-- End of debug info -->'
	fi

	#-------------------------------------ALSA Equalizer-------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>ALSA 10 band Equalizer</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="ALSAeq" value="yes" '$ALSAeqyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="ALSAeq" value="no" '$ALSAeqno'>No'
	echo '                </td>'
	echo '                <td>'

	if [ "$ALSAeq" = "yes" ]; then
		echo '                  <p><input type="button" name="CONFIG" onClick="location.href='\'''xtras_alsaequal.cgi''\''" value="Configure">&nbsp;'
	else
		echo '                  <p>'
	fi

	echo '                    Use 10 band ALSA equalizer&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Note: </b>Toggle ALSA Equalizer on off.</p>'
	echo '                    <p><b>Steps to manually adjust Equalizer settings:</b></p>'
	echo '                    <ol>'
	echo '                      <li>Login via ssh.</li>'
	echo '                      <li>Use "sudo alsamixer -D equal" and adjust the settings, press escape.</li>'
	echo '                      <li>Backup ALSA settings by typing "sudo filetool.sh -b" or use "Backup button" on the Main page.</li>'
	echo '                    <ol>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="'$ROWSHADE'">'
		echo '  <td colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $ALSAeq: '$ALSAeq'<br />'
		echo '                     [ DEBUG ] $ALSAeqno: '$ALSAeqno'<br />'
		echo '                     [ DEBUG ] $ALSAeqyes: '$ALSAeqyes'</p>'
		echo '  </td>'
		echo '</tr>'
		echo '<!-- End of debug info -->'
	fi

	#----------------------------------------------------------------------------------------
	pcp_start_row_shade
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_tweaks_audio_tweaks
#----------------------------------------------------------------------------------------

#========================================================================================
# USB audio tweaks
#----------------------------------------------------------------------------------------
pcp_tweaks_usb_audio_tweaks() {

	# Function to check the CMD radio button according to config file
	case "$CMD" in
		Default) CMDdefault="checked" ;;
		Slow) CMDslow="checked" ;;
	esac

	# Function to check the FSM radio button according to config file
	case "$FSM" in
		Default) FSMdefault="checked" ;;
		Disabled) FSMdisabled="checked" ;;
	esac

	# Function to select the FIQ-split radio button according to config file
	case "$FIQ" in
		0x1) selected1="selected" ;;
		0x2) selected2="selected" ;;
		0x3) selected3="selected" ;;
		0x4) selected4="selected" ;;
		0x7) selected5="selected" ;;
		0x8) selected6="selected" ;;
		0xf) selected7="selected" ;;
	esac

	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="usbaudiotweaks" action="writetoaudiotweak.cgi" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>USB Audio tweaks</legend>'
	echo '            <table class="bggrey percent100">'

	#-------------------------------------------dwc_otg.speed--------------------------------
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>OTG-Speed</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="CMD" value="Default" '$CMDdefault'>Default'
	echo '                  <input class="small1" type="radio" name="CMD" value="Slow" '$CMDslow'>dwc_otg.speed=1'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Fix C-Media based DACs by "dwc_otg.speed=1"&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Adds "dwc_otg.speed=1" to /mnt/mmcblk0p1/cmdline.txt</p>'
	echo '                    <p>The USB2.0 controller can have issues with USB1.1 audio devices, so this forces the controller into USB1.1 mode.</p>'
	echo '                    <p>Often needed for C-Media based DACs if sound is crackling.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="'$ROWSHADE'">'
		echo '  <td colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $CMD: '$CMD'<br />'
		echo '                     [ DEBUG ] $CMDdefault: '$CMDdefault'<br />'
		echo '                     [ DEBUG ] $CMDslow: '$CMDslow'</p>'
		echo '  </td>'
		echo '</tr>'
		echo '<!-- End of debug info -->'
	fi

	#-------------------------------------------dwc_otg.fiq_fsm_enable=0 ----------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>USB-FSM driver</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="FSM" value="Default" '$FSMdefault'>Default'
	echo '                  <input class="small1" type="radio" name="FSM" value="Disabled" '$FSMdisabled'>Disable USB-FSM'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Fix Emotiva XMC-1 DAC by "dwc_otg.fiq_fsm_enable=0"&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Adds "dwc_otg.fiq_fsm_enable=0" to /mnt/mmcblk0p1/cmdline.txt</p>'
	echo '                    <p>The USB controller can have issues with external DACs. If set to 0 the new FIQ_FSM driver is disabled and the old NOP FIQ is used.</p>'
	echo '                    <p>This is needed for Emotiva XMC-1 DAC.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="'$ROWSHADE'">'
		echo '  <td colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $FSM: '$CMD'<br />'
		echo '                     [ DEBUG ] $FSMdefault: '$FSMdefault'<br />'
		echo '                     [ DEBUG ] $FSMdisabled: '$FSMdisabled'</p>'
		echo '  </td>'
		echo '</tr>'
		echo '<!-- End of debug info -->'
	fi

	#-------------------------------------FIQ-Split acceleration-----------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>FIQ-Split acceleration</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <select class="large30" name="FIQ">'
	echo '                    <option value="0x1" '$selected1'>0x1 Accelerate non-periodic split transactions</option>'
	echo '                    <option value="0x2" '$selected2'>0x2 Accelerate periodic split transactions</option>'
	echo '                    <option value="0x3" '$selected3'>0x3 Accelerate all except high-speed isochronous transactions</option>'
	echo '                    <option value="0x4" '$selected4'>0x4 Accelerate high-speed isochronous transactions</option>'
	echo '                    <option value="0x7" '$selected5'>0x7 Accelerate all transactions [DEFAULT]</option>'
	echo '                    <option value="0x8" '$selected6'>0x8 Enable Interrupt/Control Split Transaction hack</option>'
	echo '                    <option value="0xf" '$selected7'>0xf Accelerate all transactions and Enable Interrupt/Control Split Transaction hack</option>'
	echo '                  </select>'
	echo '                </td>'
	echo '              </tr>'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>&nbsp;</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Change FIQ_FSM USB settings&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>This might solve USB audio problems.</li>'
	echo '                      <li>Important for specific USB DACs - like the Naim DAC-V1 card, try option 1, 2, 3 or 8.</li>'
	echo '                      <li>Reboot is needed.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="'$ROWSHADE'">'
		echo '  <td colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $FIQ: '$FIQ'<br />'
		echo '                     [ DEBUG ] $selected1: '$selected1'<br />'
		echo '                     [ DEBUG ] $selected2: '$selected2'<br />'
		echo '                     [ DEBUG ] $selected3: '$selected3'<br />'
		echo '                     [ DEBUG ] $selected4: '$selected4'<br />'
		echo '                     [ DEBUG ] $selected5: '$selected5'<br />'
		echo '                     [ DEBUG ] $selected6: '$selected6'</p>'
		echo '  </td>'
		echo '</tr>'
		echo '<!-- End of debug info -->'
	fi

	#----------------------------------------------------------------------------------------
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_tweaks_usb_audio_tweaks
#----------------------------------------------------------------------------------------

#-------------------------------------------Schedule CRON jobs---------------------------
#
#        *    *    *    *    *    command to be executed
#        -    -    -    -    -
#        |    |    |    |    |
#        |    |    |    |    +--- day of week (0 - 6) (Sunday=0)
#        |    |    |    +-------- month (1 - 12)
#        |    |    +------------- day of month (1 - 31)
#        |    +------------------ hour (0 - 23)
#        +----------------------- min (0 - 59)
#
#----------------------------------------------------------------------------------------
pcp_tweaks_cron() {
	case "$REBOOT" in
		Enabled) REBOOT_Y="checked" ;;
		Disabled) REBOOT_N="checked" ;;
	esac

	case "$RESTART" in
		Enabled) RESTART_Y="checked" ;;
		Disabled) RESTART_N="checked" ;;
	esac

	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="cronjob" action="writetocronjob.cgi" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Schedule CRON jobs</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column210">'
	echo '                  <p>Schedule piCorePlayer reboot<p>'
	echo '                </td>'
	echo '                <td class="column420">'
	echo '                  <label for="RB_H">Hour:</label>'
	echo '                  <input class="small2" type="text" name="RB_H" value="'$RB_H'" maxlength="2" pattern="^(2[0-3]|1[0-9]|[0-9]|\*)$" />'
	echo '                  <label for="RB_WD">&nbsp;&nbsp;Weekday (0-6):</label>'
	echo '                  <input class="small2" type="text" name="RB_WD" value="'$RB_WD'" maxlength="1" pattern="^([0-6]|\*)$" />'
	echo '                  <label for="RB_DMONTH">&nbsp;&nbsp;Day of Month:</label>'
	echo '                  <input class="small2" type="text" name="RB_DMONTH" value="'$RB_DMONTH'" maxlength="2" pattern="^(3[0-1]|2[0-9]|1[0-9]|[0-9]|\*)$" />'
	echo '                </td>'
	echo '                <td>'
	echo '                  <input class="small1" type="radio" name="REBOOT" value="Enabled" '$REBOOT_Y'>Enabled'
	echo '                  <input class="small1" type="radio" name="REBOOT" value="Disabled" '$REBOOT_N'>Disabled'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column210">'
	echo '                  <p>Schedule Squeezelite restart</p>'
	echo '                </td>'
	echo '                <td class="column420">'
	echo '                  <label for="RS_H">Hour:</label>'
	echo '                  <input class="small2" type="text" name="RS_H" value="'$RS_H'" maxlength="2" pattern="^(2[0-3]|1[0-9]|[0-9]|\*)$" />'
	echo '                  <label for="RS_WD">&nbsp;&nbsp;Weekday (0-6):</label>'
	echo '                  <input class="small2" type="text" name="RS_WD" value="'$RS_WD'" maxlength="1" pattern="^([0-6]|\*)$" />'
	echo '                  <label for="RS_DMONTH">&nbsp;&nbsp;Day of Month:</label>'
	echo '                  <input class="small2" type="text" name="RS_DMONTH" value="'$RS_DMONTH'" maxlength="2" pattern="^(3[0-1]|2[0-9]|1[0-9]|[0-9]|\*)$" />'
	echo '                </td>'
	echo '                <td>'
	echo '                  <input class="small1" type="radio" name="RESTART" value="Enabled" '$RESTART_Y'>Enabled'
	echo '                  <input class="small1" type="radio" name="RESTART" value="Disabled" '$RESTART_N'>Disabled'
	echo '                </td>'
	echo '              </tr>'

	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column210">'
	echo '                  <p></p>'
	echo '                </td>'
	echo '                <td colspan="2">'
	echo '                  <p>Fill out the crontab fields&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>"*" it means every hour, every day, every month.</p>'
	echo '                    <p><b>Example:</b></p>'
	echo '                    <ul>'
	echo '                      <li>2 * * - run job at 02:00 everyday</li>'
	echo '                      <li>0 1 * - run job at 00:00 every monday</li>'
	echo '                      <li>0 * 1 - run job at 00:00 the first every month</li>'
	echo '                    </ul>'
	echo '                    <p><b>Root crontab:</b></p>'
	echo '                    <textarea class="width600">'"$(cat /var/spool/cron/crontabs/root)"'</textarea>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">Custom Cron command</td>'
	echo '                <td>'
	echo '                  <input class="large60" type="text" name="CRON_COMMAND" value="'$CRON_COMMAND'" maxlength="254">'
	echo '                </td>'
	echo '              </tr>'

	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150"></td>'
	echo '                <td>'
	echo '                  <p>Add user defined commands to the cron scheduler&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This feature gives advanced users the possibility to manipulate the cron scheduler.'
	echo '                       It will allow users to add a single command to the cron job or'
	echo '                       to schedule a script that performs multiple actions.</p>'
	echo '                    <p>Use ordinary cron syntax.</p>'
	echo '                    <p><b>Example:</b></p>'
	echo '                    <ul>'
	echo '                      <li>1 1 * * * /path/to/your/script.sh</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan=3>'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="submit" name="SUBMIT" value="Reset">'
	[ $MODE -ge $MODE_BETA ] &&
	echo '                  <input type="submit" name="SUBMIT" value="Clear">'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="'$ROWSHADE'">'
		echo '  <td colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $REBOOT: '$REBOOT'<br />'
		echo '                     [ DEBUG ] $REBOOT_Y: '$REBOOT_Y'<br />'
		echo '                     [ DEBUG ] $REBOOT_N: '$REBOOT_N'<br />'
		echo '                     [ DEBUG ] $RESTART: '$RESTART'<br  />'
		echo '                     [ DEBUG ] $RESTART_Y: '$RESTART_Y'<br />'
		echo '                     [ DEBUG ] $RESTART_N: '$RESTART_N'<br />'
		echo '                     [ DEBUG ] $RB_H: '$RB_H'<br />'
		echo '                     [ DEBUG ] $RB_WD: '$RB_WD'<br />'
		echo '                     [ DEBUG ] $RB_DMONTH: '$RB_DMONTH'<br />'
		echo '                     [ DEBUG ] $RS_H: '$RS_H'<br />'
		echo '                     [ DEBUG ] $RS_WD: '$RS_WD'<br />'
		echo '                     [ DEBUG ] $RS_DMONTH: '$RS_DMONTH'<br />'
		echo '                     [ DEBUG ] $CRON_COMMAND: '$CRON_COMMAND'</p>'
		echo '  </td>'
		echo '</tr>'
		echo '<!-- End of debug info -->'
	fi

	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_tweaks_cron
#----------------------------------------------------------------------------------------

#----------------------------------------------User Commands-----------------------------
pcp_tweaks_user_commands() {
	# Decode variables using httpd, no quotes
	USER_COMMAND_1=$(sudo $HTTPD -d $USER_COMMAND_1)
	USER_COMMAND_1=$(echo $USER_COMMAND_1 | sed 's/"/\&quot;/g')

	USER_COMMAND_2=$(sudo $HTTPD -d $USER_COMMAND_2)
	USER_COMMAND_2=$(echo $USER_COMMAND_2 | sed 's/"/\&quot;/g')

	USER_COMMAND_3=$(sudo $HTTPD -d $USER_COMMAND_3)
	USER_COMMAND_3=$(echo $USER_COMMAND_3 | sed 's/"/\&quot;/g')

	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="setusercommands" action="writetoautostart.cgi" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>User commands</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">User command #1</td>'
	echo '                <td>'
	echo '                  <input class="large60"'
	echo '                         type="text"'
	echo '                         name="USER_COMMAND_1"'
	echo '                         value="'$USER_COMMAND_1'"'
	echo '                         maxlength="254"'
	echo '                         title="Invalid characters: &amp &quot"'
	echo '                         pattern="[^\&\x22]+"'
	echo '                  >'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">User command #2</td>'
	echo '                <td>'
	echo '                  <input class="large60"'
	echo '                         type="text"'
	echo '                         name="USER_COMMAND_2"'
	echo '                         value="'$USER_COMMAND_2'"'
	echo '                         maxlength="254"'
	echo '                         title="Invalid characters: &amp &quot"'
	echo '                         pattern="[^\&\x22]+"'
	echo '                  >'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">User command #3</td>'
	echo '                <td>'
	echo '                  <input class="large60"'
	echo '                         type="text"'
	echo '                         name="USER_COMMAND_3"'
	echo '                         value="'$USER_COMMAND_3'"'
	echo '                         maxlength="254"'
	echo '                         title="Invalid characters: &amp &quot"'
	echo '                         pattern="[^\&\x22]+"'
	echo '                  >'
	echo '                </td>'
	echo '              </tr>'

	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150"></td>'
	echo '                <td>'
	echo '                  <p>Adds user defined commands to the piCorePlayer startup procedure&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This feature gives advanced users a couple of hooks into the startup procedure.'
	echo '                       It will allow advanced users the ability to run extra instances of Squeezelite for example,'
	echo '                       or maybe, run a Linux procedure that shuts down processes, like the web server to optimise performance.</p>'
	echo '                    <p>User commands run after auto start LMS commands and auto start favorites.</p>'
	echo '                    <p>User commands will run in order 1, 2, 3.</p>'
	echo '                    <p><b>Example:</b></p>'
	echo '                    <ul>'
	echo '                      <li>ls /tmp >> /tmp/directory.log</li>'
	echo '                    </ul>'
	echo '                    <p><b>Invalid characters:</b> &amp; &quot;</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan=2>'
	echo '                  <input type="hidden" name="AUTOSTART" value="CMD"/>'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="submit" name="SUBMIT" value="Clear">'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="'$ROWSHADE'">'
		echo '  <td colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $USER_COMMAND_1: '$USER_COMMAND_1'<br />'
		echo '                     [ DEBUG ] $USER_COMMAND_2: '$USER_COMMAND_2'<br />'
		echo '                     [ DEBUG ] $USER_COMMAND_3: '$USER_COMMAND_3'</p>'
		echo '  </td>'
		echo '</tr>'
		echo '<!-- End of debug info -->'
	fi

	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_tweaks_user_commands
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
pcp_footer
[ $MODE -ge $MODE_NORMAL ] && pcp_mode
pcp_copyright
set +f
echo '</body>'
echo '</html>'