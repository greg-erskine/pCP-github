#!/bin/sh

# Version: 0.08 2015-02-04 GE
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

. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Tweaks" "SBP"

pcp_controls
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
echo '          <table class="bggrey percent100">'
echo '            <form name="squeeze" action="writetohost.cgi" method="get">'

echo '              <tr class="even">'
echo '                <td class="column150">Host name</td>'
echo '                <td class="column210">'
echo '                  <input class="large16" type="text" id="HOST" name="HOST" maxlength="26" value="'$HOST'">'
echo '                </td>'
echo '                <td>'
echo '                  <p>Provide a host name, so the player is easier to identify on your LAN&nbsp;&nbsp;'
echo '                  <a class="moreless" id="ID01a" href=# onclick="return more('\''ID01'\'')">more></a></p>'
echo '                  <div id="ID01" class="less">'
echo '                    <p><b>Note: </b>This is the linux hostname, not the piCorePlayer name used by LMS.</p>'
echo '                    <p>The Internet standards for protocols mandate that component hostname labels may '
echo '                       contain only the ASCII letters "a" through "z" (in a case-insensitive manner), '
echo '                       the digits "0" through "9", and the hyphen ("-"). No other symbols, punctuation '
echo '                       characters, or white space are permitted.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
echo '              <tr>'
echo '                <td colspan=3>'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
echo '                </td>'
echo '              </tr>'

echo '            </form>'
echo '          </table>'
echo '          <br />'

#---------------------------------------Overclock----------------------------------------
# Function to check the radio button according to config.cfg file
#----------------------------------------------------------------------------------------
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

#----------------------------------------------------------------------------------------
echo '          <table class="bggrey percent100">'
echo '            <form name="overclock" action= "writetooverclock.cgi" method="get">'
            
echo '              <tr class="even">'
echo '                <td class="column150">'
echo '                  <p>Overclock</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <select name="OVERCLOCK">'
echo '                    <option value="NONE" '$OCnone'>No overclocking</option>'
echo '                    <option value="MILD" '$OCmild'>Mild overclocking</option>'
echo '                    <option value="MODERATE" '$OCmoderate'>Moderate overclocking</option>'
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Change Raspberry Pi overclocking&nbsp;&nbsp;'
echo '                  <a class="moreless" id="ID02a" href=# onclick="return more('\''ID02'\'')">more></a></p>'
echo '                  <div id="ID02" class="less">'
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
echo '              <tr>'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
echo '                </td>'
echo '              </tr>'

echo '            </form>'
echo '          </table>'
echo '          <br />'

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

#----------------------------------------------Timezone----------------------------------
[ -f /etc/sysconfig/timezone ] && . /etc/sysconfig/timezone

echo '          <table class="bggrey percent100">'
echo '            <form name="tzone" action="writetotimezone.cgi" method="get">'

echo '              <tr class="even">'
echo '                <td class="column150">Timezone</td>'
echo '                <td class="column210">'
echo '                  <input class="large16" type="text" id="TIMEZONE" name="TIMEZONE" maxlength="26" value="'$TZ'">'
echo '                </td>'
echo '                <td>'
echo '                  <p>Add your TIMEZONE&nbsp;&nbsp;'
echo '                  <a class="moreless" id="ID03a" href=# onclick="return more('\''ID03'\'')">more></a></p>'
echo '                  <div id="ID03" class="less">'
echo '                    <p>Format: EST-10EST,M10.1.0,M4.1.0/3</p>'
echo '                    <p>Cut and paste your TIMEZONE from your favourite timezone location</p>'
echo '                    <p>Example:</p>'
echo '                    <ul>'
echo '                      <li><a href="http://wiki.openwrt.org/doc/uci/system#time.zones" target="_blank">Openwrt</a></li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'

echo '              <tr>'
echo '                <td colspan=2 >'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
echo '                </td>'
echo '              </tr>'

echo '            </form>'
echo '          </table>'
echo '          <br />'

#----------------------------------------------Password----------------------------------
# Change password - STILL UNDER DEVELOPMENT
# Note: changing passwords through a script over html is not very secure.
#----------------------------------------------------------------------------------------
echo '          <table class="bggrey percent100">'
echo '            <form name="password" action="changepassword.cgi" method="get">'

