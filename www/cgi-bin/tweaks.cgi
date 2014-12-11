#!/bin/sh

# Version: 0.06 2014-12-09 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.05 2014-10-02 GE
#	Activated $MODE=5 for AUTOSTARTLMS.

# Version: 0.04 2014-09-10 GE
#   Added reformatted html.

# Version: 0.03 2014-09-09 GE
#   Added Auto start LMS command.

# Version: 0.02 2014-09-06 SBP
#   Added cronjob.

# Version: 0.01 2014-08-06 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Tweaks" "SBP"

pcp_controls
pcp_banner
pcp_navigation

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '      <fieldset>'
echo '      <legend>General tweaks</legend>'

#----------------------------------------------Host name---------------------------------
echo '      <table class="bggrey percent100">'
echo '        <form name="squeeze" action="writetohost.cgi" method="get">'

echo '          <tr class="even">'
echo '            <td class="column150">Host name</td>'
echo '            <td class="column210">'
echo '              <input class="large16" type="text" id="HOST" name="HOST" size="32" maxlength="26" value="'$HOST'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Provide a host name, so the player is easier to identify on your LAN.</p>'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td colspan=3>'
echo '              <input type="submit" name="submit" value="Save">'
echo '            </td>'
echo '          </tr>'

echo '        </form>'
echo '      </table>'
echo '      <br />'

#----------------------------------------------Overclock---------------------------------
# Function in order to check the radiobutton according to what is present in config file
case "$OVERCLOCK" in 
	NONE)
		OCnone="selected"
		;;
	MILD)
		OCmild="selected"
		;;
	MODERATE)
		OCmoderate="selected"
		;;
	*)
		OCnone=""
		OCmild=""
		OCmoderate=""
		;;
esac

if [ $DEBUG = 1 ]; then 
	echo '<p class="debug">[ DEBUG ] $OVERCLOCK: '$OVERCLOCK'<br />'
	echo '                 [ DEBUG ] $OCnone: '$OCnone'<br />'
	echo '                 [ DEBUG ] $OCmild: '$OCmild'<br />'
	echo '                 [ DEBUG ] $OCmoderate: '$OCmoderate'</p>'
fi

echo '      <table class="bggrey percent100">'
echo '        <form name="overclock" action= "writetooverclock.cgi" method="get">'

echo '          <tr class="even">'
echo '            <td class="column150"><p>Overclock</p></td>'
echo '            <td class="column210">'
echo '              <select name="OVERCLOCK">'
echo '                <option value="NONE" '$OCnone'> No overclocking </option>'
echo '                <option value="MILD" '$OCmild'> Mild overclocking </option>'
echo '                <option value="MODERATE" '$OCmoderate'> Moderate overclocking </option>'
echo '              </select>'
echo '            </td>'
echo '            <td>'
echo '              <p>Change overclocking - If you fail to boot, then hold down the shift key during booting. '
echo '                 Or you might have to edit the config.txt file manually.'
echo '                 Reboot is needed.<p>'
echo '            </td>'
echo '          </tr>'

echo '          <tr>'
echo '            <td colspan="3">'
echo '              <input type="submit" name="submit" value="Save">'
echo '            </td>'
echo '          </tr>'

echo '        </form>'
echo '      </table>'
echo '      <br />'

#----------------------------------------------Timezone----------------------------------
[ -f /etc/sysconfig/timezone ] && . /etc/sysconfig/timezone

echo '      <table class="bggrey percent100">'
echo '        <form name="tzone" action="writetotimezone.cgi" method="get">'

echo '          <tr class="even">'
echo '            <td class="column150">Timezone</td>'
echo '            <td class="column210">'
echo '              <input class="large16" type="text" id="TIMEZONE" name="TIMEZONE" size="32" maxlength="26" value="'$TZ'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Cut and paste your TIMEZONE from this <a href="http://wiki.openwrt.org/doc/uci/system#time.zones" target="_blank">list</a>.</p>'
echo '            </td>'
echo '          </tr>'

