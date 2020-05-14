#!/bin/sh

# Version: 7.0.0 2020-05-14

set -f

. pcp-functions
. pcp-rpi-functions
. pcp-lms-functions

pcp_html_head "Tweaks" "SBP"

pcp_controls
pcp_navbar

COLUMN1_1="col-12"

COLUMN2_1="col-sm-2"
COLUMN2_2="col-10"

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"

COLUMN4_1="col-sm-2"
COLUMN4_2="col-sm-3"
COLUMN4_3="col-sm-3"
COLUMN4_4="col-sm-4"

#========================================================================================
# Functions
#----------------------------------------------------------------------------------------
pcp_the_end() {
	pcp_footer
	pcp_mode
	pcp_copyright
	set +f
	echo '</div>'
	echo '</body>'
	echo '</html>'
	exit
}

#========================================================================================
# pCP System Tweaks
#----------------------------------------------------------------------------------------
pcp_heading5 "pCP System Tweaks"

#----------------------------------------------Hostname----------------------------------
pcp_tweaks_hostname() {

	echo '  <form name="squeeze" action="writetohost.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">Host name</div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="HOST"'
	echo '               value="'$HOST'"'
	echo '               maxlength="26"'
	echo '               title="Only alphanumeric and hyphen allowed."'
	echo '               pattern="[a-zA-Z0-9-]*"'
	echo '        >'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Provide a host name, so the player is easier to identify on your LAN&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p><b>Note:</b> This is the linux hostname, not the piCorePlayer name used by LMS.</p>'
	echo '          <p>The Internet standards for protocols mandate that component hostname labels may '
	echo '             contain only the ASCII letters "a" through "z" (in a case-insensitive manner), '
	echo '             the digits "0" through "9", and the hyphen ("-"). No other symbols, punctuation '
	echo '             characters, or white space are permitted.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	echo '  <hr>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_hostname
#----------------------------------------------------------------------------------------

#----------------------------------------------Timezone----------------------------------
pcp_tweaks_timezone() {

	echo '  <form name="tzone" action="writetotimezone.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">Timezone</div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="TIMEZONE"'
	echo '               value="'$TIMEZONE'"'
	echo '               maxlength="28"'
	echo '               pattern="[a-zA-Z0-9-,./]*"'
	echo '        >'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Add or change your timezone&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p><b>Format:</b> EST-10EST,M10.1.0,M4.1.0/3</p>'
	echo '          <p>Your timezone should be automatically populated.</p>'
	echo '          <p>Delete and reboot to force piCorePlayer to automatically populate timezone.</p>'
	echo '          <p>If not, cut and paste your timezone from your favourite timezone location.</p>'
	echo '          <p><b>Examples here:</b></p>'
	echo '          <ul>'
	echo '            <li><a href="http://wiki.openwrt.org/doc/uci/system#time.zones" target="_blank">Openwrt</a></li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	echo '  <hr>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_timezone
#----------------------------------------------------------------------------------------

#----------------------------------------------Player Tabs-------------------------------
pcp_tweaks_playertabs() {

	case "$PLAYERTABS" in
		yes) PLAYERTABSyes="checked" ;;
		no)  PLAYERTABSno="checked" ;;
	esac

	echo '  <form name="playertabs" action="writetoconfig.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>piCorePlayer Tabs</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="pt1" type="radio" name="PLAYERTABS" value="yes" '$PLAYERTABSyes'>'
	echo '        <label for="pt1">Yes&nbsp;&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="pt2" type="radio" name="PLAYERTABS" value="no" '$PLAYERTABSno'>'
	echo '        <label for="pt2">No</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Display piCorePlayer Tabs&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Sometimes it might be useful to turn off the piCorePlayer Tabs.</p>'
	echo '          <p>piCorePlayer checks LMS for available players. This can be slow on older RPis.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input type="hidden" name="FROM_PAGE" value="tweaks.cgi">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	echo '  <hr>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_playertabs
#----------------------------------------------------------------------------------------

#----------------------------------------------LMS Control Toolbar-----------------------
pcp_tweaks_lmscontrols() {

	case "$LMSCONTROLS" in
		yes) LMSCONTROLSyes="checked" ;;
		no) LMSCONTROLSno="checked" ;;
	esac

	echo '  <form name="lmscontroltoolbar" action="writetoconfig.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>LMS Controls Toolbar</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="lc1" type="radio" name="LMSCONTROLS" value="yes" '$LMSCONTROLSyes'>'
	echo '        <label for="lc1">Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="lc2" type="radio" name="LMSCONTROLS" value="no" '$LMSCONTROLSno'>'
	echo '        <label for="lc2">No</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Display LMS Controls Toolbar&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Sometimes it might be useful to turn off the LMS Controls Toolbar.</p>'
	echo '          <p>These controls are not intended for normal use, but they are handy when testing.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input type="hidden" name="FROM_PAGE" value="tweaks.cgi">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	echo '  <hr>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_lmscontrols
#----------------------------------------------------------------------------------------

#----------------------------------------------HDMI Power--------------------------------
pcp_tweaks_hdmipower() {

	case "$HDMIPOWER" in
		on) HDMIPOWERon="checked" ;;
		off) HDMIPOWERoff="checked" ;;
	esac

	echo '  <form name="hdmipower" action="writetohdmipwr.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>HDMI power</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="hdmi1" type="radio" name="HDMIPOWER" value="on" '$HDMIPOWERon'>'
	echo '        <label for="hdmi1">On&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="hdmi2" type="radio" name="HDMIPOWER" value="off" '$HDMIPOWERoff'>'
	echo '        <label for="hdmi2">Off</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>HDMI power&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Powering off HDMI to save a little power.</p>'
	echo '          <p>Using this option will download and install rpi-vc.tcz.</p>'
	echo '          <p>A reboot will be required.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	echo '  <hr>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_hdmipower
#----------------------------------------------------------------------------------------

