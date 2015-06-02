#!/bin/sh

# Version: 0.01 2015-06-02 GE
#   Original version.

#========================================================================================
# References:
#   http://elinux.org/RPi_Overclocking
#   http://github.com/asb/raspi-config
#----------------------------------------------------------------------------------------

#========================================================================================
# Overclocking data from raspi-config (Rasbian 2015-05-05)
#----------------------------------------------------------------------------------------
# "None"   "700MHz ARM,  250MHz core, 400MHz SDRAM, 0 overvolt"
# "Modest" "800MHz ARM,  250MHz core, 400MHz SDRAM, 0 overvolt"
# "Medium" "900MHz ARM,  250MHz core, 450MHz SDRAM, 2 overvolt"
# "High"   "950MHz ARM,  250MHz core, 450MHz SDRAM, 6 overvolt"
# "Turbo"  "1000MHz ARM, 500MHz core, 600MHz SDRAM, 6 overvolt"
# "Pi2"    "1000MHz ARM, 500MHz core, 500MHz SDRAM, 2 overvolt"
#----------------------------------------------------------------------------------------

#========================================================================================
# Userspace: /sys/devices/system/cpu/cpu0/cpufreq/
#----------------------------------------------------------------------------------------
# affected_cpus                  related_cpus                     scaling_governor
# cpuinfo_cur_freq               scaling_available_frequencies    scaling_max_freq
# cpuinfo_max_freq               scaling_available_governors      scaling_min_freq
# cpuinfo_min_freq               scaling_cur_freq                 scaling_setspeed
# cpuinfo_transition_latency     scaling_driver
#----------------------------------------------------------------------------------------

. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras overclocking" "GE"

pcp_controls
pcp_banner
pcp_running_string
pcp_xtras
pcp_httpd_query_string

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_set_overclock() {
	[ $DEBUG = 1] && echo '<p class="info">[ INFO ] Setting OVERCLOCK to '$1'</p>'
	sudo sed -i "/arm_freq=/c\arm_freq=$2" $CONFIGTXT
	sudo sed -i "/core_freq=/c\core_freq=$3" $CONFIGTXT
	sudo sed -i "/sdram_freq=/c\sdram_freq=$4" $CONFIGTXT
	sudo sed -i "/over_voltage=/c\over_voltage=$5" $CONFIGTXT
}

pcp_set_overclock_default() {
	[ $DEBUG = 1] && echo '<p class="info">[ INFO ] Setting OVERCLOCK to DEFAULT</p>'
	pcp_set_overclock NONE 700 250 400 0
	sudo sed -i 's/^arm_freq=/#arm_freq=/g' $CONFIGTXT
	sudo sed -i 's/^core_freq=/#core_freq=/g' $CONFIGTXT
	sudo sed -i 's/^sdram_freq=/#sdram_freq=/g' $CONFIGTXT
	sudo sed -i 's/^over_voltage=/#over_voltage=/g' $CONFIGTXT
	pcp_set_force_turbo_default
}

pcp_set_force_turbo() {
	[ $DEBUG = 1] && echo '<p class="info">[ INFO ] Setting FORCE_TURBO to '$1'</p>'
	sudo sed -i "/force_turbo=/c\force_turbo=$1" $CONFIGTXT
}

pcp_set_force_turbo_default() {
	[ $DEBUG = 1] && echo '<p class="info">[ INFO ] Setting FORCE_TURBO to DEFAULT</p>'
	pcp_set_force_turbo 0
	sudo sed -i 's/^force_turbo=/#force_turbo=/g' $CONFIGTXT
}

pcp_set_gpu_memory() {
	[ $DEBUG = 1] && echo '<p class="info">[ INFO ] Setting GPU memory to '$1'</p>'
	sudo sed -i "/gpu_mem=/c\gpu_mem=$1" $CONFIGTXT
}

pcp_set_gpu_memory_default() {
	[ $DEBUG = 1] && echo '<p class="info">[ INFO ] Setting GPU memory to DEFAULT</p>'
	sudo sed -i 's/^gpu_mem=/#gpu_mem=/g' $CONFIGTXT
}

pcp_display_current() {
	echo -n '<p class="info">'
	for FILE in $(ls /sys/devices/system/cpu/cpu0/cpufreq/); do
		echo -n $FILE': '
		cat /sys/devices/system/cpu/cpu0/cpufreq/$FILE
		echo '<br />'
	done
	echo '</p>'
}

