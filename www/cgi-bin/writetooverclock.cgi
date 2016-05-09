#!/bin/sh

# Version: 0.05 2015-09-19 SBP
#	Removed httpd decoding.

# Version: 0.04 2015-05-23 GE
#	Reverted to version 0.02
#	Incorporated overclock.sh

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
pcp_save_to_config

pcp_backup

pcp_mount_mmcblk0p1

if mount | grep $VOLUME; then
	echo '<p class="info">[ INFO ] '$VOLUME' is mounted.</p>'
else
	exit 1
fi

# Set the overclock options in config.txt file
. $CONFIGCFG
case "$OVERCLOCK" in
	NONE)
		echo '<p class="info">[ INFO ] Setting OVERCLOCK to NONE</p>' 
		sudo sed -i "/arm_freq=/c\arm_freq=700" $CONFIGTXT
		sudo sed -i "/core_freq=/c\core_freq=250" $CONFIGTXT
		sudo sed -i "/sdram_freq=/c\sdram_freq=400" $CONFIGTXT
		sudo sed -i "/over_voltage=/c\over_voltage=0" $CONFIGTXT
		sudo sed -i "/force_turbo=/c\force_turbo=1" $CONFIGTXT
		;;
	MILD)
		echo '<p class="info">[ INFO ] Setting OVERCLOCK to MILD</p>' 
		sudo sed -i "/arm_freq=/c\arm_freq=800" $CONFIGTXT
		sudo sed -i "/core_freq=/c\core_freq=250" $CONFIGTXT
		sudo sed -i "/sdram_freq=/c\sdram_freq=400" $CONFIGTXT
		sudo sed -i "/over_voltage=/c\over_voltage=0" $CONFIGTXT
		sudo sed -i "/force_turbo=/c\force_turbo=1" $CONFIGTXT
		;;
	MODERATE)
		echo '<p class="info">[ INFO ] Setting OVERCLOCK to MODERATE</p>'
		sudo sed -i "/arm_freq=/c\arm_freq=900" $CONFIGTXT
		sudo sed -i "/core_freq=/c\core_freq=333" $CONFIGTXT
		sudo sed -i "/sdram_freq=/c\sdram_freq=450" $CONFIGTXT
		sudo sed -i "/over_voltage=/c\over_voltage=2" $CONFIGTXT
		sudo sed -i "/force_turbo=/c\force_turbo=0" $CONFIGTXT
		;;
esac

[ $DEBUG -eq 1 ] && pcp_show_config_txt

pcp_umount_mmcblk0p1

. $CONFIGCFG

echo '<p class="info">[ INFO ] Overclock is set to: '$OVERCLOCK'</p>'

[ $DEBUG -eq 1 ] && pcp_show_config_cfg

pcp_go_back_button

echo '</body>'
echo '</html>'