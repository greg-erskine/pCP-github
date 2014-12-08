#!/bin/sh

# Version: 0.09 2014-12-08 GE
#	HTML5 formatting.

# Version: 0.08 2014-12-08 SBP
#	Added support for Raspberry Pi Model A+.

# Version: 0.07 2014-10-22 GE
#	Using pcp_html_head now.
#	Added more comments to various options.
#	Changed remaining double quotes to single quotes.
#	Added logic to only display valid options.

# Version: 0.06 2014-10-10 SBP
#	Revised audio options.

# Version: 0.05 2014-10-09 GE
#	Revised uptime delay to use seconds.

# Version: 0.04 2014-10-02 GE
#	Added uptime delay before pcp_squeezelite_status is checked.

# Version: 0.03 2014-09-26 GE
#	Modified HTML to improve cross browser support.
#	Added more> function.

# Version: 0.02 2014-09-06 SBP
#	Changed selection of output to a dropdown list.
#	Added support for the B+ I2S-cards.
#	Graphical changes in Squeezelite table.

# Version: 0.02 2014-08-22 GE
#	Added check for pcp_squeezelite_status.

# Version: 0.01 2014-06-25 GE
#	Original.

. pcp-rpi-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

case "$AUDIO" in
	Analog*)
		ANCHECKED="selected"
		;;
	HDMI*)
		HDMICHECKED="selected"
		;;
	USB*)
		USBCHECKED="selected"
		;;
	I2SDAC*)
		I2DACCHECKED="selected"
		;;
	I2SDIG*)
		I2DIGCHECKED="selected"
		;;
	I2SAMP*)
		I2AMPCHECKED="selected"
		;;
	IQaudio*)
		IQaudioCHECKED="selected"
		;;
	I2SpDAC*)
		I2SDACpCHECKED="selected"
		;;
	I2SpDIG*)
		I2SDIGpCHECKED="selected"
		;;
	I2SpIQaudIO*)
		IQaudIOpCHECKED="selected"
		;;
	*)
		CHECKED="Not set"
		;;
esac

pcp_html_head "Squeezelite Settings" "SBP"

pcp_controls
pcp_banner
pcp_navigation

#[ $(pcp_uptime_seconds) -gt 60 ] && [ $(pcp_squeezelite_status) = 1 ] &&
#echo '<p class="error">[ ERROR ] Squeezelite not running.</p>'

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="setaudio" action="chooseoutput.cgi" method="get" id="setaudio">'
echo '      <div class="row">'
echo '      <fieldset>'
echo '        <legend>Choose audio output</legend>'
echo '        <table class="bggrey percent100">'
echo '          <tr class="even">'
echo '            <td class="column150"><p>Audio output</p></td>'
echo '            <td>'
echo '              <select name="AUDIO">'
echo '                <option value="Analog" id="ANALOG" '$ANCHECKED' size="80"> Analog audio</option>'
echo '                <option value="HDMI" id="HDMI" '$HDMICHECKED'> HDMI audio</option>'
echo '                <option value="USB" id="USB" '$USBCHECKED'> USB audio</option>'
if [ $(pcp_rpi_is_model_B_rev_2) = 0 ]; then
	echo '                <option value="I2SDAC" id="I2SDAC" '$I2DACCHECKED'> I2S-audio HiFiBerry/Sabre ES9023/Texas PCM5102A</option>'
	echo '                <option value="I2SDIG" id="I2SDIG" '$I2DIGCHECKED'> I2S-audio HiFiBerry Digi</option>'
	echo '                <option value="IQaudio" id="IQaudio" '$IQaudioCHECKED'> I2S-audio IQaudIO Pi-DAC</option>'
	echo '                <option value="I2SAMP" id="I2SAMP" '$I2AMPCHECKED'> I2S-audio HiFiBerry AMP</option>'
fi
if [ $(pcp_rpi_is_model_Bplus) = 0 ] || [ $(pcp_rpi_is_model_Aplus) = 0 ]; then
	echo '                <option value="I2SpDAC" id="I2SpDAC" '$I2SDACpCHECKED'> I2S-audio+ HiFiBerry DAC+</option>'
	echo '                <option value="I2SpDIG" id="I2SpDIG" '$I2SDIGpCHECKED'> I2S-audio+ HiFiBerry Digi+</option>'
	echo '                <option value="I2SpIQaudIO" id="I2SpIQaudIO" '$IQaudIOpCHECKED'> I2S-audio+ IQaudIO Pi-DAC+</option>'
