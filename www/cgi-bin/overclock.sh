#!/bin/sh
. pcp-functions
pcp_variables

. $CONFIGCFG

pcp_running_script
pcp_mount_mmcblk0p1

if mount | grep $VOLUME; then
	echo '<p class="info">[ INFO ] '$VOLUME' is mounted.</p>'
else
	exit 1
fi

if [ $DEBUG = 1 ]; then
	echo '<p class="info">[ INFO ] Overclock setting in $CONFIG: '$OVERCLOCK'</p>'
#	OVERCLOCK=NONE;
#	OVERCLOCK=MILD;
#	OVERCLOCK=MODERATE;
fi

# Set the overclock options in config.txt file

case $OVERCLOCK in
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

if [ $DEBUG = 1 ]; then
	pcp_show_config_txt
fi

pcp_umount_mmcblk0p1
