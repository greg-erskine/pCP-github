#!/bin/sh
# Diagnostics script

# Version: 4.0.0 2018-06-14

. pcp-functions
. pcp-rpi-functions
. pcp-pastebin-functions

# Local variables
LOG="${LOGDIR}/pcp_diagnostics.log"
pcp_log_header $0

pcp_html_head "Diagnostics" "GE"

pcp_banner
pcp_diagnostics
pcp_running_script

#=========================================================================================
# Diagnostics
#-----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Diagnostics</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td>'

pcp_textarea_inform "piCore version: $(pcp_picore_version)" "version" 60 log
pcp_textarea_inform "piCorePlayer version: $(pcp_picoreplayer_version)" "cat ${PIVERSIONCFG}" 60 log
pcp_textarea_inform "Squeezelite version and license: $(pcp_squeezelite_version)" "${SQLT_BIN} -t" 300 log
pcp_textarea_inform "Squeezelite help" "${SQLT_BIN} -h" 300 log
pcp_textarea_inform "Squeezelite Output devices" "${SQLT_BIN} -l" 150 log
pcp_textarea_inform "Squeezelite Volume controls" "${SQLT_BIN} -L" 150 log
pcp_textarea_inform "Squeezelite process" 'ps -o args | grep -v grep | grep squeezelite' 60 log

pcp_mount_bootpart >/dev/null 2>&1
if mount >/dev/null 2>&1 | grep $VOLUME; then
	pcp_textarea_inform "Current config.txt" "cat $CONFIGTXT" 150 log
	pcp_textarea_inform "Current cmdline.txt" "cat $CMDLINETXT" 150 log
	pcp_umount_bootpart >/dev/null 2>&1
fi

pcp_textarea_inform "Current config.cfg" "cat $CONFIGCFG" 150 log
pcp_textarea_inform "Current bootsync.sh" "cat $BOOTSYNC" 150 log
pcp_textarea_inform "Current bootlocal.sh" "cat $BOOTLOCAL" 150 log
pcp_textarea_inform "Current shutdown.sh" "cat $SHUTDOWN" 150 log
echo '<a name="dmesg"></a>'
pcp_textarea_inform "" "dmesg" 300 log
pcp_textarea_inform "Current /opt/.filetool.lst" "cat /opt/.filetool.lst" 300 log
pcp_textarea_inform "Current /opt/.xfiletool.lst" "cat /opt/.xfiletool.lst" 300 log
pcp_textarea_inform "Backup mydata" "tar tzf /$TCEMNT/tce/mydata.tgz" 300 log
pcp_textarea_inform "lsmod" "lsmod" 300 log
pcp_textarea_inform "Directory of www/cgi-bin" "ls -al" 300 log

echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

[ $MODE -ge $MODE_DEVELOPER ] && pcp_pastebin_button diagnostics

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'