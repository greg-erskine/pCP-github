#!/bin/sh

# Version: 0.12 2015-01-28 GE
#	Moved Disable GUI, Stop Squeezelite, Backup and Shutdown to Developers section.

# Version: 0.11 2015-01-26 SBP
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

#========================================================================================
# Main piCorePlayer operations
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Main piCorePlayer operations</legend>'
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
echo '                <p>Squeezelite is '$STATUS'&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID01a" href=# onclick="return more('\''ID01'\'')">more></a></p>'
echo '                <div id="ID01" class="less">'
echo '                  <ul>'
echo '                    <li>GREEN = Squeezelite running.</li>'
echo '                    <li>RED = Squeezelite not running.</li>'
echo '                  </ul>'
echo '                  <p><b>Note:</b></p>'
echo '                  <ul>'
echo '                    <li>Squeezelite must be running for music to play.</li>'
echo '                    <li>Squeezelite must be running for connection to LMS.</li>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Padding---------------------------------------
echo '            <tr class="padding">'
echo '              <td></td>'
echo '              <td></td>'
echo '            </tr>'

#------------------------------------------Restart---------------------------------------
echo '            <tr class="even">'
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
echo '            <tr class="odd">'
echo '              <td class="column150 center">'
echo '                <form name="updateTriode" action="updatesqlt.cgi" method="get" id="updateTriode">'
echo '                  <input type="hidden" name="VERSION" value="Triode"/>'
echo '                  <input type="submit" value="Update" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Download and install Triode'\''s latest version of Squeezelite&nbsp;&nbsp;'
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
echo '            <tr class="even">'
echo '              <td class="column150 center">'
echo '                <form name="updateRalphy" action="updatesqlt.cgi" method="get" id="updateRalphy">'
echo '                  <input type="hidden" name="VERSION" value="Ralphy"/>'
echo '                  <input type="submit" value="Update" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Download and install Ralphy'\''s latest version of Squeezelite&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID04a" href=# onclick="return more('\''ID04'\'')">more></a></p>'
echo '                <div id="ID04" class="less">'
echo '                  <p>This will download and install the latest version of Squeezelite from Ralphy'\''s repository.</p>'
echo '                  <p><b>Note: </b></p>'
echo '                  <ul>'
echo '                    <li>Internet access is required.</li>'
echo '                    <li>Ralphy version of Squeezelite is compiled this with the following options enabled:</li>'
echo '                    <ul>'
echo '                      <li>Upsampling using SOX.</li>'
echo '                      <li>Playing wma and alac via ffmpeg.</li>'
echo '                    </ul>'
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
echo '                <a class="moreless" id="ID05a" href=# onclick="return more('\''ID05'\'')">more></a></p>'
echo '                <div id="ID05" class="less">'
echo '                  <p>This will reboot piCorePlayer.</p>'
echo '                  <p><b>Note: </b>This will do the following:</p>'
echo '                  <ul>'
echo '                    <li>Shutdown piCore gracefully.</li>'
echo '                    <li>Boot piCorePlayer from scratch using the latest settings.</li>'
echo '                  </ul>'
echo '                </div>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Update pCP------------------------------------
echo '            <tr class="even">'
echo '              <td class="column150 center">'
echo '                <form name="InSitu" action="upd_picoreplayer.cgi" method="get" id="InSitu">'
echo '                  <input type="submit" value="Update pCP" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Update piCorePlayer without removing the SD card&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID06a" href=# onclick="return more('\''ID06'\'')">more></a></p>'
echo '                <div id="ID06" class="less">'
echo '                  <p>This will do an insitu update of piCorePlayer.</p>'
echo '                  <p>This can be used when the SD card is not accessible.</p>'
echo '                  <p><b>Note:</b></p>'
echo '                  <ul>'
echo '                    <li>Internet access is required.</li>'
echo '                    <li>Existing version of piCorePlayer will be overwritten.</li>'
echo '                  </ul>'