pcp_display_config_txt() {
	pcp_mount_mmcblk0p1 >/dev/null 2>&1
	echo '<textarea class="inform" style="height:80px">'
	sed -n '/uncomment to overclock/{n;p;n;p;n;p;n;p;n;p;n;p}' $CONFIGTXT
	echo '</textarea>'
	pcp_umount_mmcblk0p1 >/dev/null 2>&1
}

pcp_start_save() {
	# Decode $OVERCLOCK using httpd, add quotes
	OVERCLOCK=`sudo $HTPPD -d \"$OVERCLOCK\"`
	sudo sed -i "s/\(OVERCLOCK *=*\).*/\1$OVERCLOCK/" $CONFIGCFG

	pcp_backup >/dev/null 2>&1

	pcp_mount_mmcblk0p1_nohtml >/dev/null 2>&1

	if mount | grep $VOLUME >/dev/null 2>&1; then
		[ $DEBUG = 1] && echo '<p class="info">[ INFO ] '$VOLUME' is mounted.</p>'
	else
		pcp_go_back_button
		echo '</body>'
		echo '</html>'
	fi

	. $CONFIGCFG
	case $OVERCLOCK in
		DEFAULT)
			pcp_set_overclock_default
			;;
		UNDER)
			pcp_set_overclock UNDER 600 250 400 0
			;;
		NONE)
			pcp_set_overclock NONE 700 250 400 0
			;;
		MODEST)
			pcp_set_overclock MODEST 800 250 400 0
			;;
		MEDIUM)
			pcp_set_overclock MEDIUM 900 250 450 2
			;;
		HIGH)
			pcp_set_overclock HIGH 950 250 450 6
			;;
		TURBO)
			pcp_set_overclock TURBO 1000 500 600 6
			;;
		PI2)
			pcp_set_overclock PI2 1000 500 500 2
			;;
		*)
			[ $DEBUG = 1] && echo '<p class="error">[ ERROR ] Invalid overclock option: '$OVERCLOCK'</p>'
			;;
	esac

	case $FORCETURBO in
		DEFAULT)
			pcp_set_force_turbo_default
			;;
		0)
			pcp_set_force_turbo 0
			;;
		1)
			pcp_set_force_turbo 1
			;;
		*)
			[ $DEBUG = 1] && echo '<p class="error">[ ERROR ] Invalid force option: '$FORCETURBO'</p>'
			;;
	esac

	case $GPUMEMORY in
		DEFAULT)
			pcp_set_gpu_memory_default
			;;
		16)
			pcp_set_gpu_memory 16
			;;
		32)
			pcp_set_gpu_memory 32
			;;
		64)
			pcp_set_gpu_memory 64
			;;
		*)
			[ $DEBUG = 1] && echo '<p class="error">[ ERROR ] Invalid gpu memory option: '$GPUMEMORY'</p>'
			;;
	esac

	[ $DEBUG = 1 ] && pcp_check_config_txt
	[ $(pcp_check_force_turbo) = 0 ] && echo '<p class="info">[ INFO ] Force turbo set</p>' || echo '<p class="error">[ ERROR ] Force turbo NOT set</p>' 
	[ $(pcp_check_over_voltage) = 0 ] && echo '<p class="info">[ INFO ] Over voltage set</p>' || echo '<p class="error">[ ERROR ] Over voltage NOT set</p>'
	[ $(pcp_check_force_turbo) = 0 ] && [ $(pcp_check_over_voltage) = 0 ] && echo '<p class="error">[ ERROR ] Warranty bit will be set if you reboot</p>'

	#echo '<p class="info">Revision: '$(pcp_rpi_revision)'</p>'
	[ $(pcp_rpi_warranty) = 0 ] &&
	echo '<p class="error">[ ERROR ] Warranty bit is already set: '$(pcp_rpi_revision)'</p>' || echo '<p class="info">[ INFO ] Warranty bit is NOT set: '$(pcp_rpi_revision)'</p>'

	echo -n $OCGOVERNOR | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor >/dev/null
	pcp_umount_mmcblk0p1 >/dev/null 2>&1
}

pcp_check_config_txt() {
	for I in arm_freq= core_freq= sdram_freq= over_voltage= force_turbo= gpu_mem=; do
		if cat $CONFIGTXT | grep $I >/dev/null 2>&1; then
			echo '<p class="info">[ INFO ] "'$I'" found in '$CONFIGTXT'</p>'
		else
			echo '<p class="error">[ ERROR ] "'$I'" NOT found in '$CONFIGTXT'</p>'
		fi
	done
}

