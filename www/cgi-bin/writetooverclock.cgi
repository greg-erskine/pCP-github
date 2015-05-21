#!/bin/sh

# Version: 0.03 2015-05-21 GE
#	Incorporated overclock.sh
#	Added UNDER, HIGH, TURBO, PI2.

# Version: 0.02 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014-06-24 SBP
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write Overclock to Config" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Decode $OVERCLOCK using httpd, add quotes
OVERCLOCK=`sudo $HTPPD -d \"$OVERCLOCK\"`
sudo sed -i "s/\(OVERCLOCK *=*\).*/\1$OVERCLOCK/" $CONFIGCFG

pcp_backup

pcp_mount_mmcblk0p1

if mount | grep $VOLUME; then
	echo '<p class="info">[ INFO ] '$VOLUME' is mounted.</p>'
else
	pcp_go_back_button
	echo '</body>'
	echo '</html>'
fi

#========================================================================================
# Set the overclock options in the config.txt file
#----------------------------------------------------------------------------------------
pcp_set_overclock() {
	echo '<p class="info">[ INFO ] Setting OVERCLOCK to '$1'</p>' 
	sudo sed -i "/arm_freq=/c\arm_freq=$2" $CONFIGTXT
	sudo sed -i "/core_freq=/c\core_freq=$3" $CONFIGTXT
	sudo sed -i "/sdram_freq=/c\sdram_freq=$4" $CONFIGTXT
	sudo sed -i "/over_voltage=/c\over_voltage=$5" $CONFIGTXT
	sudo sed -i "/force_turbo=/c\force_turbo=$6" $CONFIGTXT
}

pcp_set_overclock_none() {
	echo '<p class="info">[ INFO ] Setting OVERCLOCK to NONE</p>'
	sudo sed -i 's/^arm_freq=/#arm_freq=/g' $CONFIGTXT
	sudo sed -i 's/^core_freq=/#core_freq=/g' $CONFIGTXT
	sudo sed -i 's/^sdram_freq=/#sdram_freq=/g' $CONFIGTXT
	sudo sed -i 's/^over_voltage=/#over_voltage=/g' $CONFIGTXT
	sudo sed -i 's/^force_turbo=/#force_turbo=/g' $CONFIGTXT
}

#========================================================================================
# Data from raspi-config
#----------------------------------------------------------------------------------------
# "None"   "700MHz ARM,  250MHz core, 400MHz SDRAM, 0 overvolt" \
# "Modest" "800MHz ARM,  250MHz core, 400MHz SDRAM, 0 overvolt" \
# "Medium" "900MHz ARM,  250MHz core, 450MHz SDRAM, 2 overvolt" \
# "High"   "950MHz ARM,  250MHz core, 450MHz SDRAM, 6 overvolt" \
# "Turbo"  "1000MHz ARM, 500MHz core, 600MHz SDRAM, 6 overvolt" \
# "Pi2"    "1000MHz ARM, 500MHz core, 500MHz SDRAM, 2 overvolt" \
#----------------------------------------------------------------------------------------

. $CONFIGCFG
case $OVERCLOCK in
	UNDER)
		pcp_set_overclock UNDER 600 250 400 0 1
		;;
	NONE)
		pcp_set_overclock_none
		#pcp_set_overclock NONE 700 250 400 0 1
		;;
	MILD)
		pcp_set_overclock MILD 800 250 400 0 1
		;;
	MODERATE)
		pcp_set_overclock MODERATE 900 250 450 2 0
		;;
	HIGH)
		pcp_set_overclock HIGH 950 250 450 6 0
		;;
	TURBO)
		pcp_set_overclock TURBO 1000 500 600 6 0
		;;
	RPI2)
		pcp_set_overclock RPI2 1000 500 500 2 0
		;;
	*)
		echo '<p class="error">[ ERROR ] Invalid option: '$OVERCLOCK' </p>'
		;;
esac

#========================================================================================
# Userspace: /sys/devices/system/cpu/cpu0/cpufreq/
#----------------------------------------------------------------------------------------
# affected_cpus                  related_cpus                     scaling_governor
# cpuinfo_cur_freq               scaling_available_frequencies    scaling_max_freq
# cpuinfo_max_freq               scaling_available_governors      scaling_min_freq
# cpuinfo_min_freq               scaling_cur_freq                 scaling_setspeed
# cpuinfo_transition_latency     scaling_driver
#----------------------------------------------------------------------------------------

if [ $DEBUG = 1 ]; then
	echo '<p class="debug"> Current settings: </p>'
	echo -n '<p class="debug">'
	for FILE in $(ls /sys/devices/system/cpu/cpu0/cpufreq/); do
		echo -n '[ DEBUG ] '$FILE': '
		cat /sys/devices/system/cpu/cpu0/cpufreq/$FILE
		echo '<br />'
	done
	echo '</p>'
	pcp_show_config_txt
fi

pcp_umount_mmcblk0p1

echo '<p class="info">[ INFO ] Overclock is set to: '$OVERCLOCK'</p>'
[ $DEBUG = 1 ] && pcp_show_config_cfg

pcp_footer
pcp_copyright
pcp_go_back_button

echo '</body>'
echo '</html>'