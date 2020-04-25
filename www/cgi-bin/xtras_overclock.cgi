#!/bin/sh

# Version: 6.0.0 2020-01-29

#========================================================================================
# References:
#	http://elinux.org/RPi_Overclocking
#	https://github.com/RPi-Distro/raspi-config
#----------------------------------------------------------------------------------------
# The following lines need to be included in config.txt:
#arm_freq=
#core_freq=
#sdram_freq=
#over_voltage=
#force_turbo=
#gpu_mem=
#----------------------------------------------------------------------------------------

#========================================================================================
# Userspace: /sys/devices/system/cpu/cpu0/cpufreq/
#----------------------------------------------------------------------------------------
# affected_cpus                 related_cpus                      scaling_governor
# cpuinfo_cur_freq              scaling_available_frequencies     scaling_max_freq
# cpuinfo_max_freq              scaling_available_governors       scaling_min_freq
# cpuinfo_min_freq              scaling_cur_freq                  scaling_setspeed
# cpuinfo_transition_latency    scaling_driver
#----------------------------------------------------------------------------------------

. pcp-functions
. pcp-rpi-functions

pcp_html_head "xtras overclocking" "GE"

pcp_banner
pcp_xtras
pcp_running_script
pcp_httpd_query_string

RPITYPE=$(pcp_rpi_type)
REBOOT_REQUIRED=0

#========================================================================================
# Generate warning message
#----------------------------------------------------------------------------------------
pcp_warning_message() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Warning</legend>'
	echo '          <table class="bgred percent100">'
	echo '            <tr>'
	echo '              <td>'
	echo '                <p><b>Warning:</b></p>'
	echo '                <ul>'
	echo '                  <li>It can be dangerous to play with overclocking.</li>'
	echo '                  <li>Excessive overclocking can cause your Raspberry Pi to become unstable.</li>'
	echo '                  <li>Setting "force turbo" may set warranty bit.</li>'
	echo '                  <li>Do not transfer SD card bewteen different model Raspberry Pi.</li>'
	echo '                </ul>'
	echo '                <p><b>Note:</b></p>'
	echo '                <ul>'

	MESSAGEPI0='<li>Raspberry Pi Model 0: Underclocking only.</li>'
	MESSAGEPI1='<li>Raspberry Pi Model 1: Overclocking and underclocking.</li>'
	MESSAGEPI2='<li>Raspberry Pi Model 2: Overclocking and underclocking.</li>'
	MESSAGEPI3='<li>Raspberry Pi Model 3: Underclocking only.</li>'
	MESSAGEPI4='<li>Raspberry Pi Model 4: Underclocking only.</li>'

	case $RPITYPE in
		0) MESSAGEPI0='<li><b>&lt;&lt; Raspberry Pi Model 0: Underclocking only. &gt;&gt;</b></li>' ;;
		1) MESSAGEPI1='<li><b>&lt;&lt; Raspberry Pi Model 1: Overclocking and underclocking. &gt;&gt;</b></li>' ;;
		2) MESSAGEPI2='<li><b>&lt;&lt; Raspberry Pi Model 2: Overclocking and underclocking. &gt;&gt;</b></li>' ;;
		3) MESSAGEPI3='<li><b>&lt;&lt; Raspberry Pi Model 3: Underclocking only. &gt;&gt;</b></li>' ;;
		4) MESSAGEPI4='<li><b>&lt;&lt; Raspberry Pi Model 4: Underclocking only. &gt;&gt;</b></li>' ;;
	esac

	echo "                  $MESSAGEPI0"
	echo "                  $MESSAGEPI1"
	echo "                  $MESSAGEPI2"
	echo "                  $MESSAGEPI3"
	echo "                  $MESSAGEPI4"

	echo '                </ul>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_set_overclock() {
	[ $DEBUG -eq 1 ] && echo '<p class="info">[ INFO ] Setting OVERCLOCK to '$1'</p>'

	sudo sed -i "/arm_freq=/c\arm_freq=$2" $CONFIGTXT
	case $RPITYPE in
		0|1|2|3)
			sudo sed -i "/gpu_freq=/c\gpu_freq=$3" $CONFIGTXT
			sudo sed -i "/core_freq=/c\core_freq=$4" $CONFIGTXT
			sudo sed -i "/sdram_freq=/c\sdram_freq=$5" $CONFIGTXT
			sudo sed -i "/over_voltage=/c\over_voltage=$6" $CONFIGTXT
		;;
		4)	# Cannot gpu/core/sdram frequencies are mostly locked on the pi4
			sudo sed -i 's/^gpu_freq=/#gpu_freq=/g' $CONFIGTXT
			sudo sed -i 's/^core_freq=/#core_freq=/g' $CONFIGTXT
			sudo sed -i 's/^sdram_freq=/#sdram_freq=/g' $CONFIGTXT
			sudo sed -i 's/^over_voltage=/#over_voltage=/g' $CONFIGTXT
		;;
	esac
}

