#!/bin/sh

# Version: 7.0.0 2020-06-09

. pcp-functions

pcp_html_head "Write Overclock to Config" "SBP"

pcp_remove_query_string
pcp_httpd_query_string
pcp_navbar

pcp_heading5 "Changing kernel tweaks"
pcp_infobox_begin

REBOOT_REQUIRED=0

case "$ACTION" in
	gov)
		# Set the CPU scaling governor.
		echo -n $CPUGOVERNOR | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor >/dev/null
		pcp_message INFO "CPU Governor is set to: $CPUGOVERNOR" "text"
	;;
	oc)
		# Set the overclock options in config.txt file
		pcp_mount_bootpart
		if mount | grep $VOLUME; then
			pcp_message INFO "$VOLUME is mounted." "text"
		else
			exit 1
		fi
		case "$OVERCLOCK" in
			NONE)
				pcp_message INFO "Setting OVERCLOCK to NONE" "text"
				sudo sed -i "/arm_freq=/c\arm_freq=700" $CONFIGTXT
				sudo sed -i "/core_freq=/c\core_freq=250" $CONFIGTXT
				sudo sed -i "/sdram_freq=/c\sdram_freq=400" $CONFIGTXT
				sudo sed -i "/over_voltage=/c\over_voltage=0" $CONFIGTXT
				sudo sed -i "/force_turbo=/c\force_turbo=0" $CONFIGTXT
			;;
			MILD)
				pcp_message INFO "Setting OVERCLOCK to MILD" "text"
				sudo sed -i "/arm_freq=/c\arm_freq=800" $CONFIGTXT
				sudo sed -i "/core_freq=/c\core_freq=250" $CONFIGTXT
				sudo sed -i "/sdram_freq=/c\sdram_freq=400" $CONFIGTXT
				sudo sed -i "/over_voltage=/c\over_voltage=0" $CONFIGTXT
				sudo sed -i "/force_turbo=/c\force_turbo=1" $CONFIGTXT
			;;
			MODERATE)
				pcp_message INFO "Setting OVERCLOCK to MODERATE" "text"
				sudo sed -i "/arm_freq=/c\arm_freq=900" $CONFIGTXT
				sudo sed -i "/core_freq=/c\core_freq=333" $CONFIGTXT
				sudo sed -i "/sdram_freq=/c\sdram_freq=450" $CONFIGTXT
				sudo sed -i "/over_voltage=/c\over_voltage=2" $CONFIGTXT
				sudo sed -i "/force_turbo=/c\force_turbo=1" $CONFIGTXT
			;;
		esac
		[ $DEBUG -eq 1 ] && pcp_show_config_txt
		pcp_umount_bootpart
		pcp_message INFO "Overclock is set to: $OVERCLOCK" "text"
		REBOOT_REQUIRED=1
	;;
	isol)
		pcp_message INFO "CPU isolation is set to: $CPUISOL" "text"
		pcp_mount_bootpart
		REBOOT_REQUIRED=1
		pcp_clean_cmdlinetxt
		sed -i 's/isolcpus[=][^ ]* //g' $CMDLINETXT
		[ $CPUISOL != "" ] && sed -i '1 s/^/isolcpus='$CPUISOL' /' $CMDLINETXT
		pcp_umount_bootpart
	;;
	sqlaffinity)
		# Set CPUs to run squeezelite processes
		pcp_squeezelite_stop "text"
		pcp_squeezelite_start "text" display
	;;
esac

pcp_save_to_config
pcp_backup "text"

pcp_infobox_end
[ $DEBUG -eq 1 ] && pcp_show_config_cfg
[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required

pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 10

pcp_html_end
exit
