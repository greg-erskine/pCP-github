#!/bin/sh

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

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <title>pCP - Squeezelite Settings</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Squeezelite Settings" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '  <script language="Javascript" src="../js/piCorePlayer.js"></script>'
echo '</head>'
echo ''
echo '<body>'

pcp_controls
pcp_banner
pcp_navigation

[ $(pcp_uptime_minutes) -gt 0 ] && [ $(pcp_squeezelite_status) = 1 ] &&
echo '<p class="error">[ ERROR ] Squeezelite not running.</p>'

echo '<table border="0" cellspacing="0" cellpadding="0" width="960">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="setaudio" action="chooseoutput.cgi" method="get" id="setaudio">'
echo '      <div class="row">'
echo '      <fieldset>'
echo '        <legend>Choose audio output</legend>'
echo '        <table border="0" width="100%">'
echo '          <tr>'
echo '            <td width="300" class="title">Audio output</td>'
echo '            <td class="content">'
echo '              <select name="AUDIO">'
echo '                <option value="Analog" id="ANALOG" '$ANCHECKED'> Analog audio</option>'
echo '                <option value="HDMI" id="HDMI" '$HDMICHECKED'> HDMI audio</option>'
echo '                <option value="USB" id="USB" '$USBCHECKED'> USB audio</option>'
echo '                <option value="I2SDAC" id="I2SDAC" '$I2DACCHECKED'> I2S-audio DAC (HiFiBerry or Sabre ES9023)</option>'
echo '                <option value="I2SDIG" id="I2SDIG" '$I2DIGCHECKED'> I2S-audio Digi (HiFiBerry I2S Digi)</option>'
echo '                <option value="IQaudio" id="IQaudio" '$IQaudioCHECKED'> I2S-audio IQaudIO (IQaudIO I2S DAC)</option>'
echo '                <option value="I2SpDAC" id="I2SpDAC" '$I2SDACpCHECKED'> I2S-audio I2SDAC+ (HiFiBerry DAC+)</option>'
echo '                <option value="I2SpDIG" id="I2SpDIG" '$I2SDIGpCHECKED'> I2S-audio I2SDigi+ (HiFiBerry Digi+)</option>'
echo '                <option value="I2SpIQaudIO" id="I2SpIQaudIO" '$IQaudIOpCHECKED'> I2S-audio IQaudIO+ (IQaudIO+ DAC)</option>'
echo '              </select>'
echo '            </td>'
echo '          </tr>'
echo '          <tr>'
echo '            <td colspan="2">'
echo '              <input type="submit" value="Submit">'
echo '            </td>'
echo '          </tr>'
echo '      </div>'
echo '        </table>'
echo '      </fieldset>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '  <tr>'
echo '    <td>'
echo '      <form name="squeeze" action="writetoconfig.cgi" method="get">'
echo '      <div class="row">'
echo '        <fieldset>'
echo '        <legend>Change Squeezelite settings</legend>'
echo '        <table border="0">'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td width="150">'
echo '              <p>Name of your player</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="NAME" name="NAME" size="32" maxlength="26" value="'$NAME'">'
echo '            </td>'
echo '            <td width="550">'
echo '              <p>Specify the piCorePlayer name.</p>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td width="150">'
echo '              <p>Output settings</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="OUTPUT" name="OUTPUT" size="32" value="'$OUTPUT'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Specify the output device&nbsp;&nbsp;<a class="moreless" id="ID02a" href=# onclick=\"return more('ID02')\">more></a><br /></p>"
echo '              <div id="ID02" class="less">'
echo '              <p></p>'
echo '                <ul>'
echo '                  <li>default "default"</li>'
echo '                  <li>- = output to stdout</li>'
echo '                </ul>'
echo '              <p>Squeezelite found these output devices:</p>'
echo '                <ul>'
                        /mnt/mmcblk0p2/tce/squeezelite-armv6hf -l | awk '/^  / { print "<li> "$1"</li>" }'