echo '                </div>'
echo '              </td>'
echo '            </tr>'

#------------------------------------------Save to USB-----------------------------------
echo '            <tr class="odd">'
echo '              <td class="column150 center">'
echo '                <form name="Saveconfig" action="save2usb.cgi" method="get" id="Saveconfig">'
echo '                  <input type="submit" value="Save to USB" />'
echo '                </form>'
echo '              </td>'
echo '              <td>'
echo '                <p>Save your current configuration to the USB flash drive&nbsp;&nbsp;'
echo '                <a class="moreless" id="ID07a" href=# onclick="return more('\''ID07'\'')">more></a></p>'
echo '                <div id="ID07" class="less">'
echo '                  <p>This will copy the current configuration file to the USB flash drive.</p>'
echo '                  <p>This configuration file can be used:</p>'
echo '                  <ul>'
echo '                    <li>as a backup</li>'
echo '                    <li>after an update</li>'
echo '                    <li>in another piCorePlayer.</li>'
echo '                  </ul>'
echo '                  <p><b>Note: </b>USB flash drive must be plugged into USB port.</p>'
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

#========================================================================================
# Developers operations
#----------------------------------------------------------------------------------------
if [ $MODE = 99 ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Developers operations</legend>'
			  
	echo '          <table class="bggrey percent100">'

	#------------------------------------------Stop------------------------------------------
	echo '            <tr class="even">'
	echo '              <td class="column150 center">'
	echo '                <form name="Stop" action="stop.cgi" method="get" id="Stop">'
	echo '                  <input type="submit" value="Stop" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Stop Squeezelite&nbsp;&nbsp;'
	echo '                <a class="moreless" id="ID08a" href=# onclick="return more('\''ID08'\'')">more></a></p>'
	echo '                <div id="ID08" class="less">'
	echo '                  <p>This will kill the Squeezelite process.</p>'
	echo '                  <p>Click [Restart] to start Squeezelite again.</p>'
	echo '                  <p><b>Note:</b></p>'
	echo '                  <ul>'
	echo '                    <li>Squeezelite running indicator will turn red.</li>'
	echo '                    <li>Squeezelite in the footer will turn red.</li>'
	echo '                  </ul>'
	echo '                </div>'
	echo '              </td>'
	echo '            </tr>'

	#------------------------------------------Backup----------------------------------------
	echo '            <tr class="odd">'
	echo '              <td class="column150 center">'
	echo '                <form name="backup" action="javascript:pcp_confirm('\''Do a backup?'\'','\''backup.cgi'\'')" method="get" id="backup">'
	echo '                  <input type="submit" value="Backup" />'
	echo '                </form>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>Backup your changes&nbsp;&nbsp;'
	echo '                <a class="moreless" id="ID09a" href=# onclick="return more('\''ID09'\'')">more></a></p>'
	echo '                <div id="ID09" class="less">'
	echo '                  <p>This will do a piCore backup to your SD card.</p>'
	echo '                  <p>piCorePlayer does a backup after it changes any setting, so this option is really just for "peace of mind"'
	echo '                     before doing a shutdown or reboot.</p>'
	echo '                  <p><b>Note: </b>This will backup the following:</p>'
	echo '                  <ul>'
	echo '                    <li>Your configuration file.</li>'
	echo '                    <li>Your home directory.</li>'
	echo '                    <li>Files and directories defined in /opt/.filetool.lst</li>'
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
	echo '                <a class="moreless" id="ID10a" href=# onclick="return more('\''ID10'\'')">more></a></p>'
	echo '                <div id="ID10" class="less">'
	echo '                  <p>This will shutdown piCorePlayer gracefully.</p>'
	echo '                  <p>To restart piCorePlayer you will need to remove then reapply power.</p>'
	echo '                  <p><b>Note: </b>This option is not really required - piCorePlayer can be turn off at the switch.</p>'
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
fi

pcp_footer

echo '</body>'
echo '</html>'