#!/bin/sh
. pcp-functions
pcp_variables
. $CONFIGCFG

case "$AUDIO" in
	Analog*)
		ANCHECKED="checked"
		;;
	HDMI*)
		HDMICHECKED="checked"
		;;
	USB*)
		USBCHECKED="checked"
		;;
	I2SDAC*)
		I2DACCHECKED="checked"
		;;
	I2SDIG*)
		I2DIGCHECKED="checked"
		;;
	IQaudio*)
		IQaudioCHECKED="checked"
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
echo '  <title>pCP - Main Page</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Main Page" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_controls
pcp_banner
pcp_navigation

echo '<table border="0" width="960">'
echo ' <tr>'
echo '  <td>'
echo '   <form name="setaudio" action="chooseoutput.cgi" method="get" id="setaudio">'
echo '    <div class="row">'
echo '    <fieldset>'
echo '    <legend>Choose audio output</legend>'

echo '     <table border="0">'
echo '      <tr class="odd">'
echo '       <td width="300">'
echo '        <p><input type="radio" name="AUDIO" value="Analog" id="ANALOG" '$ANCHECKED'> Analog audio</p>'
echo '       </td>'
echo '       <td width="640">'
echo '        <p>Will load optimal analog Squeezelite settings - can be changed later.</p>'
echo '       </td>'
echo '      </tr>'

echo '      <tr class="even">'
echo '       <td width="300">'
echo '        <p><input type="radio" name="AUDIO" value="HDMI" id="HDMI" '$HDMICHECKED'> HDMI audio</p>'
echo '       </td>'
echo '       <td width="640">'
echo '        <p>[REBOOT NEEDED] Will load optimal HDMI Squeezelite settings - can be changed later.</p>'
echo '       </td>'
echo '      </tr>'

echo '      <tr class="odd">'
echo '       <td width="300">'
echo '        <p><input type="radio" name="AUDIO" value="USB" id="USB" '$USBCHECKED'> USB audio</p>'
echo '       </td>'
echo '       <td width="640">'
echo '        <p>You will need to change <em>Squeezelite output settings</em> to fit your USB-DAC.</p>'
echo '       </td>'
echo '      </tr>'

echo '      <tr class="even">'
echo '       <td width="300">'
echo '        <p><input type="radio" name="AUDIO" value="I2SDAC" id="I2SDAC" '$I2DACCHECKED'> I2S-audio DAC (HiFiBerry or Sabre ES9023)</p>'
echo '       </td>'
echo '       <td width="640">'
echo '        <p>You might need to change Squeezelite settings to fit your HiFiBerry/Sabre ES9023-DAC.</p>'
echo '       </td>'
echo '      </tr>'

echo '      <tr class="odd">'
echo '       <td width="300">'
echo '        <p><input type="radio" name="AUDIO" value="I2SDIG" id="I2SDIG" '$I2DIGCHECKED'> I2S-audio Digi (HiFiBerry I2S Digi)</p>'
echo '       </td>'
echo '       <td width="640">'
echo '        <p>You might need to change Squeezelite settings to fit your HiFiBerry-Digi.</p>'
echo '       </td>'
echo '      </tr>'

echo '      <tr class="even">'
echo '       <td width="300">'
echo '        <p><input type="radio" name="AUDIO" value="IQaudio" id="IQaudio" '$IQaudioCHECKED'> I2S-audio IQaudIO (IQaudIO I2S DAC)</p>'
echo '       </td>'
echo '       <td width="640">'
echo '        <p>You might need to change Squeezelite settings to fit your IQaudIO-DAC.</p>'
echo '       </td>'
echo '      </tr>'
echo '      <tr class="odd">'
echo '       <td width="300">'
echo '        <input type="submit" value="Submit">'
echo '       </td>'
echo '       <td>'
echo '        <p>&nbsp</p>'
echo '       </td>'
echo '      </tr>'
echo '     </table>'
echo '    </fieldset>'
echo '   </form>'

echo '   <form name="USBoptions" action="usboption.cgi" method="get">'
echo '    <table border="0" width="960">'
echo '     <tr>'
echo '      <td width="300">'
echo '       <input type="submit" value="List available ALSA devices">'
echo '      </td>'
echo '      <td>'
echo '       <p>List the available <em>ALSA output devices</em>, so you can copy it and use below - this is important if you use USB-DAC.</p>'
echo '      </td>'
echo '     </tr>'
echo '    </table>'
echo '   </form>'
echo '  </td>'
echo ' </tr>'
echo '</table>'
echo '</div>'

echo '<h2>Change Squeezelite settings:</h2>'

