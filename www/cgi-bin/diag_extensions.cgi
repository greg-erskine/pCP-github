#!/bin/sh

# Version: 3.10 2017-01-06
#	Original version.

#========================================================================================
# This script checks for required extensions in repositories.
#----------------------------------------------------------------------------------------

. /etc/init.d/tc-functions
. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Diagnostics extensions" "GE"

pcp_banner
pcp_navigation

# Set variables
PCP_REPO=${PCP_REPO}/
KERNELVER=$(uname -r)
EXTENLIST="/tmp/pcp_extensions.lst"
VERBOSE=TRUE
WGET="/bin/busybox wget"
getMirror

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_internet() {
	if [ $(pcp_internet_accessible) -eq 0 ]; then
		echo "[  OK  ] Internet accessible." | tee -a $LOG
	else
		echo "[ ERROR ] Internet not accessible." | tee -a $LOG
	fi
}

pcp_picore_repo_1() {
	if [ $(pcp_picore_repo_1_accessible) -eq 0 ]; then
		echo "[  OK  ] Official piCore repository accessible. ($PICORE_REPO_1)"
	else
		echo "[ ERROR ] Official piCore repository not accessible. ($PICORE_REPO_1)"
	fi
}

pcp_picore_repo_2() {
	if [ $(pcp_picore_repo_2_accessible) -eq 0 ]; then
		echo "[  OK  ] Official piCore mirror repository accessible. ($PICORE_REPO_2)"
	else
		echo "[ ERROR ] Official piCore mirror repository not accessible. ($PICORE_REPO_2)"
	fi
}

pcp_pcp_repo() {
	if [ $(pcp_pcp_repo_accessible) -eq 0 ]; then
		echo "[  OK  ] piCorePlayer sourceforge repository accessible. ($PCP_REPO)"
	else
		echo "[ ERROR ] piCorePlayer sourceforge repository not accessible. ($PCP_REPO)"
	fi
}

pcp_set_repo() {
	MIRROR="${1}/$(getMajorVer).x/$(getBuild)/tcz"
	echo "" | tee -a $LOG
	echo "[ INFO ] Set repository to ${MIRROR}" | tee -a $LOG
}

pcp_check_extension() {
	$WGET -s "${MIRROR}/$1"
	if [ $? -eq 0 ]; then
		echo "[  OK  ] ${MIRROR}/$1" | tee -a $LOG
	else
		echo "[ FAIL ] ${MIRROR}/$1" | tee -a $LOG
	fi
}

pcp_message() {
	echo "" | tee -a $LOG
	echo "[ INFO ] Checking extensions for ${1}..." | tee -a $LOG
}

