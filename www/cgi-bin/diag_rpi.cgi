#!/bin/sh

# Version: 7.0.0 2020-05-30

. pcp-functions
. pcp-rpi-functions
. pcp-lms-functions
. pcp-pastebin-functions

pcp_html_head "Raspberry Pi Diagnostics" "GE"

pcp_controls
pcp_diagnostics

COLUMN1="col-6 col-lg-3 col-xl-2 text-right"
COLUMN2="col-6 col-lg-3 col-xl-2"
COLUMN3="col-6 col-lg-3 col-xl-2 text-right"
COLUMN4="col-6 col-lg-3 col-xl-2"
COLUMN5="col-6 col-lg-3 col-xl-2 text-right"
COLUMN6="col-6 col-lg-3 col-xl-2"

#========================================================================================
# Add information to log file.
#----------------------------------------------------------------------------------------
pcp_add_to_log() {
	START="====================> Start <===================="
	END="=====================> End <====================="

	pcp_log_header $0

	echo "Raspberry Pi" >> $LOG
	echo  ============ >> $LOG
	echo "Model: $(pcp_rpi_model)" >> $LOG
	echo "Revision: $(pcp_rpi_revision)" >> $LOG
	echo "PCB Revision: $(pcp_rpi_pcb_revision)" >> $LOG
	echo "Memory: $(pcp_rpi_memory)" >> $LOG
	echo "Shortname: $(pcp_rpi_shortname)" >> $LOG
	echo "CPU Temperature: $(pcp_rpi_thermal_temp degrees)" >> $LOG
	echo "eth0 IP: $(pcp_diag_rpi_eth0_ip)" >> $LOG
	echo "wlan0 IP: $(pcp_diag_rpi_wlan0_ip)" >> $LOG
	echo "LMS IP: $(pcp_diag_rpi_lmsip)" >> $LOG
	echo "Uptime: $(pcp_uptime_days)" >> $LOG
	echo "Physical MAC: $(pcp_diag_rpi_eth0_mac_address)" >> $LOG
	echo "Wireless MAC: $(pcp_diag_rpi_wlan0_mac_address)" >> $LOG
	echo "Configuration MAC: $(pcp_diag_rpi_config_mac_address)" >> $LOG
	echo "Controls MAC: $(pcp_controls_mac_address)" >> $LOG
	echo  >> $LOG

	echo "Squeezelite" >> $LOG
	echo  =========== >> $LOG
	echo "Version: $(pcp_squeezelite_version)" >> $LOG
	echo "Build options: $BUILD" >> $LOG
	if [ $(pcp_squeezelite_status) -eq 0 ]; then
		echo "Squeezelite running." >> $LOG
	else
		echo  "Squeezelite not running." >> $LOG
	fi
	echo  >> $LOG

	echo "piCorePlayer" >> $LOG
	echo  ============ >> $LOG
	echo "Version: $(pcp_picoreplayer_version)" >> $LOG
	echo "pCP name: $NAME" >> $LOG
	echo "Hostname: $HOST" >> $LOG
	echo  >> $LOG

	echo "piCore" >> $LOG
	echo  ====== >> $LOG
	echo "Version: $(pcp_picore_version)" >> $LOG
	echo "Linux release: $(pcp_linux_release)" >> $LOG
	if [ $(pcp_internet_accessible) -eq 0 ]; then
		echo "Internet accessible." >> $LOG
	else
		echo "Internet not accessible." >> $LOG
	fi
	if [ $(pcp_pcp_repo_accessible) -eq 0 ]; then
		echo "piCorePlayer repository accessible." >> $LOG
	else
		echo "piCorePlayer repository not accessible." >> $LOG
	fi
}

#========================================================================================
# Functions
#----------------------------------------------------------------------------------------
pcp_diag_rpi_eth0_mac_address() {
	RESULT=$(pcp_eth0_mac_address)
	echo ${RESULT:-None}
}

pcp_diag_rpi_wlan0_mac_address() {
	RESULT=$(pcp_wlan0_mac_address)
	echo ${RESULT:-None}
}

