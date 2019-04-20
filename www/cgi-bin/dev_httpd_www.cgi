#!/bin/sh

# Version: 5.0.0 2019-04-21

# Title: Configure httpd
# Description: Tool to adjust /etc/httpd.conf

. pcp-functions

pcp_html_head "web admin" "GE"

pcp_banner
pcp_running_script

pcp_httpd_query_string

#$HTTPD -d "$QUERY_STRING" | awk -F'&' '{ for(i=1;i<=NF;i++) { printf "%s\"\n",$i} }' | sed 's/=/="/'
#echo "<br>"
#$HTTPD -d "$QUERY_STRING" | awk -F'&' '{ for(i=1;i<=NF;i++) { printf "%s\047\n",$i} }' | sed "s/=/='/"
#
#DIR_FROM="/home/tc/www/"
#DIR_TO="/var/www/"

DEBUG=1

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_save_www() {
	pcp_save_to_config
	pcp_www_write_httpd_conf
	pcp_backup "nohtml"
	pcp_www_read_httpd_conf
}

#========================================================================================
# httpd routines
#----------------------------------------------------------------------------------------
pcp_httpd_start() {
	sudo /usr/local/etc/init.d/httpd start
}

pcp_httpd_stop() {
	sudo /usr/local/etc/init.d/httpd stop
}

pcp_httpd_restart() {
	sudo /usr/local/etc/init.d/httpd restart
}

pcp_httpd_status() {
	sudo /usr/local/etc/init.d/httpd status
}
#========================================================================================
# Read current httpd.conf
#----------------------------------------------------------------------------------------
pcp_www_read_httpd_conf() {
	# FORMAT - colour|text|html
	local FORMAT=$1

	if [ -f $HTTPD_CONF ]; then
		pcp_message INFO "Reading from $HTTPD_CONF..." "$FORMAT"

#		unset WWW_HOME WWW_USER_PWD WWW_USER WWW_PWD

		while read i; do
			case $i in
				\#\ Maintained\ by\ piCorePlayer)
					MAINTAINED="pCP"
					MBP="selected"
				;;
				\#\ Maintained\ by\ user)
					MAINTAINED="user"
					MBU="selected"
				;;
				*:*)
					case $i in
						H:*)
							WWW_HOME=${i#*:}
						;;
						/cgi-bin:*)
							WWW_USER_PWD=${i#*:}
							WWW_USER=${WWW_USER_PWD%:*}
							WWW_PWD=${WWW_USER_PWD#*:}
						;;
					esac
			esac
		done < $HTTPD_CONF
	fi
}

#========================================================================================
# Write httpd.conf
#----------------------------------------------------------------------------------------
pcp_www_write_httpd_conf() {
	# FORMAT - colour|text|html
	local FORMAT=$1

	if [ "$MAINTAINED" = "user" ]; then
		sudo echo '# Maintained by user'           > $HTTPD_CONF
	else
		sudo echo '# Maintained by piCorePlayer'   > $HTTPD_CONF
	fi

	sudo echo 'H:'${WWW_HOME:-/home/tc/www}       >> $HTTPD_CONF
	sudo echo "/cgi-bin:${WWW_USER}:${WWW_PWD}"   >> $HTTPD_CONF

	sudo chown root:root $HTTPD_CONF
	sudo chmod u=rw,go=r $HTTPD_CONF
}

#========================================================================================
# Action
#----------------------------------------------------------------------------------------
pcp_table_top "Action"

case "$ACTION" in
	Save)
		pcp_message INFO "Saving..." "html"
		pcp_save_www
	;;
	Start)
		pcp_httpd_start
	;;
	Stop)
		pcp_httpd_stop
	;;
	Restart)
		pcp_httpd_restart
	;;
	*)
		pcp_message INFO "Initial..." "html"
		ACTION="Initial"
		pcp_www_read_httpd_conf "html"
	;;
esac

pcp_table_end

#========================================================================================
# Debug information.
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	pcp_table_top "[ DEBUG ] Information"
	pcp_debug_variables "html" ACTION MAINTAINED HTTPD_CONF WWW_HOME WWW_USER_PWD WWW_USER WWW_PWD
	pcp_table_end

	pcp_table_top "[ DEBUG ] $HTTPD_CONF"
	pcp_textarea_inform "none" "cat ${HTTPD_CONF}" 70
	pcp_table_end
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# Start of table
#----------------------------------------------------------------------------------------
COL1="column100"
COL2="column210"
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="web_server" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>HTTPD web server settings</legend>'
echo '            <table class="bggrey percent100">'
#-----------------------------------------www port---------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COL1'">'
echo '                  <p>Port</p>'
echo '                </td>'
echo '                <td class="'$COL2'">'
echo '                  <input class="small4"'
echo '                         type="number"'
echo '                         name="WWW_PORT"'
echo '                         value="'$WWW_PORT'"'
echo '                         required'
echo '                  >'
echo '                </td>'
echo '                <td>'
echo '                  <p>www port&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>&lt;80&gt;</p>'
echo '                    <p>Define port.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#------------------------------------------Maintained by---------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COL1'">'
echo '                  <p>Maintained by</p>'
echo '                </td>'
echo '                <td class="'$COL2'">'
echo '                  <select name="MAINTAINED">'
echo '                    <option value="piCorePlayer" '$MBP'>piCorePlayer</option>'
echo '                    <option value="user" '$MBU'>user</option>'
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Maintained by piCorePlayer/User&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>Manual configuration = Maintained by user.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------------www user------------------------------------
if ! [ "$MAINTAINED" = "user" ]; then
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                  <p>User</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="WWW_USER"'
	echo '                         value="'$WWW_USER'"'
	echo '                         required'
	echo '                         title="Invalid characters: $ &amp; ` / &quot;"'
	echo '                         pattern="[^$&`/\x22]+"'
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>www user&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;admin&gt;</p>'
	echo '                    <p>Define user.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
fi
#-----------------------------------------www password-----------------------------------
if ! [ "$MAINTAINED" = "user" ]; then
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                  <p>Password</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="WWW_PWD"'
	echo '                         value="'$WWW_PWD'"'
	echo '                         required'
	#echo '                         title="Invalid characters: $ &amp; ` / &quot;"'
	#echo '                         pattern="[^$&`/\x22]+"'
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>www password&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;admin&gt;</p>'
	echo '                    <p>Define password.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
fi
#--------------------------------------Buttons-------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="ACTION" value="Save">'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
# DEVELOPER options
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>DEVELOPER options</legend>'
echo '          <form name="developer" action="'$0'" method="get">'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="ACTION" value="Start">'
echo '                  <input type="submit" name="ACTION" value="Stop">'
echo '                  <input type="submit" name="ACTION" value="Restart">'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </form>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright
pcp_remove_query_string

echo '</body>'
echo '</html>'