echo '              <tr class="even">'
echo '                <td class="column150">Password for "'$(pcp_tc_user)'"</td>'
echo '                <td class="column210">'
echo '                  <input class="large16" type="password" id="NEWPASSWORD" name="NEWPASSWORD" maxlength="26">'
echo '                </td>'
echo '                <td>'
echo '                  <p>Enter new password&nbsp;&nbsp;'
echo '                  <a class="moreless" id="ID04a" href=# onclick="return more('\''ID04'\'')">more></a></p>'
echo '                  <div id="ID04" class="less">'
echo '                    <p>Default: nosoup4u</p>'
echo '                    <p class="error"><b>Warning: </b>Changing passwords through a script over html is not very secure</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'

echo '              <tr class="even">'
echo '                <td class="column150"></td>'
echo '                <td class="column210">'
echo '                  <input class="large16" type="password" id="CONFIRMPASSWORD" name="CONFIRMPASSWORD" maxlength="26">'
echo '                </td>'
echo '                <td>'
echo '                  <p>Confirm new password.</p>'
echo '                </td>'
echo '              </tr>'

echo '              <tr>'
echo '                <td colspan=3>'
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

#========================================================================================
# Auto start tweaks
#----------------------------------------------------------------------------------------
# Function to check the A_S_LMS radio button according to config file
case "$A_S_LMS" in 
	Enabled)
		A_S_LMS_Y="checked"
		;;
	Disabled)
		A_S_LMS_N="checked"
		;;
	*)
		A_S_LMS_Y=""
		A_S_LMS_N=""
		;;
esac

# Function to check the A_S_FAV radio button according to config file
case "$A_S_FAV" in 
	Enabled)
		A_S_FAV_Y="checked"
		;;
	Disabled)
		A_S_FAV_N="checked"
		;;
	*)
		A_S_FAV_Y=""
		A_S_FAV_N=""
		;;
esac

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Auto start tweaks</legend>'

#----------------------------------------------Auto start favorite-----------------------------
# Decode variables using httpd, no quotes
AUTOSTARTFAV=`sudo /usr/local/sbin/httpd -d $AUTOSTARTFAV`

echo '          <table class="bggrey percent100">'
echo '            <form name="autostartfav" action="writetoautostart.cgi" method="get">'

echo '              <tr class="even">'
echo '                <td class="column150">Auto start favorite</td>'
echo '                <td class="column420">'
echo '                  <select name="AUTOSTARTFAV">'

# Generate a list of options

FAVLIST=`( echo "$(pcp_controls_mac_address) favorites items 0 100"; echo "exit" ) | nc $(pcp_lmsip) 9090 | sed 's/ /\+/g'`
FAVLIST=`sudo /usr/local/sbin/httpd -d $FAVLIST`
echo $FAVLIST | awk -v autostartfav="$AUTOSTARTFAV" '
BEGIN {
	RS="id:"
	FS=":"
	i = 0
}
# main
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
echo '                  <input class="small1" type="radio" name="A_S_FAV" id="A_S_FAV" value="Enabled" '$A_S_FAV_Y'>Enabled'
echo '                  <input class="small1" type="radio" name="A_S_FAV" id="A_S_FAV" value="Disabled" '$A_S_FAV_N'>Disabled'
echo '                </td>'
echo '              </tr>'

echo '              <tr class="even">'
echo '                <td class="column150">'
echo '                </td>'
echo '                <td colspan="2">'
echo '                  <p>Select your auto start favorite from list&nbsp;&nbsp;'
echo '                  <a class="moreless" id="ID06a" href=# onclick="return more('\''ID06'\'')">more></a></p>'
echo '                  <div id="ID06" class="less">'
echo '                    <p>Allows you to set an auto start favorite command that is run after'
echo '                       a "hard" power on. '
echo '                       This could be handy for people building pseudo radios.<p>'
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

echo '              <tr>'
echo '                <td colspan="3">'
echo '                  <input type="hidden" name="AUTOSTART" value="FAV"/>'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
echo '                  <input type="submit" name="SUBMIT" value="Test">'
[ $MODE -gt 4 ] &&
echo '                  <input type="submit" name="SUBMIT" value="Clear">'
echo '                </td>'
echo '              </tr>'

echo '            </form>'
echo '          </table>'
echo '          <br />'

#----------------------------------------------Autostart LMS-----------------------------
# Decode variables using httpd, no quotes
AUTOSTARTLMS=`sudo /usr/local/sbin/httpd -d $AUTOSTARTLMS`

echo '          <table class="bggrey percent100">'
echo '            <form name="autostartlms" action="writetoautostart.cgi" method="get">'