pcp_diag_rpi_config_mac_address() {
	RESULT=$(pcp_config_mac_address)
	echo ${RESULT:-Not set}
}

pcp_diag_rpi_eth0_ip() {
	RESULT=$(pcp_eth0_ip)
	echo ${RESULT:-None}
}

pcp_diag_rpi_wlan0_ip() {
	RESULT=$(pcp_wlan0_ip)
	echo ${RESULT:-None}
}

pcp_diag_rpi_lmsip() {
	RESULT=$(pcp_lmsip)
	echo ${RESULT:-None}
}

# GE - Move to pcp-functions
BUILD=$(sudo ${SQLT_BIN} -? | grep "Build options" | awk -F": " '{print $2}')


#========================================================================================
# Raspberry Pi
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "Raspberry Pi"
#-------------------------------------Row 1----------------------------------------------
echo '    <div class="row mx-1 mb-2">'
echo '      <div class="'$COLUMN1'">'
echo '        Model:'
echo '      </div>'
echo '      <div class="'$COLUMN2'">'
echo '        '$(pcp_rpi_model)
echo '      </div>'
echo '      <div class="'$COLUMN3'">'
echo '        CPU Temperature:'
echo '      </div>'
echo '      <div class="'$COLUMN4'">'
echo '        '$(pcp_rpi_thermal_temp degrees)
echo '      </div>'
echo '      <div class="'$COLUMN5'">'
echo '        Physical MAC:'
echo '      </div>'
echo '      <div class="'$COLUMN6'">'
echo '        '$(pcp_diag_rpi_eth0_mac_address)
echo '      </div>'
#-------------------------------------Row 2----------------------------------------------
echo '      <div class="'$COLUMN1'">'
echo '        Revison:'
echo '      </div>'
echo '      <div class="'$COLUMN2'">'
echo '        '$(pcp_rpi_revision)
echo '      </div>'
echo '      <div class="'$COLUMN3'">'
echo '        eth0 IP:'
echo '      </div>'
echo '      <div class="'$COLUMN4'">'
echo '        '$(pcp_diag_rpi_eth0_ip)
echo '      </div>'
echo '      <div class="'$COLUMN5'">'
echo '        Wireless MAC:'
echo '      </div>'
echo '      <div class="'$COLUMN6'">'
echo '        '$(pcp_diag_rpi_wlan0_mac_address)
echo '      </div>'
#-------------------------------------Row 3----------------------------------------------
echo '      <div class="'$COLUMN1'">'
echo '        PCB Revison:'
echo '      </div>'
echo '      <div class="'$COLUMN2'">'
echo '        '$(pcp_rpi_pcb_revision)
echo '      </div>'
echo '      <div class="'$COLUMN3'">'
echo '        wlan0 IP:'
echo '      </div>'
echo '      <div class="'$COLUMN4'">'
echo '        '$(pcp_diag_rpi_wlan0_ip)
echo '      </div>'
echo '      <div class="'$COLUMN5'">'
echo '        Configuration MAC:'
echo '      </div>'
echo '      <div class="'$COLUMN6'">'
echo '        '$(pcp_diag_rpi_config_mac_address)
echo '      </div>'
#-------------------------------------Row 4----------------------------------------------
echo '      <div class="'$COLUMN1'">'
echo '        Memory:'
echo '      </div>'
echo '      <div class="'$COLUMN2'">'
echo '        '$(pcp_rpi_memory)
echo '      </div>'
echo '      <div class="'$COLUMN3'">'
echo '        LMS IP:'
echo '      </div>'
echo '      <div class="'$COLUMN4'">'
echo '        '$(pcp_diag_rpi_lmsip)
echo '      </div>'
echo '      <div class="'$COLUMN5'">'
echo '        Controls MAC:'
echo '      </div>'
echo '      <div  class="'$COLUMN6'">'
echo '        '$(pcp_controls_mac_address)
echo '      </div>'
#-------------------------------------Row 5----------------------------------------------
echo '      <div class="'$COLUMN1'">'
echo '        Shortname:'
echo '      </div>'
echo '      <div class="'$COLUMN2'">'
echo '        '$(pcp_rpi_shortname)
echo '      </div>'
echo '      <div class="'$COLUMN3'">'
echo '        Uptime:'
echo '      </div>'
echo '      <div class="col">'
echo '        '$(pcp_uptime_days)
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
pcp_border_end