echo '                </ul>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td width="150">'
echo '              <p>ALSA settings</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="ALSA_PARAMS" name="ALSA_PARAMS" size="32" value="'$ALSA_PARAMS'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Specify the ALSA params to open output device&nbsp;&nbsp;<a class="moreless" id="ID03a" href=# onclick=\"return more('ID03')\">more></a><br /></p>"
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
echo '            <td width="150">'
echo '              <p>Buffer size settings</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="BUFFER_SIZE" name="BUFFER_SIZE" size="32" value="'$BUFFER_SIZE'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Specify internal Stream and Output buffer sizes in Kbytes&nbsp;&nbsp;<a class="moreless" id="ID04a" href=# onclick=\"return more('ID04')\">more></a><br /></p>"
echo '              <div id="ID04" class="less">'
echo '                <p>&lt;stream&gt;:&lt;output&gt;</p>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td width="150">'
echo '              <p>Codec settings</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="_CODEC" name="_CODEC" size="32" value="'$_CODEC'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Restrict codecs to those specified, otherwise load all available codecs&nbsp;&nbsp;<a class="moreless" id="ID05a" href=# onclick=\"return more('ID05')\">more></a><br /></p>"
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
echo '            <td width="150">'
echo '              <p class="row">Priority settings</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="PRIORITY" name="PRIORITY" size="32" value="'$PRIORITY'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Set real time priority of output thread (1-99)&nbsp;&nbsp;<a class="moreless" id="ID06a" href=# onclick=\"return more('ID06')\">more></a><br /></p>"
echo '              <div id="ID06" class="less">'
echo '                <p>&lt;priority&gt;</p>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td width="150">'
echo '              <p class="row">Max sample rate</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="MAX_RATE" name="MAX_RATE" size="32" value="'$MAX_RATE'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Sample rates supported, allows output to be off when Squeezelite is started&nbsp;&nbsp;<a class="moreless" id="ID07a" href=# onclick=\"return more('ID07')\">more></a><br /></p>"
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
echo '            <td width="150">'
echo '              <p class="row">Upsample settings</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="UPSAMPLE" name="UPSAMPLE" size="32" value="'$UPSAMPLE'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Resample, params&nbsp;&nbsp;<a class="moreless" id="ID08a" href=# onclick=\"return more('ID08')\">more></a><br /></p>"
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
echo '            <td width="150">'
echo '              <p class="row">MAC address</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="MAC_ADDRESS" name="MAC_ADDRESS" size="32" value="'$MAC_ADDRESS'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Set MAC address&nbsp;&nbsp;<a class="moreless" id="ID09a" href=# onclick=\"return more('ID09')\">more></a><br /></p>"
echo '              <div id="ID09" class="less">'
echo '                <p>format: ab:cd:ef:12:34:56</p>'
echo '                <p>Your RPIs physical MAC is: <em>'$(pcp_controls_mac_address)'</em></p>'
echo '                <p>Copy paste if you want to use it.</p>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td width="150">'
echo '              <p class="row">Squeezelite server IP</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="SERVER_IP" name="SERVER_IP" size="32" value="'$SERVER_IP'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Connect to specified LMS server, otherwise uses autodiscovery to find server&nbsp;&nbsp;<a class="moreless" id="ID10a" href=# onclick=\"return more('ID10')\">more></a><br /></p>"
echo '              <div id="ID10" class="less">'
echo '                <p>&lt;server&gt;[:&lt;port&gt;]</p>'
echo '                <p>Default port = 3483</p>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td width="150">'
echo '              <p class="row">Log level setting</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="LOGLEVEL" name="LOGLEVEL" size="32" value="'$LOGLEVEL'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Set logging level&nbsp;&nbsp;<a class="moreless" id="ID11a" href=# onclick=\"return more('ID11')\">more></a><br /></p>"
echo '              <div id="ID11" class="less">'
echo '                <p>&lt;log&gt;=&lt;level&gt;</p>'
echo '                <ul>'
echo '                  <li>log: all|slimproto|stream|decode|output</li>'
echo '                  <li>level: info|debug|sdebug</li>'
echo '                </ul>'
echo '                <p>Example:</p>'
echo '                <ul>'
echo '                  <li>slimproto:info</li>'
echo '                </ul>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td width="150">'
echo '              <p class="row">Log file name</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="LOGFILE" name="LOGFILE" size="32" value="'$LOGFILE'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Write debug logfile to attached USB stick&nbsp;&nbsp;<a class="moreless" id="ID12a" href=# onclick=\"return more('ID12')\">more></a><br /></p>"
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
echo '            <td width="150">'
echo '              <p class="row">Device supports DoP</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="DSDOUT" name="DSDOUT" size="32" value="'$DSDOUT'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Output device supports DSD over PCM (DoP)&nbsp;&nbsp;<a class="moreless" id="ID13a" href=# onclick=\"return more('ID13')\">more></a><br /></p>"
echo '              <div id="ID13" class="less">'
echo '                <p>LMS Server requires a DoP patch.</p>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td width="150">'
echo '              <p class="row">Visualiser support</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="VISULIZER" name="VISULIZER" size="32" value="'$VISULIZER'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Visualiser support*&nbsp;&nbsp;<a class="moreless" id="ID14a" href=# onclick=\"return more('ID14')\">more></a><br /></p>"
echo '              <div id="ID14" class="less">'
echo '                <p>*An option for jivelite if it gets ported to piCorePlayer. For now, not of any use.</p>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="even">'
echo '            <td width="150">'
echo '              <p class="row">Various input</p>'
echo '            </td>'
echo '            <td width="210">'
echo '              <input type="text" id="OTHER" name="OTHER" size="32" value="'$OTHER'">'
echo '            </td>'
echo '            <td width="550">'
echo "              <p>Add another command&nbsp;&nbsp;<a class="moreless" id="ID15a" href=# onclick=\"return more('ID15')\">more></a><br /></p>"
echo '              <div id="ID15" class="less">'
echo '                <p>Ensure to include the correct switch first, i.e. -n or -o etc</p>'
echo '              </div>'
echo '            </td>'
echo '          </tr>'
#------------------------------------------------------------------------------
echo '          <tr class="odd">'
echo '            <td colspan="3">'
echo '              <input type="submit" value="Submit">'
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
