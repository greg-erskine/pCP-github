#!/bin/sh

# Version: 7.0.0 2020-05-28

#========================================================================================
# This script checks for required extensions in repositories.
#----------------------------------------------------------------------------------------
. /etc/init.d/tc-functions
. pcp-functions
. pcp-lms-functions

pcp_html_head "Diagnostics extensions" "GE"

pcp_navbar

#========================================================================================
# Set variables
#----------------------------------------------------------------------------------------
PCP_REPO="${PCP_REPO%/}/"
KERNELVER="$(uname -r)"
EXTENLIST="/tmp/pcp_extensions.lst"
WGET="/bin/busybox wget"
getMirror

#VERBOSE=TRUE

#ValidMajorVer="8.x 9.x 10.x"
#ValidBuild="ARM6 ARM7"

#========================================================================================
# Generate a list of REQUIRED DOWNLOADED EXTENSIONS (alphabetically sorted)
#
# NOTE: This list must be maintained MANUALLY.
#----------------------------------------------------------------------------------------
pcp_downloaded_extensions() {
	VERSION=$(echo ${KERNELVER} | awk -F"-" '{print $1}')
	echo alsa-modules-${VERSION}-pcpCore.tcz      > $EXTENLIST
	echo alsa-modules-${VERSION}-pcpCore_v7.tcz  >> $EXTENLIST
	echo alsa-modules-${VERSION}-pcpCore_v7l.tcz >> $EXTENLIST
	echo alsa-utils.tcz                          >> $EXTENLIST
	echo alsa.tcz                                >> $EXTENLIST
	echo ca-certificates.tcz                     >> $EXTENLIST
	echo crda.tcz                                >> $EXTENLIST
	echo dialog.tcz                              >> $EXTENLIST
	echo firmware-atheros.tcz                    >> $EXTENLIST
	echo firmware-brcmwifi.tcz                   >> $EXTENLIST
	echo firmware-ralinkwifi.tcz                 >> $EXTENLIST
	echo firmware-rpi-wifi.tcz                   >> $EXTENLIST
	echo firmware-rtlwifi.tcz                    >> $EXTENLIST
	echo libasound.tcz                           >> $EXTENLIST
	echo libedit.tcz                             >> $EXTENLIST
	echo libgcrypt.tcz                           >> $EXTENLIST
	echo libgpg-error.tcz                        >> $EXTENLIST
	echo libiw.tcz                               >> $EXTENLIST
	echo libnl.tcz                               >> $EXTENLIST
	echo ncurses.tcz                             >> $EXTENLIST
	echo net-usb-${VERSION}-pcpCore.tcz          >> $EXTENLIST
	echo net-usb-${VERSION}-pcpCore_v7.tcz       >> $EXTENLIST
	echo net-usb-${VERSION}-pcpCore_v7l.tcz      >> $EXTENLIST
	echo never_remove.tcz                        >> $EXTENLIST
	echo openssh.tcz                             >> $EXTENLIST
	echo openssl.tcz                             >> $EXTENLIST
	echo pcp.tcz                                 >> $EXTENLIST
	echo pcp-base.tcz                            >> $EXTENLIST
	echo pcp-libfaad2.tcz                        >> $EXTENLIST
	echo pcp-libflac.tcz                         >> $EXTENLIST
	echo pcp-libmad.tcz                          >> $EXTENLIST
	echo pcp-libmpg123.tcz                       >> $EXTENLIST
	echo pcp-libogg.tcz                          >> $EXTENLIST
	echo pcp-libsoxr.tcz                         >> $EXTENLIST
	echo pcp-libvorbis.tcz                       >> $EXTENLIST
	echo pcp-squeezelite.tcz                     >> $EXTENLIST
	echo readline.tcz                            >> $EXTENLIST
	echo wireless-${VERSION}-pcpCore.tcz         >> $EXTENLIST
	echo wireless-${VERSION}-pcpCore_v7.tcz      >> $EXTENLIST
	echo wireless-${VERSION}-pcpCore_v7l.tcz     >> $EXTENLIST
	echo wireless_tools.tcz                      >> $EXTENLIST
	echo wpa_supplicant.tcz                      >> $EXTENLIST
	unset VERSION
}

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_internet() {
	if [ $(pcp_internet_accessible) -eq 0 ]; then
		pcp_green_tick "Internet accessible."
		echo "[  OK  ] Internet accessible." >> $LOG
		echo "INTERNET_ACCESSIBLE=true" > $ACCCESSIBLETXT
	else
		pcp_red_cross "Internet not accessible."
		echo "[ ERROR ] Internet not accessible." >> $LOG
		echo "unset INTERNET_ACCESSIBLE" > $ACCCESSIBLETXT
	fi
	INDICATOR="$(echo $INDICATOR | sed -e 's|"|\\"|g')"
}

