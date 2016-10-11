#!/bin/sh

# Version: 3.03 2016-10-11
#	Updated formatting. GE.
#	Added backup log. GE.

# Version: 0.04 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.03 2014-08-29 GE
#	Added pcp_go_main_button.

# Version: 0.02 2014-07-18 GE
#	Added pcp_running_script.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables

pcp_html_head "Backup mydata" "SBP" "5" "main.cgi"

pcp_banner
pcp_running_script

LOG="${LOGDIR}/pcp_backup.log"
pcp_log_header $0

#========================================================================================
# Routines - it would be nice to have these in pcp-functions eventually.
#----------------------------------------------------------------------------------------
pcp_table_top() {
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '        <legend>'$1'</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
}

pcp_table_middle() {
	echo '              </td>'
	echo '            </tr>'
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
}

pcp_table_end() {
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
# Main
#----------------------------------------------------------------------------------------
pcp_table_top "Backup"
echo '                <textarea class="inform" style="height:100px">'
pcp_backup "nohtml"
echo '                </textarea>'
pcp_table_middle
pcp_go_main_button
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'