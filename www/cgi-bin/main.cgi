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

#[ $(pcp_uptime_seconds) -gt 60 ] && [ $(pcp_squeezelite_status) = 1 ] &&
#echo '<p class="error">[ ERROR ] Squeezelite not running.</p>'

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] System uptime (sec): '$(pcp_uptime_seconds)'<br />'
	echo '                 [ DEBUG ] System uptime (min): '$(pcp_uptime_minutes)'<br />'
	echo '                 [ DEBUG ] Squeezelite status: '$(pcp_squeezelite_status)'</p>'
fi

#------------------------
echo '<table border="0" bgcolor="d8d8d8" cellspacing="0" cellpadding="0" width="960">'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '        <legend>Basic operations</legend>'
echo '        <table border="0">'


#------------Red Green info -----------------------------------------------
echo '          <tr class="even">'
echo '            <td width="150">'
if [ $(pcp_squeezelite_status) = 0 ]; then
     echo '    <div class="circle" style="background-color:green;"></div>'
     echo '    </td>'
     echo '    <td>'
     echo '      <p>Squeezelite is running</p>'
     echo '    </td>'
else 
     echo '    <div class="circle" style="background-color:red;"></div>'
     echo '    </td>'
     echo '    <td>'
     echo '      <p>Squeezelite is not running</p>'
     echo '    </td>'
 fi

#-------------------------
echo '  <tr height="8">'
echo '    <td width="180"></td>'
echo '    <td></td>'
echo '  </tr>'


#------------Stop-----

echo '      <form name="Stop" action="stop.cgi" method="get" id="Stop">'
echo '         <tr class="even">'
echo '            <td width="150">'
echo '              <input type="submit" value="Stop" />'
echo '      </form>'
echo '            </td>'
echo '            <td width="810">'
echo '              <p>Stop Squeezelite.</p>'
echo '            </td>'
echo '        </tr>'



#------------Restart-----

echo '      <form name="Restart" action="restartsqlt.cgi" method="get" id="Restart">'
echo '          <tr class="odd">'
echo '            <td width="150">'
echo '               <input type="submit" value="Restart" />'
echo '      </form>'
echo '            </td>'
echo '            <td width="810">'
echo '               <p>Restart Squeezelite with new settings.</p>'
echo '            </td>'
echo '          </tr>'


#------------Update Triode-----

echo '      <form name="updateTriode" action="updatesqlt.cgi" method="get" id="updateTriode">'
echo '          <tr class="even">'
echo '            <td width="150">'
echo '               <input type="hidden" name="VERSION" value="Triode"/>'
echo '               <input type="submit" value="Update"/>'
echo '      </form>'
echo '            </td>'
echo '            <td width="810">'
echo '                <p>Triode'\''s newest version. Download and update Squeezelite.</p>'
echo '            </td>'
echo '          </tr>'

#-------------Update Ralphy---------

echo '      <form name="updateRalphy" action="updatesqlt.cgi" method="get" id="updateRalphy">'
echo '          <tr class="odd">'
echo '            <td width="150">'
echo '               <input type="hidden" name="VERSION" value="Ralphy"/>'
echo '               <input type="submit" value="Update" />'
echo '      </form>'
echo '             </td>'
echo '             <td width="810">'
echo '                <p>Ralphy'\''s newest version. Download and update Squeezelite. This one allows upsampling using SOX and can play wma and alac via ffmpeg.</p>'
echo '            </td>'
echo '          </tr>'


#-------------Backup-----------

echo '      <form name="backup" action="javascript:pcp_confirm('\''Do a backup?'\'','\''backup.cgi'\'')" method="get" id="backup">'
echo '          <tr class="even">'
echo '            <td width="150">'
echo '                <input type="submit" value="Backup" />'
echo '      </form>'
echo '            </td>'
echo '            <td width="810">'
echo '                <p>Backup your changes.</p>'
echo '           </td>'
echo '          </tr>'


#-------------Reboot-----------
echo '      <form name="Reboot" action="javascript:pcp_confirm('\''Reboot piCorePlayer?'\'','\''reboot.cgi'\'')" method="get" id="Reboot">'
echo '          <tr class="odd">'
echo '            <td width="150">'
echo '              <input type="submit" value="Reboot" />'
echo '       </form>'
echo '             </td>'
echo '             <td width="810">'
echo '               <p>Reboot - necessary if you are enabling or disabling HDMI output.</p>'
echo '            </td>'
echo '          </tr>'


#-------------Shutdown---------


echo '      <form name="Shutdown" action="javascript:pcp_confirm('\''Shutdown piCorePlayer?'\'','\''shutdown.cgi'\'')" method="get" id="Shutdown">'
echo '          <tr class="even">'
echo '            <td width="150">'
echo '               <input type="submit" value="Shutdown" />'
echo '      </form>'
echo '            </td>'
echo '            <td width="810">'
echo '               <p>Shutdown - Put your Raspberry Pi to sleep.</p>'
echo '            </td>'
echo '          </tr>'


#------------Update PcP

echo '      <form name="InSitu" action="upd_picoreplayer.cgi" method="get" id="InSitu">'
echo '          <tr class="odd">'
echo '            <td width="150">'
echo '               <input type="submit" value="Update pCP" />'
echo '      </form>'
echo '            </td>'
echo '            <td width="810">'
echo '               <p>Update piCorePlayer without removing the SD-card.</p>'
echo '            </td>'
echo '          </tr>'


#------------Save to USB---------

echo '      <form name="Saveconfig" action="save2usb.cgi" method="get" id="Saveconfig">'
echo '         <tr class="even">'
echo '           <td width="150">'
echo '              <input type="submit" value="Save to USB" />'
echo '       </form>'
echo '            </td>'
echo '            <td width="810">'
echo '               <p>Save your current configuration to USB stick for use after update or to be used in another piCorePlayer.</p>'
echo '            </td>'
echo '          </tr>'


#-----the trings below finish the table view-----
echo '        </table>'
echo '        </fieldset>'
echo '      </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

pcp_footer

echo '</body>'
echo '</html>'