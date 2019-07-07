#!/bin/sh

# Version: 6.0.0 2019-06-08

#========================================================================================
# Disable SSH
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