#----------------------------------------------LMS Web Port------------------------------
pcp_tweaks_lmswebport() {

	echo '  <form name="lmswebport" action="writetoconfig.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>LMS Web Port</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="number"'
	echo '               name="LMSWEBPORT"'
	echo '               value="'$LMSWEBPORT'"'
	echo '               min="9001"'
	echo '               max="9999"'
	echo '        >'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Enter non-default LMS Web Port number&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;number&gt;</p>'
	echo '          <p><b>Default:</b> 9000</p>'
	echo '          <p><b>Range:</b> 9001:9999</p>'
	echo '          <p><b>Note:</b> Only add this if you have changed from the default LMS Web Port value.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input type="hidden" name="FROM_PAGE" value="tweaks.cgi">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	echo '  <hr>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_lmswebport
#----------------------------------------------------------------------------------------

#--------------------------------------Internet Check IP---------------------------------
pcp_tweaks_internet_check_ip() {

	echo '  <form name="internetcheckip" action="writetoconfig.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Internet check IP</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="INTERNET_CHECK_IP"'
	echo '               value="'$INTERNET_CHECK_IP'"'
	echo '               title="[xxx.xxx.xxx.xxx]"'
	echo '               pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"'
	echo '        >'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Enter non-default Internet check IP address&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;IP address&gt;</p>'
	echo '          <p><b>Default:</b> blank or 8.8.8.8</p>'
	echo '          <p>piCorePlayer uses this IP address to confirm that it has Internet access.</p>'
	echo '          <p>You only have to set this if 8.8.8.8 is not usable.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input type="hidden" name="FROM_PAGE" value="tweaks.cgi">'
	echo '      </div>'

	if [ $DEBUG -eq 1 ]; then

		if [ $(pcp_internet_accessible) -eq 0 ]; then
			pcp_green_tick "Internet found."
		else
			pcp_red_cross "Internet not found."
		fi

		echo '      <div class="'$COLUMN3_2'">'
		echo '        <p class="'$CLASS'">'$INDICATOR'</p>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_3'">'
		echo '        <p>'$STATUS'</p>'
		echo '      </div>'
	fi
	echo '      </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	echo '  <hr>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_internet_check_ip
#----------------------------------------------------------------------------------------

#--------------------------------------rotdash-------------------------------------------
pcp_tweaks_rotdash() {

	case "$ROTDASH" in
		yes) ROTDASHyes="checked" ;;
		no) ROTDASHno="checked" ;;
	esac

	echo '  <form name="rotdash" action="writetoconfig.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Replace rotating dash</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="rot1" type="radio" name="ROTDASH" value="yes" '$ROTDASHyes'>'
	echo '        <label for="rot1">Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="rot2" type="radio" name="ROTDASH" value="no" '$ROTDASHno'>'
	echo '        <label for="rot2">No</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Replace the default rotating dash with a new one&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>The default rotating dash displays -/|\ while the new one displays .....</p>'
	echo '          <p>You can see the difference when doing a backup for example.</p>'
	echo '          <p><b>Note:</b> Requires a reboot to activate.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input type="hidden" name="FROM_PAGE" value="tweaks.cgi">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_tweaks_rotdash
#----------------------------------------------------------------------------------------

#========================================================================================
# pCP OS/Kernel Tweaks
#----------------------------------------------------------------------------------------
if [ $MODE -ge $MODE_PLAYER ]; then
	pcp_heading5 "pCP Kernel Tweaks" hr
fi
#--------------------------------------Governor------------------------------------------
pcp_tweaks_governor() {

	echo '  <form name="governor" action= "writetooverclock.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>CPU Governor</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <select class="form-control form-control-sm" name="CPUGOVERNOR">'

	                for GOV in $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors)
	                do
	                  SCALINGGOVERNOR=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor)
	                  [ "$GOV" = "$SCALINGGOVERNOR" ] && SEL="selected" || SEL=""
	                  echo '                    <option value="'$GOV'" '$SEL'>'$GOV'</option>'
	                done

	echo '        </select>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Change CPU Governor &nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p><b>Available CPU Governors:</b></p>'
	echo '          <p>&lt;'$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors | sed 's/ $//' | sed 's/ /|/g' )'&gt;</p>'
	echo '          <p><b>Commonly used CPU Governors:</b></p>'
	echo '          <ul>'
	echo '            <li>ondemand = Sets the CPU frequency depending on the current system load.</li>'
	echo '            <li>powersave = Sets the CPU statically to the lowest frequency.</li>'
	echo '            <li>performance = Sets the CPU statically to the highest frequency.</li>'
	echo '          </ul>'
	echo '          <p>Dynamically set, no reboot is required.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input type="hidden" name="ACTION" value="gov">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	echo '  <hr>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_governor
#----------------------------------------------------------------------------------------

#---------------------------------------Overclock----------------------------------------
pcp_tweaks_overclock() {

	# Only works for Raspberry Pi Model 1, disable for the others.
	case "$(pcp_rpi_type)" in
		1) DISABLED="" ;;
		*) DISABLED="disabled" ;;
	esac

	case "$OVERCLOCK" in
		NONE) OCnone="selected" ;;
		MILD) OCmild="selected" ;;
		MODERATE) OCmoderate="selected" ;;
	esac

	echo '  <form name="overclock" action= "writetooverclock.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Overclock</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <select class="form-control form-control-sm" name="OVERCLOCK" '$DISABLED'>'
	echo '          <option value="NONE" '$OCnone'>No overclocking</option>'
	echo '          <option value="MILD" '$OCmild'>Mild overclocking</option>'
	echo '          <option value="MODERATE" '$OCmoderate'>Moderate overclocking</option>'
	echo '        </select>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Change Raspberry Pi Model 1 overclocking&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;No overclocking|Mild overclocking|Moderate overclocking&gt;</p>'
	echo '          <p><b>Note:</b> Only suitable for Raspberry Pi Model 1.</p>'
	echo '          <p>Reboot is needed.<p>'
	echo '          <p><b>Note:</b> If Raspberry Pi fails to boot:</p>'
	echo '          <ul>'
	echo '            <li>hold down the shift key during booting, or</li>'
	echo '            <li>edit the config.txt file manually</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save" '$DISABLED'>'
	echo '        <input type="hidden" name="ACTION" value="oc">'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="'$BUTTON'" type="button" name="ADVANCED_OVERCLOCK" onClick="location.href='\'''xtras_overclock.cgi''\''" value="Advanced Overclock">'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Go to Advanced Overclocking page.</p>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	pcp_debug_variables "html" OVERCLOCK OCnone OCmild OCmoderate
	echo '  <hr>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_overclock
#----------------------------------------------------------------------------------------

#-------------------------------------CPU Isolation--------------------------------------
pcp_tweaks_cpuisol() {

	echo '  <form name="overclock" action= "writetooverclock.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>CPU Isolation</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="CPUISOL"'
	echo '               value="'$CPUISOL'"'
	echo '               pattern="([0-3]+)?(,*[0-3]){0,3}"'
	echo '        >'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Comma separated list of CPUs to isolate&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Isolation means the kernel will not run user tasks on the selected CPUs, unless specified.</p>'
	echo '          <p><b>Recommended setting:&nbsp;</b>0,3</p>'
	echo '          <p>CPU 0 to only run kernel interrupts.</p>'
	echo '          <p>CPU 3 to run the squeezelite output thread.</p>'
	echo '          <p>Squeezelite process settings available after reboot with isolation.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input type="hidden" name="ACTION" value="isol">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	pcp_debug_variables "html" CPUISOL
}
[ $MODE -ge $MODE_PLAYER -a $(pcp_rpi_type) -ge 2 ] && pcp_tweaks_cpuisol
#----------------------------------------------------------------------------------------

#-------------------------------------Squeezelite cpu affinity---------------------------
pcp_tweaks_sqlite_affinity() {

	echo '  <form name="overclock" action= "writetooverclock.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '     <div class="row">'
	echo '       <div class="'$COLUMN3_1'">'
	echo '         <p>Squeezelite CPU</p>'
	echo '       </div>'
	echo '       <div class="'$COLUMN3_2'">'
	echo '         <input class="form-control form-control-sm"'
	echo '                type="text"'
	echo '                name="SQLAFFINITY"'
	echo '                value="'$SQLAFFINITY'"'
	echo '                pattern="([0-3]+)?(,*[0-3]){0,3}"'
	echo '         >'
	echo '       </div>'
	pcp_incr_id
	echo '       <div class="'$COLUMN3_3'">'
	echo '         <p>Comma separated list of CPUs to run squeezelite process&nbsp;&nbsp;'
	echo '           <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '         </p>'
	echo '         <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '           <p><b>Recommended:&nbsp;</b>blank</p>'
	echo '           <p>blank:&nbsp;Kernel decides which CPU to run Squeezelite threads.</p>'
	echo '           <p>If not resampling, then use the same settings as the output thread in next box.</p>'
	echo '         </div>'
	echo '       </div>'
	echo '     </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Squeezelite Output CPU</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="SQLOUTAFFINITY"'
	echo '               value="'$SQLOUTAFFINITY'"'
	echo '               pattern="[0-3]"'
	echo '        >'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>CPU to run squeezelite output thread&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p><b>Recommended:&nbsp;</b>3</p>'
	echo '          <p>CPU 3 to run the squeezelite output thread.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input type="hidden" name="ACTION" value="sqlaffinity">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	pcp_debug_variables "html" SQLAFFINITY SQLOUTAFFINITY
}
[ $MODE -ge $MODE_PLAYER -a $(pcp_rpi_type) -ge 2 -a "$(cat /proc/cmdline | grep isolcpus)" != "" ] && pcp_tweaks_sqlite_affinity
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

	pcp_heading5 "Wake-on-LAN (WOL)" hr

	echo '  <form name="wol" action="writetoconfig.cgi" method="get">'
	#----------------------------------WOL-----------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>WOL</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="wol1" type="radio" name="WOL" value="yes" '$WOLyes'>'
	echo '        <label for="wol1">Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="wol2" type="radio" name="WOL" value="no" '$WOLno'>'
	echo '        <label for="wol2">No</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>LMS Wake-on-LAN&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Transmits a Wake-On-LAN (WOL) "Magic Packet", used for restarting machines that have been soft-powered-down.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#----------------------------------LMS NIC-------------------------------------------
	pcp_incr_id
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>LMS NIC</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="input'$ID'"'
	echo '               class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="WOL_NIC"'
	echo '               value="'$WOL_NIC'"'
	echo '               title="LMS NIC: ( eth0 | eth1 | wlan0 | wlan1 )"'
	echo '               pattern="(eth0|eth1|wlan0|wlan1)"'
	echo '               '$WOLDISABLED
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>LMS Network Interface Card&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;'
	echo '            <span id="option'$ID'a" class="pointer" title="Click to use" onclick="pcp_copy_click_to_input('\'input${ID}\',\'option${ID}a\'')">eth0</span> |'
	echo '            <span id="option'$ID'b" class="pointer" title="Click to use" onclick="pcp_copy_click_to_input('\'input${ID}\',\'option${ID}b\'')">eth1</span> |'
	echo '            <span id="option'$ID'c" class="pointer" title="Click to use" onclick="pcp_copy_click_to_input('\'input${ID}\',\'option${ID}c\'')">wlan0</span> |'
	echo '            <span id="option'$ID'd" class="pointer" title="Click to use" onclick="pcp_copy_click_to_input('\'input${ID}\',\'option${ID}d\'')">wlan1</span> '
	echo '            &gt;</p>'
	echo '          <p class="pointer" title="Click to use '$7'" onclick="pcp_copy_click_to_input('\'input${ID}\',\'example${ID}\'')">'
	echo '            <b>Example:</b> <span id="example'$ID'">'$7'</span></p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#----------------------------------LMS MAC address-----------------------------------
	pcp_incr_id
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>LMS MAC address</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="input'$ID'"'
	echo '               class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="WOL_LMSMACADDRESS"'
	echo '               value="'$WOL_LMSMACADDRESS'"'
	echo '               title="01:23:45:67:ab:cd:ef"'
	echo '               pattern="([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})"'
	echo '               '$WOLDISABLED
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>LMS MAC address&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;01:23:45:67:ab:cd:ef&gt;</p>'
	echo '          <p class="pointer" title="Click to use '$4'" onclick="pcp_copy_click_to_input('\'input${ID}\',\'example${ID}\'')">'
	echo '            <b>Example:</b> <span id="example'$ID'">'$4'</span></p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#----------------------------------Submit button-------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input type="hidden" name="FROM_PAGE" value="tweaks.cgi">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_wol