pcp_set_overclock_default() {
	[ $DEBUG -eq 1 ] && echo '<p class="info">[ INFO ] Setting OVERCLOCK to DEFAULT</p>'
	sudo sed -i 's/^arm_freq=/#arm_freq=/g' $CONFIGTXT
	sudo sed -i 's/^gpu_freq=/#gpu_freq=/g' $CONFIGTXT
	sudo sed -i 's/^core_freq=/#core_freq=/g' $CONFIGTXT
	sudo sed -i 's/^sdram_freq=/#sdram_freq=/g' $CONFIGTXT
	sudo sed -i 's/^over_voltage=/#over_voltage=/g' $CONFIGTXT
	pcp_set_force_turbo_default
}

pcp_set_force_turbo() {
	[ $DEBUG -eq 1 ] && echo '<p class="info">[ INFO ] Setting FORCE_TURBO to '$1'</p>'
	sudo sed -i "/force_turbo=/c\force_turbo=$1" $CONFIGTXT
}

pcp_set_force_turbo_default() {
	[ $DEBUG -eq 1 ] && echo '<p class="info">[ INFO ] Setting FORCE_TURBO to DEFAULT</p>'
	pcp_set_force_turbo 0
	sudo sed -i 's/^force_turbo=/#force_turbo=/g' $CONFIGTXT
}

pcp_set_gpu_memory() {
	[ $DEBUG -eq 1 ] && echo '<p class="info">[ INFO ] Setting GPU memory to '$1'</p>'
	sudo sed -i "/gpu_mem=/c\gpu_mem=$1" $CONFIGTXT
}

pcp_set_gpu_memory_default() {
	[ $DEBUG -eq 1 ] && echo '<p class="info">[ INFO ] Setting GPU memory to DEFAULT</p>'
	sudo sed -i 's/^gpu_mem=/#gpu_mem=/g' $CONFIGTXT
}

pcp_display_current() {
	echo -n '<p style="font-family:courier">'
	for FILE in $(ls /sys/devices/system/cpu/cpu0/cpufreq/ | grep -v stats); do
		echo -n $FILE': '
		cat /sys/devices/system/cpu/cpu0/cpufreq/$FILE | sed 's/[<>]//g'
		echo '<br />'
	done
	echo '</p>'
}

pcp_display_config_txt() {
	pcp_mount_bootpart >/dev/null 2>&1
	echo '<textarea class="inform" style="height:80px">'
	sed -n '/uncomment to overclock/{n;p;n;p;n;p;n;p;n;p;n;p}' $CONFIGTXT
	echo '</textarea>'
	pcp_umount_bootpart >/dev/null 2>&1
}