echo '<table width="960">'
echo '  <form name="squeeze" action="writetoconfig.cgi" method="get">'
echo '    <tr class="odd">'
echo '      <td width="150"><p>Name of your player</p></td>'
echo '      <td width="210"><input type="text" id="NAME" name="NAME" size="32" maxlength="26" value="'$NAME'"></td>'
echo '      <td><p>Set the player name</p></td>'
echo '    </tr>'
echo '    <tr class="even">'
echo '      <td width="150"><p>Output settings</p></td>'
echo '      <td width="210"><input type="text" id="OUTPUT" name="OUTPUT" size="32" value="'$OUTPUT'"></td>'
echo '      <td><p>Specify output device, default = default</p></td>'
echo '    </tr>'
echo '    <tr class="odd">'
echo '       <td width="150"><p>ALSA settings</p></td>'
echo '       <td width="210"><input type="text" id="ALSA_PARAMS" name="ALSA_PARAMS" size="32" value="'$ALSA_PARAMS'"></td>'
echo '       <td><p>b : p : f : m : d  / b = buffer time, p = period count, f sample format (16|24|24_3|32), m = use mmap (0|1) (d is non-documented and opens ALSA twice like -a ::::d) </p></td>'
echo '    </tr>'
echo '    <tr class="even">'
echo '       <td width="150"><p>Buffer size settings</p></td>'
echo '       <td width="210"><input type="text" id="BUFFER_SIZE" name="BUFFER_SIZE" size="32" value="'$BUFFER_SIZE'"></td>'
echo '       <td><p>stream : output - Specify internal Stream and Output buffer sizes in Kbytes</td>'
echo '    </tr>'
echo '    <tr class="odd">'
echo '      <td width="150"><p>Codec settings</p></td>'
echo '      <td width="210"><input type="text" id="_CODEC" name="_CODEC" size="32" value="'$_CODEC'"></td>'
echo '      <td><p>codec1,codec2 - Restrict codecs, otherwise load all available codecs; known codecs: flac,pcm,mp3,ogg,aac,wma,alac (mad,mpg for specific mp3 codec)</p></td>'
echo '    </tr>'
echo '    <tr class="even">'
echo '      <td width="150"><p class="row">Priority settings</p></td>'
echo '      <td width="210"><input type="text" id="PRIORITY" name="PRIORITY" size="32" value="'$PRIORITY'"></td>'
echo '      <td><p>priority - Set real time priority of output thread (1-99)</p></td>'
echo '    </tr>'
echo '    <tr class="odd">'
echo '      <td width="150"><p class="row">Max sample rate</p></td>'
echo '      <td width="210"><input type="text" id="MAX_RATE" name="MAX_RATE" size="32" value="'$MAX_RATE'"></td>'
echo '      <td><p>rate - Max sample rate for output device, enables output device to be off when Squeezelite is started</p></td>'
echo '    </tr>'
echo '    <tr class="even">'
echo '      <td width="150"><p class="row">Upsample settings</p></td>'
echo '      <td width="210"><input type="text" id="UPSAMPLE" name="UPSAMPLE" size="32" value="'$UPSAMPLE'"></td>'
echo '      <td><p>Please read more on <a href="https://code.google.com/p/squeezelite/">Squeezelite web page</p></td>'
echo '    </tr>'
echo '    <tr class="odd">'
echo '      <td width="150"><p class="row">MAC address</p></td>'
echo '      <td width="210"><input type="text" id="MAC_ADDRESS" name="MAC_ADDRESS" size="32" value="'$MAC_ADDRESS'"></td>'
echo '      <td><p>Set mac address, format: ab:cd:ef:12:34:56. Your RPIs physical MAC is: <em>'$(pcp_controls_mac_address)'</em> Copy paste if you want to use it</p></td>'
echo '    </tr>'
echo '    <tr class="even">'
echo '      <td width="150"><p class="row">Squeezelite server IP</p></td>'
echo '      <td width="210"><input type="text" id="SERVER_IP" name="SERVER_IP" size="32" value="'$SERVER_IP'"></td>'
echo '      <td><p>server:port - Connect to specified server, (use port 3483 (default)) otherwise uses autodiscovery to find server</p></td>'
echo '    </tr>'
echo '    <tr class="odd">'
echo '      <td width="150"><p class="row">Log level setting</p></td>'
echo '      <td width="210"><input type="text" id="LOGLEVEL" name="LOGLEVEL" size="32" value="'$LOGLEVEL'"></td>'
echo '      <td><p>log=level - Set logging level, logs: all|slimproto|stream|decode|output, level: info|debug|sdebug</p></td>'
echo '    </tr>'
echo '    <tr class="even">'
echo '      <td width="150"><p class="row">Log file name</p></td>'
echo '      <td width="210"><input type="text" id="LOGFILE" name="LOGFILE" size="32" value="'$LOGFILE'"></td>'
echo '      <td><p>Write debug to logfile at attached USB stick - should be present during booting</p></td>'
echo '    </tr>'
echo '    <tr class="odd">'
echo '      <td width="150"><p class="row">Device supports DoP</p></td>'
echo '      <td width="210"><input type="text" id="DSDOUT" name="DSDOUT" size="32" value="'$DSDOUT'"></td>'
echo '      <td><p>Output device supports DSD over PCM DoP needs a patch in LMS Server</p></td>'
echo '    </tr>'
echo '    <tr class="even">'
echo '      <td width="150"><p class="row">Visualizer support</p></td>'
echo '      <td width="210"><input type="text" id="VISULIZER" name="VISULIZER" size="32" value="'$VISULIZER'"></td>'
echo '      <td><p>Visualizer support - if and when jivelite ever get ported to piCorePlayer, for now not of much use</p></td>'
echo '    </tr>'
echo '    <tr class="odd">'
echo '      <td width="150"><p class="row">Various input</p></td>'
echo '      <td width="210"><input type="text" id="OTHER" name="OTHER" size="32" value="'$OTHER'"></td>'
echo '      <td><p>Add another command here, please use the correct switch first like -n or -o etc</p></td>'
echo '    </tr>'
echo '    <tr class="even">'
echo '      <td colspan="3"><input type="submit" value="Submit"></td>'
echo '    </tr>'
echo '  </form>'
echo '</table>'

[ $DEBUG = 1 ] && pcp_show_config_cfg
pcp_refresh_button
pcp_footer

echo '</body>'
echo '</html>'
