#!/bin/sh

# Version: 0.04 2016-03-29 GE
#	Rewrite.

# Version: 0.03 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.02 2014-08-28 GE
#	Changed refresh time from 30 to 20 seconds.
#	Added pcp_go_main_button.
#	Added textarea with listing of *config.cfg on USB

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables

MNT_SDA1="/mnt/sda1"
DEV_SDA1="/dev/sda1"
FAIL_MSG="OK"
WAS_MOUNTED=0
IS_MOUNTED=0

pcp_html_head "Save configuration file to USB device" "SBP" "20" "main.cgi"

pcp_banner
pcp_running_script

#========================================================================================
# Generate staus message and finish html page
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
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'

	pcp_footer
	pcp_copyright

	if [ "${FAIL_MSG:0:2}" = "OK" ] ; then
		pcp_go_main_button
	fi

	echo '</body>'
	echo '</html>'
	exit
}

#========================================================================================
# First fieldset table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Coping configuration file to USB device ('$MNT_SDA1')</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <textarea class="inform" style="height:100px">'
#----------------------------------------------------------------------------------------

if mount | grep $MNT_SDA1 >/dev/null 2>&1; then
	echo '[  OK  ] USB device is already mounted.'
	WAS_MOUNTED=1
	IS_MOUNTED=1
else
	echo -n '[ INFO ] Mounting USB device...'
	sudo mount $DEV_SDA1
	[ $? -eq 0 ] && IS_MOUNTED=1 && echo " OK" || echo ""
	sleep 1
fi

if [ $IS_MOUNTED -eq 1 ]; then
	echo -n '[ INFO ] Copying configuration file to USB device...'
	[ -f ${MNT_SDA1}/newconfig.cfg ] && sudo mv ${MNT_SDA1}/newconfig.cfg ${MNT_SDA1}/newconfig.cfg~
	sudo /bin/cp -f /usr/local/sbin/config.cfg ${MNT_SDA1}/newconfig.cfg
	[ $? -eq 0 ] && echo " OK" || echo "" || FAIL_MSG="Failed to copy configuration file to USB device."
	if [ -f ${MNT_SDA1}/newconfig.cfg ]; then
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
		sudo umount $DEV_SDA1
		[ $? -eq 0 ] && echo " OK" || echo "" || FAIL_MSG="Failed unmount USB device."
	else
		echo '[  OK  ] Leaving USB device mounted.'
	fi
else
	echo '[ ERROR ] USB device is not mounted.'
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
