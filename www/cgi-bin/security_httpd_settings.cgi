#!/bin/sh

# Version: 6.0.0 2019-08-31

#========================================================================================
# Functions
#----------------------------------------------------------------------------------------
pcp_save_httpd_conf() {
	[ $DEBUG -eq 0 ] && pcp_table_top "Saving..."
	pcp_save_to_config
	pcp_httpd_generate_passwd_hash
	pcp_httpd_write_httpd_conf
	pcp_backup
#	pcp_httpd_read_httpd_conf
	[ $DEBUG -eq 0 ] && pcp_table_end
}

#========================================================================================
# httpd functions - NOTE: GE remove unused options.
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
# Password functions  <==== GE replace "openssl passwd" with "mkpasswd" + sha256/512
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
	echo '      <p><b>Warning:</b></p>'
	echo '      <ul>'
	echo '        <li>'$HTTPD_CONF' is marked as \"Maintained by user\".</li>'
	echo '        <li>Configuration file will be not be editted by piCorePlayer.</li>'
	echo '        <li>Use manual methods to maintain.</li>'
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
	pcp_remove_query_string

	echo '</body>'
	echo '</html>'
}

#========================================================================================
# Read current httpd.conf
#----------------------------------------------------------------------------------------
pcp_httpd_read_httpd_conf() {
	# FORMAT - colour|text|html
	FORMAT=$1

	if [ -f $HTTPD_CONF ]; then
		[ $DEBUG -eq 1 ] && pcp_message INFO "Reading from $HTTPD_CONF..." "$FORMAT"
		unset HTTPD_HOME HTTPD_USER_PWD HTTPD_USER HTTPD_PWD_HASH HTTPD_USER_ACTIVE
		MAINTAINED="user"

		while read i
		do
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
# Write httpd.conf - NOTE: GE remove /home/tc/www
#----------------------------------------------------------------------------------------
pcp_httpd_write_httpd_conf() {
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

pcp_httpd_write_default_httpd_conf() {
	sudo echo '# Maintained by piCorePlayer'  > $HTTPD_CONF
	sudo echo 'H:'${WWWROOT}                 >> $HTTPD_CONF
	sudo echo "#/cgi-bin:admin:admin"        >> $HTTPD_CONF

	sudo chown root:root $HTTPD_CONF
	sudo chmod u=rw,go=r $HTTPD_CONF
}

pcp_httpd_user_password() {
	ENABLE=$1

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
		pcp_httpd_read_httpd_conf "html"
		HTTPD_PARAM=restart
	;;
	Defaults)
		[ $DEBUG -eq 1 ] && pcp_message INFO "Writing default $HTTPD_CONF..." "html"
		pcp_httpd_write_default_httpd_conf
		pcp_httpd_read_httpd_conf "html"
		WWW_PORT="80"
		pcp_save_to_config
		HTTPD_PARAM=restart
	;;
	SavePort)
		[ $DEBUG -eq 1 ] && pcp_message INFO "Saving port ($WWW_PORT)..." "html"
		pcp_save_to_config
		pcp_httpd_read_httpd_conf "html"
		HTTPD_PARAM=restart
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
	pcp_table_top "Debug Information"
	pcp_debug_variables "html" DEBUG ACTION MAINTAINED MBP MBU HTTPD_CONF HTTPD_HOME \
		HTTPD_USER_PWD HTTPD_USER HTTPD_PWD HTTPD_PWD_HASH HTTPD_USER_ENABLED \
		RANDOM_SALT HTTPD_PARAM WWW_PORT
	pcp_table_end

	pcp_table_top "$HTTPD_CONF"
	pcp_textarea_inform "none" "cat ${HTTPD_CONF}" 70
	pcp_table_end
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# Start of table
#----------------------------------------------------------------------------------------
COL1="column150"
COL2="column220"
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="http_server" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>HTTPD server settings</legend>'
echo '            <table class="bggrey percent100">'
#------------------------------------User/password enabled-------------------------------
case "$HTTPD_USER_ENABLED" in
	yes) HUEyes="checked" ;;
	no) HUEno="checked" ;;
esac

pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COL1'">'
echo '                  <p>User/password</p>'
echo '                </td>'
echo '                <td class="'$COL2'">'
echo '                  <input id="rad1" type="radio" name="HTTPD_USER_ENABLED" value="yes" '$HUEyes'>'
echo '                  <label for="rad1">Enabled&nbsp;&nbsp;</label>'
echo '                  <input id="rad2" type="radio" name="HTTPD_USER_ENABLED" value="no" '$HUEno'>'
echo '                  <label for="rad2">Disabled</label>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Enable user/password for httpd&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>By default, user/password is disabled.</p>'
echo '                    <p>If user/password is enabled, accessing the web GUI will require a username and password.</p>'
echo '                    <p>The httpd username and password is maintained independent from the piCore Linux usernames/passwords.</p>'
echo '                    <p>Passwords are not stored as plain text. Passwords are converted to a salted, md5 encrypted hash.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#------------------------------------------httpd user------------------------------------
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
	echo '                  <p>Set httpd user&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>If user/password is enabled, the default user is admin.</p>'
	echo '                    <p>This will allow a unique user access to the web GUI.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
fi
#---------------------------------------httpd password-----------------------------------
if ! [ "$MAINTAINED" = "user" ]; then
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1'">'
	echo '                  <p>Password</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="password"'
	echo '                         name="HTTPD_PWD"'
	echo '                         value="'$HTTPD_PWD'"'
	echo '                         required'
	echo '                         title="Invalid characters: $ &amp; ` / &quot;"'
	echo '                         pattern="[^$&`/\x22]+"'
	echo '                  >*'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set httpd password&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>If user/password is enabled, the default password is admin.</p>'
	echo '                    <p>This will set the password of the unique web GUI user.</p>'
	echo '                    <p>Passwords are not stored as plain text. Passwords are converted to a salted, md5 encrypted hash.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
fi
#-------------------------------------httpd password hash--------------------------------
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
	echo '                    <p>This is the auto-generated password hash.</p>'
	echo '                    <p>Passwords are converted to a salted, md5 encrypted hash.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
fi
#--------------------------------------Buttons-------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COL1'">'
echo '                  <input type="submit" name="ACTION" value="Save">'
echo '                </td>'
echo '                <td class="'$COL2'">'
echo '                  <input type="submit" name="ACTION" value="Defaults" form="http_port">'
echo '                  <input type="hidden" name="CALLED_BY" value="httpd settings">'
echo '                </td>'
echo '                <td>'
echo '                  <p>* required field</p>'
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
# Start of httpd port table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form id="http_port" name="http_port" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>HTTPD port</legend>'
echo '            <table class="bggrey percent100">'
#---------------------------------------httpd port---------------------------------------
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
echo '                  <p>Set httpd port&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>The default httpd port is port 80.</p>'
echo '                    <p>If the port is changed from the default value, the port number will be required to be added to the web GUI URL.</p>'
echo '                    <p>Eg. http//192.168.1.42:8080</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#--------------------------------------Buttons-------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COL1'">'
echo '                  <button type="submit" name="ACTION" value="SavePort">Save'
echo '                  <input type="hidden" name="CALLED_BY" value="httpd settings">'
echo '                </td>'
echo '                <td class="'$COL2'">'
echo '                </td>'
echo '                <td>'
echo '                  <p>* required field</p>'
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

pcp_httpd_html_end
[ x"$HTTPD_PARAM" = x"" ] || pcp_httpd $HTTPD_PARAM &
