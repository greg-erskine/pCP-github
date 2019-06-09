#!/bin/sh

# Version: 5.0.0 2019-05-19

# Title: Configure httpd
# Description: Tool to adjust /etc/httpd.conf

. pcp-functions

pcp_html_head "web admin" "GE"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#DEBUG=1
#unset HTTPD_PARAM

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_save_httpd_conf() {
	pcp_save_to_config
	pcp_httpd_generate_passwd_hash
	pcp_httpd_write_httpd_conf
	pcp_backup "nohtml"
	pcp_httpd_read_httpd_conf
}

#========================================================================================
# httpd routines
#----------------------------------------------------------------------------------------
pcp_httpd() {
	case $HTTPD_PARAM in
		restart)
			sudo /usr/local/etc/init.d/httpd restart
		;;
		start)
			sudo /usr/local/etc/init.d/httpd start
		;;
		stop)
			sudo /usr/local/etc/init.d/httpd stop
		;;
		status)
			sudo /usr/local/etc/init.d/httpd status
		;;
		*) :
		;;
	esac
}

#========================================================================================
# Password routines
#----------------------------------------------------------------------------------------
pcp_httpd_generate_passwd_hash() {
	RANDOM_SALT=$(tr -dc 'a-zA-Z0-9' < /dev/urandom | fold -w 8 | head -n 1)
	HTTPD_PWD_HASH=$(openssl passwd -1 -salt $RANDOM_SALT $HTTPD_PWD)
}

#========================================================================================
# Warning message
#----------------------------------------------------------------------------------------
pcp_httpd_warning_message() {
	echo '<table class="bgred">'
	echo '  <tr class="warning">'
	echo '    <td>'
	echo '      <p style="color:white"><b>Warning:</b></p>'
	echo '      <ul>'
	echo '        <li style="color:white">'$HTTPD_CONF' is marked as \"Maintained by user\".</li>'
	echo '        <li style="color:white">Configuration file will be not be editted by piCorePlayer.</li>'
	echo '        <li style="color:white">Use manual methods to maintain.</li>'
	echo '      </ul>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	pcp_httpd_html_end
	exit
}

#========================================================================================
# HTML end
#----------------------------------------------------------------------------------------
pcp_httpd_html_end() {
	pcp_footer
	pcp_copyright
	pcp_remove_query_string

	echo '</body>'
	echo '</html>'
}

#========================================================================================
# Read current httpd.conf
#----------------------------------------------------------------------------------------
pcp_httpd_read_httpd_conf() {
	# FORMAT - colour|text|html
	local FORMAT=$1

	if [ -f $HTTPD_CONF ]; then
		pcp_message INFO "Reading from $HTTPD_CONF..." "$FORMAT"
		unset HTTPD_HOME HTTPD_USER_PWD HTTPD_USER HTTPD_PWD HTTPD_PWD_HASH HTTPD_USER_ACTIVE
		MAINTAINED="user"

		while read i; do
			case "$i" in
				\#\ Maintained\ by\ piCorePlayer)
					MAINTAINED="pCP"
					MBP="selected"
				;;
				\#\ Maintained\ by\ user)
					MAINTAINED="user"
					MBU="selected"
				;;
				*:*)
					case "$i" in
						H:*)
							HTTPD_HOME=${i#*:}
						;;
						/cgi-bin:*)
							HTTPD_USER_PWD=${i#*:}
							HTTPD_USER=${HTTPD_USER_PWD%:*}
							HTTPD_PWD_HASH=${HTTPD_USER_PWD#*:}
							HTTPD_USER_ENABLED="yes"
						;;
						\#/cgi-bin:*)
							HTTPD_USER_PWD=${i#*:}
							HTTPD_USER=${HTTPD_USER_PWD%:*}
							HTTPD_PWD_HASH=${HTTPD_USER_PWD#*:}
							HTTPD_USER_ENABLED="no"
						;;
					esac
				;;
			esac
		done < $HTTPD_CONF
	fi
}

#========================================================================================
# Write httpd.conf
#----------------------------------------------------------------------------------------
pcp_httpd_write_httpd_conf() {
	# FORMAT - colour|text|html
	local FORMAT=$1

	sudo echo '# Maintained by piCorePlayer'                   > $HTTPD_CONF
	sudo echo 'H:'${HTTPD_HOME:-/home/tc/www}                 >> $HTTPD_CONF
	if [ "$HTTPD_USER_ENABLED" = "yes" ]; then
		sudo echo "/cgi-bin:${HTTPD_USER}:${HTTPD_PWD_HASH}"  >> $HTTPD_CONF
	else
		sudo echo "#/cgi-bin:${HTTPD_USER}:${HTTPD_PWD_HASH}" >> $HTTPD_CONF
	fi

	sudo chown root:root $HTTPD_CONF
	sudo chmod u=rw,go=r $HTTPD_CONF
}

pcp_httpd_user_password() {
	local ENABLE=$1

	[ "$ENABLE" = "enable" ] && sed -i "s/\#\/cgi-bin:/\/cgi-bin:/g" $HTTPD_CONF
	[ "$ENABLE" = "disable" ] && sed -i "s/^\/cgi-bin:/\#\/cgi-bin:/g" $HTTPD_CONF
}

#========================================================================================
# Action
#----------------------------------------------------------------------------------------
[ $DEBUG -eq 1 ] && pcp_table_top "Action"

case "$ACTION" in
	Save)
		[ $DEBUG -eq 1 ] && pcp_message INFO "Saving..." "html"
		pcp_save_httpd_conf
		HTTPD_PARAM=restart
	;;
	Restart)
		HTTPD_PARAM=restart
	;;
	Start)
		pcp_httpd_start
	;;
	Stop)
		pcp_httpd_stop
	;;
	Status)
		HTTPD_PARAM=status
	;;
	Defaults)
		HTTPD_USER="admin"
		HTTPD_PWD="admin"
		pcp_httpd_write_httpd_conf
	;;
	Enable)
		pcp_httpd_user_password enable
	;;
	Disable)
		pcp_httpd_user_password disable
	;;
	*)
		[ $DEBUG -eq 1 ] && pcp_message INFO "Initial..." "html"
		ACTION="Initial"
		pcp_httpd_read_httpd_conf "html"
	;;