echo '          <tr>'
echo '            <td colspan=2 >'
echo '              <input type="submit" name="submit" value="Save">'
echo '            </td>'
echo '          </tr>'

echo '        </form>'
echo '      </table>'
echo '      <br />'

#----------------------------------------------Password----------------------------------
# Change password - STILL UNDER DEVELOPMENT
# Note: changing passwords through a script over html is not very secure.
#----------------------------------------------------------------------------------------
echo '      <table class="bggrey percent100">'
echo '        <form name="password" action="changepassword.cgi" method="get">'

echo '          <tr class="even">'
echo '            <td class="column150">Password for "'$(pcp_tc_user)'"</td>'
echo '            <td class="column210">'
echo '              <input class="large16" type="password" id="NEWPASSWORD" name="NEWPASSWORD" size="32" maxlength="26">'
echo '            </td>'
echo '            <td>'
echo '              <p>Enter new password.</p>'
echo '            </td>'
echo '          </tr>'

echo '          <tr class="even">'
echo '            <td class="column150"></td>'
echo '            <td class="column210">'
echo '              <input class="large16" type="password" id="CONFIRMPASSWORD" name="CONFIRMPASSWORD" size="32" maxlength="26">'
echo '            </td>'
echo '            <td>'
echo '              <p>Confirm new password.</p>'
echo '            </td>'
echo '          </tr>'

echo '          <tr>'
echo '            <td colspan=3>'
echo '              <input type="submit" name="submit" value="Save">'
echo '            </td>'
echo '          </tr>'

echo '        </form>'
echo '      </table>'
echo '      <br />'

#----------------------------------------------Autostart LMS-----------------------------
# Decode variables using httpd, no quotes
if [ $MODE -gt 4 ]; then
	AUTOSTARTLMS=`sudo /usr/local/sbin/httpd -d $AUTOSTARTLMS`

	echo '      <table class="bggrey percent100">'
	echo '        <form name="autostartlms" action="writetoautostartlms.cgi" method="get">'

	echo '          <tr class="even">'
	echo '            <td class="column150">Auto start LMS</td>'
	echo '            <td class="column210">'
	echo '              <input class="large16" type="text" id="AUTOSTARTLMS" name="AUTOSTARTLMS" size="100" maxlength="254" value="'$AUTOSTARTLMS'">'
	echo '            </td>'
	echo '            <td>'
	echo '              <p>Cut and paste your auto start LMS command.</p>'
	echo '            </td>'
	echo '          </tr>'

	echo '          <tr>'
	echo '            <td colspan="3">'
	echo '              <input type="submit" name="submit" value="Save">'
	echo '            </td>'
	echo '          </tr>'

	echo '        </form>'
	echo '      </table>'
fi

#----------------------------------------------------------------------------------------
echo '      </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

if [ $DEBUG = 1 ]; then 
	echo '<h1>[ INFO ] Current overclocking settings</h1>'

	case $OVERCLOCK in
		NONE)
			echo '<p class="info">Overclocking is: '$OVERCLOCK'<br /><br />'
			echo '                arm_freq=700<br />'
			echo '                core_freq=250<br />'
			echo '                sdram_freq=400<br />'
			echo '                force_turbo=1</p>'
			;;
		MILD)
			echo '<p class="info">Overclocking is: '$OVERCLOCK'<br /><br />'
			echo '                arm_freq=800<br />' 
			echo '                core_freq=250<br />'
			echo '                sdram_freq=400<br />'
			echo '                force_turbo=1</p>'
			;;
		MODERATE)
			echo '<p class="info">Overclocking is: '$OVERCLOCK'<br /><br />'
			echo '                arm_freq=900<br />'
			echo '                core_freq=333<br />'
			echo '                sdram_freq=450<br />'
			echo '                force_turbo=0</p>'
			;;
	esac
fi

# Function to check the CMD-radio button according to config file
case "$CMD" in 
	Default)
		CMDdefault="checked"
		;;
	Slow)
		CMDslow="checked"
		;;
	*)
		CMDdefault=""
		CMDslow=""
		;;
