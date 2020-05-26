#!/bin/sh

# Version: 7.0.0 2020-05-26

. pcp-functions

USBDRIVES=$(blkid -o device | grep -E 'sd[a-z]1' | awk -F '/dev/' '{print $2}')

# Use the last disk found, it is more than likely one that was just inserted
USB_FOUND=0
for DISK in $USBDRIVES; do
	case $BOOTDEV in
		/dev/$DISK);;
		*) USB_FOUND=1; MNT_USB="/mnt/$DISK"; DEV_USB="/dev/$DISK";;
	esac
done

[ $USB_FOUND -eq 0 ] && DEV_USB="No Device Found"

FAIL_MSG="OK"
WAS_MOUNTED=0
IS_MOUNTED=0

pcp_html_head "Save configuration file to USB device" "SBP"

pcp_navbar

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_heading5 "Coping configuration file to USB device ($DEV_USB)"
echo '    <div class="row">'
echo '      <div class="col-12">'
pcp_infobox_begin
#----------------------------------------------------------------------------------------

if [ $USB_FOUND -eq 1 ]; then
	if mount | grep $DEV_USB >/dev/null 2>&1; then
		MNT_USB=$(mount | grep $DEV_USB | awk -F ' ' '{print $3}')
		echo '[  OK  ] USB device is already mounted at '$MNT_USB'.'
		WAS_MOUNTED=1
		IS_MOUNTED=1
	else
		echo -n '[ INFO ] Mounting USB device at '$MNT_USB'...'
		sudo mount $DEV_USB
		[ $? -eq 0 ] && IS_MOUNTED=1 && echo " OK" || echo ""
		sleep 1
	fi
fi

if [ $IS_MOUNTED -eq 1 ]; then
	echo -n '[ INFO ] Copying configuration files to USB device...'
	[ -f ${MNT_USB}/newpcp.cfg ] && sudo mv ${MNT_USB}/newpcp.cfg ${MNT_USB}/newpcp.cfg~
	sudo /bin/cp -f $PCPCFG ${MNT_USB}/newpcp.cfg
	[ -f ${MNT_USB}/wpa_supplicant.conf ] && sudo mv ${MNT_USB}/wpa_supplicant.conf ${MNT_USB}/wpa_supplicant.conf~
	sudo /bin/cp -f $WPASUPPLICANTCONF ${MNT_USB}/wpa_supplicant.conf
	[ $? -eq 0 ] && echo " OK" || echo "" || FAIL_MSG="Failed to copy configuration file to USB device."
	if [ -f ${MNT_USB}/newpcp.cfg ]; then
		echo '[  OK  ] Your configuration file has been saved to your USB device.'
		FAIL_MSG="OK - Your configuration file has been saved to your USB device."
		echo '[ INFO ] If you boot with this USB device attached, this configuration file will used.'
		echo '[ INFO ] This is handy if you update your piCorePlayer or want to setup another piCorePlayer with similar settings.'
	else
		pcp_message ERROR "Your configuration file was not saved - reboot with your USB device attached and then try to save your configuration file again." "text"
		FAIL_MSG='Your configuration file was not saved.'
	fi
	sync
	if [ $WAS_MOUNTED -eq 0 ]; then
		echo -n '[ INFO ] Unmounting USB device...'
		sudo umount $DEV_USB
		[ $? -eq 0 ] && echo " OK" || echo "" || FAIL_MSG="Failed unmount USB device."
	else
		echo '[  OK  ] Leaving USB device mounted.'
	fi
else
	pcp_message ERROR "USB device is not mounted." "text"
	pcp_message ERROR "This routine will not save to the Boot Device if booting from USB." "text"
	pcp_message ERROR "Insert USB device and try again." "text"
	FAIL_MSG="USB device is not mounted - Insert USB device and try again."
fi

#----------------------------------------------------------------------------------------
pcp_infobox_end
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------

#========================================================================================
# Generate status message and finish HTML page.
#----------------------------------------------------------------------------------------
pcp_heading5 "Status"
pcp_border_begin
echo '    <div class="row mx-1">'
echo '      <div class="col-12">'
echo '        <p>'$FAIL_MSG'</p>'
echo '      </div>'
echo '    </div>'
pcp_border_end

pcp_redirect_button "Go to Main Page" "main.cgi" 100

pcp_html_end
exit