pcp_start_save() {
	pcp_save_to_config
	pcp_backup >/dev/null 2>&1

	pcp_mount_bootpart_nohtml >/dev/null 2>&1

	if mount | grep $VOLUME >/dev/null 2>&1; then
		[ $DEBUG -eq 1 ] && echo '<p class="info">[ INFO ] '$VOLUME' is mounted.</p>'
	else
		pcp_go_back_button
		echo '</body>'
		echo '</html>'
	fi

	. $PCPCFG

	#========================================================================================
	# Official overclocking data from raspi-config - Raspbian
	#----------------------------------------------------------------------------------------
	#  RPi0
	#     "None"
	#  RPi1
	#     "None"   "700MHz ARM, 250MHz gpu, 250MHz core, 400MHz SDRAM, 0 overvolt"
	#     "Modest" "800MHz ARM, 250MHz gpu, 250MHz core, 400MHz SDRAM, 0 overvolt"
	#     "Medium" "900MHz ARM, 250MHz gpu, 250MHz core, 450MHz SDRAM, 2 overvolt"
	#     "High"   "950MHz ARM, 250MHz gpu, 250MHz core, 450MHz SDRAM, 6 overvolt"
	#     "Turbo" "1000MHz ARM, 250MHz gpu, 500MHz core, 600MHz SDRAM, 6 overvolt"
	#  RPi2
	#     "None"   "900MHz ARM, 250MHz gpu, 250MHz core, 450MHz SDRAM, 0 overvolt"
	#     "High"  "1000MHz ARM, 250MHz gpu, 500MHz core, 500MHz SDRAM, 2 overvolt"
	#  RPi3
	#     "None"
	#----------------------------------------------------------------------------------------

	#========================================================================================
	# Underclocking data
	#----------------------------------------------------------------------------------------
	#  RPi0
	#     "Lowest"  "600MHz ARM, 250MHz gpu, 250MHz core, 400MHz SDRAM, 0 overvolt"
	#     "Under"   "800MHz ARM, 200MHz gpu, 200MHz core, 400MHz SDRAM, 0 overvolt"
	#  RPi1
	#     "Lowest"  "600MHz ARM, 250MHz gpu, 250MHz core, 400MHz SDRAM, 0 overvolt"
	#     "Under"   "800MHz ARM, 200MHz gpu, 200MHz core, 400MHz SDRAM, 0 overvolt"
	#  RPi2
	#     "Lowest"  "600MHz ARM, 250MHz gpu, 250MHz core, 400MHz SDRAM, 0 overvolt"
	#     "Under"   "800MHz ARM, 200MHz gpu, 200MHz core, 400MHz SDRAM, 0 overvolt"
	#  RPi3
	#     "Lowest"  "600MHz ARM, 250MHz gpu, 250MHz core, 400MHz SDRAM, 0 overvolt"
	#     "Under"   "800MHz ARM, 200MHz gpu, 200MHz core, 400MHz SDRAM, 0 overvolt"
	#----------------------------------------------------------------------------------------

	case $RPITYPE in
		0)
			case "$ADVOVERCLOCK" in
				Lowest)pcp_set_overclock Lowest 600 250 250 400 0 ;;
				Under) pcp_set_overclock Under 800 200 200 400 0 ;;
				None)  pcp_set_overclock_default ;;
				*)     pcp_set_overclock_default ;;
			esac
		;;
		1)
			case "$ADVOVERCLOCK" in
				Lowest) pcp_set_overclock Lowest 600 250 250 400 0 ;;
				Under)  pcp_set_overclock Under 800 200 200 400 0 ;;
				None)   pcp_set_overclock_default ;;
				Modest) pcp_set_overclock Modest 800 250 250 400 0 ;;
				Medium) pcp_set_overclock Medium 900 250 250 450 2 ;;
				High)   pcp_set_overclock High 950 250 250 450 6 ;;
				Turbo)  pcp_set_overclock Turbo 1000 250 500 600 6 ;;
				*)      pcp_set_overclock_default ;;
			esac
		;;
		2)
			case "$ADVOVERCLOCK" in
				Lowest)pcp_set_overclock Lowest 600 250 250 400 0 ;;
				Under) pcp_set_overclock Under 800 200 200 400 0 ;;
				None)  pcp_set_overclock_default ;;
				High)  pcp_set_overclock High 1000 250 500 500 2 ;;
				*)     pcp_set_overclock_default ;;
			esac
		;;
		3)
			case "$ADVOVERCLOCK" in
				Lowest)pcp_set_overclock Lowest 600 250 250 400 0 ;;
				Under) pcp_set_overclock Under 800 200 200 400 0 ;;
				None)  pcp_set_overclock_default ;;
				*)     pcp_set_overclock_default ;;
			esac
		;;
		4)
			case "$ADVOVERCLOCK" in
				Under) pcp_set_overclock Under 800 500 500 3200 0 ;;
				None)  pcp_set_overclock_default ;;
				*)     pcp_set_overclock_default ;;
			esac
		;;
	esac

	case "$FORCETURBO" in
		DEFAULT) pcp_set_force_turbo_default ;;
		0)       pcp_set_force_turbo 0 ;;
		1)       pcp_set_force_turbo 1 ;;
		*)       [ $DEBUG -eq 1 ] && echo '<p class="error">[ ERROR ] Invalid force option: '$FORCETURBO'</p>' ;;
	esac

	case "$GPUMEMORY" in
		DEFAULT) pcp_set_gpu_memory_default ;;
		16)      pcp_set_gpu_memory 16 ;;
		32)      pcp_set_gpu_memory 32 ;;
		64)      pcp_set_gpu_memory 64 ;;
		128)     pcp_set_gpu_memory 128 ;;
		256)     pcp_set_gpu_memory 256 ;;
		*)       [ $DEBUG -eq 1 ] && echo '<p class="error">[ ERROR ] Invalid gpu memory option: '$GPUMEMORY'</p>' ;;
	esac

	if [ $DEBUG -eq 1 ]; then
		pcp_check_config_txt
		[ $(pcp_check_force_turbo) -eq 0 ] && echo '<p class="debug">[ DEBUG ] Force turbo set</p>' || echo '<p class="debug">[ DEBUG ] Force turbo NOT set</p>'
		[ $(pcp_check_over_voltage) -eq 0 ] && echo '<p class="debug">[ DEBUG ] Over voltage set</p>' || echo '<p class="debug">[ DEBUG ] Over voltage NOT set</p>'
		[ $(pcp_check_force_turbo) -eq 0 ] && [ $(pcp_check_over_voltage) -eq 0 ] && echo '<p class="debug">[ DEBUG ] Warranty bit will be set if you reboot</p>'
		[ $(pcp_rpi_warranty) -eq 0 ] &&
			echo '<p class="debug">[ DEBUG ] Warranty bit is already set: '$(pcp_rpi_revision)'</p>' ||
			echo '<p class="debug">[ DEBUG ] Warranty bit is NOT set: '$(pcp_rpi_revision)'</p>'
	fi

	pcp_umount_bootpart >/dev/null 2>&1
	REBOOT_REQUIRED=1
}