esac

if [ $DEBUG = 1 ]; then 
	echo '<p class="debug">[ DEBUG ] $CMD: '$CMD'<br />'
	echo '                 [ DEBUG ] $CMDdefault: '$CMDdefault'<br />'
	echo '                 [ DEBUG ] $CMDslow: '$CMDslow'</p>'
fi

# Function to check the FIQ-split radio button according to config file

if [ $FIQ = 0x1 ]; then selected1="selected"; else selected1=""; fi
if [ $FIQ = 0x2 ]; then selected2="selected"; else selected2=""; fi
if [ $FIQ = 0x3 ]; then selected3="selected"; else selected3=""; fi
if [ $FIQ = 0x4 ]; then selected4="selected"; else selected4=""; fi
if [ $FIQ = 0x7 ]; then selected5="selected"; else selected5=""; fi
if [ $FIQ = 0x8 ]; then selected6="selected"; else selected6=""; fi

if [ $DEBUG = 1 ]; then 
	echo '<p class="debug">[ DEBUG ] $FIQ: '$FIQ'<br />'
	echo '                 [ DEBUG ] $selected1: '$selected1'<br />'
	echo '                 [ DEBUG ] $selected2: '$selected2'<br />'
	echo '                 [ DEBUG ] $selected3: '$selected3'<br />'
	echo '                 [ DEBUG ] $selected4: '$selected4'<br />'
	echo '                 [ DEBUG ] $selected5: '$selected5'<br />'
	echo '                 [ DEBUG ] $selected6: '$selected6'</p>'
fi

# Function to check the ALSA-radio button according to config file
case "$ALSAlevelout" in 
	Default)
		ALSAdefault="checked"
		;;
	Custom)
		ALSAcustom="checked"
		;;
	*)
		ALSAdefault=""
		ALSAcustom=""
		;;
esac

if [ $DEBUG = 1 ]; then 
	echo '<p class="debug">[ DEBUG ] $ALSAlevelout: '$ALSAlevelout'<br />'
	echo '                 [ DEBUG ] $ALSAdefault: '$ALSAdefault'<br />'
	echo '                 [ DEBUG ] $ALSAcustom: '$ALSAcustom'</p>'
fi

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="setaudiotweaks" action="writetoaudiotweak.cgi" method="get">'
echo '      <div class="row">'
echo '      <fieldset>'
echo '        <legend>Audio tweaks</legend>'
echo '        <table class="bggrey percent100">'

echo '          <tr class="even">'
echo '            <td class="column150">'
echo '               <p>OTG-Speed</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="small1" type="radio" name="CMD" id="not enabled" value="Default" '$CMDdefault'>Default'
echo '              <input class="small1" type="radio" name="CMD" id="Custom" value="Slow" '$CMDslow'>dwc_otg.speed=1'
echo '            </td>'
echo '            <td>'
echo '              <p>Often needed for C-Media based DACs, try to use "dwc_otg.speed=1" if sound is crackling.</p>'
echo '            </td>'
echo '          </tr>'

echo '          <tr class="odd">'
echo '            <td class="column150">'
echo '              <p>ALSA output level</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="small1" type="radio" name="ALSAlevelout" id="Default" value="Default" '$ALSAdefault'>Default'
echo '              <input class="small1" type="radio" name="ALSAlevelout" id="Custom" value="Custom" '$ALSAcustom'>Custom'
echo '            </td>'
echo '            <td>'
echo '              <p>Use only if you have changed ALSA output level via ALSA-mixer, allows custom output level after reboot.'
echo '              <span style="color:blue;" title="Use alsamixer via SHH, and save your custom settings by sudo amixer store">HELP</span><p>'
echo '            </td>'
echo '          </tr>'

