#!/bin/sh

# Version: 6.0.0 2019-08-16

# Title: Screen setup
# Description: Load modules for Waveshare screens

# Define red cross
RED='&nbsp;<span class="indicator_red">&#x2718;</span>'
RED=""
# Define green tick
GREEN='&nbsp;<span class="indicator_green">&#x2714;</span>'

. pcp-functions

pcp_html_head "Screen setup" "GE"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#========================================================================================
# Generate warning message
#----------------------------------------------------------------------------------------
pcp_warning_message() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <table class="bgred percent100">'
	echo '            <tr class="warning">'
	echo '              <td>'
	echo '                <p><b>Warning:</b> Copyright Notice.</p>'
	echo '                <ul>'
	echo '                  <li>Wavewshare screens.</li>'
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
# Generate html end code
#----------------------------------------------------------------------------------------
pcp_html_end() {
	pcp_footer
	pcp_copyright

	echo '</body>'
	echo '</html>'
}

# Backup cmdline.txt if one does not exist. Use ssh to restore.
pcp_mount_bootpart_nohtml >/dev/null 2>&1
[ ! -f ${CMDLINETXT}.bak ] && pcp_backup_cmdlinetxt


case "$SUBMIT" in
	Restore) pcp_restore_cmdlinetxt ;;
	Backup) pcp_backup_cmdlinetxt ;;
	Clean) pcp_clean_cmdlinetxt ;;
esac

SCR_CMDLINE_TXT="fbcon=map:10 fbcon=font:ProFont6x11 logo.nologo"
SCR_CONFIG_CFG="dtoverlay=ads7846,cs=1,penirq=17,penirq_pull=2,speed=1000000,keep_vref_on=1,swapxy=1,pmax=255,xohms=60,xmin=200,xmax=3900,ymin=200,ymax=3900"



pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
exit
