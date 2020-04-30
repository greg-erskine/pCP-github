#!/bin/sh
# Diagnostics script

# Version: 7.0.0 2020-04-30

. pcp-functions
. pcp-rpi-functions
. pcp-pastebin-functions

# Local variables
LOG="${LOGDIR}/pcp_diagnostics.log"
pcp_log_header $0

pcp_html_head "Diagnostics" "GE"

pcp_diagnostics

#=========================================================================================
# Diagnostics
#-----------------------------------------------------------------------------------------
pcp_textarea_inform "piCorePlayer version: $(pcp_picoreplayer_version)" "cat ${PCPVERSIONCFG}; echo \"WWW_BUILD: $WWW_BUILD\"" 3 log
pcp_textarea_inform "piCore version: $(pcp_picore_version)" "version" 2 log
pcp_textarea_inform "Squeezelite version and license: $(pcp_squeezelite_version)" "${SQLT_BIN} -t" 10 log
pcp_textarea_inform "Squeezelite help" "${SQLT_BIN} -h" 10 log
pcp_textarea_inform "Squeezelite Output devices" "${SQLT_BIN} -l" 10 log
pcp_textarea_inform "Squeezelite Volume controls" "${SQLT_BIN} -L" 10 log
pcp_textarea_inform "Squeezelite process" 'ps -o args | grep -v grep | grep squeezelite' 2 log

pcp_mount_bootpart >/dev/null 2>&1
if mount >/dev/null 2>&1 | grep $VOLUME; then
	pcp_textarea_inform "Current config.txt" "cat $CONFIGTXT" 10 log
	pcp_textarea_inform "Current cmdline.txt" "cat $CMDLINETXT" 10 log
	pcp_umount_bootpart >/dev/null 2>&1
fi

pcp_textarea_inform "Current pcp.cfg" "cat $PCPCFG" 10 log
pcp_textarea_inform "Current bootsync.sh" "cat $BOOTSYNC" 10 log
pcp_textarea_inform "Current bootlocal.sh" "cat $BOOTLOCAL" 10 log
pcp_textarea_inform "Current shutdown.sh" "cat $SHUTDOWN" 10 log
echo '<a name="dmesg"></a>'
pcp_textarea_inform "" "dmesg" 10 log
pcp_textarea_inform "Current /opt/.filetool.lst" "cat /opt/.filetool.lst" 10 log
pcp_textarea_inform "Current /opt/.xfiletool.lst" "cat /opt/.xfiletool.lst" 10 log
pcp_textarea_inform "Backup mydata" "tar tzf /$TCEMNT/tce/mydata.tgz" 10 log
pcp_textarea_inform "lsmod" "lsmod" 10 log
pcp_textarea_inform "Directory of www/cgi-bin" "ls -al" 10 log

[ $MODE -ge $MODE_DEVELOPER ] && pcp_pastebin_button diagnostics

pcp_footer
pcp_copyright
#echo '</div>'
echo '</body>'
echo '</html>'
exit