#----------------------------------------------------------------------------------------

#========================================================================================
# Auto start tweaks
#----------------------------------------------------------------------------------------
pcp_tweaks_auto_start() {

	pcp_heading5 "Auto start tweaks" hr

	#---------------------------------Auto start favorite--------------------------------
	case "$A_S_FAV" in
		Enabled) A_S_FAV_Y="checked" ;;
		Disabled) A_S_FAV_N="checked" ;;
	esac

	echo '  <form name="autostartfav" action="writetoautostart.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">Auto start favorite</div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <select class="large30" name="AUTOSTARTFAV">'
	                pcp_lms_favorites_list select
	echo '        </select>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <input id="as1" type="radio" name="A_S_FAV" value="Enabled" '$A_S_FAV_Y'>'
	echo '        <label for="as1">Enabled</label>'
	echo '        <input id="as2" type="radio" name="A_S_FAV" value="Disabled" '$A_S_FAV_N'>'
	echo '        <label for="as2">Disabled</label>'
	echo '      </div>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '      </div>'
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Select your auto start favorite from list&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Allows you to set an auto start favorite command that is run after'
	echo '             a "hard" power on. '
	echo '             This could be handy for people building Internet radios.<p>'
	echo '          <p><b>Note:</b></p>'
	echo '          <ul>'
	echo '            <li>Squeezelite must be running.</li>'
	echo '            <li>LMS IP address is auto-discovered.</li>'
	echo '            <li>Favorites must exist in LMS.</li>'
	echo '            <li>Favorites must be at the top level.</li>'
	echo '            <li>Folders will not be navigated.</li>'
	echo '            <li>Maximum of 100 favorites.</li>'
	echo '            <li>Favorite name can not have an "&" - Rename using LMS.</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Test">'
	echo '        <input type="hidden" name="AUTOSTART" value="FAV">'
	[ $MODE -ge $MODE_PLAYER ] &&
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Clear">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	#------------------------------------------------------------------------------------
	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		pcp_infobox_begin
		pcp_message DEBUG "Controls MAC: $(pcp_controls_mac_address)" "html"
		pcp_message DEBUG "LMS IP: $(pcp_lmsip)" "html"
		pcp_infobox_end
		pcp_debug_variables "html" AUTOSTARTFAV
		pcp_textarea FAVLIST "cat /tmp/json_list" 5
		echo '<!-- End of debug info -->'
	fi
	echo '  <p></p>' # Add a little space
	#------------------------------------------------------------------------------------

	#---------------------------------Autostart LMS--------------------------------------
	AUTOSTARTLMS=`sudo $HTTPD -d $AUTOSTARTLMS`
	case "$A_S_LMS" in
		Enabled) A_S_LMS_Y="checked" ;;
		Disabled) A_S_LMS_N="checked" ;;
	esac

	echo '  <form name="autostartlms" action="writetoautostart.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">Auto start LMS</div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm" type="text" name="AUTOSTARTLMS" maxlength="254" value="'$AUTOSTARTLMS'">'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <input id="as3" type="radio" name="A_S_LMS" value="Enabled" '$A_S_LMS_Y'>'
	echo '        <label for="as3">Enabled</label>'
	echo '        <input id="as4" type="radio" name="A_S_LMS" value="Disabled" '$A_S_LMS_N'>'
	echo '        <label for="as4">Disabled</label>'
	echo '      </div>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '      </div>'
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Cut and paste your auto start LMS command&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Allows you to set an auto start LMS command that is run after'
	echo '             a "hard" power on. This field can contain any valid LMS CLI command.'
	echo '             This could be handy for people building Internet radios.<p>'
	echo '          <p><b>Example:</b></p>'
	echo '          <ul>'
	echo '            <li>randomplay tracks</li>'
	echo '            <li>playlist play http://stream-tx1.radioparadise.com/aac-32</li>'
	echo '            <li>playlist play http://radioparadise.com/m3u/aac-128.m3u</li>'
	echo '          </ul>'
	echo '          <p><b>Note:</b></p>'
	echo '          <ul>'
	echo '            <li>Squeezelite must be running.</li>'
	echo '            <li>LMS IP address is auto-discovered.</li>'
	echo '            <li>Do not include MAC address in CLI command.</li>'
	echo '            <li>Maximum number of characters 254.</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Test">'
	echo '        <input type="hidden" name="AUTOSTART" value="LMS">'
	[ $MODE -ge $MODE_PLAYER ] &&
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Clear">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	#------------------------------------------------------------------------------------
	pcp_debug_variables "html" AUTOSTARTLMS A_S_LMS_Y A_S_LMS_N
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_auto_start

#========================================================================================
# Jivelite/Screen functions
#----------------------------------------------------------------------------------------
[ $MODE -ge $MODE_PLAYER ] && pcp_heading5 "Jivelite Setup" hr

