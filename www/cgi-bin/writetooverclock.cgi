#!/bin/sh

# Version: 4.0.0 2018-07-24

. pcp-functions

pcp_html_head "Write Overclock to Config" "SBP"

pcp_banner
pcp_running_script
pcp_remove_query_string
pcp_httpd_query_string

pcp_table_top "Changing kernel tweaks"
pcp_save_to_config
pcp_backup

REBOOT_REQUIRED=0

case "$ACTION" in
	gov)
		# Set the CPU scaling governor.
		echo -n $CPUGOVERNOR | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor >/dev/null
		echo '<p class="info">[ INFO ] CPU Governor is set to: '$CPUGOVERNOR'</p>'
	;;
	oc)
		# Set the overclock options in config.txt file
		pcp_mount_bootpart
		if mount | grep $VOLUME; then
			echo '<p class="info">[ INFO ] '$VOLUME' is mounted.</p>'
		else
			exit 1
		fi
		case "$OVERCLOCK" in
			NONE)
				echo '<p class="info">[ INFO ] Setting OVERCLOCK to NONE</p>'
				sudo sed -i "/arm_freq=/c\arm_freq=700" $CONFIGTXT
				sudo sed -i "/core_freq=/c\core_freq=250" $CONFIGTXT
				sudo sed -i "/sdram_freq=/c\sdram_freq=400" $CONFIGTXT
				sudo sed -i "/over_voltage=/c\over_voltage=0" $CONFIGTXT
				sudo sed -i "/force_turbo=/c\force_turbo=0" $CONFIGTXT
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
				sudo sed -i "/force_turbo=/c\force_turbo=1" $CONFIGTXT
			;;
		esac
		[ $DEBUG -eq 1 ] && pcp_show_config_txt
		pcp_umount_bootpart
		echo '<p class="info">[ INFO ] Overclock is set to: '$OVERCLOCK'</p>'
		REBOOT_REQUIRED=1
	;;
	isol)
		# Set CPU isolation
		pcp_mount_bootpart
		REBOOT_REQUIRED=1
		pcp_clean_cmdlinetxt
		sed -i 's/isolcpus[=][^ ]* //g' $CMDLINETXT
		[ $CPUISOL != "" ] && sed -i '1 s/^/isolcpus='$CPUISOL' /' $CMDLINETXT
		pcp_umount_bootpart
	;;
	sqlaffinity)
		#Set CPUs to run squeezelite processes
		pcp_table_middle
		echo '<textarea class="inform" style="height:160px">'
		pcp_squeezelite_stop nohtml
		pcp_squeezelite_start nohtml display
		echo '</textarea>'
	;;
esac

[ $DEBUG -eq 1 ] && pcp_show_config_cfg
[ $REBOOT_REQUIRED -eq 1 ] && pcp_reboot_required
pcp_table_middle
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 10
pcp_table_end

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'