#!/bin/sh

# Version: 7.0.0 2020-05-17
# Title: Advanced overclock
# Description: Set overclock options for Raspberry Pi 0, 2, 3, 4

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

pcp_xtras
pcp_httpd_query_string

RPITYPE=$(pcp_rpi_type)
REBOOT_REQUIRED=0

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-2"
COLUMN3_3="col-sm-8"

#========================================================================================
# Generate warning message
#----------------------------------------------------------------------------------------
pcp_warning_message() {
	pcp_heading5 "Warning"

	echo '  <div class="row">'
	echo '    <div class="col-12">'
	echo '      <p><b>Warning:</b></p>'
	echo '      <ul>'
	echo '        <li>It can be dangerous to play with overclocking.</li>'
	echo '        <li>Setting "force turbo" may set warranty bit.</li>'
	echo '        <li>Do not transfer SD card bewteen different model Raspberry Pi.</li>'
	echo '      </ul>'
	echo '      <p><b>Note:</b></p>'
	echo '      <ul>'

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

	echo "        $MESSAGEPI0"
	echo "        $MESSAGEPI1"
	echo "        $MESSAGEPI2"
	echo "        $MESSAGEPI3"
	echo "        $MESSAGEPI4"
	echo '      <ul>'
	echo '    </div>'
	echo '  </div>'
}

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_set_overclock() {
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Setting OVERCLOCK to $1" "html"

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
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Setting OVERCLOCK to DEFAULT" "html"
	sudo sed -i 's/^arm_freq=/#arm_freq=/g' $CONFIGTXT
	sudo sed -i 's/^gpu_freq=/#gpu_freq=/g' $CONFIGTXT
	sudo sed -i 's/^core_freq=/#core_freq=/g' $CONFIGTXT
	sudo sed -i 's/^sdram_freq=/#sdram_freq=/g' $CONFIGTXT
	sudo sed -i 's/^over_voltage=/#over_voltage=/g' $CONFIGTXT
	pcp_set_force_turbo_default
}

pcp_set_force_turbo() {
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Setting FORCE_TURBO to $1" "html"
	sudo sed -i "/force_turbo=/c\force_turbo=$1" $CONFIGTXT
}

pcp_set_force_turbo_default() {
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Setting FORCE_TURBO to DEFAULT" "html"
	pcp_set_force_turbo 0
	sudo sed -i 's/^force_turbo=/#force_turbo=/g' $CONFIGTXT
}

pcp_set_gpu_memory() {
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Setting GPU memory to $1" "html"
	sudo sed -i "/gpu_mem=/c\gpu_mem=$1" $CONFIGTXT
}

pcp_set_gpu_memory_default() {
	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Setting GPU memory to DEFAULT" "html"
	sudo sed -i 's/^gpu_mem=/#gpu_mem=/g' $CONFIGTXT
}

pcp_display_current() {
	pcp_textarea_begin "" 15
	for FILE in $(ls /sys/devices/system/cpu/cpu0/cpufreq/ | grep -v stats); do
		echo -n $FILE': '
		cat /sys/devices/system/cpu/cpu0/cpufreq/$FILE | sed 's/[<>]//g'
	done
	pcp_textarea_end
}

pcp_display_config_txt() {
	pcp_textarea_begin "" 8
	pcp_mount_bootpart >/dev/null 2>&1
	sed -n '/uncomment to overclock/{n;p;n;p;n;p;n;p;n;p;n;p}' $CONFIGTXT
	pcp_umount_bootpart >/dev/null 2>&1
	pcp_textarea_end
}

pcp_start_save() {
	pcp_save_to_config
	pcp_backup >/dev/null 2>&1
	pcp_mount_bootpart >/dev/null 2>&1

	if mount | grep $VOLUME >/dev/null 2>&1; then
		[ $DEBUG -eq 1 ] && pcp_message INFO "$VOLUME is mounted." "html"
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
		*)       [ $DEBUG -eq 1 ] && pcp_message ERROR "Invalid force option: $FORCETURBO" "html" ;;
	esac

	case "$GPUMEMORY" in
		DEFAULT) pcp_set_gpu_memory_default ;;
		16)      pcp_set_gpu_memory 16 ;;
		32)      pcp_set_gpu_memory 32 ;;
		64)      pcp_set_gpu_memory 64 ;;
		128)     pcp_set_gpu_memory 128 ;;
		256)     pcp_set_gpu_memory 256 ;;
		*)       [ $DEBUG -eq 1 ] && pcp_message ERROR "Invalid gpu memory option: $GPUMEMORY" "html";
	esac

	if [ $DEBUG -eq 1 ]; then
		pcp_check_config_txt
		[ $(pcp_check_force_turbo) -eq 0 ] && pcp_message DEBUG "Force turbo set" "html" || pcp_message DEBUG "Force turbo NOT set" "html"
		[ $(pcp_check_over_voltage) -eq 0 ] && pcp_message DEBUG "Over voltage set" "html" || pcp_message DEBUG "Over voltage NOT set" "html"
		[ $(pcp_check_force_turbo) -eq 0 ] && [ $(pcp_check_over_voltage) -eq 0 ] && pcp_message DEBUG "Warranty bit will be set if you reboot" "html"
		[ $(pcp_rpi_warranty) -eq 0 ] &&
			pcp_message DEBUG "Warranty bit is already set: $(pcp_rpi_revision)" "html" ||
			pcp_message DEBUG "Warranty bit is NOT set: $(pcp_rpi_revision)" "html"
	fi

	pcp_umount_bootpart >/dev/null 2>&1
	REBOOT_REQUIRED=1
}

