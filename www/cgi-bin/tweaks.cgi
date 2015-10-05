#!/bin/sh

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

#=========================================================================================
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>General tweaks</legend>'

#----------------------------------------------Hostname---------------------------------
pcp_tweaks_hostname() {
	pcp_incr_id
	echo '          <table class="bggrey percent100">'
	echo '            <form name="squeeze" action="writetohost.cgi" method="get">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">Host name</td>'
	echo '                <td class="column210">'
	echo '                  <input class="large16" type="text" name="HOST" value="'$HOST'" maxlength="26" pattern="^[a-zA-Z0-9-]*$">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Provide a host name, so the player is easier to identify on your LAN&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Note: </b>This is the linux hostname, not the piCorePlayer name used by LMS.</p>'
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

#---------------------------------------Jivelite-----------------------------------------
# Function to check the radio button according to config.cfg file
#----------------------------------------------------------------------------------------
pcp_tweaks_jivelite() {
	case "$JIVELITE" in
		YES) JIVEyes="selected" ;;
		NO) JIVEno="selected" ;;
	esac

	pcp_incr_id
	echo '          <table class="bggrey percent100">'
	echo '            <form name="jivelite" action= "writetojivelite.cgi" method="get">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Jivelite</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <select class="large16" name="JIVELITE">'
	echo '                    <option value="YES" '$JIVEyes'>Jivelite enabled</option>'
	echo '                    <option value="NO" '$JIVEno'>Jivelite disabled</option>'
	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enable/disable Jivelite&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Allows to view and control piCorePlayer via Jivelite on an attached screen.</p>'
	echo '                    <p>A reboot after installation is needed.<p>'
	echo '                    <p><b>Note:</b> For the first configuration of Jivelite an attached keyboard is needed.</p>'
	echo '                    <ul>'
	echo '                      <li>Jivelite enabled - Downloads and installs Jivelite.</li>'
	echo '                      <li>Jivelite disabled - Removes all traces of Jivelite.</li>'
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

	if [ $DEBUG = 1 ]; then
		echo '<p class="debug">[ DEBUG ] $JIVELITE: '$JIVELITE'<br />'
		echo '                 [ DEBUG ] $JIVEyes: '$JIVEyes'<br />'
		echo '                 [ DEBUG ] $JIVEno: '$JIVEno'</p>'
	fi
}
[ $MODE -ge $MODE_NORMAL ] && pcp_tweaks_jivelite
#----------------------------------------------------------------------------------------

#---------------------------------------Screen rotate-----------------------------------------
# Function to check the radio button according to config.cfg file
#----------------------------------------------------------------------------------------
pcp_tweaks_screenrotate() {
	case "$SCREENROTATE" in
		YES) SCREENyes="selected" ;;
		NO) SCREENno="selected" ;;
	esac

	pcp_incr_id
	echo '          <table class="bggrey percent100">'
	echo '            <form name="screen_rotate" action= "writetoscreenrotate.cgi" method="get">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Rotate screen</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <select class="large16" name="SCREENROTATE">'
	echo '                    <option value="YES" '$SCREENyes'>Rotate screen</option>'
	echo '                    <option value="NO" '$SCREENno'>Default screen rotattion</option>'
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

	if [ $DEBUG = 1 ]; then
		echo '<p class="debug">[ DEBUG ] $SCREENROTATE: '$SCREENROTATE'<br />'
		echo '                 [ DEBUG ] $SCREENyes: '$SCREENyes'<br />'
		echo '                 [ DEBUG ] $SCREENno: '$SCREENno'</p>'
	fi
}
[ $MODE -ge $MODE_NORMAL ] && pcp_tweaks_screenrotate
#----------------------------------------------------------------------------------------

