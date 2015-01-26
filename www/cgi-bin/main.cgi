#!/bin/sh

# Version: 0.11 2015-01-26 GE
#	Added Disable GUI.

# Version: 0.10 2014-12-20 GE
#	Modified Squeezelite running indicator.

# Version: 0.09 2014-12-09 GE
#	HTML5 formatted.

# Version: 0.08 2014-12-08 SBP
#	Revised button order.
#	Added Squeezelite running indicator.
#	Reformatted.

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

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Change Squeezelite settings</legend>'
          
echo '          <table class="bggrey percent100">'

#------------------------------------------Squeezelite Indication------------------------
if [ $(pcp_squeezelite_status) = 0 ]; then
	IMAGE="green.png"
	STATUS="running"
else
	IMAGE="red.png"
	STATUS="not running"
fi

echo '            <tr class="even">'
echo '              <td class="column150">'
echo '                <p class="centre"><img src="../images/'$IMAGE'" alt="'$STATUS'"></p>'
echo '              </td>'
echo '              <td>'
echo '                <p>Squeezelite is '$STATUS'.</p>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Padding---------------------------------------
echo '            <tr class="padding">'
echo '              <td></td>'
echo '              <td></td>'
echo '            </tr>'

#------------------------------------------Stop------------------------------------------
echo '            <tr class="even">'
echo '              <td class="column150 center">'
echo '                <form name="Stop" action="stop.cgi" method="get" id="Stop">'
echo '                  <input type="submit" value="Stop" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Stop Squeezelite&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID01a" href=# onclick="return more('\''ID01'\'')">more></a></p>'
echo '                <div id="ID01" class="less">'
echo '                  <p>This will kill the Squeezelite process.</p>'
echo '                  <p>Click on the Restart button to start Squeezelite again.</p>'
echo '                  <p><b>Note:</b></p>'
echo '                  <ul>'
echo '                    <li>Squeezelite running indicator will turn red.</li>'
echo '                    <li>Squeezelite in the footer will turn red.</li>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Restart---------------------------------------
echo '            <tr class="odd">'
echo '              <td class="column150 center">'
echo '                <form name="Restart" action="restartsqlt.cgi" method="get" id="Restart">'
echo '                  <input type="submit" value="Restart" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Restart Squeezelite with new settings&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID02a" href=# onclick="return more('\''ID02'\'')">more></a></p>'
echo '                <div id="ID02" class="less">'
echo '                  <p>This will kill the Squeezelite process then restart it.</p>'
echo '                  <p><b>Note:</b></p>'
echo '                  <ul>'
echo '                    <li>A restart of Squeezelite is required after you change any of the Squeezelite settings.</li>'
echo '                    <li>Squeezelite running indicator will turn green.</li>'
echo '                    <li>Squeezelite in the footer will turn green.</li>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Update Squeezelite - Triode-------------------
echo '            <tr class="even">'
echo '              <td class="column150 center">'
echo '                <form name="updateTriode" action="updatesqlt.cgi" method="get" id="updateTriode">'
echo '                  <input type="hidden" name="VERSION" value="Triode"/>'
echo '                  <input type="submit" value="Update" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Download and update to Triode'\''s newest version of Squeezelite&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID03a" href=# onclick="return more('\''ID03'\'')">more></a></p>'
echo '                <div id="ID03" class="less">'
echo '                  <p>This will download and install the latest version of Squeezelite from Triode'\''s repository.</p>'
echo '                  <p><b>Note:</b></p>'
echo '                  <ul>'
echo '                    <li>Internet access is required.</li>'
echo '                    <li>Triode is the author of Squeezelite.</li>'
echo '                    <li>For more information on Squeezelite - see <a href="https://code.google.com/p/squeezelite/">Squeezelit Google code</a>.</li>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Update Squeezelite - Ralphy-------------------
echo '            <tr class="odd">'
echo '              <td class="column150 center">'
echo '                <form name="updateRalphy" action="updatesqlt.cgi" method="get" id="updateRalphy">'
echo '                  <input type="hidden" name="VERSION" value="Ralphy"/>'
echo '                  <input type="submit" value="Update" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Download and update to Ralphy'\''s newest version of Squeezelite&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID04a" href=# onclick="return more('\''ID04'\'')">more></a></p>'
echo '                <div id="ID04" class="less">'
echo '                  <p>This will download and install the latest version of Squeezelite from Ralphy'\''s repository.</p>'
echo '                  <p><b>Note: </b></p>'
echo '                  <ul>'
echo '                    <li>Internet access is required.</li>'
echo '                    <li>Ralphy has compiled this version of Squeezelite with the following options enabled:</li>'
echo '                    <ul>'
echo '                      <li>Upsampling using SOX.</li>'
echo '                      <li>Playing wma and alac via ffmpeg.</li>'
echo '                    </ul>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Backup----------------------------------------
echo '            <tr class="even">'
echo '              <td class="column150 center">'
echo '                <form name="backup" action="javascript:pcp_confirm('\''Do a backup?'\'','\''backup.cgi'\'')" method="get" id="backup">'
echo '                  <input type="submit" value="Backup" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Backup your changes&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID05a" href=# onclick="return more('\''ID05'\'')">more></a></p>'
echo '                <div id="ID05" class="less">'
echo '                  <p>This will do a piCore backup to your SD-card.</p>'
echo '                  <p>piCorePlayer does a backup after it changes any setting, so this option is really just for "peace of mind"'
echo '                     before doing a shutdown or reboot.</p>'
echo '                  <p><b>Note: </b>It will backup the following:</p>'
echo '                  <ul>'
echo '                    <li>Your configuration file.</li>'
echo '                    <li>Your home directory.</li>'
echo '                    <li>Files and directories defined in /opt/.filetool.lst</li>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Reboot----------------------------------------
echo '            <tr class="odd">'
echo '              <td class="column150 center">'
echo '                <form name="Reboot" action="javascript:pcp_confirm('\''Reboot piCorePlayer?'\'','\''reboot.cgi'\'')" method="get" id="Reboot">'
echo '                  <input type="submit" value="Reboot" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Reboot piCorePlayer after enabling or disabling HDMI output&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID06a" href=# onclick="return more('\''ID06'\'')">more></a></p>'
echo '                <div id="ID06" class="less">'
echo '                  <p>This will reboot piCorePlayer.</p>'
echo '                  <p><b>Note: </b>It will do the following:</p>'
echo '                  <ul>'
echo '                    <li>Graceful piCore shutdown.</li>'
echo '                    <li>Boot piCorePlayer from scratch using latest settings.</li>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Shutdown--------------------------------------
echo '            <tr class="even">'
echo '              <td class="column150 center">'
echo '                <form name="Shutdown" action="javascript:pcp_confirm('\''Shutdown piCorePlayer?'\'','\''shutdown.cgi'\'')" method="get" id="Shutdown">'
echo '                  <input type="submit" value="Shutdown" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Shutdown piCorePlayer&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID07a" href=# onclick="return more('\''ID07'\'')">more></a></p>'
echo '                <div id="ID07" class="less">'
echo '                  <p>This will gracefully shutdown piCorePlayer.</p>'
echo '                  <p>To restart piCorePlayer you will need to remove then reapply power.</p>'
echo '                  <p><b>Note: </b>This option is not really required as you can simply turn piCorePlayer off at the switch.</p>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Update pCP------------------------------------
echo '            <tr class="odd">'
echo '              <td class="column150 center">'
echo '                <form name="InSitu" action="upd_picoreplayer.cgi" method="get" id="InSitu">'
echo '                  <input type="submit" value="Update pCP" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Update piCorePlayer without removing the SD-card&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID08a" href=# onclick="return more('\''ID08'\'')">more></a></p>'
echo '                <div id="ID08" class="less">'
echo '                  <p>This will do an insitu update to piCorePlayer.</p>'
echo '                  <p>This can be used when the SD-card is not accessible to burn a new image.</p>'
echo '                  <p><b>Note: </b>Internet access is required.</p>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Save to USB-----------------------------------
echo '            <tr class="even">'
echo '              <td class="column150 center">'
echo '                <form name="Saveconfig" action="save2usb.cgi" method="get" id="Saveconfig">'
echo '                  <input type="submit" value="Save to USB" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Save your current configuration to USB stick&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID09a" href=# onclick="return more('\''ID09'\'')">more></a></p>'
echo '                <div id="ID09" class="less">'
echo '                  <p>This will copy the current configuration file to USB stick (defaults to sda1).</p>'
echo '                  <p>Can be used:</p>'
echo '                  <ul>'
echo '                    <li>as a backup</li>'
echo '                    <li>after an update</li>'
echo '                    <li>in another piCorePlayer.</li>'
echo '                  </ul>'
echo '                  <p><b>Note: </b>USB stick must be plugged into USB port.</p>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Disable GUI-----------------------------------
echo '            <tr class="odd">'
echo '              <td class="column150 center">'
echo '                <form name="disablegui" action="disablegui.sh" method="get" id="disablegui">'
echo '                  <input type="submit" value="Disable GUI" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Disable web server (useful in public areas)&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID10a" href=# onclick="return more('\''ID10'\'')">more></a></p>'
echo '                <div id="ID10" class="less">'
echo '                  <p>It can be useful to disable web access to the GUI is you don'\''t want access to your settings.</p>'
echo '                  <p>If you need access to web GUI later, you will need to re-enable the web server:</p>'
echo '                  <ul>'
echo '                    <li>Log in via ssh and at the command prompt type: enablegui</li>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

pcp_footer

echo '</body>'
echo '</html>'