fi
echo '              </select>'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td colspan="2">'
echo '              <input type="submit" value="Save">'
echo '            </td>'
echo '          </tr>'
echo '        </table>'
echo '      </fieldset>'
echo '      </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '  <tr>'
echo '    <td>'
echo '      <form name="squeeze" action="writetoconfig.cgi" method="get">'
echo '      <div class="row">'
echo '        <fieldset>'
echo '        <legend>Change Squeezelite settings</legend>'
echo '        <table class="bggrey percent100">'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td class="column150">'
echo '              <p>Name of your player</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="NAME" name="NAME" size="32" maxlength="26" value="'$NAME'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Specify the piCorePlayer name&nbsp;&nbsp;<a class="moreless" id="ID01a" href=# onclick="return more('\''ID01'\'')">more></a><br /></p>'
echo '              <div id="ID01" class="less">'
echo '              <p>This is the player name that will be used by LMS, so this name will appear in the web interface and your apps.'
echo '                 It is recommended that you use standard alphanumeric characters for maximum compatibility.</p>'
echo '              <p>Invalid characters:</p>'
echo '                <ul>'
echo '                  <li>`</li>'
echo '                  <li>&</li>'
echo '                  <li>$</li>'
echo '                  <li>others</li>'
echo '                </ul>'
echo '              <p>Examples:</p>'
echo '                <ul>'
echo '                  <li>piCorePlayer2</li>'
echo '                  <li>Main Stereo</li>'
echo '                  <li>Bed Room</li>'
echo '                </ul>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td class="column150">'
echo '              <p>Output settings</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="OUTPUT" name="OUTPUT" size="32" value="'$OUTPUT'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Specify the output device&nbsp;&nbsp;<a class="moreless" id="ID02a" href=# onclick="return more('\''ID02'\'')">more></a><br /></p>'
echo '              <div id="ID02" class="less">'
echo '              <p></p>'
echo '                <ul>'
echo '                  <li>default "default"</li>'
echo '                  <li>- = output to stdout</li>'
echo '                </ul>'
echo '              <p>Squeezelite found these output devices:</p>'
echo '                <ul>'
                        /mnt/mmcblk0p2/tce/squeezelite-armv6hf -l | awk '/^  / { print "                  <li> "$1"</li>" }'