pcp_dns() {
	if [ $(pcp_dns_accessible) -eq 0 ]; then
		pcp_green_tick "DNS accessible."
		echo "[  OK  ] DNS accessible." >> $LOG
		echo "DNS_ACCESSIBLE=true" >> $ACCCESSIBLETXT
	else
		pcp_red_cross "DNS not accessible."
		echo "[ ERROR ] DNS not accessible." >> $LOG
		echo "unset DNS_ACCESSIBLE" >> $ACCCESSIBLETXT
	fi
	INDICATOR="$(echo $INDICATOR | sed -e 's|"|\\"|g')"
}

pcp_pcp_repo_1() {
	if [ $(pcp_pcp_repo_1_accessible) -eq 0 ]; then
		pcp_green_tick "piCorePlayer main repository accessible ($PCP_REPO_1)."
		echo "[  OK  ] piCorePlayer main repository accessible. ($PCP_REPO_1)" >> $LOG
		echo "PCP_REPO_1_ACCESSIBLE=true" >> $ACCCESSIBLETXT
	else
		pcp_red_cross "piCorePlayer main repository not accessible ($PCP_REPO_1)."
		echo "[ ERROR ] piCorePlayer main repository not accessible. ($PCP_REPO_1)" >> $LOG
		echo "unset PCP_REPO_1_ACCESSIBLE" >> $ACCCESSIBLETXT
	fi
	INDICATOR="$(echo $INDICATOR | sed -e 's|"|\\"|g')"
}

pcp_pcp_repo_2() {
	if [ $(pcp_pcp_repo_2_accessible) -eq 0 ]; then
		pcp_green_tick "piCorePlayer mirror repository accessible ($PCP_REPO_2)."
		echo "[  OK  ] piCorePlayer mirror repository accessible. ($PCP_REPO_2)" >> $LOG
		echo "PCP_REPO_2_ACCESSIBLE=true" >> $ACCCESSIBLETXT
	else
		pcp_red_cross "piCorePlayer mirror repository not accessible ($PCP_REPO_2)."
		echo "[ ERROR ] piCorePlayer mirror repository not accessible. ($PCP_REPO_2)" >> $LOG
		echo "unset PCP_REPO_2_ACCESSIBLE" >> $ACCCESSIBLETXT
	fi
	INDICATOR="$(echo $INDICATOR | sed -e 's|"|\\"|g')"
}

pcp_picore_repo_1() {
	if [ $(pcp_picore_repo_1_accessible) -eq 0 ]; then
		pcp_green_tick "Official piCore repository accessible ($PICORE_REPO_1)."
		echo "[  OK  ] Official piCore repository accessible. ($PICORE_REPO_1)" >> $LOG
		echo "PICORE_REPO_1_ACCESSIBLE=true" >> $ACCCESSIBLETXT
	else
		pcp_red_cross "Official piCore repository not accessible ($PICORE_REPO_1)."
		echo "[ ERROR ] Official piCore repository not accessible. ($PICORE_REPO_1)" >> $LOG
		echo "unset PICORE_REPO_1_ACCESSIBLE" >> $ACCCESSIBLETXT
	fi
	INDICATOR="$(echo $INDICATOR | sed -e 's|"|\\"|g')"
}

pcp_picore_repo_2() {
	if [ $(pcp_picore_repo_2_accessible) -eq 0 ]; then
		pcp_green_tick "Official piCore mirror repository accessible ($PICORE_REPO_2)."
		echo "[  OK  ] Official piCore mirror repository accessible. ($PICORE_REPO_2)" >> $LOG
		echo "PICORE_REPO_2_ACCESSIBLE=true" >> $ACCCESSIBLETXT
	else
		pcp_red_cross "Official piCore mirror repository not accessible ($PICORE_REPO_2)."
		echo "[ ERROR ] Official piCore mirror repository not accessible. ($PICORE_REPO_2)" >> $LOG
		echo "unset PICORE_REPO_2_ACCESSIBLE" >> $ACCCESSIBLETXT
	fi
	INDICATOR="$(echo $INDICATOR | sed -e 's|"|\\"|g')"
}

pcp_set_repo() {
	MIRROR="${1}/$(getMajorVer).x/$(getBuild)/tcz"
	echo "" | tee -a $LOG
	echo "[ INFO ] Set repository to ${MIRROR}" | tee -a $LOG
}

pcp_check_extension() {
	$WGET --spider "${MIRROR}/$1"
	if [ $? -eq 0 ]; then
		echo "[  OK  ] ${MIRROR}/$1" | tee -a $LOG
	else
		echo "[ FAIL ] ${MIRROR}/$1" | tee -a $LOG
	fi
}