pcp_check_force_turbo() {
	FTSET=$(cat $CONFIGTXT | grep force_turbo=)
	case $FTSET in
		force_turbo=1)
			echo 0
			;;
		*)
			echo 1
			;;
	esac
}

pcp_check_over_voltage() {
	OVSET=$( cat $CONFIGTXT | grep over_voltage= )
	case $OVSET in
		over_voltage=0 | \#over_voltage=*)
			echo 1
			;;
		over_voltage=*)
			echo 0
			;;
	esac
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
case $SUBMIT in
	Save)
		[ $DEBUG = 1] && echo '<p class="info">[ INFO ] SUBMIT='$SUBMIT' </p>'
		pcp_start_save
		;;
	*)
		[ $DEBUG = 1] && echo '<p class="error">[ ERROR ] Invalid submit option: '$SUBMIT'</p>'
		;;
esac

#----------------------------------------------------------------------------------------
# Function to set selected item in the pull down list
#----------------------------------------------------------------------------------------
case $OVERCLOCK in
	DEFAULT)
		OCdefault="selected"
		;;
	UNDER)
		OCunder="selected"
		;;
	NONE)
		OCnone="selected"
		;;
	MODEST)
		OCmodest="selected"
		;;
	MEDIUM)
		OCmedium="selected"
		;;
	HIGH)
		OChigh="selected"
		;;
	TURBO)
		OCturbo="selected"
		;;
	PI2)
		OCpi2="selected"
		;;
	*)
		OCdefault=""
		OCunder=""
		OCnone=""
		OCmodest=""
		OCmedium=""
		OChigh=""
		OCturbo=""
		OCpi2=""
		;;
esac

#----------------------------------------------------------------------------------------
# Function to set selected item in the pull down list
#----------------------------------------------------------------------------------------
pcp_mount_mmcblk0p1 >/dev/null 2>&1
FORCETURBO=$(cat $CONFIGTXT | grep force_turbo)

case $FORCETURBO in
	\#force_turbo=0)
		FTdefault="selected"
		;;
	force_turbo=0)
		FT0="selected"
		;;
	force_turbo=1)
		FT1="selected"
		;;
esac

GPUMEMORY=$(cat $CONFIGTXT | grep gpu_mem)

case $GPUMEMORY in
	\#gpu_mem=)
		GMdefault="selected"
		;;
	gpu_mem=16)
		GM16="selected"
		;;
	gpu_mem=32)
		GM32="selected"
		;;
	gpu_mem=64)
		GM64="selected"
		;;
esac

pcp_umount_mmcblk0p1 >/dev/null 2>&1

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Overclocking</legend>'
echo '          <table class="bggrey percent100">'
echo '            <form name="overclock" action= "xtras_overclock.cgi" method="get">'
echo '              <tr class="warning">'
echo '                <td colspan="3">'
echo '                  <p style="color:white"><b>Note:</b> Excessive overclocking can cause your Raspberry Pi to become unstable.</b></p>'
echo '                </td>'
echo '              </tr>'
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Overclock</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <select name="OVERCLOCK">'
if [ $(pcp_rpi_is_model_2B) = 1 ]; then
	[ $MODE = 99 ] &&
	echo '                    <option value="DEFAULT" '$OCdefault'>Default</option>'
	echo '                    <option value="UNDER" '$OCunder'>Under</option>'
	echo '                    <option value="NONE" '$OCnone'>None</option>'
	echo '                    <option value="MODEST" '$OCmodest'>Modest</option>'
	echo '                    <option value="MEDIUM" '$OCmedium'>Moderate</option>'
	if [ $MODE = 99 ]; then
		echo '                    <option value="HIGH" '$OChigh'>High</option>'
		echo '                    <option value="TURBO" '$OCturbo'>Turbo</option>'
	fi
fi
if [ $(pcp_rpi_is_model_2B) = 0 ]; then
	echo '                    <option value="DEFAULT" '$OCdefault'>Default</option>'
	echo '                    <option value="PI2" '$OCpi2'>Pi2</option>'