echo '              <tr class="even">'
echo '                <td class="column150">Auto start LMS</td>'
echo '                <td class="column420">'
echo '                  <input class="large30" type="text" id="AUTOSTARTLMS" name="AUTOSTARTLMS" maxlength="254" value="'$AUTOSTARTLMS'">'
echo '                </td>'
echo '                <td>'
echo '                  <input class="small1" type="radio" name="A_S_LMS" id="A_S_LMS" value="Enabled" '$A_S_LMS_Y'>Enabled'
echo '                  <input class="small1" type="radio" name="A_S_LMS" id="A_S_LMS" value="Disabled" '$A_S_LMS_N'>Disabled'
echo '                </td>'
echo '              </tr>'

echo '              <tr class="even">'
echo '                <td class="column150">'
echo '                </td>'
echo '                <td colspan="2">'
echo '                  <p>Cut and paste your auto start LMS command&nbsp;&nbsp;'
echo '                  <a class="moreless" id="ID05a" href=# onclick="return more('\''ID05'\'')">more></a></p>'
echo '                  <div id="ID05" class="less">'
echo '                    <p>Allows you to set an auto start LMS command that is run after'
echo '                       a "hard" power on. This field can contain any valid LMS CLI conmand.'
echo '                       This could be handy for people building pseudo radios.<p>'
echo '                    <p><b>Example:</b></p>'
echo '                    <ul>'
echo '                      <li>randomplay tracks</li>'
echo '                      <li>playlist play http://stream-tx1.radioparadise.com/aac-32</li>'
echo '                      <li>playlist play http://radioparadise.com/m3u/aac-128.m3u</li>'
echo '                    </ul>'
echo '                    <p><b>Note:</b></p>'
echo '                    <ul>'
echo '                      <li>LMS IP address must be set on Squeezelite Settings page.</li>'
echo '                      <li>Maximum number of characters 254.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
echo '              <tr>'
echo '                <td colspan="3">'
echo '                  <input type="hidden" name="AUTOSTART" value="LMS"/>'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
echo '                  <input type="submit" name="SUBMIT" value="Test">'
[ $MODE -gt 4 ] &&
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

#----------------------------------------------Password----------------------------------
# Determine state of check boxes.
#----------------------------------------------------------------------------------------
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

# Function to check the FIQ-split radio button according to config file
case "$FIQ" in
	0x1)
		selected1="selected"
		;;
	0x2)
		selected2="selected"
		;;
	0x3)
		selected3="selected"
		;;
	0x4)
		selected4="selected"
		;;
	0x7)
		selected5="selected"
		;;
	0x8)
		selected6="selected"
		;;
	*)
		selected1=""
		selected2=""
		selected3=""
		selected4=""
		selected5=""
		selected6=""
		;;
esac

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

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="setaudiotweaks" action="writetoaudiotweak.cgi" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Audio tweaks</legend>'
echo '            <table class="bggrey percent100">'

#-------------------------------------------dwc_otg.speed--------------------------------
echo '              <tr class="even">'
echo '                <td class="column150">'
echo '                  <p>OTG-Speed</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="small1" type="radio" name="CMD" id="not enabled" value="Default" '$CMDdefault'>Default'
echo '                  <input class="small1" type="radio" name="CMD" id="Custom" value="Slow" '$CMDslow'>dwc_otg.speed=1'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set "dwc_otg.speed=1"&nbsp;&nbsp;'
echo '                  <a class="moreless" id="ID07a" href=# onclick="return more('\''ID07'\'')">more></a></p>'
echo '                  <div id="ID07" class="less">'
echo '                    <p>Adds "dwc_otg.speed=1" to /mnt/mmcblk0p1/cmdline.txt</p>'
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
echo '              <tr class="odd">'
echo '                <td class="column150">'
echo '                  <p>ALSA output level</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="small1" type="radio" name="ALSAlevelout" id="Default" value="Default" '$ALSAdefault'>Default'
echo '                  <input class="small1" type="radio" name="ALSAlevelout" id="Custom" value="Custom" '$ALSAcustom'>Custom'
echo '                </td>'
echo '                <td>'
echo '                  <p>Custom allows for ALSA output level to be restored after reboot&nbsp;&nbsp;'
echo '                  <a class="moreless" id="ID08a" href=# onclick="return more('\''ID08'\'')">more></a></p>'
echo '                  <div id="ID08" class="less">'
echo '                    <p class="error"><b>Note: </b>Use only if you have changed ALSA output level via alsamixer.</p>'
echo '                    <p>Use alsamixer via ssh and save your custom settings by typing "sudo amixer store".</p>'
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
echo '              <tr class="even">'
echo '                <td class="column150">'
echo '                  <p>FIQ-Split acceleration</p>'
echo '                </td>'
echo '                <td>'
echo '                  <select name="FIQ">'
echo '                    <option value="0x1" '$selected1'>0x1 Accelerate non-periodic split transactions</option>'
echo '                    <option value="0x2" '$selected2'>0x2 Accelerate periodic split transactions</option>'
echo '                    <option value="0x3" '$selected3'>0x3 Accelerate all except high-speed isochronous transactions</option>'
echo '                    <option value="0x4" '$selected4'>0x4 Accelerate high-speed isochronous transactions</option>'
echo '                    <option value="0x7" '$selected5'>0x7 Accelerate all transactions [DEFAULT]</option>'
echo '                    <option value="0x8" '$selected6'>0x8 Enable Interrupt/Control Split Transaction hack</option>'
echo '                  </select>'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="even">'
echo '                <td class="column150">'
echo '                  <p>&nbsp;</p>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Change FIQ_FSM USB settings&nbsp;&nbsp;'
echo '                  <a class="moreless" id="ID09a" href=# onclick="return more('\''ID09'\'')">more></a></p>'
echo '                  <div id="ID09" class="less">'
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