pcp_extn_message() {
	echo "" | tee -a $LOG
	echo "[ INFO ] Checking extensions for ${1}..." | tee -a $LOG
}

#========================================================================================
# Display debug information
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	pcp_debug_variables "html" PICORE_REPO_1 PICORE_REPO_2 PCP_REPO LOG
}

#========================================================================================
# Javascript - move to picoreplayer.js
#----------------------------------------------------------------------------------------
pcp_indicator_js() {
	echo '<script>'
	echo 'var theIndicator = document.querySelector("#indicator'$ID'");'
	echo '	document.getElementById("indicator'$ID'").innerHTML = "'$INDICATOR'";'
	echo '	document.getElementById("status'$ID'").innerHTML = "'$STATUS'";'
	echo '</script>'
}

pcp_indicator () {
	INDICATOR_MESSAGE="$1"
	COLUMN2_1="col-1"
	COLUMN2_2="col-11"

	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN2_1' text-md-right">'
	echo '        <p id="indicator'$ID'">?</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN2_2'">'
	echo '        <p id="status'$ID'">'$INDICATOR_MESSAGE'</p>'
	echo '      </div>'
	echo '    </div>'
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_debug_info
pcp_log_header $0

COLUMN2_1="col-1"
COLUMN2_2="col-11"
#----------------------------------------------------------------------------------------
# Repository accessibility indicators.
#----------------------------------------------------------------------------------------
pcp_heading5 "Checking Internet and repository accessibility. . . "
pcp_border_begin
#---------------------------------Internet accessible------------------------------------
pcp_indicator "Checking internet..."
pcp_internet
pcp_indicator_js
#-----------------------------------DNS accessible---------------------------------------
pcp_indicator "Checking DNS..."
pcp_dns
pcp_indicator_js
#---------------------------piCorePlayer repository 1 accessible-------------------------
pcp_indicator "Checking piCorePlayer repository..."
pcp_pcp_repo_1
pcp_indicator_js
#---------------------------piCorePlayer repository 2 accessible-------------------------
pcp_indicator "Checking piCorePlayer mirror repository..."
pcp_pcp_repo_2
pcp_indicator_js
#--------------------------Official piCore repository accessible-------------------------
pcp_indicator "Checking piCore repository..."
pcp_picore_repo_1
pcp_indicator_js
#----------------------Official piCore mirror repository accessible----------------------
if [ $MODE -ge $MODE_DEVELOPER ]; then
	pcp_indicator "Checking piCore mirror repository..."
	pcp_picore_repo_2
	pcp_indicator_js
fi
#----------------------------------------------------------------------------------------
pcp_border_end
#----------------------------------------------------------------------------------------

#========================================================================================
#  Check standard extensions are downloaded.
#  Check for extra extensions.
#----------------------------------------------------------------------------------------
echo "" >> $LOG 
echo "List of standard extensions" >> $LOG
echo "---------------------------" >> $LOG
echo "" >> $LOG

pcp_heading5 "Checking the standard extensions are downloaded. . ."

pcp_infobox_begin
echo "[ INFO  ] The list of standard extensions must be maintained MANUALLY." | tee -a $LOG
pcp_downloaded_extensions

for i in $(cat $EXTENLIST)
do
	if [ -f /$TCEMNT/tce/optional/${i} ]; then
		[ $VERBOSE ] && echo "[ FOUND ] $i" | tee -a $LOG
	else
		echo "[ MISSING ] $i" | tee -a $LOG
	fi
done 

pcp_infobox_end

#----------------------------------------------------------------------------------------
echo "" >> $LOG
echo "List of additional (non-standard) extensions" >> $LOG
echo "--------------------------------------------" >> $LOG
echo "" >> $LOG

pcp_heading5 "Checking for extra extensions . . ."
pcp_infobox_begin

EXTNS=$(ls $TCEMNT/tce/optional/*.tcz | awk -F 'optional/' '{print $2}')

for i in $EXTNS
do
	if grep $i $EXTENLIST >/dev/null 2>&1; then
		[ $VERBOSE ] && echo "[ OK ] $i"  | tee -a $LOG
	else
		echo "[ EXTRA ] $i" | tee -a $LOG
	fi
done 

pcp_infobox_end
#----------------------------------------------------------------------------------------

echo "" >> $LOG
ls $TCEMNT/tce/optional/*.tcz | awk -F 'optional/' '{print $2}' > /tmp/downloadedextensions
pcp_write_to_log "Downloaded extensions" "cat /tmp/downloadedextensions"
pcp_write_to_log "Installed extensions" "tce-status -i"
pcp_write_to_log "Uninstalled extensions" "tce-status -u"

pcp_hr

#--------------------------------------Warning message-----------------------------------
echo '    <div class="alert alert-primary" role="alert">'
echo '      <b>Warning:</b>'
echo '      <p>The checks below only refer to extensions for:</p>'
echo '      <ul>'
echo '        <li>Kernel: '${KERNELVER}'</li>'
echo '        <li>Major version: '$(getMajorVer)'.x</li>'
echo '        <li>Build version: '$(getBuild)'</li>'
echo '      </ul>'
echo '      </div>'
#----------------------------------------------------------------------------------------

pcp_heading5 "Checking extensions. . ."
pcp_infobox_begin

echo "" >> $LOG
echo "Checking repositories for extensions" >> $LOG
#========================================================================================
pcp_set_repo ${PCP_REPO%/}
#========================================================================================
pcp_extn_message "LIRC"
#----------------------
pcp_check_extension pcp-lirc.tcz
pcp_check_extension libcofi.tcz
pcp_check_extension media-rc-${KERNELVER}.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "Raspberry Pi Touch Screen"
#-------------------------------------------
pcp_check_extension touchscreen-${KERNELVER}.tcz
pcp_check_extension libts.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "Jivelite"
#--------------------------
pcp_check_extension libts.tcz
pcp_check_extension libcofi.tcz
pcp_check_extension pcp-jivelite.tcz
pcp_check_extension pcp-jivelite_hdskins.tcz
pcp_check_extension VU_Meter_Kolossos_Oval.tcz
pcp_check_extension VU_Meter_Jstraw_Dark.tcz
pcp_check_extension VU_Meter_Jstraw_Dark_Peak.tcz
pcp_check_extension VU_Meter_Jstraw_Vintage.tcz
pcp_check_extension VU_Meter_Logitech_Black.tcz
pcp_check_extension VU_Meter_Logitech_White.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "Audiophonics"
#------------------------------
pcp_check_extension Audiophonics-powerscript.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "LMS"
#---------------------
pcp_check_extension slimserver.tcz
pcp_check_extension slimserver-CPAN.tcz
pcp_check_extension perl5.tcz
pcp_check_extension gcc_libs.tcz
pcp_check_extension openssl.tcz
pcp_check_extension ca-certificates.tcz
pcp_check_extension perl_io_socket_ssl.tcz
pcp_check_extension perl_mozilla_ca.tcz
pcp_check_extension perl_net_ssleay.tcz
pcp_check_extension perl_crypt_openssl_rsa.tcz
pcp_check_extension perl_common_sense.tcz
pcp_check_extension perl_linux_inotify2.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "Broadcom USB wifi adaptor"
#-------------------------------------------
pcp_check_extension firmware-brcmwifi.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "Shairport-sync"
#--------------------------------
pcp_check_extension pcp-shairportsync.tcz
pcp_check_extension libcofi.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "ALSA equaliser"
#--------------------------------
pcp_check_extension alsaequal.tcz
pcp_check_extension caps.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "networking"
#----------------------------
pcp_check_extension ntfs-3g.tcz
pcp_check_extension filesystems-${KERNELVER}.tcz
pcp_check_extension net-usb-${KERNELVER}.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "standard extensions"
#-------------------------------------
pcp_check_extension alsa-modules-${KERNELVER}.tcz
pcp_check_extension alsa-utils.tcz
pcp_check_extension alsa.tcz
pcp_check_extension dialog.tcz
pcp_check_extension libasound.tcz
pcp_check_extension libedit.tcz
pcp_check_extension libiw.tcz
pcp_check_extension libnl.tcz
pcp_check_extension ncurses.tcz
pcp_check_extension openssh.tcz
pcp_check_extension openssl.tcz
pcp_check_extension readline.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "pastebin"
#--------------------------
pcp_check_extension wget.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "wifi"
#----------------------
pcp_check_extension crda.tcz
pcp_check_extension firmware-atheros.tcz
pcp_check_extension firmware-ralinkwifi.tcz
pcp_check_extension firmware-rpi-wifi.tcz
pcp_check_extension firmware-rtlwifi.tcz
pcp_check_extension libgcrypt.tcz
pcp_check_extension libgpg-error.tcz
pcp_check_extension libnl.tcz
pcp_check_extension wireless_tools.tcz
pcp_check_extension wpa_supplicant.tcz
#----------------------------------------------------------------------------------------
pcp_extn_message "Common extensions"
#-----------------------------------
pcp_check_extension nano.tcz
#----------------------------------------------------------------------------------------

#========================================================================================
pcp_set_repo ${PICORE_REPO_1%/}
#========================================================================================
pcp_extn_message "wifi diagnositcs"
#----------------------------------
pcp_check_extension usbutils.tcz
#----------------------------------------------------------------------------------------

echo "" | tee -a $LOG
echo "[ DONE ] Log report complete." | tee -a $LOG

pcp_infobox_end
#----------------------------------------------------------------------------------------

pcp_html_end
exit
