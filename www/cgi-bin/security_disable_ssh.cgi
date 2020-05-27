#!/bin/sh

# Version: 7.0.0 2020-05-27

COLUMN3_1="col-sm-3"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-6"
#========================================================================================
# Disable SSH
#----------------------------------------------------------------------------------------
pcp_ssh_status() {
	sudo /usr/local/etc/init.d/openssh status
	RESULT=$?
}

#------------------------------------------------------------------------------------
# Look for ssh file on boot partition. Only start sshd if ssh file is found.
#------------------------------------------------------------------------------------
pcp_security_ssh() {
	SSH_FOUND=0
	BOOTDEVLIST="mmcblk0p1 sda1"

	pcp_debug_variables "html" BOOTDEVLIST

	for DISK in $BOOTDEVLIST
	do
		if fdisk -l /dev/${DISK} | grep /dev/${DISK} >/dev/null 2>&1; then break; fi
	done

	[ $DEBUG -eq 1 ] && pcp_message DEBUG "Checking for ssh file on ($DISK)..." "text"
	# Check if $DISK is mounted, otherwise mount it.
	if mount | grep ${DISK} >/dev/null 2>&1; then
		eval ${DISK}WASMNT=1
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "/dev/${DISK} already mounted." "text"
	else
		eval ${DISK}WASMNT=0
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "Mounting /dev/${DISK}." "text"
		mount /dev/$DISK >/dev/null 2>&1
	fi

	[ "$1" = "enable" ] && touch /mnt/${DISK}/ssh
	[ "$1" = "disable" ] && rm -f /mnt/${DISK}/ssh

	if [ -f /mnt/${DISK}/ssh ]; then
		SSH_FOUND=$((SSH_FOUND + 1))
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "SSH found on ${DISK}." "text"
	else
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "SSH NOT found on ${DISK}." "text"
	fi

	if [ $(eval echo \${${DISK}WASMNT}) -eq 0 ]; then
		umount /mnt/$DISK
		[ $DEBUG -eq 1 ] && pcp_message DEBUG "/mnt/${DISK} unmounted." "text"
	fi

	[ $SSH_FOUND -eq 0 ] && ACTION_MESSAGE="Ensable SSH" || ACTION_MESSAGE="Disable SSH"
}

#----------------------------------------------------------------------------------------
case $ACTION in
	"Enable SSH")
		pcp_security_ssh enable
		REBOOT_REQUIRED=TRUE
	;;
	"Disable SSH")
		pcp_security_ssh disable
		REBOOT_REQUIRED=TRUE
	;;
	*)
		pcp_security_ssh
	;;
esac

#----------------------------------------------------------------------------------------
pcp_border_begin
pcp_heading5 "Disable ssh"
echo '  <form name="ssh" action="'$0'" method="get">'
#----------------------------------------------------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>'$(pcp_ssh_status)'</p>'
echo '      </div>'
echo '      <div class="'$COLUMN3_2'">'
echo '        <p>Number of SSH files found: '$SSH_FOUND'</p>'
echo '      </div>'
pcp_incr_id
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>'$ACTION_MESSAGE' on boot&nbsp;&nbsp;'
pcp_helpbadge
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>SSH will start on boot if an ssh file is found in the pCP boot partition.</p>'
echo '          <p>By default Secure Shell daemon (sshd) is started on boot.</p>'
echo '          <p>To increase the level of security you can disable SSH.</p>'
echo '          <p>A reboot is required to activate the new setting.</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="col-2">'
	        if [ $SSH_FOUND -eq 0 ]; then
echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Enable SSH">Enable SSH</button>'
	        else
echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Disable SSH">Disable SSH</button>'
	        fi
echo '        <input type="hidden" name="CALLED_BY" value="Disable SSH">'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '  </form>'
pcp_border_end
#----------------------------------------------------------------------------------------