pcp_check_config_txt() {
	for I in arm_freq= core_freq= sdram_freq= over_voltage= force_turbo= gpu_mem=; do
		if cat $CONFIGTXT | grep $I >/dev/null 2>&1; then
			echo '<p class="debug">[ DEBUG ] "'$I'" found in '$CONFIGTXT'</p>'
		else
			echo '<p class="debug">[ DEBUG ] "'$I'" NOT found in '$CONFIGTXT'</p>'
		fi
	done
}

pcp_check_force_turbo() {
	FTSET=$(cat $CONFIGTXT | grep force_turbo=)
	case "$FTSET" in
		force_turbo=1) echo 0 ;;
		*) echo 1 ;;
	esac
}

pcp_check_over_voltage() {
	OVSET=$( cat $CONFIGTXT | grep over_voltage= )
	case "$OVSET" in
		over_voltage=0 | \#over_voltage=*) echo 1 ;;
		over_voltage=*) echo 0 ;;
	esac
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
case "$SUBMIT" in
	Save)
		[ $DEBUG -eq 1 ] && echo '<p class="info">[ INFO ] SUBMIT='$SUBMIT' </p>'
		pcp_start_save
	;;
	*)
		[ $DEBUG -eq 1 ] && echo '<p class="error">[ ERROR ] Invalid submit option: '$SUBMIT'</p>'
	;;
esac

#----------------------------------------------------------------------------------------
# Function to set selected item in the pull down list
#----------------------------------------------------------------------------------------
case "$ADVOVERCLOCK" in
	Lowest) OClowest="selected";;
	Under)  OCunder="selected" ;;
	None)   OCnone="selected" ;;
	Modest) OCmodest="selected" ;;
	Medium) OCmedium="selected" ;;
	High)   OChigh="selected" ;;
	Turbo)  OCturbo="selected" ;;
esac

#----------------------------------------------------------------------------------------
# Function to set selected item in the pull down list
#----------------------------------------------------------------------------------------
pcp_mount_bootpart >/dev/null 2>&1
FORCETURBO=$(cat $CONFIGTXT | grep force_turbo)

case "$FORCETURBO" in
	\#force_turbo=0) FTdefault="selected" ;;
	force_turbo=0)   FT0="selected" ;;
	force_turbo=1)   FT1="selected" ;;
esac

GPUMEMORY=$(cat $CONFIGTXT | grep gpu_mem)