fi
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Change Raspberry Pi overclocking&nbsp;&nbsp;'
echo '                  <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a></p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>&lt;Default|None|Under|Modest|Medium|High|Turbo|Pi2&gt;</p>'
echo '                    <p>Reboot is required.<p>'
echo '                    <p><b>Note:</b> If Raspberry Pi fails to boot:</p>'
echo '                    <ul>'
echo '                      <li>hold down the shift key during booting, or</li>'
echo '                      <li>edit the config.txt file manually</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'

pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="warning">'
echo '                <td class="column150">'
echo '                  <p style="color:white">Force turbo</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <select name="FORCETURBO">'
echo '                    <option value="DEFAULT" '$FTdefault'>Default</option>'
echo '                    <option value="0" '$FT0'>0</option>'
echo '                    <option value="1" '$FT1'>1</option>'
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p style="color:white">Change Raspberry Pi force turbo setting&nbsp;&nbsp;'
echo '                  <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a></p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p style="color:white">&lt;Default|0|1&gt;</p>'
echo '                    <p style="color:white"><b>Warning: </b>Setting force turbo may set warranty bit.<p>'
echo '                    <p style="color:white">Reboot is required.<p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'

pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Overclock governor</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <select name="OCGOVERNOR">'
                          for GOV in $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors); do
                              SCALINGGOVERNOR=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor)
                              [ $GOV = $SCALINGGOVERNOR ] && SEL="selected" || SEL=""
                              echo '                    <option value="'$GOV'" '$SEL'>'$GOV'</option>'
                          done
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Change overclocking governor &nbsp;&nbsp;'
echo '                  <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a></p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>&lt;'$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors)'&gt;</p>'
echo '                    <p>Dynamically set, no reboot is required.<p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'

pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>GPU memory</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <select name="GPUMEMORY">'
echo '                    <option value="DEFAULT" '$GMdefault'>Default</option>'
echo '                    <option value="16" '$GM16'>16</option>'
echo '                    <option value="32" '$GM32'>32</option>'
echo '                    <option value="64" '$GM64'>64</option>'
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Change GPU memory setting&nbsp;&nbsp;'
echo '                  <a class="moreless" id="'$ID'a" href=# onclick="return more('\'''$ID''\'')">more></a></p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>&lt;Default|16|32|64&gt;</p>'
echo '                    <p>Reboot is required.<p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'

pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
echo '                </td>'
echo '              </tr>'

pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                </td>'
echo '              </tr>'

pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
                        pcp_display_config_txt
echo '                </td>'
echo '              </tr>'
echo '            </form>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

if [ $DEBUG = 1 ]; then
	#========================================================================================
	# Display debug information
	#----------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="debug information" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Debug information</legend>'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p class="debug">[ DEBUG ] $OVERCLOCK: '$OVERCLOCK'<br />'
	echo '                                   [ DEBUG ] $OCdefault: '$OCdefault'<br />'
	echo '                                   [ DEBUG ] $OCunder: '$OCunder'<br />'
	echo '                                   [ DEBUG ] $OCnone: '$OCnone'<br />'
	echo '                                   [ DEBUG ] $OCmodest: '$OCmodest'<br />'
	echo '                                   [ DEBUG ] $OCmedium: '$OCmedium'<br />'
	echo '                                   [ DEBUG ] $OChigh: '$OChigh'<br />'
	echo '                                   [ DEBUG ] $OCturbo: '$OCturbo'<br />'
	echo '                                   [ DEBUG ] $OCpi2: '$OCpi2'</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p class="debug">[ DEBUG ] $FORCETURBO: '$FORCETURBO'<br />'
	echo '                                   [ DEBUG ] $FT0: '$FT0'<br />'
	echo '                                   [ DEBUG ] $FT1: '$FT1'</p>'
	echo '                  <p class="debug">[ DEBUG ] $GPUMEMORY: '$GPUMEMORY'<br />'
	echo '                                   [ DEBUG ] $GMdefault: '$GMdefault'<br />'
	echo '                                   [ DEBUG ] $GM16: '$GM16'<br />'
	echo '                                   [ DEBUG ] $GM32: '$GM32'<br />'
	echo '                                   [ DEBUG ] $GM64: '$GM64'</p>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

if [ $MODE = 99 ]; then
	#========================================================================================
	# Display current overclock settings
	#----------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="overclock_settings" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Current overclock settings</legend>'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_display_current
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'

	#========================================================================================
	# Display current config.cfg
	#----------------------------------------------------------------------------------------
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="current_config.cfg" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Current config.cfg</legend>'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "cat $CONFIGCFG" 400
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'