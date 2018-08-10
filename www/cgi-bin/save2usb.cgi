#!/bin/sh

# Version: 4.0.0 2018-08-11

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

pcp_banner
pcp_running_script

#========================================================================================
# Generate status message and finish HTML page.
#----------------------------------------------------------------------------------------
pcp_html_end() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Status</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '                <p>'$FAIL_MSG'</p>'
	echo '              </td>'
	echo '            </tr>'
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	                      pcp_redirect_button "Go to Main Page" "main.cgi" 10
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'

	pcp_footer
	pcp_copyright

	echo '</body>'
	echo '</html>'
	exit
}

#========================================================================================
# First fieldset table.
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Coping configuration file to USB device ('$DEV_USB')</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <textarea class="inform" style="height:100px">'
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
		echo '[ NOTE ] If you boot with this USB device attached, this configuration file will used.'
		echo '[ NOTE ] This is handy if you update your piCorePlayer or want to setup another piCorePlayer with similar settings.'
	else
		echo '[ ERROR ] Your configuration file was not saved - reboot with your USB device attached and then try to save your configuration file again.'
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
	echo '[ ERROR ] USB device is not mounted.'
	echo '[ ERROR ] This routine will not save to the Boot Device if booting from USB.'
	echo '[ ERROR ] Insert USB device and try again.'
	FAIL_MSG='USB device is not mounted - Insert USB device and try again.'
fi

#----------------------------------------------------------------------------------------
echo '                  </textarea>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

pcp_html_end