#----------------------------------------------------------------------------------------
# Function to download/install/delete Jivelite
#----------------------------------------------------------------------------------------
pcp_tweaks_install_jivelite() {

	echo '  <div class="row">'

	if [ ! -f $TCEMNT/tce/optional/pcp-jivelite.tcz ]; then
		echo '    <div class="'$COLUMN3_1'">'
		echo '      <form name="jivelite1" action="writetojivelite.cgi" method="get">'
		echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Install">'
		echo '        <input type="hidden" name="OPTION" value="JIVELITE">'
		echo '      </form>'
		echo '    </div>'
		echo '    <div class="'$COLUMN3_2'">'
		echo '    </div>'
		pcp_incr_id
		echo '    <div class="'$COLUMN3_3'">'
		echo '      <p>Install Jivelite on pCP&nbsp;&nbsp;'
		echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
		echo '      </p>'
		echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '        <p>This will install Jivelite and VU meters on pCP.</p>'
		echo '      </div>'
		echo '    </div>'
	else
		echo '    <div class="col">'
		echo '      <form name="jivelite1" action="writetojivelite.cgi" method="get">'
		echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Update">'
		echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Reset">'
		echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Remove">'
		echo '        <input type="hidden" name="OPTION" value="JIVELITE">'
		echo '      </form>'
		echo '    </div>'
		pcp_incr_id
		echo '    <div class="'$COLUMN3_3'">'
		echo '      <p>Update, Reset or Remove Jivelite from pCP&nbsp;&nbsp;'
		echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
		echo '      </p>'
		echo '      <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '        <p>Allows to view and control piCorePlayer via Jivelite on an attached screen.</p>'
		echo '        <p>Jivelite for piCorePlayer is add-on extension developed by Ralphy.<p>'
		echo '        <p>A reboot after installation is needed.<p>'
		echo '        <p><b>Note:</b> For the first configuration of Jivelite an attached keyboard or touch screen is needed.</p>'
		echo '        <ul>'
		echo '          <li>Install - Downloads and installs Jivelite.</li>'
		echo '          <li>Update - Updates the Jivelite Package, preferences are kept.  Reboot required.</li>'
		echo '          <li>Reset - Resets Jivelite preferences.</li>'
		echo '          <li>Remove - Removes all traces of Jivelite.</li>'
		echo '        </ul>'
		echo '        <p>Jivelite requires resizing the file system.<p>'
		echo '        <p>Installing Jivelite will also install the VU Meters.<p>'
		echo '      </div>'
		echo '    </div>'
	fi
	echo '  </div>'
	#------------------------------------------------------------------------------------
	pcp_debug_variables "html" JIVELITE JIVEyes JIVEno
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_install_jivelite

#-----------------------------Enable/disable autostart of Jivelite-----------------------
pcp_tweaks_enable_jivelite() {

	if [ -f $TCEMNT/tce/optional/pcp-jivelite.tcz ]; then
		JLDISABLED=""
	else
		JLDISABLED="disabled"
	fi

	case "$JIVELITE" in
		yes) JIVEyes="checked" ;;
		no) JIVEno="checked" ;;
	esac

	echo '  <form name="jivelite2" action="writetojivelite.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <input class="'$BUTTON'" type="submit" value="Set Autostart" '$JLDISABLED'>'
	echo '        <input type="hidden" name="OPTION" value="JIVELITE">'
	echo '        <input type="hidden" name="ACTION" value="Onboot">'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="jive1" type="radio" name="JIVELITE" value="yes" '$JIVEyes'>'
	echo '        <label for="jive1">Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="jive2" type="radio" name="JIVELITE" value="no" '$JIVEno'>'
	echo '        <label for="jive2">No</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Automatic start of Jivelite when pCP boots&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Yes - will enable automatic start of Jivelite when pCP boots.</p>'
	echo '          <p>No - will disable automatic start of Jivelite when pCP boots.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_enable_jivelite
#----------------------------------------------------------------------------------------

#---------------------------------------VU Meters----------------------------------------
# Function to download/install/delete Jivelite VU Meters
#----------------------------------------------------------------------------------------
pcp_tweaks_vumeter() {

	echo '  <form name="vumeter" action= "writetojivelite.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Jivelite VU Meter</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <select class="form-control form-control-sm" name="VUMETER">'

	                LOADED_VU_METER=$( cat $ONBOOTLST | grep VU_Meter )
	                VUMETERS=$( ls $PACKAGEDIR | grep VU_Meter | grep .tcz$ )
	                for i in $VUMETERS
	                do
	                  [ "$i" = "$LOADED_VU_METER" ] && SEL="selected" || SEL=""
	                  DISPLAY=$( echo $i | sed -e 's/^VU_Meter_//' -e 's/.tcz$//' -e 's/_/ /g' )
	                  echo '          <option value="'$i'" '$SEL'>'$DISPLAY'</option>'
	                done

	echo '        </select>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Select Jivelite VU Meter (Joggler/Grid Skins only)&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Allows you to select VU Meters from a dropdown list.</p>'
	echo '          <p>Jivelite will restart after changing VU Meter.<p>'
	echo '          <p>VU Meters have been sourced from various community members. Thank you.<p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="col">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Download">'
	echo '        <input type="hidden" name="OPTION" value="VUMETER">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'

	if [ $DEBUG -eq 1 ]; then
		#================================================================================
		# Display debug information
		#--------------------------------------------------------------------------------
		echo '<!-- Start of debug info -->'
		#--------------------------------------------------------------------------------
		echo '    <div class="row">'
		echo '      <div class="'$COLUMN1_1'">'
		echo '        <p class="debug">[ DEBUG ] Loop mounted extensions</p>'
		echo '      </div>'
		echo '    </div>'
		#--------------------------------------------------------------------------------
		echo '    <div class="row">'
		echo '      <div class="'$COLUMN1_1'">'
		                       pcp_textarea "none" "df | grep /dev/loop " 200
		echo '      </div>'
		echo '    </div>'
		#--------------------------------------------------------------------------------
		echo '    <div class="row">'
		echo '      <div class="'$COLUMN1_1'">'
		echo '        <p class="debug">[ DEBUG ] Installed extensions</p>'
		echo '      </div>'
		echo '    </div>'
		#--------------------------------------------------------------------------------
		echo '    <div class="row">'
		echo '      <div class="'$COLUMN1_1'">'
		                       ls /usr/local/tce.installed >/tmp/installed.lst
		                       pcp_textarea "none" "cat /tmp/installed.lst" 100
		echo '      </div>'
		echo '    </div>'
		#--------------------------------------------------------------------------------
		pcp_debug_variables "html" LOADED_VU_METER DISPLAY PACKAGEDIR VUMETERS
		echo '<!-- End of debug info -->'
	fi
}
[ $MODE -ge $MODE_PLAYER ] && [ "$JIVELITE" = "yes" ] && pcp_tweaks_vumeter
#----------------------------------------------------------------------------------------

#---------------------------------------Screen rotation----------------------------------
pcp_tweaks_screenrotate() {

	case "$SCREENROTATE" in
		0|no) SCREEN0="checked" ;;
		180|yes) SCREEN180="checked" ;;
	esac

	echo '  <form name="screen_rotate" action="writetoscreenrotate.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <button class="'$BUTTON'" name="ACTION" value="Rotation">Set Rotation</button>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="scrrot1" type="radio" name="SCREENROTATE" value="0" '$SCREEN0'>'
	echo '        <label for="scrrot1">0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="scrrot2" type="radio" name="SCREENROTATE" value="180" '$SCREEN180'>'
	echo '        <label for="scrrot2">180</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Screen rotation (0|180)&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Allows you to rotate the screen if the display is upside down.</p>'
	echo '          <p>A reboot is required to activate the changes.<p>'
	echo '          <p><b>Note:</b> On some (most) screen mounts, the screen is actually upside down.</p>'
	echo '          <ul>'
	echo '            <li>0 - brown ribbon cable at bottom of screen.</li>'
	echo '            <li>180 - brown ribbon cable at top of screen (default).</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	#------------------------------------------------------------------------------------
	pcp_debug_variables "html" SCREENROTATE SCREEN0 SCREEN180
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_screenrotate
#----------------------------------------------------------------------------------------