esac

[ $DEBUG -eq 1 ] && pcp_table_end

[ "$ACTION" = "Initial" ] && [ "$MAINTAINED" = "user" ] && pcp_httpd_warning_message

#========================================================================================
# Debug information.
#----------------------------------------------------------------------------------------
if [ $DEBUG -eq 1 ]; then
	pcp_table_top "[ DEBUG ] Information"
	pcp_debug_variables "html" DEBUG ACTION MAINTAINED MBP MBU HTTPD_CONF HTTPD_HOME\
		HTTPD_USER_PWD HTTPD_USER HTTPD_PWD HTTPD_PWD_HASH HTTPD_USER_ENABLED\
		RANDOM_SALT HTTPD_PARAM
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
echo '                  >*'
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
#------------------------------------User/password enbled--------------------------------
pcp_incr_id
pcp_toggle_row_shade

case "$HTTPD_USER_ENABLED" in
	yes) HUEyes="checked" ;;
	no) HUEno="checked" ;;
esac

echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COL1'">'
echo '                  <p>User/password</p>'
echo '                </td>'
echo '                <td class="'$COL2'">'
echo '                  <input class="small1" type="radio" name="HTTPD_USER_ENABLED" value="yes" '$HUEyes'>Enabled&nbsp;&nbsp;&nbsp;'
echo '                  <input class="small1" type="radio" name="HTTPD_USER_ENABLED" value="no" '$HUEno'>Disabled'
echo '                </td>'
echo '                <td>'
echo '                  <p>Enable User/password for httpd&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>Accessing the web GUI will require a username and password.</p>'
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
	echo '                         name="HTTPD_USER"'
	echo '                         value="'$HTTPD_USER'"'
	echo '                         required'
	echo '                         title="Invalid characters: $ &amp; ` / &quot;"'
	echo '                         pattern="[^$&`/\x22]+"'
	echo '                  >*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>httpd user&nbsp;&nbsp;'
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
	echo '                         name="HTTPD_PWD"'
	echo '                         value="'$HTTPD_PWD'"'
	echo '                         required'
#	echo '                         title="Invalid characters: $ &amp; ` / &quot;"'
#	echo '                         pattern="[^$&`/\x22]+"'
	echo '                  >*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>httpd password&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;admin&gt;</p>'
	echo '                    <p>Define password.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
fi
#---------------------------------------www password hash--------------------------------
if ! [ "$MAINTAINED" = "user" ] && [ $DEBUG -eq 1 ]; then
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                  <p>Password hash</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="HTTPD_PWD_HASH"'
	echo '                         value="'$HTTPD_PWD_HASH'"'
	echo '                         maxlength="34"'
	echo '                         disabled'
	echo '                  >'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>httpd password hash&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Auto-generated password hash.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
fi
#--------------------------------------Buttons-------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="ACTION" value="Save">'
echo '                  <input type="submit" name="ACTION" value="Defaults">'
#echo '                  <input type="hidden" name="HTTPD_PWD" value="'$HTTPD_PWD'">'
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
if [ $MODE -ge $MODE_DEVELOPER ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>DEVELOPER options</legend>'
	echo '          <form name="developer" action="'$0'" method="get">'
	echo '            <table class="bggrey percent100">'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="ACTION" value="Restart">'
	echo '                  <input type="submit" name="ACTION" value="Start">'
	echo '                  <input type="submit" name="ACTION" value="Stop">'
	echo '                  <input type="submit" name="ACTION" value="Status">'
	echo '                  <input type="submit" name="ACTION" value="Enable">'
	echo '                  <input type="submit" name="ACTION" value="Disable">'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------
	echo '            </table>'
	echo '          </form>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi
#----------------------------------------------------------------------------------------

pcp_httpd_html_end
[ x"$HTTPD_PARAM" = x"" ] || pcp_httpd $HTTPD_PARAM

exit