echo '          <tr class="even">'
echo '            <td class="column150">'
echo '              <p>FIQ-Split acceleration</p>'
echo '            </td>'
echo '            <td>'
echo '              <select name="FIQ">'
echo '                <option value="0x1" '$selected1'> 1. Accelerate non-periodic split transactions - Value 0x1 </option>'
echo '                <option value="0x2" '$selected2'> 2. Accelerate periodic split transactions - Value 0x2 </option>'
echo '                <option value="0x3" '$selected3'> 3. Accelerate all except high-speed isochronous transactions - Value 0x3 </option>'
echo '                <option value="0x4" '$selected4'> 4. Accelerate high-speed isochronous transactions - Value 0x4 </option>'
echo '                <option value="0x7" '$selected5'> 5. Accelerate all transactions DEFAULT - Value 0x7 </option>'
echo '                <option value="0x8" '$selected6'> 6. Enable Interrupt/Control Split Transaction hack - Value 0x8 </option>'
echo '              </select>'
echo '            </td>'
echo '          </tr>'
echo '          <tr class="even">'
echo '            <td class="column150">'
echo '              <p>&nbsp;</p>'
echo '            </td>'
echo '            <td>'
echo '              <p>Change FIQ_FSM USB settings. This might solve USB audio problems. Important for specific USB-DACs'
echo '                 - like the Naim DAC-V1 card, try option 1, 2, 3 or 8. Reboot is needed.</p>'
echo '            </td>'
echo '          </tr>'

echo '          <tr class="odd">'
echo '            <td colspan=3>'
echo '              <input type="submit" name="submit" value="Save">'
echo '            </td>'
echo '          </tr>'

echo '        </table>'
echo '      </fieldset>'
echo '      </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

# Info section:
if [ $DEBUG = 1 ]; then
	echo '<h1>[ INFO ] Current ALSA output level</h1>'
	case $ALSAlevelout in
		Default)
			echo '<p class="info">Default - ALSA output level is used<br /></p>'
			;;
		Custom)
			echo '<p class="info">Custom - ALSA output level will be defined from your custom settings.<br /></p>'
			;;
	esac

	echo '<h1>[ INFO ] Current FIG-split acceleration settings</h1>'
	case $FIQ in
		0x1)
			echo '<p class="info">FIQ-split value is: '$FIQ'<br />'
			echo '                Accelerate non-periodic split transactions</p>'
			;;
		0x2)
			echo '<p class="info">FIQ-split value is: '$FIQ'<br />'
			echo '                Accelerate periodic split transactions</p>'
			;;
		0x3)
			echo '<p class="info">FIQ-split value is: '$FIQ'<br />'
			echo '                Accelerate all except high-speed isochronous transactions</p>'
			;;
		0x4)
			echo '<p class="info">FIQ-split value is: '$FIQ'<br />'
			echo '                Accelerate high-speed isochronous transactions</p>'
			;;
		0x7)
			echo '<p class="info">FIQ-split value is: '$FIQ'<br />'
			echo '                Accelerate all transactions - DEFAULT</p>'
			;;
		0x8)
			echo '<p class="info">FIQ-split value is: '$FIQ'<br />'
			echo '                Enable Interrupt/Control Split Transaction hack</p>'
			;;
		*)
			echo '<p class="error">FIQ-split value is: INVALID</p>'
			;;
	esac
fi

#========================================================================================
# Function to check the CRON Job schedule according to config file
#----------------------------------------------------------------------------------------
pcp_variables

if [ $REBOOT = Enabled ]; then REBOOT_Y="checked"; else REBOOT_Y=""; fi
if [ $REBOOT = Disabled ]; then REBOOT_N="checked"; else REBOOT_N=""; fi
if [ $RESTART = Enabled ]; then RESTART_Y="checked"; else RESTART_Y=""; fi
if [ $RESTART = Disabled ]; then RESTART_N="checked"; else RESTART_N=""; fi