case "$GPUMEMORY" in
	\#gpu_mem=)  GMdefault="selected" ;;
	gpu_mem=16)  GM16="selected" ;;
	gpu_mem=32)  GM32="selected" ;;
	gpu_mem=64)  GM64="selected" ;;
	gpu_mem=128) GM128="selected" ;;
	gpu_mem=256) GM256="selected" ;;
esac

pcp_umount_bootpart >/dev/null 2>&1

pcp_warning_message

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Overclocking/underclocking</legend>'
echo '          <form name="overclock" action= "xtras_overclock.cgi" method="get">'
echo '            <table class="bggrey percent100">'

#--------------------------------------Overclock/underclock------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Overclock/underclock</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <select class="large16" name="ADVOVERCLOCK">'

case $RPITYPE in
	0)
		echo '                    <option value="Lowest" '$OClowest'>Lowest</option>'
		echo '                    <option value="Under" '$OCunder'>Under</option>'
		echo '                    <option value="None" '$OCnone'>None</option>'
	;;
	1)
		echo '                    <option value="Lowest" '$OClowest'>Lowest</option>'
		echo '                    <option value="Under" '$OCunder'>Under</option>'
		echo '                    <option value="None" '$OCnone'>None</option>'
		echo '                    <option value="Modest" '$OCmodest'>Modest</option>'
		echo '                    <option value="Medium" '$OCmedium'>Moderate</option>'
		echo '                    <option value="High" '$OChigh'>High</option>'
		echo '                    <option value="Turbo" '$OCturbo'>Turbo</option>'
	;;
	2)
		echo '                    <option value="Lowest" '$OClowest'>Lowest</option>'
		echo '                    <option value="Under" '$OCunder'>Under</option>'
		echo '                    <option value="None" '$OCnone'>None</option>'
		echo '                    <option value="High" '$OChigh'>High</option>'
	;;
	3)
		echo '                    <option value="Lowest" '$OClowest'>Lowest</option>'
		echo '                    <option value="Under" '$OCunder'>Under</option>'
		echo '                    <option value="None" '$OCnone'>None</option>'
	;;
	4)
		echo '                    <option value="Under" '$OCunder'>Under</option>'
		echo '                    <option value="None" '$OCnone'>None</option>'
	;;
esac

echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Change Raspberry Pi overclocking/underclocking&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>Reboot is required.<p>'
echo '                    <p><b>Note:</b> If Raspberry Pi fails to boot:</p>'
echo '                    <ul>'
echo '                      <li>hold down the shift key during booting, or</li>'
echo '                      <li>edit the config.txt file manually</li>'
echo '                    </ul>'
echo '                    <p><b>Underclocking data</b></p>'
echo '                    <ul>'
echo '                      <li><b>Lowest</b>&nbsp;600MHz ARM, 250MHz gpu, 250MHz core, 400MHz SDRAM, 0 overvolt</li>'
echo '                      <li><b>Under</b>&nbsp;800MHz ARM, 200MHz gpu, 200MHz core, 400MHz SDRAM, 0 overvolt</li>'
echo '                    </ul>'
echo '                    <p><b>Overclocking data</b></p>'
echo '                    <p><b>&nbsp;&nbsp;RPi0</b></p>'
echo '                    <ul>'
echo '                      <li><b>None</b></li>'
echo '                    </ul>'
echo '                    <p><b>&nbsp;&nbsp;RPi1</b></p>'
echo '                    <ul>'
echo '                      <li><b>None</b>&nbsp;700MHz ARM, 250MHz gpu, 250MHz core, 400MHz SDRAM, 0 overvolt</li>'
echo '                      <li><b>Modest</b>&nbsp;800MHz ARM, 250MHz gpu, 250MHz core, 400MHz SDRAM, 0 overvolt</li>'
echo '                      <li><b>Medium</b>&nbsp;900MHz ARM, 250MHz gpu, 250MHz core, 450MHz SDRAM, 2 overvolt</li>'
echo '                      <li><b>High</b>&nbsp;950MHz ARM, 250MHz gpu, 250MHz core, 450MHz SDRAM, 6 overvolt</li>'
echo '                      <li><b>Turbo</b>&nbsp;1000MHz ARM, 250MHz gpu, 500MHz core, 600MHz SDRAM, 6 overvolt</li>'
echo '                    </ul>'
echo '                    <p><b>&nbsp;&nbsp;RPi2</b></p>'
echo '                    <ul>'
echo '                      <li><b>None</b>&nbsp;900MHz ARM, 250MHz gpu, 250MHz core, 450MHz SDRAM, 0 overvolt</li>'
echo '                      <li><b>High</b>&nbsp;1000MHz ARM, 250MHz gpu, 500MHz core, 500MHz SDRAM, 2 overvolt</li>'
echo '                    </ul>'
echo '                    <p><b>&nbsp;&nbsp;RPi3</b></p>'
echo '                    <ul>'
echo '                      <li><b>None</b></li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Force turbo---------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE' warning">'
echo '                <td class="column150">'
echo '                  <p>Force turbo</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <select class="large16" name="FORCETURBO">'
echo '                    <option value="DEFAULT" '$FTdefault'>Default</option>'
echo '                    <option value="1" '$FT1'>Yes</option>'
echo '                    <option value="0" '$FT0'>No</option>'
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Change Raspberry Pi force turbo setting&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>&lt;Default|Yes|No&gt;</p>'
echo '                    <p><b>Warning: </b>Setting force turbo may set warranty bit.<p>'
echo '                    <p>Reboot is required.<p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------GPU memory----------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>GPU memory</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <select class="large16" name="GPUMEMORY">'
echo '                    <option value="DEFAULT" '$GMdefault'>Default</option>'
echo '                    <option value="16" '$GM16'>16</option>'
echo '                    <option value="32" '$GM32'>32</option>'
echo '                    <option value="64" '$GM64'>64</option>'
echo '                    <option value="128" '$GM128'>128</option>'
echo '                    <option value="256" '$GM256'>256</option>'
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Change GPU memory setting&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>&lt;Default|16|32|64|128|256&gt;</p>'
echo '                    <p>Reboot is required.<p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Buttons-------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </form>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

