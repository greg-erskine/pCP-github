#!/bin/sh

# Version: 5.1.0 2019-06-22

#========================================================================================
# Change tc password
#----------------------------------------------------------------------------------------
USERNAME=$(pcp_tc_user)
DEFAULTPASSWD="piCore"

#========================================================================================
# Is the username valid on this RPi?
#----------------------------------------------------------------------------------------
pcp_security_is_user_valid() {
	id -u "$USERNAME" > /dev/null
	if [ $? -eq 0 ]; then
		pcp_message OK "User $USERNAME is valid." "html"
	else
		pcp_message ERROR "User $USERNAME is invalid." "html"
	fi
}

pcp_security_check_password() {
	pcp_security_get_currentpasswdhash

	if [ "$CURRENTPASSWDHASH" = "$(pcp_security_passwd_hash "$CURRENTPASSWORD")" ]; then
		echo 0
	else
		echo 1
	fi
}

#========================================================================================
#    -m,--md5                Encrypt using md5, not des
#    -c,--crypt-method ALG   des,md5,sha256/512 (default md5)
#----------------------------------------------------------------------------------------
pcp_security_change_password() {
	pcp_table_top "Changing password"

	if [ $(pcp_security_check_password) -eq 0 ]; then
		pcp_message OK "Current password correct." "html"
		if [ "$NEWPASSWORD" = "$CONFIRMPASSWORD" ]; then
			if [ $DEBUG -eq 1 ]; then
				pcp_message DEBUG "NEWPASSWORD: $NEWPASSWORD" "html"
				pcp_message DEBUG "CONFIRMPASSWORD: $CONFIRMPASSWORD" "html"
				pcp_message OK "New passwords match." "html"
			fi
#			echo "${USERNAME}:${NEWPASSWORD}" | sudo /usr/sbin/chpasswd --crypt-method sha256
			echo "${USERNAME}:${NEWPASSWORD}" | sudo /usr/sbin/chpasswd -m
			pcp_backup
		else
			pcp_message ERROR "New passwords not confirmed. Try again." "html"
		fi
	else
		pcp_message ERROR "Current password incorrect." "html"
		pcp_message ERROR "Password not changed." "html"
	fi

	pcp_table_end
	pcp_remove_query_string
}

#========================================================================================
# $ cat /etc/shadow | grep tc
# tc:$1$ZLWmhSQb$R9fyDPYFS1Dvc/1tyoRLD0:16435:0:99999:7:::
#    ----------password-hash-----------
#
#    $1$ZLWmhSQb$R9fyDPYFS1Dvc/1tyoRLD0
#  ALGO|--SALT--|------PASSWORD-------|
#
# $ openssl passwd -1 -salt ZLWmhSQb piCore  <==== GE replace "openssl passwd" with "mkpasswd" + sha256/512
# $1$ZLWmhSQb$R9fyDPYFS1Dvc/1tyoRLD0
#----------------------------------------------------------------------------------------
pcp_security_passwd_hash() {
	PASSWD="$1"
	pcp_security_get_currentpasswdhash
	openssl passwd -$ALGO -salt "$SALT" "$PASSWD"
}

pcp_security_get_currentpasswdhash() {
	CURRENTPASSWDHASH=$(grep -w "$USERNAME" /etc/shadow | cut -d: -f2)
	ALGO=$(echo "$CURRENTPASSWDHASH" | cut -d$ -f2)
	SALT=$(echo "$CURRENTPASSWDHASH" | cut -d$ -f3)
}

case $ACTION in
	SavePW)
		pcp_security_change_password
		pcp_security_get_currentpasswdhash
	;;
	*)
		pcp_security_get_currentpasswdhash
	;;
esac

DEFAULTPASSWDHASH=$(pcp_security_passwd_hash "$DEFAULTPASSWD")

#--------------------------------------Debug---------------------------------------------
if [ $DEBUG -eq 1 ]; then
	pcp_table_top "Debug Information"
	pcp_debug_variables "html" USERNAME DEFAULTPASSWD DEFAULTPASSWDHASH \
		CURRENTPASSWDHASH ALGO SALT
	pcp_security_is_user_valid
	pcp_table_end
fi
#----------------------------------------------------------------------------------------

COLUMN1="column200"
COLUMN2="column210"
#========================================================================================
# tc password main
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Change '$USERNAME' password</legend>'
echo '          <form name="password" action="./security.cgi" method="get">'
echo '            <table class="bggrey percent100">'
#------------------------------------Warning---------------------------------------------
if [ "$CURRENTPASSWDHASH" = "$(pcp_security_passwd_hash "$DEFAULTPASSWD")" ]; then
	echo '              <tr class="warning">'
	echo '                <td>'
	echo '                  <div style="color:white">'
	echo '                    <p><b>WARNING: </b>Using default '$USERNAME' password.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_table_padding
fi
#--------------------------------Current password----------------------------------------
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">Change password for "'$USERNAME'"</td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <input class="large16"'
echo '                         type="password"'
echo '                         name="CURRENTPASSWORD"'
echo '                         maxlength="26"'
echo '                         title="Invalid characters: $ &amp; ` / &quot;"'
echo '                         pattern="[^$&`/\x22]+"'
echo '                         required'
echo '                  >*'
echo '                </td>'
echo '                <td>'
echo '                  <p>Enter current password.</p>'
echo '                </td>'
echo '              </tr>'
#---------------------------------New password-------------------------------------------
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'"></td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <input class="large16"'
echo '                         type="password"'
echo '                         name="NEWPASSWORD"'
echo '                         title="Invalid characters: $ &amp; ` / &quot;"'
echo '                         pattern="[^$&`/\x22]+"'
echo '                         maxlength="26"'
echo '                         required'
echo '                  >*'
echo '                </td>'
echo '                <td>'
echo '                  <p>Enter new password.</p>'
echo '                </td>'
echo '              </tr>'
#---------------------------------Confirm password---------------------------------------
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'"></td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <input class="large16"'
echo '                         type="password"'
echo '                         name="CONFIRMPASSWORD"'
echo '                         title="Invalid characters: $ &amp; ` / &quot;"'
echo '                         pattern="[^$&`/\x22]+"'
echo '                         maxlength="26"'
echo '                         required'
echo '                  >*'
echo '                </td>'
echo '                <td>'
echo '                  <p>Confirm new password.</p>'
echo '                </td>'
echo '              </tr>'
#-----------------------------------Save button------------------------------------------
pcp_toggle_row_shade
pcp_incr_id
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">'
echo '                  <button type="submit"'
echo '                          name="ACTION"'
echo '                          value="SavePW"'
echo '                          onclick="return(validate());"'
echo '                          >Save'
echo '                  </button>'
echo '                </td>'
echo '                <td colspan="2">'
echo '                  <p>* required field&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>The piCorePlayer default user/password is tc/piCore.</p>'
echo '                    <p>Changing passwords through a script over http is possibly not 100% secure.'
echo '                       If you are concerned, manually set the password using the CLI, a keyboard and monitor.</p>'
echo '                    <p>Passwords are not stored as plain text. Passwords are converted to a salted, md5 encrypted hash.</p>'
echo '                    <p>Complex passwords are better handled directly through the CLI.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </form>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------Script------------------------------------------
echo '<script>'
echo 'function validate() {'
echo '  if ( document.password.NEWPASSWORD.value != document.password.CONFIRMPASSWORD.value ){'
echo '    alert("[ ERROR ] New passwords do NOT match. Try again.");'
echo '    return false;'
echo '  }'
echo '  return true;'
echo '}'
echo '</script>'
#----------------------------------------------------------------------------------------