if [ $DEBUG = 1 ]; then 
	echo '<p class="debug">[ DEBUG ] $REBOOT: '$REBOOT'<br />'
	echo '                 [ DEBUG ] $REBOOT_Y: '$REBOOT_Y' <br />'
	echo '                 [ DEBUG ] $REBOOT_N: '$REBOOT_N' <br />'
	echo '                 [ DEBUG ] $RESTART: '$RESTART'<br  />'
	echo '                 [ DEBUG ] $RESTART_Y: '$RESTART_Y' <br />'
	echo '                 [ DEBUG ] $RESTART_N: '$RESTART_N' <br />'
	echo '                 [ DEBUG ] $RB_H: '$RB_H' <br />'
	echo '                 [ DEBUG ] $RB_WD: '$RB_WD' <br />'
	echo '                 [ DEBUG ] $RB_DMONTH: '$RB_DMONTH' <br />'
	echo '                 [ DEBUG ] $RS_H: '$RS_H' <br />'
	echo '                 [ DEBUG ] $RS_WD: '$RS_WD' <br />'
	echo '                 [ DEBUG ] $RS_DMONTH: '$RS_DMONTH' <br />'
fi

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="cronjob" action="writetocronjob.cgi" method="get">'
echo '      <div class="row">'
echo '      <fieldset>'
echo '        <legend>Schedule CRON jobs</legend>'
echo '        <table class="bggrey percent100">'

echo '          <tr class="even">'
echo '            <td colspan="3">Please fill out the fields. If you use * it means every hour, every day etc.</td>'
echo '          </tr>'

echo '          <tr class="odd">'
echo '            <td class="column210">'
echo '              <p>Schedule reboot<p></td>'
echo '            <td class="column420">'
echo '              <label for="RB_H">Hour:</label>'
echo '              <input class="small2" type="text" name="RB_H" id="RB_H" maxlength="2" size="2" value='$RB_H' />'
echo '              <label for="RB_WD">&nbsp;&nbsp;Weekday (0-7):</label>'
echo '              <input class="small2" type="text" name="RB_WD" id="RB_WD" maxlength="1" size="1" value='$RB_WD' />'
echo '              <label for="RB_DMONTH">&nbsp;&nbsp;Day of Month:</label>'
echo '              <input class="small2" type="text" name="RB_DMONTH" id="RB_DMONTH" maxlength="2" size="2" value='$RB_DMONTH' />'
echo '            </td>'
echo '            <td>'
echo '              <input class="small1" type="radio" name="REBOOT" id="Scheduled" value="Enabled" '$REBOOT_Y'>Enabled'
echo '              <input class="small1" type="radio" name="REBOOT" id="Scheduled" value="Disabled" '$REBOOT_N'>Disabled'
echo '            </td>'
echo '          </tr>'

echo '          <tr class="even">'
echo '            <td class="column210">'
echo '              <p>Schedule restart Squeezelite</p>'
echo '            </td>'
echo '            <td class="column420">'
echo '              <label for="RS_H">Hour:</label>'
echo '              <input class="small2" type="text" name="RS_H" id="RS_H" maxlength="2" size="2" value='$RS_H' />'
echo '              <label for="RS_WD">&nbsp;&nbsp;Weekday (0-7):</label>'
echo '              <input class="small2" type="text" name="RS_WD" id="RS_WD" maxlength="1" size="1" value='$RS_WD' />'
echo '              <label for="RS_DMONTH">&nbsp;&nbsp;Day of Month:</label>'
echo '              <input class="small2" type="text" name="RS_DMONTH" id="RS_DMONTH" maxlength="2" size="2" value='$RS_DMONTH' />'
echo '            </td>'
echo '            <td>'
echo '              <input class="small1" type="radio" name="RESTART" id="Scheduled" value="Enabled" '$RESTART_Y'>Enabled'
echo '              <input class="small1" type="radio" name="RESTART" id="Scheduled" value="Disabled" '$RESTART_N'>Disabled'
echo '            </td>'
echo '          </tr>'

echo '          <tr class="odd">'
echo '            <td colspan=3>'
echo '              <input type="submit" name="submit" value="Save">'
echo '            </td>'
echo '          </tr>'

echo '        </table>'
echo '      </fieldset>'
echo '      </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

[ $DEBUG = 1 ] && pcp_show_config_cfg

pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'