if [ $DEBUG -eq 1 ]; then
	#======================================================================================
	# Display debug information
	#--------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Debug information</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '                <p class="debug">[ DEBUG ] $ADVOVERCLOCK: '$ADVOVERCLOCK'<br />'
	echo '                                 [ DEBUG ] $OCunder: '$OCunder'<br />'
	echo '                                 [ DEBUG ] $OCdefault: '$OCdefault'<br />'
	echo '                                 [ DEBUG ] $OCnone: '$OCnone'<br />'
	echo '                                 [ DEBUG ] $OCmodest: '$OCmodest'<br />'
	echo '                                 [ DEBUG ] $OCmedium: '$OCmedium'<br />'
	echo '                                 [ DEBUG ] $OChigh: '$OChigh'<br />'
	echo '                                 [ DEBUG ] $OCturbo: '$OCturbo'<br />'
	echo '                                 [ DEBUG ] $OCpi2: '$OCpi2'<br />'
	echo '                                 [ DEBUG ] $Raspberry Pi: '$RPITYPE'</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p class="debug">[ DEBUG ] $FORCETURBO: '$FORCETURBO'<br />'
	echo '                                 [ DEBUG ] $FT0: '$FT0'<br />'
	echo '                                 [ DEBUG ] $FT1: '$FT1'</p>'
	echo '                <p class="debug">[ DEBUG ] $GPUMEMORY: '$GPUMEMORY'<br />'
	echo '                                 [ DEBUG ] $GMdefault: '$GMdefault'<br />'
	echo '                                 [ DEBUG ] $GM16: '$GM16'<br />'
	echo '                                 [ DEBUG ] $GM32: '$GM32'<br />'
	echo '                                 [ DEBUG ] $GM64: '$GM64'<br />'
	echo '                                 [ DEBUG ] $GM128: '$GM128'<br />'
	echo '                                 [ DEBUG ] $GM256: '$GM256'</p>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

if [ $MODE -ge $MODE_PLAYER ]; then
	#====================================================================================
	# Display current overclock settings
	#------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Current config.txt (partial)</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	                      pcp_display_config_txt
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'

	#====================================================================================
	# Display current overclock settings
	#------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Current overclock settings</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	                      pcp_display_current
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'

	#====================================================================================
	# Display current pcp.cfg - partial
	#------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Current pcp.cfg (partial)</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	                      pcp_textarea_inform "none" "grep -C2 OVERCLOCK $PCPCFG" 80
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

pcp_footer
pcp_copyright

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

echo '</body>'
echo '</html>'