#---------------------------------------Screen Size--------------------------------------
pcp_tweaks_screensize() {

	echo '  <form name="screen_size" action="writetoscreenrotate.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <button name="ACTION" value="Size">Set Size</button>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>Width:&nbsp;</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <p><input class="form-control form-control-sm" type="text" name="JL_SCREEN_WIDTH" value="'$JL_SCREEN_WIDTH'"></p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Height: <input class="form-control form-control-sm" type="text" name="JL_SCREEN_HEIGHT" value="'$JL_SCREEN_HEIGHT'"></p>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <p>Screen size&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Allows you to set a custom Jivelite screen size.</p>'
	echo '          <p>Zero/Zero uses the default screen resolution.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	#------------------------------------------------------------------------------------
	pcp_debug_variables "html" JL_SCREEN_WIDTH JL_SCREEN_HEIGHT
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_screensize
#----------------------------------------------------------------------------------------

pcp_tweaks_framebuffer() {

	echo '  <form name="screen_size" action="writetoscreenrotate.cgi" method="get">'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <button name="ACTION" value="FrameBuffer">Set FB</button>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>Frame Buffer:&nbsp;</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <p><input class="form-control form-control-sm" type="text" name="JL_FRAME_BUFFER" value="'$JL_FRAME_BUFFER'"></p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set the Frame Buffer Device. (default: /dev/fb0)</p>'
	echo '      </div>'
	echo '    </div>'
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>&nbsp;</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2' right">'
	echo '        <p>Frame Rate:&nbsp;</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <p><input class="form-control form-control-sm" type="number" min="4" max="60" name="JL_FRAME_RATE" value="'$JL_FRAME_RATE'" ></p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set the Frame Buffer refresh rate.</p>'
	echo '      </div>'
	echo '    </div>'
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>&nbsp;</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2' right">'
	echo '        <p>Frame Depth:&nbsp;</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <p><input class="form-control form-control-sm" type="text" name="JL_FRAME_DEPTH" value="'$JL_FRAME_DEPTH'" pattern="(8|16|24|32)" ></p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set the Frame Buffer color depth.</p>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	#------------------------------------------------------------------------------------
	pcp_debug_variables "html" JL_FRAME_BUFFER JL_FRAME_RATE JL_FRAME_DEPTH
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_framebuffer
#----------------------------------------------------------------------------------------

if [ $MODE -ge $MODE_PLAYER ]; then
	pcp_heading5 "IR remote control" hr
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# IR Remote table
#----------------------------------------------------------------------------------------
pcp_tweaks_lirc() {

	pgrep lircd > /dev/null && IR_RUN=0
	if [ $IR_RUN -eq 0 ]; then
		pcp_green_tick "running"
	else
		pcp_red_cross "not running"
	fi

	echo '  <form name="LIRC" action="lirc.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>IR remote control</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '       <p class="'$CLASS'">'$INDICATOR'</p>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>LIRC IR remote control is '$STATUS' &nbsp;&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>LIRC will not automatically start if jivelite is installed.</p>'
	echo '          <p>Go to IR page to:</p>'
	echo '          <ul>'
	echo '            <li>Install/remove LIRC.</li>'
	echo '            <li>Configure LIRC.</li>'
	echo '            <li>Change GPIO number.</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	if [ "$JIVELITE" = "yes" ]; then
		if [ $IR_KEYTABLES = "yes" ]; then
			pcp_green_tick "loaded"
		else
			pcp_red_cross "not loaded"
		fi

		echo '    <div class="row">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <p>IR remote control</p>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '       <p class="'$CLASS'">'$INDICATOR'</p>'
		echo '      </div>'
		pcp_incr_id
		echo '      <div class="'$COLUMN3_3'">'
		echo '        <p>IR remote control for jivelite, using kernel keytables, is '$STATUS' &nbsp;&nbsp;&nbsp;'
		echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>Go to IR page to...</p>'
		echo '          <p>Install/remove IR Tools.</p>'
		echo '          <p>Change GPIO number for ir receiver.</p>'
		echo '          <p>Upload keytable map.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
	fi
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="IR page">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_lirc
#----------------------------------------------------------------------------------------

#========================================================================================
# Poweroff/Shutdown Table
#----------------------------------------------------------------------------------------
pcp_tweaks_poweroff() {

	pcp_heading5 "Poweroff/Shutdown Overlays" hr

	echo '  <form name="poweroff" action="writetoconfig.cgi" method="get">'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Poweroff GPIO&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Drives a GPIO pin High/Low to signal external device to power down.</p>'
	echo '          <p>Refer to '$BOOTMNT'/overlays/README<p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	case $GPIOPOWEROFF in
		yes) GPIOPOWEROFF_yes="checked";;
		no)  GPIOPOWEROFF_no="checked";;
	esac
	case $GPIOPOWEROFF_HI in
		yes) GPIOPOWEROFF_HI_yes="checked";;
		no)  GPIOPOWEROFF_HI_no="checked";;
	esac

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <button type="submit" name="SUBMIT" value="Poweroff">gpio-poweroff</button>'
	echo '        <input type="hidden" name="FROM_PAGE" value="tweaks.cgi">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <input id="gpio1" type="radio" name="GPIOPOWEROFF" value="yes" '$GPIOPOWEROFF_yes'>'
	echo '        <label for="gpio1">Yes&nbsp;&nbsp;</label>'
	echo '        <input id="gpio2" type="radio" name="GPIOPOWEROFF" value="no" '$GPIOPOWEROFF_no'>'
	echo '        <label for="gpio2">No</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        GPIO: <input class="form-control form-control-sm"'
	echo '             type="number"'
	echo '             name="GPIOPOWEROFF_GPIO"'
	echo '             value="'$GPIOPOWEROFF_GPIO'"'
	echo '             title="( 0 - 31 )"'
	echo '             min="0"'
	echo '             max="31"'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <input id="gpio3" type="radio" name="GPIOPOWEROFF_HI" value="yes" '$GPIOPOWEROFF_HI_yes'>'
	echo '        <label for="gpio3">Active High</label>'
	echo '        <input id="gpio4" type="radio" name="GPIOPOWEROFF_HI" value="no" '$GPIOPOWEROFF_HI_no'>'
	echo '        <label for="gpio4">Active Low</label>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'

	#------------------------------------------------------------------------------------
	echo '  <form name="shutdown" action="writetoconfig.cgi" method="get">'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Shutdown GPIO&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Defines a GPIO pin as a linux KEY_POWER event</p>'
	echo '          <p>Works in conjunction with shutdown-monitor.tcz -or- a custom shell script.</p>'
	echo '          <p>Refer to '$BOOTMNT'/overlays/README<p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	case $GPIOSHUTDOWN in
		yes) GPIOSHUTDOWN_yes="checked";;
		no)  GPIOSHUTDOWN_no="checked";;
	esac
	case $GPIOSHUTDOWN_HI in
		yes) GPIOSHUTDOWN_HI_yes="checked";;
		no)  GPIOSHUTDOWN_HI_no="checked";;
	esac
	case $GPIOSHUTDOWN_PU in
		up)   GPIOSHUTDOWN_PU_up="checked";;
		down) GPIOSHUTDOWN_PU_down="checked";;
		off)  GPIOSHUTDOWN_PU_off="checked";;
	esac

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <button type="submit" name="SUBMIT" value="Shutdown">gpio-shutdown</button>'
	echo '        <input type="hidden" name="FROM_PAGE" value="tweaks.cgi">'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <input id="gpiosd1" type="radio" name="GPIOSHUTDOWN" value="yes" '$GPIOSHUTDOWN_yes'>'
	echo '        <label for="gpiosd1">Yes&nbsp;&nbsp;</label>'
	echo '        <input id="gpiosd2" type="radio" name="GPIOSHUTDOWN" value="no" '$GPIOSHUTDOWN_no'>'
	echo '        <label for="gpiosd2">No</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        GPIO: <input class="form-control form-control-sm"'
	echo '             type="number"'
	echo '             name="GPIOSHUTDOWN_GPIO"'
	echo '             value="'$GPIOSHUTDOWN_GPIO'"'
	echo '             title="( 0 - 31 )"'
	echo '             min="0"'
	echo '             max="31"'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="gpiosd3" type="radio" name="GPIOSHUTDOWN_HI" value="yes" '$GPIOSHUTDOWN_HI_yes'>'
	echo '        <label for="gpiosd3">Active High</label>'
	echo '        <input id="gpiosd4" type="radio" name="GPIOSHUTDOWN_HI" value="no" '$GPIOSHUTDOWN_HI_no'>'
	echo '        <label for="gpiosd4">Active Low</label>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <input id="gpiosd5" type="radio" name="GPIOSHUTDOWN_PU" value="up" '$GPIOSHUTDOWN_PU_up'>'
	echo '        <label for="gpiosd5">Pull Up&nbsp;&nbsp;</label>'
	echo '        <input id="gpiosd6" type="radio" name="GPIOSHUTDOWN_PU" value="down" '$GPIOSHUTDOWN_PU_down'>'
	echo '        <label for="gpiosd6">Pull Down&nbsp;</label>'
	echo '        <input id="gpiosd7" type="radio" name="GPIOSHUTDOWN_PU" value="off" '$GPIOSHUTDOWN_PU_off'>'
	echo '        <label for="gpiosd7">Off</label>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
	#------------------------------------------------------------------------------------
	if [ "$GPIOSHUTDOWN" = "yes" -a ! -f /usr/local/bin/shutdown-monitor ]; then
		echo '  <form name="shutdown-monitor" action="writetoconfig.cgi" method="get">'
		#--------------------------------------------------------------------------------
		echo '    <div class="row">'
		echo '      <div class="'$COLUMN2_1'">'
		echo '        <button type="submit" name="SUBMIT" value="Install-monitor">Install Monitor</button>'
		echo '        <input type="hidden" name="FROM_PAGE" value="tweaks.cgi">'
		echo '      </div>'
		pcp_incr_id
		echo '      <div class="'$COLUMN2_2'">'
		echo '        <p>Install Shutdown Monitor (REQURIED to actually shutdown pCP)&nbsp;&nbsp;'
		echo '          <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>Monitors the gpio-keys driver for a linux KEY_POWER event</p>'
		echo '          <p>issues a system shutdown.</p>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
		#--------------------------------------------------------------------------------
		echo '  </form>'
	fi
	#------------------------------------------------------------------------------------
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_poweroff
#----------------------------------------------------------------------------------------

