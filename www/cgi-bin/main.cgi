#!/bin/sh

# Version: 0.07 2014-10-22 GE
#	Using pcp_html_head now.

# Version: 0.06 2014-10-09 GE
#	Revised uptime delay to use seconds.

# Version: 0.05 2014-10-08 GE
#	Size of input buttons controlled through input[type=submit] style.

# Version: 0.04 2014-10-02 GE
#	Added uptime delay before pcp_squeezelite_status is checked.

# Version: 0.03 2014-09-20 GE
#	Modified HTML to improve cross browser support.

# Version: 0.02 2014-08-22 GE
#	Added check for pcp_squeezelite_status.

# Version: 0.01 2014-06-25 GE
#	Original.

. pcp-functions
pcp_variables

pcp_html_head "Main Page" "SBP"

pcp_controls
pcp_banner
pcp_navigation

[ $(pcp_uptime_seconds) -gt 60 ] && [ $(pcp_squeezelite_status) = 1 ] &&
echo '<p class="error">[ ERROR ] Squeezelite not running.</p>'

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] System uptime (sec): '$(pcp_uptime_seconds)'<br />'
	echo '                 [ DEBUG ] System uptime (min): '$(pcp_uptime_minutes)'<br />'
	echo '                 [ DEBUG ] Squeezelite status: '$(pcp_squeezelite_status)'</p>'
fi

echo '<table border="0" bgcolor="d8d8d8" cellspacing="0" cellpadding="0" width="960">'

echo '  <tr height="8">'
echo '    <td width="180"></td>'
echo '    <td></td>'
echo '  </tr>'

echo '  <tr height="28">'
echo '    <td align="center" width="180">'
echo '      <form name="updateTriode" action="updatesqlt.cgi" method="get" id="updateTriode">'
echo '        <input type="hidden" name="VERSION" value="Triode"/>'
echo '        <input type="submit" value="Update" size="300"/>'
echo '      </form>'
echo '    </td>'
echo '    <td valign="center">'
echo '      <p>Triode'\''s newest version. Download and update Squeezelite.</p>'
echo '    </td>'
echo '  </tr>'

echo '  <tr height="28">'
echo '    <td align="center">'
echo '      <form name="updateRalphy" action="updatesqlt.cgi" method="get" id="updateRalphy">'
echo '        <input type="hidden" name="VERSION" value="Ralphy"/>'
echo '        <input type="submit" value="Update" />'
echo '      </form>'
echo '    </td>'
echo '    <td valign="center">'
echo '      <p>Ralphy'\''s newest version. Download and update Squeezelite. This one allows upsampling using SOX and can play wma and alac via ffmpeg.</p>'
echo '    </td>'
echo '  </tr>'

echo '  <tr height="28">'
echo '    <td align="center">'
echo '      <form name="Restart" action="restartsqlt.cgi" method="get" id="Restart">'
echo '        <input type="submit" value="Restart" />'
echo '      </form>'
echo '    </td>'
echo '    <td valign="center">'
echo '      <p>Restart Squeezelite with new settings.</p>'
echo '    </td>'
echo '  </tr>'

echo '  <tr height="28">'
echo '    <td align="center">'
echo '      <form name="Stop" action="stop.cgi" method="get" id="Stop">'
echo '        <input type="submit" value="Stop" />'
echo '      </form>'
echo '    </td>'
echo '    <td valign="center">'
echo '      <p>Stop Squeezelite.</p>'
echo '    </td>'
echo '  </tr>'

echo '  <tr height="28">'
echo '    <td align="center">'
echo '      <form name="backup" action="javascript:pcp_confirm('\''Do a backup?'\'','\''backup.cgi'\'')" method="get" id="backup">'
echo '        <input type="submit" value="Backup" />'
echo '      </form>'
echo '    </td>'
echo '    <td valign="center">'
echo '      <p>Backup your changes.</p>'
echo '    </td>'
echo '  </tr>'

echo '  <tr height="28">'
echo '    <td align="center">'
echo '      <form name="Reboot" action="javascript:pcp_confirm('\''Reboot piCorePlayer?'\'','\''reboot.cgi'\'')" method="get" id="Reboot">'
echo '        <input type="submit" value="Reboot" />'
echo '      </form>'
echo '    </td>'
echo '    <td valign="center">'
echo '      <p>Reboot - necessary if you are enabling or disabling HDMI output.</p>'
echo '    </td>'
echo '  </tr>'

echo '  <tr height="28">'
echo '    <td align="center">'
echo '      <form name="Shutdown" action="javascript:pcp_confirm('\''Shutdown piCorePlayer?'\'','\''shutdown.cgi'\'')" method="get" id="Shutdown">'
echo '        <input type="submit" value="Shutdown" />'
echo '      </form>'
echo '    </td>'
echo '    <td valign="center">'
echo '      <p>Shutdown - Put your Raspberry Pi to sleep.</p>'
echo '    </td>'
echo '  </tr>'

echo '  <tr height="28">'
echo '    <td align="center">'
echo '      <form name="InSitu" action="upd_picoreplayer.cgi" method="get" id="InSitu">'
echo '        <input type="submit" value="Update pCP" />'
echo '      </form>'
echo '    </td>'
echo '    <td valign="center">'
echo '      <p>Update piCorePlayer without removing the SD-card.</p>'
echo '    </td>'
echo '  </tr>'

echo '  <tr height="28">'
echo '    <td align="center">'
echo '      <form name="Saveconfig" action="save2usb.cgi" method="get" id="Saveconfig">'
echo '        <input type="submit" value="Save to USB" />'
echo '      </form>'
echo '    </td>'
echo '    <td valign="center">'
echo '      <p>Save your current configuration to USB stick for use after update or to be used in another piCorePlayer.</p>'
echo '    </td>'
echo '  </tr>'

echo '</table>'

pcp_footer

echo '</body>'
echo '</html>'