#---------------------------------------Overclock----------------------------------------
# Function to check the radio button according to config.cfg file
#----------------------------------------------------------------------------------------
pcp_tweaks_overclock() {
	if [ $(pcp_rpi_is_model_2B) = 1 ] || [ $MODE -ge $MODE_BETA ] ; then
		case "$OVERCLOCK" in
			NONE) OCnone="selected" ;;
			MILD) OCmild="selected" ;;
			MODERATE) OCmoderate="selected" ;;
		esac

		#----------------------------------------------------------------------------------------
		pcp_incr_id
		echo '          <table class="bggrey percent100">'
		echo '            <form name="overclock" action= "writetooverclock.cgi" method="get">'
		pcp_start_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150">'
		echo '                  <p>Overclock</p>'
		echo '                </td>'
		echo '                <td class="column210">'
		echo '                  <select class="large16" name="OVERCLOCK">'
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
		echo '                  <input type="submit" name="SUBMIT" value="Save">'
		[ $MODE -ge $MODE_BETA ] &&
		echo '                  <input class="large16" type="button" name="ADVANCED_OVERCLOCK" onClick="location.href='\'''xtras_overclock.cgi''\''" value="Advanced Overclock">'
		echo '                </td>'
		echo '              </tr>'
		echo '            </form>'
		echo '          </table>'

		if [ $DEBUG = 1 ]; then
			echo '<p class="debug">[ DEBUG ] $OVERCLOCK: '$OVERCLOCK'<br />'
			echo '                 [ DEBUG ] $OCnone: '$OCnone'<br />'
			echo '                 [ DEBUG ] $OCmild: '$OCmild'<br />'
			echo '                 [ DEBUG ] $OCmoderate: '$OCmoderate'</p>'

			case $OVERCLOCK in
				NONE)
					echo '<p class="debug">[ DEBUG ] arm_freq=700<br />'
					echo '                 [ DEBUG ] core_freq=250<br />'
					echo '                 [ DEBUG ] sdram_freq=400<br />'
					echo '                 [ DEBUG ] force_turbo=1</p>'
					;;
				MILD)
					echo '<p class="debug">[ DEBUG ] arm_freq=800<br />'
					echo '                 [ DEBUG ] core_freq=250<br />'
					echo '                 [ DEBUG ] sdram_freq=400<br />'
					echo '                 [ DEBUG ] force_turbo=1</p>'
					;;
				MODERATE)
					echo '<p class="debug">[ DEBUG ] arm_freq=900<br />'
					echo '                 [ DEBUG ] core_freq=333<br />'
					echo '                 [ DEBUG ] sdram_freq=450<br />'
					echo '                 [ DEBUG ] force_turbo=0</p>'
					;;
			esac
		fi
	fi

}
[ $MODE -ge $MODE_NORMAL ] && pcp_tweaks_overclock
#----------------------------------------------------------------------------------------

#----------------------------------------------Timezone----------------------------------
pcp_tweaks_timezone() {
	pcp_incr_id
	echo '          <table class="bggrey percent100">'
	echo '            <form name="tzone" action="writetotimezone.cgi" method="get">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">Timezone</td>'
	echo '                <td class="column210">'
	echo '                  <input class="large16" type="text" name="TIMEZONE" value="'$TIMEZONE'" maxlength="28" pattern="^[a-zA-Z0-9-,./]*$">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Add or change your timezone&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Format: EST-10EST,M10.1.0,M4.1.0/3</p>'
	echo '                    <p>Your timezone should be automatically populated.</p>'
	echo '                    <p>If not, cut and paste your timezone from your favourite timezone location.</p>'
	echo '                    <p>Example:</p>'
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
# Change password - STILL UNDER DEVELOPMENT
# Note: changing passwords through a script over html is not very secure.
#----------------------------------------------------------------------------------------
pcp_tweaks_password() {
	pcp_incr_id
	echo '          <table class="bggrey percent100">'
	echo '            <form name="password" action="changepassword.cgi" method="get">'
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
	echo '                    <p>Default: piCore</p>'
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

#----------------------------------------------------------------------------------------
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

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

	# Decode variables using httpd, no quotes
	AUTOSTARTFAV=`sudo $HTPPD -d $AUTOSTARTFAV`

	pcp_incr_id
	echo '          <table class="bggrey percent100">'
	echo '            <form name="autostartfav" action="writetoautostart.cgi" method="get">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">Auto start favorite</td>'
	echo '                <td class="column420">'
	echo '                  <select class="large30" name="AUTOSTARTFAV">'

	# Generate a list of options
	FAVLIST=`( echo "$(pcp_controls_mac_address) favorites items 0 100"; echo "exit" ) | nc $(pcp_lmsip) 9090 | sed 's/ /\+/g'`
	FAVLIST=`sudo $HTPPD -d $FAVLIST`
	echo $FAVLIST | awk -v autostartfav="$AUTOSTARTFAV" '
	BEGIN {
		RS="id:"
		FS=":"
		i = 0
	}
	# Main
	{
		i++
		split($1,a," ")
		id[i]=a[1]
		split(id[i],b,".")
		num[i]=b[2]
		name[i]=$2
		gsub(" type","",name[i])
		sel[i]=""
		if ( name[i] == autostartfav ) {
			sel[i]="selected"
		}
		hasitems[i]=$5
		gsub("count","",hasitems[i])
		if ( hasitems[i] != "0 " ) {
			i--
		}
	}
	END {
		for (j=1; j<=i; j++) {
			printf "                    <option value=\"%s\" id=\"%10s\" %s>%s - %s</option>\n",name[j],id[j],sel[j],num[j],name[j]
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
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG = 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="even">'
		echo '  <td  colspan="3">'
		echo '    <p class="debug">[ DEBUG ] Controls MAC: '$(pcp_controls_mac_address)'<br />'
		echo '                     [ DEBUG ] LMS IP: '$(pcp_lmsip)'<br />'
		echo '                     [ DEBUG ] $FAVLIST: '$FAVLIST'</p>'
		echo '    <textarea class="inform">'
		            ifconfig
		echo '    </textarea>'
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
	AUTOSTARTLMS=`sudo $HTPPD -d $AUTOSTARTLMS`

	pcp_incr_id
	echo '          <table class="bggrey percent100">'
	echo '            <form name="autostartlms" action="writetoautostart.cgi" method="get">'
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

	[ $DEBUG = 1 ] && pcp_favorites
}
[ $MODE -ge $MODE_NORMAL ] && pcp_tweaks_auto_start
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
# Determine state of check boxes.
#----------------------------------------------------------------------------------------
pcp_tweaks_audio_tweaks() {
	# Function to check the CMD-radio button according to config file
	case "$CMD" in
		Default) CMDdefault="checked" ;;
		Slow) CMDslow="checked" ;;
	esac

	# Function to select the FIQ-split radio button according to config file
	case "$FIQ" in
		0x1) selected1="selected" ;;
		0x2) selected2="selected" ;;
		0x3) selected3="selected" ;;
		0x4) selected4="selected" ;;
		0x7) selected5="selected" ;;
		0x8) selected6="selected" ;;
	esac

	# Function to check the ALSA-radio button according to config file
	case "$ALSAlevelout" in
		Default) ALSAdefault="checked" ;;
		Custom) ALSAcustom="checked" ;;
	esac

	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="setaudiotweaks" action="writetoaudiotweak.cgi" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Audio tweaks</legend>'
	echo '            <table class="bggrey percent100">'

	#-------------------------------------------dwc_otg.speed--------------------------------
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
	echo '                  <p>Set "dwc_otg.speed=1"&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Adds "dwc_otg.speed=1" to /mnt/mmcblk0p1/cmdline.txt</p>'
	echo '                    <p>The USB2.0 controller can have issues with USB1.1 audio devices, so this forces the controller into USB1.1 mode.</p>'
	echo '                    <p>Often needed for C-Media based DACs if sound is crackling.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG = 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="even">'
		echo '  <td  colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $CMD: '$CMD'<br />'
		echo '                     [ DEBUG ] $CMDdefault: '$CMDdefault'<br />'
		echo '                     [ DEBUG ] $CMDslow: '$CMDslow'</p>'
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

	if [ $DEBUG = 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="odd">'
		echo '  <td  colspan="3">'
		echo '    <p class="debug">[ DEBUG ] $ALSAlevelout: '$ALSAlevelout'<br />'
		echo '                     [ DEBUG ] $ALSAdefault: '$ALSAdefault'<br />'
		echo '                     [ DEBUG ] $ALSAcustom: '$ALSAcustom'</p>'
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

	if [ $DEBUG = 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="even">'
		echo '  <td  colspan="3">'
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

	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                </td>'
	echo '              </tr>'

	#----------------------------------------------------------------------------------------
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

	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="cronjob" action="writetocronjob.cgi" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Schedule CRON jobs</legend>'
	echo '            <table class="bggrey percent100">'
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
	echo '                  <input class="small2" type="text" name="RS_DMONTH" value="'$RS_DMONTH'" maxlength="2" pattern="^(3[0-1]|2[0-9]|1[0-9]|[0-9]|\*)$"  />'
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
	echo '                  <input class="large36" type="text" name="CRON_COMMAND" value="'$CRON_COMMAND'" maxlength="254">'
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

	if [ $DEBUG = 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<tr class="odd">'
		echo '  <td  colspan="3">'
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

#----------------------------------------------User Commands---------------------------------
pcp_tweaks_user_commands() {
	# Decode variables using httpd, no quotes
	USER_COMMAND_1=`sudo $HTPPD -d $USER_COMMAND_1`
	USER_COMMAND_2=`sudo $HTPPD -d $USER_COMMAND_2`
	USER_COMMAND_3=`sudo $HTPPD -d $USER_COMMAND_3`

	pcp_incr_id
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="setusercommands" action="writetoautostart.cgi" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>User commands</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">User command #1</td>'
	echo '                <td>'
	echo '                  <input class="large36" type="text" name="USER_COMMAND_1" value="'$USER_COMMAND_1'" maxlength="254">'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">User command #2</td>'
	echo '                <td>'
	echo '                  <input class="large36" type="text" name="USER_COMMAND_2" value="'$USER_COMMAND_2'" maxlength="254">'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">User command #3</td>'
	echo '                <td>'
	echo '                  <input class="large36" type="text" name="USER_COMMAND_3" value="'$USER_COMMAND_3'" maxlength="254">'
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
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan=2>'
	echo '                  <input type="hidden" name="AUTOSTART" value="CMD"/>'
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
[ $MODE -ge $MODE_NORMAL ] && pcp_tweaks_user_commands
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
[ $DEBUG = 1 ] && pcp_show_config_cfg

pcp_footer
[ $MODE -ge $MODE_NORMAL ] && pcp_mode
pcp_copyright
set +f
echo '</body>'
echo '</html>'