#========================================================================================
# Audio tweaks
#----------------------------------------------------------------------------------------
pcp_tweaks_audio_tweaks() {

	pcp_heading5 "Audio tweaks" hr

	case "$SQUEEZELITE" in
		yes) SQUEEZELITEyes="checked" ;;
		no) SQUEEZELITEno="checked" ;;
	esac

	echo '  <form name="setaudiotweaks" action="writetoaudiotweak.cgi" method="get">'
#-------------------------------------------Squeezelite------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Squeezelite</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="squeez1" type="radio" name="SQUEEZELITE" value="yes" '$SQUEEZELITEyes'>'
	echo '        <label for="squeez1">Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="squeez2" type="radio" name="SQUEEZELITE" value="no" '$SQUEEZELITEno'>'
	echo '        <label for="squeez2">No</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Automatically start Squeezelite when pCP starts&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Enable or disable that Squeezelite starts automatically.</p>'
	echo '          <p>If pCP is used as a LMS server or touch controler for other players it is not needed that Squeezelite starts.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#------------------------------------------------------------------------------------
	pcp_debug_variables "html" SQUEEZELITE SQUEEZELITEyes SQUEEZELITEno
#-------------------------------------------Shairport--------------------------------
	case "$SHAIRPORT" in
		yes) SHAIRPORTyes="checked" ;;
		no) SHAIRPORTno="checked" ;;
	esac

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Shairport-sync</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="shair1" type="radio" name="SHAIRPORT" value="yes" '$SHAIRPORTyes'>'
	echo '        <label for="shair1">Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="shair2" type="radio" name="SHAIRPORT" value="no" '$SHAIRPORTno'>'
	echo '        <label for="shair2">No</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'

	if [ "$SHAIRPORT" = "yes" ]; then
		echo '        <p><input type="button" name="CONFIG" onClick="location.href='\'''shairportsync.cgi''\''" value="Configure">&nbsp;'
	else
		echo '        <p>'
	fi

	echo '        <p>Use Shairport-sync to stream from iDevices&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Automatically start Shairport when pCP starts to stream audio from your iDevice.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#------------------------------------------------------------------------------------
	pcp_debug_variables "html" SHAIRPORT SHAIRPORTyes SHAIRPORTno
#-------------------------------------ALSA Equalizer---------------------------------
	case "$ALSAeq" in
		yes) ALSAeqyes="checked" ;;
		no) ALSAeqno="checked" ;;
	esac

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>ALSA 10 band Equalizer</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="alsaeq1" type="radio" name="ALSAeq" value="yes" '$ALSAeqyes'>'
	echo '        <label for="alsaeq1">Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="alsaeq2" type="radio" name="ALSAeq" value="no" '$ALSAeqno'>'
	echo '        <label for="alsaeq2">No</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'

	if [ "$ALSAeq" = "yes" ]; then
		echo '        <p><input type="button" name="CONFIG" onClick="location.href='\'''xtras_alsaequal.cgi''\''" value="Configure">&nbsp;'
	else
		echo '        <p>'
	fi

	echo '          Use 10 band ALSA equalizer&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p><b>Note: </b>Toggle ALSA Equalizer on off.</p>'
	echo '          <p><b>Steps to manually adjust Equalizer settings:</b></p>'
	echo '          <ol>'
	echo '            <li>Login via ssh.</li>'
	echo '            <li>Use "sudo alsamixer -D equal" and adjust the settings, press escape.</li>'
	echo '            <li>Backup ALSA settings by typing "sudo filetool.sh -b" or use "Backup button" on the Main page.</li>'
	echo '          </ol>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
#------------------------------------------------------------------------------------
	if [ "$ALSAeq" = "yes" ]; then
		echo '    <div class="row">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <p>Equalizer Device</p>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '        <input id="input'$ID'"'
		echo '               class="XXXX"'
		echo '               type="text"'
		echo '               name="EQUAL_OUT_DEVICE"'
		echo '               value="'$EQUAL_OUT_DEVICE'"'
		echo '               title="Select from list of input devices"'
		echo '               READONLY'
		echo '        >'
		echo '      </div>'
		pcp_incr_id
		echo '      <div class="'$COLUMN3_3'">'
		echo '        <p>Specify the input device from list&nbsp;&nbsp;'
		echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>Available input devices (click to use):</p>'
		echo '          <ul>'

		OPTION=1
		aplay -L 2>/dev/null | grep -E "^hw:" | while read -r IN
		do
			echo '            <li class="pointer" title="Click to use" onclick="pcp_copy_click_to_input('\'input${ID}\',\'EQoption${OPTION}\'')">'
			echo '              <span id="EQoption'${OPTION}'">'$IN'</span></li>'
			OPTION=$((OPTION + 1))
		done 

		echo '          </ul>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
	fi
#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '    </div>'
#------------------------------------------------------------------------------------
	pcp_debug_variables "html" ALSAeq ALSAeqno ALSAeqyes EQUAL_OUT_DEVICE
#--------------------------------------PCP Streamer----------------------------------
	case "$STREAMER" in
		yes) STREAMERyes="checked" ;;
		no) STREAMERno="checked" ;;
	esac

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Streamer for Audio Input</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="streamer1" type="radio" name="STREAMER" value="yes" '$STREAMERyes'>'
	echo '        <label for="streamer1">Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>'
	echo '        <input id="streamer2" type="radio" name="STREAMER" value="no" '$STREAMERno'>'
	echo '        <label for="streamer2">No</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	if [ "$STREAMER" = "no" ]; then
		echo '        <p>'
		echo '          Run streaming server for audio line-in or bluetooth input&nbsp;&nbsp;'
	else
		echo '        <p >Streamer installed. Basic url:'
		echo '          <a id="stream_url" href=""></a>&nbsp;&nbsp;'
	fi
	echo '            <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '            <p>To play stream from LMS, play URL as follows.</p>'
	echo '            <ul>'
	echo '              <li id="stream_usage"></li>'
	echo '              <li id="stream_flac"></li>'
	echo '              <li>pCP will stream 16bit, 44.1khz, 2 channels, flac output on port 9100.</li>'
	echo '            </ul>'
	echo '          </div>'
	echo '        </p>'
	echo '      </div>'
	echo '    </div>'
#------------------------------------------------------------------------------------
	if [ "$STREAMER" = "yes" ]; then
		echo '    <div class="row">'
		echo '      <div class="'$COLUMN3_1'">'
		echo '        <p>Input Device</p>'
		echo '      </div>'
		echo '      <div class="'$COLUMN3_2'">'
		echo '        <input id="input'$ID'"'
		echo '               class="XXXX"'
		echo '               type="text"'
		echo '               name="STREAMER_IN_DEVICE"'
		echo '               value="'$STREAMER_IN_DEVICE'"'
		echo '               title="Select from list of input devices"'
		echo '               READONLY'
		echo '        >'
		echo '      </div>'
		pcp_incr_id
		echo '      <div class="'$COLUMN3_3'">'
		echo '        <p>Specify the input device from list&nbsp;&nbsp;'
		echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
		echo '        </p>'
		echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
		echo '          <p>Available input devices (click to use):</p>'
		echo '          <ul>'

		OPTION=1
			arecord -L 2>/dev/null | grep -E "^hw:" | while read -r IN
		do
			echo '            <li class="pointer" title="Click to use" onclick="pcp_copy_click_to_input('\'input${ID}\',\'STRoption${OPTION}\'')">'
			echo '              <span id="STRoption'${OPTION}'">'$IN'</span></li>'
			OPTION=$((OPTION + 1))
		done 

		echo '          </ul>'
		echo '        </div>'
		echo '      </div>'
		echo '    </div>'
	fi
#------------------------------------------------------------------------------------
	echo '    <script>'
	if [ "$STREAMER" = "yes" ]; then
		echo '      document.getElementById("stream_url").setAttribute( "href",  "http://" + window.location.hostname + ":9100/S16_LE/44100/2/F" );'
		echo '      document.getElementById("stream_url").innerHTML = "http://" + window.location.hostname + ":9100/S16_LE/44100/2/F";'
	fi
	echo '      document.getElementById("stream_usage").innerHTML = "http://" + window.location.hostname + ":9100/&lt;format&gt;/&lt;rate&gt;/&lt;channels&gt;/&lt;F-flac or M-mp3&gt;";'
	echo '      document.getElementById("stream_flac").innerHTML = "i.e. http://" + window.location.hostname + ":9100/S16_LE/44100/2/F";'
	echo '    </script>'
#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '    </div>'
#------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_audio_tweaks
#----------------------------------------------------------------------------------------

#========================================================================================
# USB audio tweaks
#----------------------------------------------------------------------------------------
pcp_tweaks_usb_audio_tweaks() {

	pcp_heading5 "USB Audio tweaks" hr

	case "$CMD" in
		Default) CMDdefault="checked" ;;
		Slow) CMDslow="checked" ;;
	esac
	
	echo '  <form name="usbaudiotweaks" action="writetoaudiotweak.cgi" method="get">'
	#-----------------------------------------dwc_otg.speed------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>OTG-Speed</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="dwc1" type="radio" name="CMD" value="Default" '$CMDdefault'>'
	echo '        <label for="dwc1">Default</label>'
	echo '        <input id="dwc2" type="radio" name="CMD" value="Slow" '$CMDslow'>'
	echo '        <label for="dwc2">dwc_otg.speed=1</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Fix C-Media based DACs by "dwc_otg.speed=1"&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Adds "dwc_otg.speed=1" to cmdline.txt on the boot Device</p>'
	echo '          <p>The USB2.0 controller can have issues with USB1.1 audio devices, so this forces the controller into USB1.1 mode.</p>'
	echo '          <p>Often needed for C-Media based DACs if sound is crackling.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	pcp_debug_variables "html" CMD CMDdefault CMDslow
	#-------------------------------------------dwc_otg.fiq_fsm_enable=0 ----------------
	case "$FSM" in
		Default) FSMdefault="checked" ;;
		Disabled) FSMdisabled="checked" ;;
	esac

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>USB-FSM driver</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input id="fsm1" type="radio" name="FSM" value="Default" '$FSMdefault'>'
	echo '        <label for="fsm1">Default</label>'
	echo '        <input id="fsm2" type="radio" name="FSM" value="Disabled" '$FSMdisabled'>'
	echo '        <label for="fsm2">Disable USB-FSM</label>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Fix Emotiva XMC-1 DAC by "dwc_otg.fiq_fsm_enable=0"&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Adds "dwc_otg.fiq_fsm_enable=0" to cmdline.txt on the boot device</p>'
	echo '          <p>The USB controller can have issues with external DACs. If set to 0 the new FIQ_FSM driver is disabled and the old NOP FIQ is used.</p>'
	echo '          <p>This is needed for Emotiva XMC-1 DAC.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	pcp_debug_variables "html" FSM FSMdefault FSMdisabled
	#-----------------------------------FIQ-Split acceleration---------------------------
	case "$FIQ" in
		0x1) selected1="selected" ;;
		0x2) selected2="selected" ;;
		0x3) selected3="selected" ;;
		0x4) selected4="selected" ;;
		0x7) selected5="selected" ;;
		0x8) selected6="selected" ;;
		0xF) selected7="selected" ;;
	esac

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>FIQ-Split acceleration</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <select class="XXXX" name="FIQ">'
	echo '          <option value="0x1" '$selected1'>0x1 Accelerate non-periodic split transactions</option>'
	echo '          <option value="0x2" '$selected2'>0x2 Accelerate periodic split transactions</option>'
	echo '          <option value="0x3" '$selected3'>0x3 Accelerate all except high-speed isochronous transactions</option>'
	echo '          <option value="0x4" '$selected4'>0x4 Accelerate high-speed isochronous transactions</option>'
	echo '          <option value="0x7" '$selected5'>0x7 Accelerate all transactions</option>'
	echo '          <option value="0x8" '$selected6'>0x8 Enable Interrupt/Control Split Transaction hack</option>'
	echo '          <option value="0xF" '$selected7'>0xF Accelerate all transactions and Enable Split Transaction hack [DEFAULT]</option>'
	echo '        </select>'
	echo '      </div>'
	echo '    </div>'
	pcp_incr_id
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>&nbsp;</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <p>Change FIQ_FSM USB settings&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <ul>'
	echo '            <li>This might solve USB audio problems.</li>'
	echo '            <li>Important for specific USB DACs - like the Naim DAC-V1 card, try option 1, 2, 3 or 8.</li>'
	echo '            <li>Reboot is needed.</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	pcp_debug_variables "html" FIQ selected1 selected2 selected3 selected4
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_usb_audio_tweaks
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

	pcp_heading5 "Schedule CRON jobs" hr

	/etc/init.d/services/crond status >/dev/null 2>&1
	if [ $? -eq 0 ]; then
		pcp_green_tick " is running"
	else
		pcp_red_cross " is not running"
	fi

	echo '  <form name="cronjob" action="writetocronjob.cgi" method="get">'
	#-------------------------------------crond indicator--------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <p class="'$CLASS'">'$INDICATOR'</p>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>crond is '$STATUS'&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <ul>'
	echo '            <li><span class="indicator_green">&#x2714;</span> = crond running.</li>'
	echo '            <li><span class="indicator_red">&#x2718;</span> = crond not running.</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#-------------------------------------piCorePlayer reboot----------------------------
	case "$REBOOT" in
		Enabled) REBOOT_Y="checked" ;;
		Disabled) REBOOT_N="checked" ;;
	esac

	echo '    <div class="row">'
	echo '      <div class="col-3">'
	echo '        <p>Schedule piCorePlayer reboot<p>'
	echo '      </div>'

	echo '      <div class="col-12">'
	echo '        <div class="col">'
	echo '          <label for="RB_H">Hour:</label>'
	echo '          <input id="RB_H"'
	echo '                 class="form-control-sm"'
	echo '                 type="text"'
	echo '                 name="RB_H"'
	echo '                 value="'$RB_H'"'
	echo '                 maxlength="2"'
	echo '                 pattern="^(2[0-3]|1[0-9]|[0-9]|\*)$"'
	echo '          >'
	echo '        </div>'
	echo '        <div class="col">'
	echo '          <label for="RB_WD">&nbsp;&nbsp;Weekday (0-6):</label>'
	echo '          <input id="RB_WD"'
	echo '                 class="form-control-sm"'
	echo '                 type="text"'
	echo '                 name="RB_WD"'
	echo '                 value="'$RB_WD'"'
	echo '                 maxlength="1" pattern="^([0-6]|\*)$"'
	echo '          >'
	echo '        </div>'
	echo '        <div class="col">'
	echo '          <label for="RB_DMONTH">&nbsp;&nbsp;Day of Month:</label>'
	echo '          <input id="RB_DMONTH"'
	echo '                 class="form-control-sm"'
	echo '                 type="text"'
	echo '                 name="RB_DMONTH"'
	echo '                 value="'$RB_DMONTH'"'
	echo '                 maxlength="2"'
	echo '                 pattern="^(3[0-1]|2[0-9]|1[0-9]|[0-9]|\*)$"'
	echo '          >'
	echo '        </div>'
	echo '      </div>'
	echo '      <div class="col-3">'
	echo '        <input id="reboot1" type="radio" name="REBOOT" value="Enabled" '$REBOOT_Y'>'
	echo '        <label for="reboot1">Enabled</label>'
	echo '        <input id="reboot2" type="radio" name="REBOOT" value="Disabled" '$REBOOT_N'>'
	echo '        <label for="reboot2">Disabled</label>'
	echo '      </div>'
	echo '    </div>'
	#-------------------------------------Squeezelite restart----------------------------
	case "$RESTART" in
		Enabled) RESTART_Y="checked" ;;
		Disabled) RESTART_N="checked" ;;
	esac

	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Schedule Squeezelite restart</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <label for="RS_H">Hour:</label>'
	echo '        <input id="RS_H"'
	echo '               class="XXXX"'
	echo '               type="text"'
	echo '               name="RS_H"'
	echo '               value="'$RS_H'"'
	echo '               maxlength="2"'
	echo '               pattern="^(2[0-3]|1[0-9]|[0-9]|\*)$"'
	echo '        >'
	echo '        <label for="RS_WD">&nbsp;&nbsp;Weekday (0-6):</label>'
	echo '        <input id="RS_WD"'
	echo '               class="XXXX"'
	echo '               type="text"'
	echo '               name="RS_WD"'
	echo '               value="'$RS_WD'"'
	echo '               maxlength="1"'
	echo '               pattern="^([0-6]|\*)$"'
	echo '        >'
	echo '        <label for="RS_DMONTH">&nbsp;&nbsp;Day of Month:</label>'
	echo '        <input id="RS_DMONTH"'
	echo '               class="XXXX"'
	echo '               type="text"'
	echo '               name="RS_DMONTH"'
	echo '               value="'$RS_DMONTH'"'
	echo '               maxlength="2"'
	echo '               pattern="^(3[0-1]|2[0-9]|1[0-9]|[0-9]|\*)$"'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <input id="restart1" type="radio" name="RESTART" value="Enabled" '$RESTART_Y'>'
	echo '        <label for="restart1">Enabled</label>'
	echo '        <input id="restart2" type="radio" name="RESTART" value="Disabled" '$RESTART_N'>'
	echo '        <label for="restart2">Disabled</label>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p></p>'
	echo '      </div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <p>Fill out the crontab fields&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>"*" it means every hour, every day, every month.</p>'
	echo '          <p><b>Example:</b></p>'
	echo '          <ul>'
	echo '            <li>2 * * - run job at 02:00 everyday</li>'
	echo '            <li>0 1 * - run job at 00:00 every monday</li>'
	echo '            <li>0 * 1 - run job at 00:00 the first every month</li>'
	echo '          </ul>'
	echo '          <p><b>Root crontab:</b></p>'
	echo '          <textarea class="width600">'"$(cat /var/spool/cron/crontabs/root)"'</textarea>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#-------------------------------------Custom Cron command----------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_1'">Custom Cron command</div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm" type="text" name="CRON_COMMAND" value="'$CRON_COMMAND'" maxlength="254">'
	echo '      </div>'
	echo '    </div>'
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN3_2'"></div>'
	pcp_incr_id
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Add user defined commands to the cron scheduler&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This feature gives advanced users the possibility to manipulate the cron scheduler.'
	echo '             It will allow users to add a single command to the cron job or'
	echo '             to schedule a script that performs multiple actions.</p>'
	echo '          <p>Use ordinary cron syntax.</p>'
	echo '          <p><b>Example:</b></p>'
	echo '          <ul>'
	echo '            <li>1 1 * * * /path/to/your/script.sh</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#-------------------------------------Buttons----------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN1_1'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Reset">'
	[ $MODE -ge $MODE_PLAYER ] &&
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Clear">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	pcp_debug_variables "html" REBOOT REBOOT_Y REBOOT_N RESTART RESTART_Y RESTART_N
	#------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_cron
#----------------------------------------------------------------------------------------

#----------------------------------------------User Commands-----------------------------
pcp_tweaks_user_commands() {

	pcp_heading5 "User commands" hr

	echo '  <form name="setusercommands" action="writetoautostart.cgi" method="get">'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN2_1'">User command #1</div>'
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               id="USER_COMMAND_1"'
	echo '               name="USER_COMMAND_1"'
	echo '               value="'$USER_COMMAND_1'"'
	echo '               maxlength="254"'
	echo '               title="Invalid characters: &amp; &quot;"'
	echo '               pattern="[^\&\x22]+"'
	echo '        >'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN2_1'">User command #2</div>'
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               id="USER_COMMAND_2"'
	echo '               name="USER_COMMAND_2"'
	echo '               value="'$USER_COMMAND_2'"'
	echo '               maxlength="254"'
	echo '               title="Invalid characters: &amp; &quot;"'
	echo '               pattern="[^\&\x22]+"'
	echo '        >'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN2_1'">User command #3</div>'
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               id="USER_COMMAND_3"'
	echo '               name="USER_COMMAND_3"'
	echo '               value="'$USER_COMMAND_3'"'
	echo '               maxlength="254"'
	echo '               title="Invalid characters: &amp; &quot;"'
	echo '               pattern="[^\&\x22]+"'
	echo '        >'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <script>'
	echo '       var cmd1 = "'$USER_COMMAND_1'";'
	echo '       var cmd2 = "'$USER_COMMAND_2'";'
	echo '       var cmd3 = "'$USER_COMMAND_3'";'
	echo '       document.getElementById("USER_COMMAND_1").value = decodeURIComponent(cmd1.replace(/\+/g, "%20"));'
	echo '       document.getElementById("USER_COMMAND_2").value = decodeURIComponent(cmd2.replace(/\+/g, "%20"));'
	echo '       document.getElementById("USER_COMMAND_3").value = decodeURIComponent(cmd3.replace(/\+/g, "%20"));'
	echo '    </script>'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN2_1'"></div>'
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p>Adds user defined commands to the piCorePlayer startup procedure&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This feature gives advanced users a couple of hooks into the startup procedure.'
	echo '             It will allow advanced users the ability to run extra instances of Squeezelite for example,'
	echo '             or maybe, run a Linux procedure that shuts down processes, like the web server to optimise performance.</p>'
	echo '          <p>User commands run after auto start LMS commands and auto start favorites.</p>'
	echo '          <p>User commands will run in order 1, 2, 3.</p>'
	echo '          <p><b>Example:</b></p>'
	echo '          <ul>'
	echo '            <li>ls /tmp >> /tmp/directory.log</li>'
	echo '          </ul>'
	echo '          <p><b>Invalid characters:</b> &amp; &quot;</p>'
	echo '          <p>If starting a second instance of Squeezelite - notice that we only accepts name without empty space. So change <b>first floor</b> to <b>first_floor</b> etc.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	echo '    <div class="row">'
	echo '      <div class="'$COLUMN2_1'">'
	echo '        <input class="'$BUTTON' mb-1" type="submit" name="SUBMIT" value="Save">'
	echo '        <input class="'$BUTTON' mb-1" type="submit" name="SUBMIT" value="Clear">'
	echo '        <input type="hidden" name="AUTOSTART" value="CMD">'
	echo '      </div>'
	echo '    </div>'
	#------------------------------------------------------------------------------------
	pcp_debug_variables "html" USER_COMMAND_1 USER_COMMAND_2 USER_COMMAND_3
	#------------------------------------------------------------------------------------
	echo '  </form>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_tweaks_user_commands
#----------------------------------------------------------------------------------------

pcp_the_end