#========================================================================================
# Squeezelite
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "Squeezelite"
#-------------------------------------Row 1----------------------------------------------

if [ $(pcp_squeezelite_status) -eq 0 ]; then
	pcp_green_tick "Squeezelite running."
else
	pcp_red_cross "Squeezelite not running."
fi

echo '    <div class="row mx-1 mb-2">'
echo '      <div class="'$COLUMN1' text-right">'
echo '        '$INDICATOR
echo '      </div>'
echo '      <div class="'$COLUMN2'">'
echo '        '$STATUS
echo '      </div>'
echo '      <div class="'$COLUMN3'">'
echo '        Version:'
echo '      </div>'
echo '      <div class="'$COLUMN4'">'
echo '        '$(pcp_squeezelite_version)
echo '      </div>'
#-------------------------------------Row 2----------------------------------------------
echo '      <div class="'$COLUMN1'">'
echo '        Build options:'
echo '      </div>'
echo '      <div class="col">'
echo '        '$BUILD
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
pcp_border_end

#========================================================================================
# piCorePlayer
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "piCorePlayer"
#-------------------------------------Row 1----------------------------------------------
echo '    <div class="row mx-1 mb-2">'
echo '      <div class="'$COLUMN1'">'
echo '        Version:'
echo '      </div>'
echo '      <div class="'$COLUMN2'">'
echo '        '$(pcp_picoreplayer_version)
echo '      </div>'
echo '      <div class="'$COLUMN3'">'
echo '        pCP name:'
echo '      </div>'
echo '      <div class="'$COLUMN4'">'
echo '        '$NAME
echo '      </div>'
echo '      <div class="'$COLUMN5'">'
echo '        Hostname:'
echo '      </div>'
echo '      <div class="'$COLUMN6'">'
echo '        '$HOST
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
pcp_border_end

#========================================================================================
# piCore
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "piCore"
#-------------------------------------Row 1----------------------------------------------
echo '    <div class="row mx-1 mb-2">'
echo '      <div class="'$COLUMN1'">'
echo '        Version:'
echo '      </div>'
echo '      <div class="'$COLUMN2'">'
echo '        '$(pcp_picore_version)
echo '      </div>'
echo '      <div class="'$COLUMN3'">'
echo '        Linux release:'
echo '      </div>'
echo '      <div class="'$COLUMN4'">'
echo '        '$(pcp_linux_release)
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
pcp_border_end

#========================================================================================
# Internet and piCorePlayer repository accessible
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "Internet"
#-------------------------------------Row 1----------------------------------------------

if [ $(pcp_internet_accessible) -eq 0 ]; then
    pcp_green_tick "Internet accessible."
else
    pcp_red_cross "Internet not accessible."
fi

echo '    <div class="row mx-1 mb-2">'
echo '      <div class="col-2 text-right">'
echo '        '$INDICATOR
echo '      </div>'
echo '      <div class="col">'
echo '        '$STATUS
echo '      </div>'
echo '    </div>'

if [ $(pcp_pcp_repo_1_accessible) -eq 0 ]; then
    pcp_green_tick "piCorePlayer repository accessible."
else
    pcp_red_cross "piCorePlayer repository not accessible."
fi

echo '    <div class="row mx-1 mb-2">'
echo '      <div class="col-2 text-right">'
echo '        '$INDICATOR
echo '      </div>'
echo '      <div class="col">'
echo '        '$STATUS
echo '      </div>'
echo '    </div>'
#--------------------------------------------------------------------------------
pcp_border_end

[ $MODE -ge $MODE_DEVELOPER ] && pcp_pastebin_button "Raspberry-Pi"

pcp_html_end

pcp_add_to_log
exit