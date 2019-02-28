#!/bin/sh

# Version: 5.0.0 2019-03-01

# Title: Security
# Description: Security related configuration

. pcp-functions

pcp_html_head "Security" "GE"

pcp_banner
pcp_running_script
pcp_httpd_query_string

unset REBOOT_REQUIRED

#========================================================================================
# Web GUI
#----------------------------------------------------------------------------------------
STOP_HTTPD_SH="/tmp/stop_httpd.sh"

case $ACTION in
	Save\ GUI)
		pcp_save_to_config
		pcp_backup >/dev/null 2>&1
		REBOOT_REQUIRED=TRUE
	;;
	Abort\ GUI)
		sudo killall $STOP_HTTPD_SH
		REBOOT_REQUIRED=TRUE
	;;
	*)
		pcp_security_ssh
	;;
esac

COLUMN1="column210"
COLUMN2="column210"
#---------------------------------------web GUI------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form id="GUI_Disable" name="GUI_Disable" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Disable web GUI</legend>'
echo '            <table class="bggrey percent100">'
pcp_start_row_shade
pcp_incr_id
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">'
echo '                  <p>Disable web GUI</p>'
echo '                </td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <input class="large6"'
echo '                         type="text"'
echo '                         name="GUI_DISABLE"'
echo '                         value="'$GUI_DISABLE'"'
echo '                         pattern="\d*"'
echo '                         title="Use numbers."'
echo '                  > seconds'
echo '                </td>'
echo '                <td>'
echo '                  <p>Set disable web GUI time&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>&lt;xx seconds&gt;</p>'
echo '                    <p><b>Default: </b>0 = enable web GUI</p>'
echo '                    <p>1 = never start web GUI</p>'
echo '                    <p>&gt;20 = minimum value</p>'
echo '                    <p>This sets the time, in seconds, between piCorePlayer booting and the web GUI being disabled.</p>'
echo '                    <p>This increases security because it gives limited access window to the web GUI.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <button type="submit" name="ACTION" value="Save GUI">Save</button>'
                        [ -f $STOP_HTTPD_SH ] &&
echo '                  <button type="submit" name="ACTION" value="Abort GUI">Abort</button>'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
# SSH section
#----------------------------------------------------------------------------------------
pcp_ssh_status() {
	sudo /usr/local/etc/init.d/openssh status
	RESULT=$?
}

#------------------------------------------------------------------------------------
# Look for ssh file on boot partition. Only start sshd if file found.
#------------------------------------------------------------------------------------
BOOTDEVLIST=$(blkid -o device | grep -E 'sd[a-z]1|mmcblk0p1' | awk -F '/dev/' '{print $2}')

pcp_security_ssh() {
	[ $DEBUG -eq 1 ] && pcp_table_top "Debug Information"
	SSH_FOUND=0

	for DISK in $BOOTDEVLIST; do
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "Checking for ssh file on $DISK..." "html"
		# Check if $DISK is mounted, otherwise mount it.
		if mount | grep ${DISK} >/dev/null 2>&1; then
			eval ${DISK}WASMNT=1
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "/dev/${DISK} mounted." "html"
		else
			eval ${DISK}WASMNT=0
			[ -d /mnt/$DISK ] || mkdir -p /mnt/$DISK
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "Mounting /dev/${DISK}." "html"
			mount /dev/$DISK >/dev/null 2>&1
		fi

		[ $1 = "enable" ] && touch /mnt/${DISK}/ssh
		[ $1 = "disable" ] && rm -f /mnt/${DISK}/ssh

		if [ -f /mnt/${DISK}/ssh ]; then
			SSH_FOUND=$(($SSH_FOUND + 1))
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "SSH found on ${DISK}." "html"
		else
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "SSH NOT found on ${DISK}." "html"
		fi

		if [ $(eval echo \${${DISK}WASMNT}) -eq 0 ]; then
			umount /mnt/$DISK
			[ $DEBUG -eq 1 ] && pcp_message DEBUG "/mnt/${DISK} unmounted." "html"
		fi
	done

	[ $DEBUG -eq 1 ] && pcp_table_end
}

case $ACTION in
	Enable\ SSH)
		pcp_security_ssh enable
		REBOOT_REQUIRED=TRUE
	;;
	Disable\ SSH)
		pcp_security_ssh disable
		REBOOT_REQUIRED=TRUE
	;;
	*)
		pcp_security_ssh
	;;
esac

COLUMN1="column210"
COLUMN2="column210"
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Disable ssh</legend>'
echo '          <form name="ssh" action="'$0'" method="get">'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_start_row_shade
pcp_incr_id
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="'$COLUMN1'">'
echo '                  <p>'$(pcp_ssh_status)'</p>'
echo '                </td>'
echo '                <td class="'$COLUMN2'">'
echo '                  <p>Number of SSH files found: '$SSH_FOUND'</p>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Disable SSH on boot&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p><b>Default:</b> Secure Shell daemon (sshd) is started.</p>'
echo '                    <p>To decrease access to pCP and increase security you can disable SSH.</p>'
echo '                    <p>SSH will start automatically if an ssh file is found in the pCP boot partition.</p>'
echo '                    <p>A reboot required to activate new setting.</p>'
echo '                  </div>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
                      if [ $SSH_FOUND -eq 0 ]; then
echo '                  <input type="submit" name="ACTION" value="Enable SSH">'
                      else
echo '                  <input type="submit" name="ACTION" value="Disable SSH">'
                      fi
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
#----------------------------------------------------------------------------------------

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
# password main
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Change password</legend>'
#----------------------------------------------------------------------------------------

#-----------------------------------Password---------------------------------------------
echo '          <form name="password" action="'$0'" method="get">'
echo '            <table class="bggrey percent100">'
if [ "$CURRENTPASSWDHASH" = "$(pcp_security_passwd_hash "$DEFAULTPASSWD")" ]; then
	echo '              <tr class="warning">'
	echo '                <td>'
	echo '                  <div style="color:white">'
	echo '                    <p><b>WARNING: </b>Using piCorePlayer default password.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_table_padding
fi
pcp_start_row_shade
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

pcp_footer
pcp_copyright
pcp_remove_query_string
[ $REBOOT_REQUIRED ] && pcp_reboot_required

echo '</body>'
echo '</html>'
exit
