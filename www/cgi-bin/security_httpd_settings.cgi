#!/bin/sh

# Version: 7.0.0 2020-05-27

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"
#========================================================================================
# Functions
#----------------------------------------------------------------------------------------
pcp_save_httpd_conf() {
	pcp_save_to_config
	pcp_httpd_generate_passwd_hash
	pcp_httpd_write_httpd_conf
	pcp_backup
#	pcp_httpd_read_httpd_conf
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
	echo '  <div class="warning">'
	echo '    <div>'
	echo '      <p><b>Warning:</b></p>'
	echo '      <ul>'
	echo '        <li>'$HTTPD_CONF' is marked as \"Maintained by user\".</li>'
	echo '        <li>Configuration file will be not be editted by piCorePlayer.</li>'
	echo '        <li>Use manual methods to maintain.</li>'
	echo '      </ul>'
	echo '    </div>'
	echo '  </div>'
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
case "$ACTION" in
	Save)
		[ $DEBUG -eq 1 ] && pcp_message INFO "Saving..." "text"
		pcp_save_httpd_conf
		pcp_httpd_read_httpd_conf "text"
		HTTPD_PARAM=restart
	;;
	Defaults)
		[ $DEBUG -eq 1 ] && pcp_message INFO "Writing default $HTTPD_CONF..." "text"
		pcp_httpd_write_default_httpd_conf
		pcp_httpd_read_httpd_conf "text"
		WWW_PORT="80"
		pcp_save_to_config
		HTTPD_PARAM=restart
	;;
	SavePort)
		[ $DEBUG -eq 1 ] && pcp_message INFO "Saving port ($WWW_PORT)..." "text"
		pcp_save_to_config
		pcp_httpd_read_httpd_conf "text"
		HTTPD_PARAM=restart
	;;
	*)
		[ $DEBUG -eq 1 ] && pcp_message INFO "Initial..." "text"
		ACTION="Initial"
		pcp_httpd_read_httpd_conf "text"
	;;
esac

[ "$ACTION" = "Initial" ] && [ "$MAINTAINED" = "user" ] && pcp_httpd_warning_message

#========================================================================================
# Debug information.
#----------------------------------------------------------------------------------------
pcp_debug_variables "html" DEBUG ACTION MAINTAINED MBP MBU HTTPD_CONF HTTPD_HOME \
	HTTPD_USER_PWD HTTPD_USER HTTPD_PWD HTTPD_PWD_HASH HTTPD_USER_ENABLED \
	RANDOM_SALT HTTPD_PARAM WWW_PORT

[ $DEBUG -eq 1 ] && pcp_textarea "none" "cat ${HTTPD_CONF}" 70
#----------------------------------------------------------------------------------------

#========================================================================================
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "HTTPD server settings"
echo '  <form name="http_server" action="'$0'" method="get">'
#------------------------------------User/password enabled-------------------------------
case "$HTTPD_USER_ENABLED" in
	yes) HUEyes="checked" ;;
	no) HUEno="checked" ;;
esac

pcp_incr_id
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>User/password</p>'
echo '      </div>'
echo '      <div class="'$COLUMN3_2'">'
echo '        <input id="rad1" type="radio" name="HTTPD_USER_ENABLED" value="yes" '$HUEyes'>'
echo '        <label for="rad1">Enabled&nbsp;&nbsp;</label>'
echo '        <input id="rad2" type="radio" name="HTTPD_USER_ENABLED" value="no" '$HUEno'>'
echo '        <label for="rad2">Disabled</label>'
echo '      </div>'
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Enable user/password for httpd&nbsp;&nbsp;'
pcp_helpbadge
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>By default, user/password is disabled.</p>'
echo '          <p>If user/password is enabled, accessing the web GUI will require a username and password.</p>'
echo '          <p>The httpd username and password is maintained independent from the piCore Linux usernames/passwords.</p>'
echo '          <p>Passwords are not stored as plain text. Passwords are converted to a salted, md5 encrypted hash.</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#------------------------------------------httpd user------------------------------------
if ! [ "$MAINTAINED" = "user" ]; then
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>User*</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="HTTPD_USER"'
	echo '               value="'$HTTPD_USER'"'
	echo '               required'
	echo '               title="Invalid characters: $ &amp; ` / &quot;"'
	echo '               pattern="[^$&`/\x22]+"'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Set httpd user&nbsp;&nbsp;'
pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>If user/password is enabled, the default user is admin.</p>'
	echo '          <p>This will allow a unique user access to the web GUI.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
fi
#---------------------------------------httpd password-----------------------------------
if ! [ "$MAINTAINED" = "user" ]; then
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Password*</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="password"'
	echo '               name="HTTPD_PWD"'
	echo '               value="'$HTTPD_PWD'"'
	echo '               required'
	echo '               title="Invalid characters: $ &amp; ` / &quot;"'
	echo '               pattern="[^$&`/\x22]+"'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>Set httpd password&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>If user/password is enabled, the default password is admin.</p>'
	echo '          <p>This will set the password of the unique web GUI user.</p>'
	echo '          <p>Passwords are not stored as plain text. Passwords are converted to a salted, md5 encrypted hash.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
fi
#-------------------------------------httpd password hash--------------------------------
if ! [ "$MAINTAINED" = "user" ] && [ $DEBUG -eq 1 ]; then
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <p>Password hash</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_2'">'
	echo '        <input class="form-control form-control-sm"'
	echo '               type="text"'
	echo '               name="HTTPD_PWD_HASH"'
	echo '               value="'$HTTPD_PWD_HASH'"'
	echo '               maxlength="34"'
	echo '               disabled'
	echo '        >'
	echo '      </div>'
	echo '      <div class="'$COLUMN3_3'">'
	echo '        <p>httpd password hash&nbsp;&nbsp;'
	pcp_helpbadge
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This is the auto-generated password hash.</p>'
	echo '          <p>Passwords are converted to a salted, md5 encrypted hash.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
fi
#--------------------------------------Buttons-------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Save">'
echo '      </div>'
echo '      <div class="'$COLUMN3_1'">'
echo '        <input class="'$BUTTON'" type="submit" name="ACTION" value="Defaults" form="http_port">'
echo '        <input type="hidden" name="CALLED_BY" value="httpd settings">'
echo '      </div>'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>* required field</p>'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '  </form>'
pcp_border_end
#----------------------------------------------------------------------------------------

#========================================================================================
pcp_border_begin
pcp_heading5 "HTTPD port"
echo '  <form id="http_port" name="http_port" action="'$0'" method="get">'
#---------------------------------------httpd port---------------------------------------
pcp_incr_id
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>Port*</p>'
echo '      </div>'
echo '      <div class="'$COLUMN3_2'">'
echo '        <input class="form-control form-control-sm"'
echo '               type="number"'
echo '               name="WWW_PORT"'
echo '               value="'$WWW_PORT'"'
echo '               required'
echo '        >'
echo '      </div>'
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Set httpd port&nbsp;&nbsp;'
pcp_helpbadge
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>The default httpd port is port 80.</p>'
echo '          <p>If the port is changed from the default value, the port number will be required to be added to the web GUI URL.</p>'
echo '          <p>Eg. http//192.168.1.42:8080</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#--------------------------------------Buttons-------------------------------------------
echo '     <div class="row mx-1">'
echo '       <div class="'$COLUMN3_1'">'
echo '         <button class="'$BUTTON'" type="submit" name="ACTION" value="SavePort">Save'
echo '         <input type="hidden" name="CALLED_BY" value="httpd settings">'
echo '       </div>'
echo '       <div class="'$COLUMN3_2'">'
echo '         <p>* required field</p>'
echo '       </div>'
echo '     </div>'
#----------------------------------------------------------------------------------------
echo '  </form>'
pcp_border_end
#----------------------------------------------------------------------------------------

pcp_httpd_html_end
[ x"$HTTPD_PARAM" = x"" ] || pcp_httpd $HTTPD_PARAM &
