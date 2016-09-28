#!/bin/sh
# Diagnostics script

# Version: 3.03 2016-09-28
#	Changed to using pcp_log_header. GE.

# Version: 0.13 2016-03-28 GE
#	Changed log location to /var/log.

# Version: 0.12 2016-02-03 GE
#	Moved pcp_pastebin_button to Developer mode.

# Version: 0.11 2015-12-24 GE
#	Added Upload to pastebin feature.

# Version: 0.10 2015-07-04 GE
#	Minor updates.

# Version: 0.09 2015-04-28 GE
#	More minor updates.

# Version: 0.08 2015-03-07 GE
#	Minor updates.

# Version: 0.07 2015-02-01 GE
#	Added diagnostics toolbar. 

# Version: 0.06 2014-12-11 GE
#	Added logging to log file.

# Version: 0.05 2014-10-22 GE
#	Testing $LMSIP.
#	Removed sound output to diag_snd.cgi
#	Using pcp_html_head now.

# Version: 0.04 2014-10-02 GE
#	Added $MODE=5 requirement.
#	Modified textarea behaviour.

# Version: 0.03 2014-09-21 GE
#	Added sound diagnostics output.

# version: 0.02 2014-07-21 GE
#	Added pcp_go_main_button.

# version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables
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
pcp_textarea_inform "piCorePlayer version: $(pcp_picoreplayer_version)" "cat /usr/local/sbin/piversion.cfg" 60 log
pcp_textarea_inform "Squeezelite version and license: $(pcp_squeezelite_version)" "/mnt/mmcblk0p2/tce/squeezelite-armv6hf -t" 300 log
pcp_textarea_inform "Squeezelite help" "/mnt/mmcblk0p2/tce/squeezelite-armv6hf -h" 300 log
pcp_textarea_inform "Squeezelite Output devices" "/mnt/mmcblk0p2/tce/squeezelite-armv6hf -l" 150 log
pcp_textarea_inform "Squeezelite Volume controls" "/mnt/mmcblk0p2/tce/squeezelite-armv6hf -L" 150 log
pcp_textarea_inform "Squeezelite process" 'ps -o args | grep -v grep | grep squeezelite' 60 log

pcp_mount_mmcblk0p1 >/dev/null 2>&1
if mount >/dev/null 2>&1 | grep $VOLUME; then
	pcp_textarea_inform "Current config.txt" "cat $CONFIGTXT" 150 log
	pcp_textarea_inform "Current cmdline.txt" "cat $CMDLINETXT" 150 log
	pcp_umount_mmcblk0p1 >/dev/null 2>&1
fi

pcp_textarea_inform "Current config.cfg" "cat $CONFIGCFG" 150 log
pcp_textarea_inform "Current bootsync.sh" "cat $BOOTSYNC" 150 log
pcp_textarea_inform "Current bootlocal.sh" "cat $BOOTLOCAL" 150 log
pcp_textarea_inform "Current shutdown.sh" "cat $SHUTDOWN" 150 log
pcp_textarea_inform "" "dmesg" 300 log
pcp_textarea_inform "Current /opt/.filetool.lst" "cat /opt/.filetool.lst" 300 log
pcp_textarea_inform "Current /opt/.xfiletool.lst" "cat /opt/.xfiletool.lst" 300 log
pcp_textarea_inform "Backup mydata" "tar tzf /mnt/mmcblk0p2/tce/mydata.tgz" 300 log
pcp_textarea_inform "lsmod" "lsmod" 300 log
pcp_textarea_inform "Directory of www/cgi-bin" "ls -al" 300 log

[ $MODE -ge $MODE_DEVELOPER ] && pcp_pastebin_button diagnostics

echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'