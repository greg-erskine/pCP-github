#!/bin/sh

# Version: 0.01 2016-03-30 GE
#	Original.

. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Logs" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

PCPLOGS=$(cd "${LOGDIR}"; ls pcp_*.log)
[ x"" = x"$PCPLOGS" ] && FIRST="No log files found." || FIRST="All"

LMSLOGS=$(cd "${LOGDIR}"; ls slimserver/*.log)
[ x"" = x"$LMSLOGS" ] && LMSLOGS="No LMS log files found."

LOGS=$PCPLOGS" "$LMSLOGS

#/var/log/slimserver/server.log
#/var/log/slimserver/scanner.log

#========================================================================================
# Selection form
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Log file operations</legend>'
echo '          <table class="bggrey percent100">'
echo '            <form name="log" action="'$0'" method="get">'

#----------------------------------------------------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column300">'
echo '                <select class="large22" name="SELECTION">'
echo '                  <option value="'$FIRST'">'$FIRST'</option>'

	                    for LOG in $LOGS
	                    do
	                      echo '<option value="'$LOG'">'$LOG'</option>'
	                    done

#	                    for LOG in $LMSLOGS
#	                    do
#	                      echo '<option value="slimserver/'$LOG'">'$LOG'</option>'
#	                    done

echo '                </select>'
echo '              </td>'
echo '              <td>'
echo '                <p>Select log file&nbsp;&nbsp;'
echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                </p>'
echo '                <div id="'$ID'" class="less">'
echo '                  <p>Show logs in text area below.</p>'
echo '                </div>'
echo '              </td>'

if [ "$FIRST" = "All" ]; then
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <input type="submit" name="ACTION" value="Show">'
	echo '                </td>'
	echo '              </tr>'
fi
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#------------------------------------------Log text area---------------------------------
pcp_log_show() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Show log file</legend>'
	echo '          <table class="bggrey percent100">'

	if [ "$SELECTION" = "All" ]; then
		for LOG in $LOGS
		do
			echo '            <tr>'
			echo '              <td>'
			                      pcp_textarea_inform "$LOG" 'cat ${LOGDIR}/$LOG' 250
			echo '              </td>'
			echo '            </tr>'
		done
	else
		echo '            <tr>'
		echo '              <td>'
		                      pcp_textarea_inform "$SELECTION" 'cat ${LOGDIR}/$SELECTION' 250
		echo '              </td>'
		echo '            </tr>'
	fi

	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ "$ACTION" = "Show" ] && pcp_log_show
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'