pcp_check_config_txt() {
	for I in arm_freq= core_freq= sdram_freq= over_voltage= force_turbo= gpu_mem=; do
		if cat $CONFIGTXT | grep $I >/dev/null 2>&1; then
			pcp_message DEBUG "$I found in $CONFIGTXT" "html"
		else
			pcp_message DEBUG "$I NOT found in $CONFIGTXT" "html"
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
		pcp_debug_variables "html" SUBMIT
		pcp_start_save
	;;
	*)
		[ $DEBUG -eq 1 ] && pcp_message ERROR "Invalid submit option: $SUBMIT" "html"
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

pcp_heading5 "Overclocking/underclocking" hr

echo '  <form name="overclock" action="xtras_overclock.cgi" method="get">'
#--------------------------------------Overclock/underclock------------------------------
pcp_incr_id
echo '    <div class="row">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>Overclock/underclock</p>'
echo '      </div>'
echo '      <div class="input-group '$COLUMN3_2'">'
echo '        <select class="custom-select custom-select-sm" name="ADVOVERCLOCK">'

case $RPITYPE in
	0)
		echo '          <option value="Lowest" '$OClowest'>Lowest</option>'
		echo '          <option value="Under" '$OCunder'>Under</option>'
		echo '          <option value="None" '$OCnone'>None</option>'
	;;
	1)
		echo '          <option value="Lowest" '$OClowest'>Lowest</option>'
		echo '          <option value="Under" '$OCunder'>Under</option>'
		echo '          <option value="None" '$OCnone'>None</option>'
		echo '          <option value="Modest" '$OCmodest'>Modest</option>'
		echo '          <option value="Medium" '$OCmedium'>Moderate</option>'
		echo '          <option value="High" '$OChigh'>High</option>'
		echo '          <option value="Turbo" '$OCturbo'>Turbo</option>'
	;;
	2)
		echo '          <option value="Lowest" '$OClowest'>Lowest</option>'
		echo '          <option value="Under" '$OCunder'>Under</option>'
		echo '          <option value="None" '$OCnone'>None</option>'
		echo '          <option value="High" '$OChigh'>High</option>'
	;;
	3)
		echo '          <option value="Lowest" '$OClowest'>Lowest</option>'
		echo '          <option value="Under" '$OCunder'>Under</option>'
		echo '          <option value="None" '$OCnone'>None</option>'
	;;
	4)
		echo '          <option value="Under" '$OCunder'>Under</option>'
		echo '          <option value="None" '$OCnone'>None</option>'
	;;
esac

echo '        </select>'
echo '      </div>'

echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Change Raspberry Pi overclocking/underclocking&nbsp;&nbsp;'
echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>Reboot is required.<p>'
echo '          <p><b>Note:</b> If Raspberry Pi fails to boot:</p>'
echo '          <ul>'
echo '            <li>hold down the shift key during booting, or</li>'
echo '            <li>edit the config.txt file manually</li>'
echo '          </ul>'
echo '          <p><b>Underclocking data</b></p>'
echo '          <ul>'
echo '            <li><b>Lowest</b>&nbsp;600MHz ARM, 250MHz gpu, 250MHz core, 400MHz SDRAM, 0 overvolt</li>'
echo '            <li><b>Under</b>&nbsp;800MHz ARM, 200MHz gpu, 200MHz core, 400MHz SDRAM, 0 overvolt</li>'
echo '          </ul>'
echo '          <p><b>Overclocking data</b></p>'
echo '          <p><b>&nbsp;&nbsp;RPi0</b></p>'
echo '          <ul>'
echo '            <li><b>None</b></li>'
echo '          </ul>'
echo '          <p><b>&nbsp;&nbsp;RPi1</b></p>'
echo '          <ul>'
echo '            <li><b>None</b>&nbsp;700MHz ARM, 250MHz gpu, 250MHz core, 400MHz SDRAM, 0 overvolt</li>'
echo '            <li><b>Modest</b>&nbsp;800MHz ARM, 250MHz gpu, 250MHz core, 400MHz SDRAM, 0 overvolt</li>'
echo '            <li><b>Medium</b>&nbsp;900MHz ARM, 250MHz gpu, 250MHz core, 450MHz SDRAM, 2 overvolt</li>'
echo '            <li><b>High</b>&nbsp;950MHz ARM, 250MHz gpu, 250MHz core, 450MHz SDRAM, 6 overvolt</li>'
echo '            <li><b>Turbo</b>&nbsp;1000MHz ARM, 250MHz gpu, 500MHz core, 600MHz SDRAM, 6 overvolt</li>'
echo '          </ul>'
echo '          <p><b>&nbsp;&nbsp;RPi2</b></p>'
echo '          <ul>'
echo '            <li><b>None</b>&nbsp;900MHz ARM, 250MHz gpu, 250MHz core, 450MHz SDRAM, 0 overvolt</li>'
echo '            <li><b>High</b>&nbsp;1000MHz ARM, 250MHz gpu, 500MHz core, 500MHz SDRAM, 2 overvolt</li>'
echo '          </ul>'
echo '          <p><b>&nbsp;&nbsp;RPi3</b></p>'
echo '          <ul>'
echo '            <li><b>None</b></li>'
echo '          </ul>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#--------------------------------------Force turbo---------------------------------------
pcp_incr_id
echo '    <div class="row">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>Force turbo</p>'
echo '      </div>'
echo '      <div class="input-group '$COLUMN3_2'">'
echo '        <select class="custom-select custom-select-sm" name="FORCETURBO">'
echo '          <option value="DEFAULT" '$FTdefault'>Default</option>'
echo '          <option value="1" '$FT1'>Yes</option>'
echo '          <option value="0" '$FT0'>No</option>'
echo '        </select>'
echo '      </div>'
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Change Raspberry Pi force turbo setting&nbsp;&nbsp;'
echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>&lt;Default|Yes|No&gt;</p>'
echo '          <p><b>Warning: </b>Setting force turbo may set warranty bit.<p>'
echo '          <p>Reboot is required.<p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#--------------------------------------GPU memory----------------------------------------
pcp_incr_id
echo '    <div class="row">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>GPU memory</p>'
echo '      </div>'
echo '      <div class="input-group '$COLUMN3_2'">'
echo '        <select class="custom-select custom-select-sm" name="GPUMEMORY">'
echo '          <option value="DEFAULT" '$GMdefault'>Default</option>'
echo '          <option value="16" '$GM16'>16</option>'
echo '          <option value="32" '$GM32'>32</option>'
echo '          <option value="64" '$GM64'>64</option>'
echo '          <option value="128" '$GM128'>128</option>'
echo '          <option value="256" '$GM256'>256</option>'
echo '        </select>'
echo '      </div>'
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Change GPU memory setting&nbsp;&nbsp;'
echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>&lt;Default|16|32|64|128|256&gt;</p>'
echo '          <p>Reboot is required.<p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#--------------------------------------Buttons-------------------------------------------
echo '    <div class="row">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Save">'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '  </form>'

if [ $DEBUG -eq 1 ]; then
	#======================================================================================
	# Display debug information
	#--------------------------------------------------------------------------------------
	pcp_heading5 "Debug information"
	pcp_debug_variables "html" ADVOVERCLOCK OCunder OCdefault OCnone OCmodest OCmedium \
		OChigh OCturbo OCpi2 RPITYPE FORCETURBO FT0 FT1 GPUMEMORY GMdefault GM16 GM32 \
		GM64 GM128 GM256
fi

if [ $MODE -ge $MODE_PLAYER ]; then
	#====================================================================================
	# Display current overclock settings
	#------------------------------------------------------------------------------------
	pcp_heading5 "Current config.txt (partial)" hr
	pcp_display_config_txt

	#====================================================================================
	# Display current overclock settings
	#------------------------------------------------------------------------------------
	pcp_heading5 "Current overclock settings" hr
	pcp_display_current

	#====================================================================================
	# Display current pcp.cfg - partial
	#------------------------------------------------------------------------------------
	pcp_heading5 "Current pcp.cfg (partial)" hr
	pcp_textarea "none" "grep -C2 OVERCLOCK $PCPCFG" 80
fi

[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

pcp_html_end