#========================================================================================
# Generate a list of REQUIRED DOWNLOADED EXTENSIONS (alphabetically sorted)
#
# NOTE: This list must be maintained MANUALLY.
#----------------------------------------------------------------------------------------
pcp_downloaded_extensions() {
	VERSION=$(echo ${KERNELVER} | awk -F"-" '{print $1}')
	echo alsa-modules-${VERSION}-piCore+.tcz     > $EXTENLIST
	echo alsa-modules-${VERSION}-piCore_v7+.tcz >> $EXTENLIST
	echo alsa-utils.tcz                         >> $EXTENLIST
	echo alsa.tcz                               >> $EXTENLIST
	echo backlight-${VERSION}-piCore+.tcz       >> $EXTENLIST
	echo backlight-${VERSION}-piCore_v7+.tcz    >> $EXTENLIST
	echo busybox-httpd.tcz                      >> $EXTENLIST
	echo dialog.tcz                             >> $EXTENLIST
	echo firmware-atheros.tcz                   >> $EXTENLIST
	echo firmware-brcmwifi.tcz                  >> $EXTENLIST
	echo firmware-ralinkwifi.tcz                >> $EXTENLIST
	echo firmware-rpi3-wireless.tcz             >> $EXTENLIST
	echo firmware-rtlwifi.tcz                   >> $EXTENLIST
	echo libasound.tcz                          >> $EXTENLIST
	echo libedit.tcz                            >> $EXTENLIST
	echo libelf.tcz                             >> $EXTENLIST
	echo libgcrypt.tcz                          >> $EXTENLIST
	echo libgpg-error.tcz                       >> $EXTENLIST
	echo libiw.tcz                              >> $EXTENLIST
	echo libnl.tcz                              >> $EXTENLIST
	echo libssh2.tcz                            >> $EXTENLIST
	echo libts.tcz                              >> $EXTENLIST
	echo ncurses.tcz                            >> $EXTENLIST
	echo openssh.tcz                            >> $EXTENLIST
	echo openssl.tcz                            >> $EXTENLIST
	echo readline.tcz                           >> $EXTENLIST
	echo touchscreen-${VERSION}-piCore+.tcz     >> $EXTENLIST
	echo touchscreen-${VERSION}-piCore_v7+.tcz  >> $EXTENLIST
	echo wifi.tcz                               >> $EXTENLIST
	echo wireless-${VERSION}-piCore+.tcz        >> $EXTENLIST
	echo wireless-${VERSION}-piCore_v7+.tcz     >> $EXTENLIST
	echo wireless_tools.tcz                     >> $EXTENLIST
	echo wpa_supplicant.tcz                     >> $EXTENLIST
	unset VERSION
}

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
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="warning">'
	echo '              <td>'
	echo '                <p style="color:white">The checks below only refer to extensions for:</p>'
	echo '                <ul>'
	echo '                  <li style="color:white">Kernel: '${KERNELVER}'</li>'
	echo '                  <li style="color:white">Major version: '$(getMajorVer)'.x</li>'
	echo '                  <li style="color:white">Build version: '$(getBuild)'</li>'
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
# Display debug information
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	if [ $DEBUG -eq 1 ]; then
		echo '                 [ DEBUG ] $SUBMIT: '$SUBMIT'<br />'
		echo '                 [ DEBUG ] $PICORE_REPO_1: '$PICORE_REPO_1'<br />'
		echo '                 [ DEBUG ] $PICORE_REPO_2: '$PICORE_REPO_2'<br />'
		echo '                 [ DEBUG ] $PCP_REPO: '$PCP_REPO'</p>'
	fi
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_running_script
pcp_debug_info
pcp_log_header $0

#========================================================================================
#	Check standard extensions are downloaded
#	Check for extra extensions
#----------------------------------------------------------------------------------------
echo "List of standard extensions" >> $LOG
echo "" >> $LOG

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Checking the standard extensions are downloaded . . .</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" style="height:300px">'

echo "[ INFO  ] The list of standard extensions must be maintained MANUALLY." | tee -a $LOG
pcp_downloaded_extensions
for i in $(cat $EXTENLIST)
do
	if [ -f /mnt/mmcblk0p2/tce/optional/${i} ]; then
		[ $VERBOSE ] && echo "[ FOUND ] $i" | tee -a $LOG
	else
		echo "[ MISSING ] $i" | tee -a $LOG
	fi
done 

echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------
echo "" >> $LOG
echo "List of additional (non-standard) extensions" >> $LOG
echo "" >> $LOG

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Checking for extra extensions . . .</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'
echo '                <textarea class="inform" style="height:300px">'