echo '              <tr class="odd">'
echo '                <td colspan=3>'
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

#========================================================================================
# Function to check the CRON Job schedule according to config file
#----------------------------------------------------------------------------------------
case "$REBOOT" in
	Enabled)
		REBOOT_Y="checked"
		;;
	Disabled)
		REBOOT_N="checked"
		;;
	*)
		REBOOT_Y=""
		REBOOT_N=""
		;;
esac

case "$RESTART" in
	Enabled)
		RESTART_Y="checked"
		;;
	Disabled)
		RESTART_N="checked"
		;;
	*)
		RESTART_Y=""
		RESTART_N=""
		;;
esac

#-------------------------------------------Schedule CRON jobs---------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="cronjob" action="writetocronjob.cgi" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Schedule CRON jobs</legend>'
echo '            <table class="bggrey percent100">'

echo '              <tr class="even">'
echo '                <td class="column210">'
echo '                  <p>Schedule piCorePlayer reboot<p>'
echo '                </td>'
echo '                <td class="column420">'
echo '                  <label for="RB_H">Hour:</label>'
echo '                  <input class="small2" type="text" name="RB_H" id="RB_H" maxlength="2" value='$RB_H' />'
echo '                  <label for="RB_WD">&nbsp;&nbsp;Weekday (0-7):</label>'
echo '                  <input class="small2" type="text" name="RB_WD" id="RB_WD" maxlength="1" value='$RB_WD' />'
echo '                  <label for="RB_DMONTH">&nbsp;&nbsp;Day of Month:</label>'
echo '                  <input class="small2" type="text" name="RB_DMONTH" id="RB_DMONTH" maxlength="2" value='$RB_DMONTH' />'
echo '                </td>'
echo '                <td>'
echo '                  <input class="small1" type="radio" name="REBOOT" id="Scheduled" value="Enabled" '$REBOOT_Y'>Enabled'
echo '                  <input class="small1" type="radio" name="REBOOT" id="Scheduled" value="Disabled" '$REBOOT_N'>Disabled'
echo '                </td>'
echo '              </tr>'

echo '              <tr class="odd">'
echo '                <td class="column210">'
echo '                  <p>Schedule Squeezelite restart</p>'
echo '                </td>'
echo '                <td class="column420">'
echo '                  <label for="RS_H">Hour:</label>'
echo '                  <input class="small2" type="text" name="RS_H" id="RS_H" maxlength="2" value='$RS_H' />'
echo '                  <label for="RS_WD">&nbsp;&nbsp;Weekday (0-7):</label>'
echo '                  <input class="small2" type="text" name="RS_WD" id="RS_WD" maxlength="1" value='$RS_WD' />'
echo '                  <label for="RS_DMONTH">&nbsp;&nbsp;Day of Month:</label>'
echo '                  <input class="small2" type="text" name="RS_DMONTH" id="RS_DMONTH" maxlength="2" value='$RS_DMONTH' />'
echo '                </td>'
echo '                <td>'
echo '                  <input class="small1" type="radio" name="RESTART" id="Scheduled" value="Enabled" '$RESTART_Y'>Enabled'
echo '                  <input class="small1" type="radio" name="RESTART" id="Scheduled" value="Disabled" '$RESTART_N'>Disabled'
echo '                </td>'
echo '              </tr>'