echo '                </ul>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td class="column150">'
echo '              <p>ALSA settings</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="ALSA_PARAMS" name="ALSA_PARAMS" size="32" value="'$ALSA_PARAMS'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Specify the ALSA params to open output device&nbsp;&nbsp;<a class="moreless" id="ID03a" href=# onclick="return more('\''ID03'\'')">more></a><br /></p>'
echo '              <div id="ID03" class="less">'
echo '                <p>&lt;b&gt;:&lt;p&gt;:&lt;f&gt;:&lt;m&gt;:&lt;d&gt;</p>'
echo '                <ul>'
echo '                  <li>b = buffer time in ms or size in bytes</li>'
echo '                  <li>p = period count or size in bytes</li>'
echo '                  <li>f = sample format (16|24|24_3|32)</li>'
echo '                  <li>m = use mmap (0|1)</li>'
echo '                  <li>d = opens ALSA twice (undocumented) i.e. ::::d</li>'
echo '                </ul>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td class="column150">'
echo '              <p>Buffer size settings</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="BUFFER_SIZE" name="BUFFER_SIZE" size="32" value="'$BUFFER_SIZE'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Specify internal Stream and Output buffer sizes in Kbytes&nbsp;&nbsp;<a class="moreless" id="ID04a" href=# onclick="return more('\''ID04'\'')">more></a><br /></p>'
echo '              <div id="ID04" class="less">'
echo '                <p>&lt;stream&gt;:&lt;output&gt;</p>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td class="column150">'
echo '              <p>Codec settings</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="_CODEC" name="_CODEC" size="32" value="'$_CODEC'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Restrict codecs to those specified, otherwise load all available codecs&nbsp;&nbsp;<a class="moreless" id="ID05a" href=# onclick="return more('\''ID05'\'')">more></a><br /></p>'
echo '              <div id="ID05" class="less">'
echo '                <p>&lt;codec1,codec2&gt;</p>'
echo '                <p>Known codecs:</p>'
echo '                <ul>'
echo '                  <li>flac</li>'
echo '                  <li>pcm</li>'
echo '                  <li>mp3</li>'
echo '                  <li>ogg</li>'
echo '                  <li>aac</li>'
echo '                  <li>wma</li>'
echo '                  <li>alac</li>'
echo '                  <li>mad, mpg for specific mp3 codec</li>'
echo '                </ul>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td class="column150">'
echo '              <p class="row">Priority settings</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="PRIORITY" name="PRIORITY" size="32" value="'$PRIORITY'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Set real time priority of output thread (1-99)&nbsp;&nbsp;<a class="moreless" id="ID06a" href=# onclick="return more('\''ID06'\'')">more></a><br /></p>'
echo '              <div id="ID06" class="less">'
echo '                <p>&lt;priority&gt;</p>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td class="column150">'
echo '              <p class="row">Max sample rate</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="MAX_RATE" name="MAX_RATE" size="32" value="'$MAX_RATE'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Sample rates supported, allows output to be off when Squeezelite is started&nbsp;&nbsp;<a class="moreless" id="ID07a" href=# onclick="return more('\''ID07'\'')">more></a><br /></p>'
echo '              <div id="ID07" class="less">'
echo '                <p>&lt;rates&gt;[:&lt;delay&gt;]</p>'
echo '                <ul>'
echo '                  <li>rates = &lt;maxrate&gt;|&lt;minrate&gt;-&lt;maxrate&gt;|&lt;rate1&gt;,&lt;rate2&gt;,&lt;rate3&gt;</li>'
echo '                  <li>delay = optional delay switching rates in ms</li>'
echo '                </ul>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td class="column150">'
echo '              <p class="row">Upsample settings</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="UPSAMPLE" name="UPSAMPLE" size="32" value="'$UPSAMPLE'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Resample, params&nbsp;&nbsp;<a class="moreless" id="ID08a" href=# onclick="return more('\''ID08'\'')">more></a><br /></p>'
echo '              <div id="ID08" class="less">'
echo '                <p>&lt;recipe&gt;:&lt;flags&gt;:&lt;attenuation&gt;:&lt;precision&gt;:<br />'
echo '                   &lt;passband_end&gt;:&lt;stopband_start&gt;:&lt;phase_response&gt;</p>'
echo '                <ul>'
echo '                  <li>recipe = (v|h|m|l|q)(L|I|M)(s) [E|X]</li>'
echo '                  <ul>'
echo '                    <li>E = exception - resample only if native rate not supported</li>'
echo '                    <li>X = async - resample to max rate for device, otherwise to max sync rate</li>'
echo '                  </ul>'
echo '                  <li>flags = num in hex</li>'
echo '                  <li>attenuation = attenuation in dB to apply (default is -1db if not explicitly set)</li>'
echo '                  <li>precision = number of bits precision (NB. HQ = 20. VHQ = 28)</li>'
echo '                  <li>passband_end = number in percent (0dB pt. bandwidth to preserve. nyquist = 100%)</li>'
echo '                  <li>stopband_start = number in percent (Aliasing/imaging control. > passband_end)</li>'
echo '                  <li>phase_response = 0-100 (0 = minimum / 50 = linear / 100 = maximum)</li>'
echo '                </ul>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td class="column150">'
echo '              <p class="row">MAC address</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="MAC_ADDRESS" name="MAC_ADDRESS" size="32" value="'$MAC_ADDRESS'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Set MAC address&nbsp;&nbsp;<a class="moreless" id="ID09a" href=# onclick="return more('\''ID09'\'')">more></a><br /></p>'
echo '              <div id="ID09" class="less">'
echo '                <p>format: ab:cd:ef:12:34:56</p>'
echo '                <p>This is used if you want to use a fake MAC address or you want to overwrite the default MAC address determined by Squeezelite.'
echo '                   Usually you will not need to set a MAC address.</p>'
echo '                <p>By default Squeezelite will use one of the following MAC addresses:</p>'
echo '                <ul>'
echo '                  <li>Physical MAC address: '$(pcp_eth0_mac_address)'</li>'
echo '                  <li>Wireless MAC address: '$(pcp_wlan0_mac_address)'</li>'
echo '                </ul>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td class="column150">'
echo '              <p class="row">Squeezelite server IP</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="SERVER_IP" name="SERVER_IP" size="32" value="'$SERVER_IP'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Connect to specified LMS server, otherwise uses autodiscovery to find server&nbsp;&nbsp;<a class="moreless" id="ID10a" href=# onclick="return more('\''ID10'\'')">more></a><br /></p>'
echo '              <div id="ID10" class="less">'
echo '                <p>&lt;server&gt;[:&lt;port&gt;]</p>'
echo '                <p>Default LMS port = 3483</p>'
echo '                <p><b>Note:</b> Do not include the port number unless you have changed the LMS default port numbers.</p>'
echo '                <p>Current LMS server'\''s IP is:</p>'
echo '                <ul>'
echo '                  <li>'$(pcp_lmsip)'</li>'
echo '                </ul>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td class="column150">'
echo '              <p class="row">Log level setting</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="LOGLEVEL" name="LOGLEVEL" size="32" value="'$LOGLEVEL'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Set logging level&nbsp;&nbsp;<a class="moreless" id="ID11a" href=# onclick="return more('\''ID11'\'')">more></a><br /></p>'
echo '              <div id="ID11" class="less">'
echo '                <p>&lt;log&gt;=&lt;level&gt;</p>'
echo '                <ul>'
echo '                  <li>log: all|slimproto|stream|decode|output</li>'
echo '                  <li>level: info|debug|sdebug</li>'
echo '                </ul>'
echo '                <p>Example:</p>'
echo '                <ul>'
echo '                  <li>slimproto=info</li>'
echo '                </ul>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td class="column150">'
echo '              <p class="row">Log file name</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="LOGFILE" name="LOGFILE" size="32" value="'$LOGFILE'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Write debug logfile to attached USB stick&nbsp;&nbsp;<a class="moreless" id="ID12a" href=# onclick="return more('\''ID12'\'')">more></a><br /></p>'
echo '              <div id="ID12" class="less">'
echo '                <ul>'
echo '                  <li>Log level settings needs to be set</li>'
echo '                  <li>USB stick should be inserted before booting</li>'
echo '                </ul>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td class="column150">'
echo '              <p class="row">Device supports DoP</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="DSDOUT" name="DSDOUT" size="32" value="'$DSDOUT'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Output device supports DSD over PCM (DoP)&nbsp;&nbsp;<a class="moreless" id="ID13a" href=# onclick="return more('\''ID13'\'')">more></a><br /></p>'
echo '              <div id="ID13" class="less">'
echo '                <p>LMS Server requires a DoP patch.</p>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td class="column150">'
echo '              <p class="row">Visualiser support</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="VISULIZER" name="VISULIZER" size="32" value="'$VISULIZER'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Visualiser support*&nbsp;&nbsp;<a class="moreless" id="ID14a" href=# onclick="return more('\''ID14'\'')">more></a><br /></p>'
echo '              <div id="ID14" class="less">'
echo '                <p>*An option for jivelite if it gets ported to piCorePlayer. For now, not of any use.</p>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td class="column150">'
echo '              <p class="row">Various input</p>'
echo '            </td>'
echo '            <td class="column210">'
echo '              <input class="large15" type="text" id="OTHER" name="OTHER" size="32" value="'$OTHER'">'
echo '            </td>'
echo '            <td>'
echo '              <p>Add another command&nbsp;&nbsp;<a class="moreless" id="ID15a" href=# onclick="return more('\''ID15'\'')">more></a><br /></p>'
echo '              <div id="ID15" class="less">'
echo '                <p>Ensure to include the correct switch first, i.e. -n or -o etc</p>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td colspan="3">'
echo '              <input type="submit" value="Save">'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '        </table>'
echo '        </fieldset>'
echo '      </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

[ $DEBUG = 1 ] && pcp_show_config_cfg
pcp_refresh_button
pcp_footer

echo '</body>'
echo '</html>'
