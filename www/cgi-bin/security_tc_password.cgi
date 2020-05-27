#!/bin/sh

# Version: 7.0.0 2020-05-28

COLUMN3_1="col-sm-3"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-6"
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
		pcp_message OK "User $USERNAME is valid." "text"
	else
		pcp_message ERROR "User $USERNAME is invalid." "text"
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
	pcp_infobox_begin
	if [ $(pcp_security_check_password) -eq 0 ]; then
		pcp_message OK "Current password entered correctly." "text"
		if [ "$NEWPASSWORD" = "$CONFIRMPASSWORD" ]; then
			if [ $DEBUG -eq 1 ]; then
				pcp_message DEBUG "NEWPASSWORD: $NEWPASSWORD" "text"
				pcp_message DEBUG "CONFIRMPASSWORD: $CONFIRMPASSWORD" "text"
				pcp_message OK "New passwords match." "text"
			fi
#			echo "${USERNAME}:${NEWPASSWORD}" | sudo /usr/sbin/chpasswd --crypt-method sha256
			echo "${USERNAME}:${NEWPASSWORD}" | sudo /usr/sbin/chpasswd -m
			if [ $? -eq 0 ]; then
				pcp_message OK "Password changed." "text"
			else
				pcp_message ERROR "Password not changed." "text"
			fi
			pcp_backup "text"
		else
			pcp_message ERROR "New passwords not confirmed. Try again." "text"
		fi
	else
		pcp_message ERROR "Current password incorrect." "text"
		pcp_message ERROR "Password not changed." "text"
	fi
	pcp_remove_query_string
	pcp_infobox_end
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
	pcp_debug_variables "html" USERNAME DEFAULTPASSWD DEFAULTPASSWDHASH \
		CURRENTPASSWDHASH ALGO SALT
	pcp_security_is_user_valid
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# tc password main
#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "Change $USERNAME password"
echo '  <form name="password" action="./security.cgi" method="get">'
#------------------------------------Warning---------------------------------------------
if [ "$CURRENTPASSWDHASH" = "$(pcp_security_passwd_hash "$DEFAULTPASSWD")" ]; then
	echo '    <div class="alert alert-primary" role="alert">'
	echo '      <p><b>WARNING: </b>Using default '$USERNAME' password.</p>'
	echo '    </div>'
fi
#--------------------------------Current password----------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>Change password for "'$USERNAME'"</p>'
echo '      </div>'
echo '      <div class="'$COLUMN3_2'">'
echo '        <input class="form-control form-control-sm"'
echo '               type="password"'
echo '               name="CURRENTPASSWORD"'
echo '               maxlength="26"'
echo '               title="Invalid characters: $ &amp; ` / &quot;"'
echo '               pattern="[^$&`/\x22]+"'
echo '               required'
echo '        >'
echo '      </div>'
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Enter current password.*</p>'
echo '      </div>'
echo '    </div>'
#---------------------------------New password-------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN3_1'"></div>'
echo '      <div class="'$COLUMN3_2'">'
echo '        <input class="form-control form-control-sm"'
echo '               type="password"'
echo '               name="NEWPASSWORD"'
echo '               title="Invalid characters: $ &amp; ` / &quot;"'
echo '               pattern="[^$&`/\x22]+"'
echo '               maxlength="26"'
echo '               required'
echo '        >'
echo '      </div>'
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Enter new password.*</p>'
echo '      </div>'
echo '    </div>'
#---------------------------------Confirm password---------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN3_1'"></div>'
echo '      <div class="'$COLUMN3_2'">'
echo '        <input class="form-control form-control-sm"'
echo '               type="password"'
echo '               name="CONFIRMPASSWORD"'
echo '               title="Invalid characters: $ &amp; ` / &quot;"'
echo '               pattern="[^$&`/\x22]+"'
echo '               maxlength="26"'
echo '               required'
echo '        >'
echo '      </div>'
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Confirm new password.*</p>'
echo '      </div>'
echo '    </div>'
#-----------------------------------Save button------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="col-2">'
echo '        <button class="'$BUTTON'"'
echo '                type="submit"'
echo '                name="ACTION"'
echo '                value="SavePW"'
echo '                onclick="return(validate());"'
echo '                >Save'
echo '        </button>'
echo '      </div>'
echo '      <div class="col-4"></div>'
pcp_incr_id
echo '      <div class="col-6">'
echo '        <p>* required field&nbsp;&nbsp;'
pcp_helpbadge
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>The piCorePlayer default user/password is tc/piCore.</p>'
echo '          <p>Changing passwords through a script over http is possibly not 100% secure.'
echo '             If you are concerned, manually set the password using the CLI, a keyboard and monitor.</p>'
echo '          <p>Passwords are not stored as plain text. Passwords are converted to a salted, md5 encrypted hash.</p>'
echo '          <p>Complex passwords are better handled directly through the CLI.</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '  </form>'
pcp_border_end

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