EXTNS=$(ls /mnt/mmcblk0p2/tce/optional/*.tcz | sed 's/\/mnt\/mmcblk0p2\/tce\/optional\///g')

for i in $EXTNS
do
	if grep $i $EXTENLIST >/dev/null 2>&1; then
		[ $VERBOSE ] && echo "[ OK ] $i"  | tee -a $LOG
	else
		echo "[ EXTRA ] $i" | tee -a $LOG
	fi
done 

echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

echo "" >> $LOG
pcp_write_to_log "Downloaded extensions" "ls /mnt/mmcblk0p2/tce/optional/*.tcz | sed 's/\/mnt\/mmcblk0p2\/tce\/optional\///g'"
pcp_write_to_log "Installed extensions" "tce-status -i"
pcp_write_to_log "Uninstalled extensions" "tce-status -u"

#----------------------------------------------------------------------------------------

pcp_warning_message

#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Checking extensions. . .</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <textarea class="inform" style="height:300px">'

pcp_internet | tee -a $LOG
pcp_picore_repo_1 | tee -a $LOG
pcp_pcp_repo | tee -a $LOG

echo "" >> $LOG
echo "Checking repositories for extensions" >> $LOG

#========================================================================================
pcp_set_repo ${PCP_REPO%/}
#========================================================================================
pcp_message "LIRC"
#-----------------
pcp_check_extension lirc.tcz
pcp_check_extension irda-${KERNELVER}.tcz
pcp_check_extension libcofi.tcz
#----------------------------------------------------------------------------------------
pcp_message "Raspberry Pi Touch Screen"
#--------------------------------------
pcp_check_extension backlight-${KERNELVER}.tcz
pcp_check_extension touchscreen-${KERNELVER}.tcz
pcp_check_extension libts.tcz
#----------------------------------------------------------------------------------------
pcp_message "Jivelite"
#---------------------
pcp_check_extension jivelite_touch.tcz
pcp_check_extension VU_Meter_Kolossos_Oval.tcz
pcp_check_extension VU_Meter_Jstraw_Dark.tcz
pcp_check_extension VU_Meter_Jstraw_Dark_Peak.tcz
pcp_check_extension VU_Meter_Jstraw_Vintage.tcz
pcp_check_extension VU_Meter_Logitech_Black.tcz
pcp_check_extension VU_Meter_Logitech_White.tcz
#----------------------------------------------------------------------------------------
pcp_message "Audiophonics"
#-------------------------
pcp_check_extension Audiophonics-powerscript.tcz
#----------------------------------------------------------------------------------------
pcp_message "LMS"
#----------------
pcp_check_extension slimserver.tcz
pcp_check_extension slimserver-CPAN.tcz
pcp_check_extension perl5.tcz
pcp_check_extension gcc_libs.tcz
pcp_check_extension openssl.tcz
pcp_check_extension perl_io_socket_ssl.tcz
pcp_check_extension perl_mozilla_ca.tcz
pcp_check_extension perl_net_ssleay.tcz
#----------------------------------------------------------------------------------------
pcp_message "Broadcom USB wifi adaptor"
#--------------------------------------
pcp_check_extension firmware-brcmwifi.tcz
#----------------------------------------------------------------------------------------
pcp_message "Shairport"
#----------------------
pcp_check_extension avahi.tcz
pcp_check_extension dbus.tcz
pcp_check_extension expat2.tcz
pcp_check_extension libattr.tcz
pcp_check_extension libavahi.tcz
pcp_check_extension libcap.tcz
pcp_check_extension libcofi.tcz
pcp_check_extension libdaemon.tcz
pcp_check_extension nss-mdns.tcz 
#----------------------------------------------------------------------------------------
pcp_message "ALSA equaliser"
#---------------------------
pcp_check_extension alsaequal.tcz
pcp_check_extension caps-0.4.5.tcz
#----------------------------------------------------------------------------------------

#========================================================================================
pcp_set_repo ${PICORE_REPO_1%/}
#========================================================================================
pcp_message "standard extensions"
#--------------------------------
pcp_check_extension alsa-modules-${KERNELVER}.tcz
pcp_check_extension alsa-utils.tcz
pcp_check_extension alsa.tcz
pcp_check_extension busybox-httpd.tcz
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
pcp_message "pastebin"
#---------------------
pcp_check_extension wget.tcz
#----------------------------------------------------------------------------------------
pcp_message "wifi"
#-----------------
pcp_check_extension firmware-atheros.tcz
pcp_check_extension firmware-brcmwifi.tcz
pcp_check_extension firmware-ralinkwifi.tcz
pcp_check_extension firmware-rpi3-wireless.tcz
pcp_check_extension firmware-rtlwifi.tcz
pcp_check_extension wifi.tcz
pcp_check_extension wireless-${KERNELVER}.tcz
pcp_check_extension wireless_tools.tcz
pcp_check_extension wpa_supplicant.tcz
#----------------------------------------------------------------------------------------
pcp_message "wifi diagnositcs"
#-----------------------------
pcp_check_extension usbutils.tcz
#----------------------------------------------------------------------------------------
pcp_message "networking"
#-----------------------
pcp_check_extension filesystems-${KERNELVER}.tcz
pcp_check_extension ntfs-3g.tcz
pcp_check_extension net-usb-${KERNELVER}.tcz
#----------------------------------------------------------------------------------------
pcp_message "Common extensions"
#------------------------------
pcp_check_extension nano.tcz
#----------------------------------------------------------------------------------------

echo "" | tee -a $LOG
echo "[ DONE ] Log report complete." | tee -a $LOG

echo '                </textarea>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'