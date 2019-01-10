#!/bin/sh

# Version: 4.2.0 2019-01-11

# Title: Security
# Description: Gathering pieces of code to increase security

. pcp-functions

DEBUG=1 #<============= GE

pcp_html_head "Security" "GE"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#========================================================================================
# Change Password Section
#----------------------------------------------------------------------------------------
DEFAULTPASSWD="piCore"
USERNAME=$(pcp_tc_user)
[ $DEBUG -eq 1 ] && pcp_security_valid_user

pcp_security_valid_user() {
	id -u $USERNAME > /dev/null
	if [ $? -eq 0 ]; then
		pcp_message OK "User $USERNAME is valid." "html"
	else
		pcp_message ERROR "User $USERNAME is valid." "html"
	fi
}

pcp_security_check_password() {
	pcp_security_get_currentpasswdhash

	if [ "$CURRENTPASSWDHASH" = "$(pcp_security_passwd_hash "$CURRENTPASSWORD")" ]; then
		pcp_message OK "Correct password" "html"
	else
		pcp_message ERROR "Incorrect password" "html"
	fi
}

pcp_security_change_password() {
	pcp_table_top "Changing password"
	pcp_security_check_password
	
	if [ "$NEWPASSWORD" = "$CONFIRMPASSWORD" ]; then
		if [ $DEBUG -eq 1 ]; then
			pcp_message INFO "NEWPASSWORD: $NEWPASSWORD" "html"
			pcp_message INFO "CONFIRMPASSWORD: $CONFIRMPASSWORD" "html"
			pcp_message OK "Passwords match." "html"
		fi
		echo "${USERNAME}:${NEWPASSWORD}" | sudo /usr/sbin/chpasswd -m
		pcp_backup
	else
		pcp_message ERROR "Password not confirmed. Try again." "html"
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
# $ openssl passwd -1 -salt ZLWmhSQb piCore
# $1$ZLWmhSQb$R9fyDPYFS1Dvc/1tyoRLD0
#----------------------------------------------------------------------------------------
pcp_security_passwd_hash() {
	local PASSWD=$1
	pcp_security_get_currentpasswdhash
	openssl passwd -1 -salt $SALT $PASSWD
}

pcp_security_get_currentpasswdhash() {
	CURRENTPASSWDHASH=$(grep -w "$USERNAME" /etc/shadow | cut -d: -f2)
	SALT=$(echo $CURRENTPASSWDHASH | cut -d$ -f3)
}

#pcp_security_get_currentpasswdhash
#DEFAULTPASSWDHASH=$(pcp_security_passwd_hash "$DEFAULTPASSWD")

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

if [ $DEBUG -eq 1 ]; then
	pcp_table_top "Debug Information"
	pcp_debug_variables "html" USERNAME DEFAULTPASSWD CURRENTPASSWDHASH SALT DEFAULTPASSWDHASH
	pcp_table_end
fi

echo '<script>'
echo 'function validate() {'
echo '  if ( document.password.NEWPASSWORD.value != document.password.CONFIRMPASSWORD.value ){'
echo '    alert("Passwords do NOT match!");'
echo '    return false;'
echo '  }'
echo '  return true;'
echo '}'
echo '</script>'

COLUMN1="column200"
COLUMN2="column210"
#========================================================================================
# Main password HTML
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Password</legend>'
#----------------------------------------------------------------------------------------

#-----------------------------------Password---------------------------------------------
# Note: changing passwords through a script over http is not very secure.
#----------------------------------------------------------------------------------------
echo '          <form name="password" action="'$0'" method="get">'
echo '            <table class="bggrey percent100">'
pcp_start_row_shade
if [ "$CURRENTPASSWDHASH" = "$(pcp_security_passwd_hash "$DEFAULTPASSWD")" ]; then
	echo '              <tr class="warning">'
	echo '                <td>'
	echo '                  <div style="color:white">'
	echo '                    <p><b>WARNING: </b>Using default password.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_table_padding
fi
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">Change password for "'$(pcp_tc_user)'"</td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <input class="large16"'
echo '                         type="password"'
echo '                         name="CURRENTPASSWORD"'
echo '                         maxlength="26"'
echo '                  >*'
echo '                </td>'
echo '                <td>'
echo '                  <p>Enter current password.</p>'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'"></td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <input class="large16"'
echo '                         type="password"'
echo '                         name="NEWPASSWORD"'
echo '                         maxlength="26"'
echo '                  >*'
echo '                </td>'
echo '                <td>'
echo '                  <p>Enter new password.</p>'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'"></td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <input class="large16"'
echo '                         type="password"'
echo '                         name="CONFIRMPASSWORD"'
echo '                         maxlength="26"'
echo '                  >*'
echo '                </td>'
echo '                <td>'
echo '                  <p>Retype new password.</p>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
pcp_incr_id
echo '              <tr class="'$ROWSHADE'" >'
echo '                <td class="'$COLUMN1'">'
echo '                  <button type="submit"'
echo '                          name="ACTION"'
echo '                          value="SavePW"'
echo '                          onclick="return(validate());"'
echo '                          >Save'
echo '                  </button>'
echo '                </td>'
echo '                <td colspan="2">'
echo '                  <p><a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a></p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p><b>Default:</b> piCore</p>'
echo '                    <p class="error"><b>Warning: </b>Changing passwords through a script over http is not very secure.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </form>'
#----------------------------------------------------------------------------------------
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
# SSH
#----------------------------------------------------------------------------------------
# Start openssh if file ssh found. $SSH set in NEWCONFIGFOUND process.
#----------------------------------------------------------------------------------------
pcp_ssh_start() {
	/usr/local/etc/init.d/openssh start >/dev/null 2>&1
}

pcp_ssh_stop() {
	/usr/local/etc/init.d/openssh stop >/dev/null 2>&1
}

pcp_ssh_status() {
	sudo /usr/local/etc/init.d/openssh status
	RESULT=$?
}

BOOTDEVLIST=$(blkid -o device | grep -E 'sd[a-z]1|mmcblk0p1' | awk -F '/dev/' '{print $2}')

COLUMN1="column150"
COLUMN2="column120"
COLUMN3="column210"
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>ssh</legend>'
echo '          <form name="ssh" action="'$0'" method="get">'
echo '            <table class="bggrey percent100">'
echo '              <tr>'
echo '                <td class="'$COLUMN1'">'
echo '                  <p>'$(pcp_ssh_status)'</p>'
echo '                </td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <p>Error result: '$RESULT'</p>'
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

#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Web GUI</legend>'
echo '          <table class="bggrey percent100">'
echo '            <tr>'
echo '              <td>'

echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Quiet boot</legend>'
echo '          <table class="bggrey percent100">'
echo '            <tr>'
echo '              <td>'

echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
exit