echo '              <tr class="even">'
echo '                <td class="column210">'
echo '                  <p></p>'
echo '                </td>'
echo '                <td colspan="2">'
echo '                  <p>Fill out the crontab fields&nbsp;&nbsp;'
echo '                  <a class="moreless" id="ID11a" href=# onclick="return more('\''ID11'\'')">more></a></p>'
echo '                  <div id="ID11" class="less">'
echo '                    <p>"*" it means every hour, every day, ever month.</p>'
echo '                    <p><b>Example:</b></p>'
echo '                    <ul>'
echo '                      <li>2 * * - run job at 02:00 everyday</li>'
echo '                      <li>0 * * - run job at 00:00 everyday</li>'
echo '                    </ul>'
echo '                    <p><b>Root crontab:</b></p>'
echo '                    <textarea class="width600">'"$(cat /var/spool/cron/crontabs/root)"'</textarea>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'

echo '              <tr class="odd">'
echo '                <td colspan=3>'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
[ $MODE -gt 4 ] &&
echo '              <input type="submit" name="SUBMIT" value="Reset">'
[ $MODE -eq 99 ] &&
echo '              <input type="submit" name="SUBMIT" value="Clear">'
echo '            </td>'
echo '          </tr>'

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
	echo '                     [ DEBUG ] $RS_DMONTH: '$RS_DMONTH'</p>'
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

if [ $MODE -gt 4 ]; then
#----------------------------------------------User Commands---------------------------------
	# Decode variables using httpd, no quotes
	USER_COMMAND_1=`sudo /usr/local/sbin/httpd -d $USER_COMMAND_1`
	USER_COMMAND_2=`sudo /usr/local/sbin/httpd -d $USER_COMMAND_2`
	USER_COMMAND_3=`sudo /usr/local/sbin/httpd -d $USER_COMMAND_3`

	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="setusercommands" action="writetoautostart.cgi" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>User commands</legend>'
	echo '            <table class="bggrey percent100">'

	echo '              <tr class="even">'
	echo '                <td class="column150">User command #1</td>'
	echo '                <td>'
	echo '                  <input class="large36" type="text" id="USER_COMMAND_1" name="USER_COMMAND_1" maxlength="254" value="'$USER_COMMAND_1'">'
	echo '                </td>'
	echo '              </tr>'

	echo '              <tr class="odd">'
	echo '                <td class="column150">User command #2</td>'
	echo '                <td>'
	echo '                  <input class="large36" type="text" id="USER_COMMAND_2" name="USER_COMMAND_2" maxlength="254" value="'$USER_COMMAND_2'">'
	echo '                </td>'
	echo '              </tr>'

	echo '              <tr class="even">'
	echo '                <td class="column150">User command #3</td>'
	echo '                <td>'
	echo '                  <input class="large36" type="text" id="USER_COMMAND_3" name="USER_COMMAND_3" maxlength="254" value="'$USER_COMMAND_3'">'
	echo '                </td>'
	echo '              </tr>'

	echo '              <tr class="even">'
	echo '                <td class="column150"></td>'
	echo '                <td>'
	echo '                  <p>Adds user defined commands to the piCorePlayer startup procedure&nbsp;&nbsp;'
	echo '                  <a class="moreless" id="ID12a" href=# onclick="return more('\''ID12'\'')">more></a></p>'
	echo '                  <div id="ID12" class="less">'
	echo '                    <p>This feature gives advanced users a couple of hooks into the startup procedure.'
	echo '                       It will allow advanced users the ability to run extra instances of Squeezelite for example,'
	echo '                       or maybe, run a Linux procedure that shuts down processes, like the web server to optimise performance.</p>'
	echo '                    <p>User commands run after auto start LMS commands and auto start favorites.</p>'
	echo '                    <p>User commands will run in order 1, 2, 3.</p>'
	echo '                    <p><b>Example:</b></p>'
	echo '                      <ul>'
	echo '                        <li>ls /tmp >> /tmp/directory.log</li>'
	echo '                      </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	echo '              <tr class="odd">'
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
#----------------------------------------------------------------------------------------
fi

#----------------------------------------------------------------------------------------
[ $DEBUG = 1 ] && pcp_show_config_cfg

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'