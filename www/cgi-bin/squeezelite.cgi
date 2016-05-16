#!/bin/sh

# Version: 0.25 2016-05-17 GE
#	Added multi ALSA_PARAMS.

# Version: 0.24 2016-03-29 PH
#	Fixed $VISUALISER and $IR_LIRC.
#	Changed log location to /var/log.

# Version: 0.23 2016-03-14 GE
#	Updated -e option.
#	Updated -U option.
#	Updated -V option.
#	Added -G option.
#	Added -S option.
#	Revised various help messages.
#	Updated -G option for Output Active High or Low. PH.
#	Updated $VISUALISER and $IR_LIRC.

# Version: 0.22 2016-02-22 GE
#	Updated for Raspberry Pi Zero.
#	Added support for raspidac3 and rpi_dac.

# Version: 0.21 2016-02-09 SBP
#	Change Output settings for alsaequal.

# Version: 0.20 2015-09-20 GE
#	Added -e option.
#	Added -U option (not working).
#	Added -V option (not working).

# Version: 0.19 2015-09-16 SBP
#	Added Raspberry Pi Model A.

# Version: 0.18 2015-09-01 GE
#	Fixed bug in pcp_squeezelite_alsa.

# Version: 0.17 2015-08-29 SBP
#	Removed pcp_squeezelite_visualiser.
#	Revised modes.
#	Turned pcp_picoreplayers tabs on in normal mode.
#	Revised initial mode settings.

# Version: 0.16 2015-07-01 GE
#	Added pcp_mode tabs.
#	Added pcp_picoreplayers tabs.

# Version: 0.15 2015-06-05 GE
#	Started adding HTML5 input field validation.
#	Added pcp_incr_id and pcp_start_row_shade.
#	Improved debug level setting.
#	Removed some unnecessary code.

# Version: 0.14 2015-03-13 GE
#	Updated and fixed spelling of the Visualiser option.
#	Added pcp_rpi_model_unknown checks.

# Version: 0.13 2015-03-06 GE
#	Updated help.

# Version: 0.12 2015-02-27 SBP
#	Added RPi2 support.

# Version: 0.11 2015-02-09 GE
#	Added Squeezelite command string.
#	Added copyright.
#	Updated descriptions and more/less help.
#	Removed maxsize=26 for player name.

# Version: 0.10 2015-01-23 SBP
#	Added CLOSEOUT.
#	Minor cosmetic changes.

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

. pcp-lms-functions
. pcp-rpi-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Squeezelite Settings" "SBP"

[ $MODE -ge $MODE_NORMAL ] && pcp_picoreplayers
[ $MODE -ge $MODE_ADVANCED ] && pcp_controls
pcp_banner
pcp_navigation

#========================================================================================
# Create Squeezelite command string
#----------------------------------------------------------------------------------------
STRING="/mnt/mmcblk0p2/tce/squeezelite-armv6hf "
[ x"" != x"$NAME" ]         && STRING="$STRING -n \"$NAME\""
[ x"" != x"$OUTPUT" ]       && STRING="$STRING -o $OUTPUT"
[ x"" != x"$ALSA_PARAMS" ]  && STRING="$STRING -a "$ALSA_PARAMS""
[ x"" != x"$BUFFER_SIZE" ]  && STRING="$STRING -b $BUFFER_SIZE"
[ x"" != x"$_CODEC" ]       && STRING="$STRING -c $_CODEC"
[ x"" != x"$XCODEC" ]       && STRING="$STRING -e $XCODEC"
[ x"" != x"$PRIORITY" ]     && STRING="$STRING -p $PRIORITY"
[ x"" != x"$MAX_RATE" ]     && STRING="$STRING -r $MAX_RATE"
[ x"" != x"$UPSAMPLE" ]     && STRING="$STRING -R $UPSAMPLE"
[ x"" != x"$MAC_ADDRESS" ]  && STRING="$STRING -m $MAC_ADDRESS"
[ x"" != x"$SERVER_IP" ]    && STRING="$STRING -s $SERVER_IP"
[ x"" != x"$LOGLEVEL" ]     && STRING="$STRING -d $LOGLEVEL -f ${LOGDIR}/pcp_squeezelite.log"
[ x"" != x"$DSDOUT" ]       && STRING="$STRING -D $DSDOUT"
[ "$VISUALISER" = "yes" ]   && STRING="$STRING -v"
[ x"" != x"$CLOSEOUT" ]     && STRING="$STRING -C $CLOSEOUT"
[ x"" != x"$UNMUTE" ]       && STRING="$STRING -U $UNMUTE"
[ x"" != x"$ALSAVOLUME" ]   && STRING="$STRING -V $ALSAVOLUME"
[ "$IR_LIRC" = "yes" ]      && STRING="$STRING -i $IR_CONFIG"
[ x"" != x"$POWER_GPIO" ]   && STRING="$STRING -G $POWER_GPIO:$POWER_OUTPUT"
[ x"" != x"$POWER_SCRIPT" ] && STRING="$STRING -S $POWER_SCRIPT"
[ x"" != x"$OTHER" ]        && STRING="$STRING $OTHER"
STRING="$STRING &"

#========================================================================================
# Missing squeezelite options
#----------------------------------------------------------------------------------------
#  -M <modelname>		Set the squeezelite player model name sent to the server (default: SqueezeLite)
#  -N <filename>		Store player name in filename to allow server defined name changes to be shared between servers (not supported with -n)
#  -P <filename>		Store the process id (PID) in filename

#========================================================================================
# Start table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="setaudio" action="chooseoutput.cgi" method="get" id="setaudio">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Choose audio output</legend>'
echo '            <table class="bggrey percent100">'
#--------------------------------------Audio output-------------------------------
case "$AUDIO" in
	Analog)      ANCHECKED="selected" ;;
	HDMI)        HDMICHECKED="selected" ;;
	USB)         USBCHECKED="selected" ;;
	I2SDAC)      I2DACCHECKED="selected";;
	I2SDIG)      I2DIGCHECKED="selected" ;;
	I2SAMP)      I2AMPCHECKED="selected" ;;
	IQaudio)     IQaudioCHECKED="selected" ;;
	I2SpDAC)     I2SDACpCHECKED="selected" ;;
	I2SpDIG)     I2SDIGpCHECKED="selected" ;;
	I2SpIQaudIO) IQaudIOpCHECKED="selected" ;;
	I2SpIQAMP)   IQAMPCHECKED="selected" ;;
	raspidac3)   raspidac3CHECKED="selected" ;;
	rpi_dac)     rpi_dacCHECKED="selected" ;;
	*)           CHECKED="Not set" ;;
esac

pcp_incr_id
pcp_start_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Audio output</p>'
echo '                </td>'
echo '                <td class="column350">'
echo '                  <select name="AUDIO">'
echo '                    <option value="Analog" '$ANCHECKED'>Analog audio:</option>'
echo '                    <option value="HDMI" '$HDMICHECKED'>HDMI audio:</option>'
echo '                    <option value="USB" '$USBCHECKED'>USB audio:</option>'

if [ $(pcp_rpi_is_hat) -ne 0 ] || [ $(pcp_rpi_model_unknown) -eq 0 ] || [ $MODE -ge $MODE_BETA ]; then
	echo '                    <option value="I2SDAC" '$I2DACCHECKED'>I2S audio: HiFiBerry/Sabre ES9023/TI PCM5102A</option>'
	echo '                    <option value="I2SDIG" '$I2DIGCHECKED'>I2S audio: HiFiBerry Digi</option>'
	echo '                    <option value="IQaudio" '$IQaudioCHECKED'>I2S audio: IQaudIO Pi-DAC</option>'
	echo '                    <option value="I2SAMP" '$I2AMPCHECKED'>I2S audio: HiFiBerry AMP</option>'
fi

if [ $(pcp_rpi_is_hat) -eq 0 ] || [ $(pcp_rpi_model_unknown) -eq 0 ] || [ $MODE -ge $MODE_BETA ]; then
	echo '                    <option value="I2SDAC" '$I2DACCHECKED'>I2S audio: generic</option>'
	echo '                    <option value="I2SpDAC" '$I2SDACpCHECKED'>I2S audio: HiFiBerry DAC+</option>'
	echo '                    <option value="I2SpDIG" '$I2SDIGpCHECKED'>I2S audio: HiFiBerry Digi+</option>'
	echo '                    <option value="I2SpIQaudIO" '$IQaudIOpCHECKED'>I2S audio: IQaudIO Pi-DAC+</option>'
	echo '                    <option value="I2SpIQAMP" '$IQAMPCHECKED'>I2S audio: IQaudIO Pi-(Digi)AMP+</option>'
	echo '                    <option value="I2SAMP" '$I2AMPCHECKED'>I2S audio: HiFiBerry AMP+</option>'
fi

echo '                    <option value="raspidac3" '$raspidac3CHECKED'>I2S audio: RaspiDAC Rev.3x</option>'
echo '                    <option value="rpi_dac" '$rpi_dacCHECKED'>I2S audio: RPi DAC</option>'

echo '                  </select>'
echo '                </td>'

echo '                <td>'
echo '                  <p>Select Audio output&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>Set Audio output before changing Squeezelite settings below.</p>'
echo '                    <p>This will overwrite some default values of the Squeezelite settings below. You may need to reset them.</p>'
echo '                  </div>'
echo '                </td>'

echo '              </tr>'
echo '              <tr>'
echo '                <td colspan="2">'
echo '                  <input type="submit" value="Save">'
echo '                </td>'
echo '              </tr>'

#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '  <tr>'
echo '    <td>'
echo '      <form name="squeeze" action="writetoconfig.cgi" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Change Squeezelite settings</legend>'
echo '            <table class="bggrey percent100">'
#--------------------------------------Name of your player-------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Name of your player</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="large15" type="text" name="NAME" value="'$NAME'" required pattern="^[^$&`/]*$">'
echo '                </td>'
echo '                <td>'
echo '                  <p>Specify the piCorePlayer name (-n)&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>&lt;name&gt;</p>'
echo '                    <p>This is the player name that will be used by LMS, it will appear in the web interface and apps.'
echo '                       It is recommended that you use standard alphanumeric characters for maximum compatibility.</p>'
echo '                    <p>Invalid characters:</p>'
echo '                    <ul>'
echo '                      <li>`</li>'
echo '                      <li>&</li>'
echo '                      <li>$</li>'
echo '                      <li>others</li>'
echo '                    </ul>'
echo '                    <p>Examples:</p>'
echo '                    <ul>'
echo '                      <li>piCorePlayer2</li>'
echo '                      <li>Main Stereo</li>'
echo '                      <li>Bed Room</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------

#--------------------------------------Output settings-----------------------------------
case "$ALSAeq" in
	yes) READONLY="readonly" ;;
	*)   READONLY="" ;;
esac

pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Output setting</p>'
echo '                </td>'
echo '                <td class="column210">'
echo '                  <input class="large15" type="text" name="OUTPUT" value="'$OUTPUT'" '$READONLY' pattern="^[a-zA-Z0-9:,=]*$">'
echo '                </td>'
echo '                <td>'

if [ "$ALSAeq" = "yes" ]; then
	echo '                  <p><b>Note:</b> ALSA equalizer has set the output to "equal".</p>'
else
	echo '                  <p>Specify the output device (-o)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;output device&gt;</p>'
	echo '                    <ul>'
	echo '                      <li>Default: default</li>'
	echo '                      <li>- = output to stdout</li>'
	echo '                    </ul>'
	echo '                    <p>Squeezelite found these output devices:</p>'
	echo '                    <ul>'
	                            /mnt/mmcblk0p2/tce/squeezelite-armv6hf -l | awk '/^  / { print "                      <li> "$1"</li>" }'
	echo '                    </ul>'
	echo '                    <p><b>Note:</b></p>'
	echo '                    <ul>'
	echo '                      <li>Sometimes clearing this field completely may help. This forces the default ALSA setting to be used.</li>'
	echo '                      <li>Using ALSA equalizer will set the output to "equal".</li>'
	echo '                    </ul>'
	echo '                  </div>'
fi

echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------

#--------------------------------------OLD ALSA settings---------------------------------
##### GE - OBSOLETE - DELETE ####
#----------------------------------------------------------------------------------------
pcp_old_squeezelite_alsa() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>OLD ALSA setting</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="ALSA_PARAMS" value="'$ALSA_PARAMS'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify the ALSA params to open output device (-a)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;b&gt;:&lt;p&gt;:&lt;f&gt;:&lt;m&gt;:&lt;d&gt;</p>'
	echo '                    <ul>'
	echo '                      <li>b = buffer time in ms or size in bytes</li>'
	echo '                      <li>p = period count or size in bytes</li>'
	echo '                      <li>f = sample format (16|24|24_3|32)</li>'
	echo '                      <li>m = use mmap (0|1)</li>'
	echo '                      <li>d = opens ALSA twice (undocumented) i.e. ::::d</li>'
	echo '                    </ul>'
	echo '                    <p>Buffer value &lt; 500 treated as buffer time in ms, otherwise size in bytes.</p>'
	echo '                    <p>Period value &lt; 50 treated as period count, otherwise size in bytes.</p>'
	echo '                    <p>mmap = memory map<p>'
	echo '                    <p>Sample format:<p>'
	echo '                    <ul>'
	echo '                      <li>16 = Signed 16 bit Little Endian</li>'
	echo '                      <li>24 = Signed 24 bit Little Endian using low three bytes in 32-bit word</li>'
	echo '                      <li>24_3 = Signed 24 bit Little Endian in 3bytes format</li>'
	echo '                      <li>32 = Signed 32 bit Big Endian</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_old_squeezelite_alsa
#----------------------------------------------------------------------------------------

#--------------------------------------ALSA settings-------------------------------------
pcp_squeezelite_alsa() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>ALSA setting</p>'
	echo '                </td>'
	echo '                <td class="column210">'

	                        ALSA_PARAMS1=$(echo $ALSA_PARAMS | cut -d: -f1 ) # b = buffer time in ms or size in bytes
	                        ALSA_PARAMS2=$(echo $ALSA_PARAMS | cut -d: -f2 ) # p = period count or size in bytes
	                        ALSA_PARAMS3=$(echo $ALSA_PARAMS | cut -d: -f3 ) # f = sample format (16|24|24_3|32)
	                        ALSA_PARAMS4=$(echo $ALSA_PARAMS | cut -d: -f4 ) # m = use mmap (0|1)
	                        ALSA_PARAMS5=$(echo $ALSA_PARAMS | cut -d: -f5 ) # d = opens ALSA twice

	echo '                  <input class="small3" type="text" name="ALSA_PARAMS1" value="'$ALSA_PARAMS1'" title="buffer time">'
	echo '                  <input class="small3" type="text" name="ALSA_PARAMS2" value="'$ALSA_PARAMS2'" title="period count">'
	echo '                  <input class="small3" type="text" name="ALSA_PARAMS3" value="'$ALSA_PARAMS3'" pattern="^(16|24|24_3|32)$" title="sample format ( 16 | 24 | 24_3 | 32 )">'
	echo '                  <input class="small1" type="text" name="ALSA_PARAMS4" value="'$ALSA_PARAMS4'" pattern="^[0-1]$" title="mmap ( 0 | 1 )">'
	echo '                  <input class="small1" type="text" name="ALSA_PARAMS5" value="'$ALSA_PARAMS5'" pattern="^[d]$" title="ALSA twice (d)">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify the ALSA params to open output device (-a)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;b&gt;:&lt;p&gt;:&lt;f&gt;:&lt;m&gt;:&lt;d&gt;</p>'
	echo '                    <ul>'
	echo '                      <li>b = buffer time in ms or size in bytes</li>'
	echo '                      <li>p = period count or size in bytes</li>'
	echo '                      <li>f = sample format (16|24|24_3|32)</li>'
	echo '                      <li>m = use mmap (0|1)</li>'
	echo '                      <li>d = opens ALSA twice (undocumented) i.e. ::::d</li>'
	echo '                    </ul>'
	echo '                    <p><b>Note:</b></p>'
	echo '                    <p>Buffer value &lt; 500 treated as buffer time in ms, otherwise size in bytes.</p>'
	echo '                    <p>Period value &lt; 50 treated as period count, otherwise size in bytes.</p>'
	echo '                    <p>mmap = memory map<p>'
	echo '                    <p><b>Sample format:</b><p>'
	echo '                    <ul>'
	echo '                      <li>16 = Signed 16 bit Little Endian</li>'
	echo '                      <li>24 = Signed 24 bit Little Endian using low 3 bytes in 32 bit word</li>'
	echo '                      <li>24_3 = Signed 24 bit Little Endian in 3 bytes format</li>'
	echo '                      <li>32 = Signed 32 bit Big Endian</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'

	if [ $DEBUG -eq 1 ]; then
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150">'
		echo '                </td>'
		echo '                <td class="column210">'
		echo '                  <input class="large15" type="text" name="ALSA_PARAMS" value="'$ALSA_PARAMS'" readonly>'
		echo '                </td>'
		echo '                <td>'
		echo '                </td>'
		echo '              </tr>'
	fi
}
[ $MODE -ge $MODE_BASIC ] && pcp_squeezelite_alsa
#----------------------------------------------------------------------------------------

#--------------------------------------Buffer size settings------------------------------
pcp_squeezelite_buffer() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Buffer size settings</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="BUFFER_SIZE" value="'$BUFFER_SIZE'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify internal Stream and Output buffer sizes in Kb (-b)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;stream&gt;:&lt;output&gt;</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_squeezelite_buffer
#----------------------------------------------------------------------------------------

#--------------------------------------Codec settings------------------------------------
pcp_squeezelite_codec() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Restrict codec setting</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="_CODEC" value="'$_CODEC'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Restrict codecs to those specified, otherwise load all available codecs (-c)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;codec1,codec2&gt;</p>'
	echo '                    <p>Known codecs:</p>'
	echo '                    <ul>'
	echo '                      <li>flac</li>'
	echo '                      <li>pcm</li>'
	echo '                      <li>mp3</li>'
	echo '                      <li>ogg</li>'
	echo '                      <li>aac</li>'
	echo '                      <li>wma</li>'
	echo '                      <li>alac</li>'
	echo '                      <li>mad, mpg for specific mp3 codec</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_squeezelite_codec
#----------------------------------------------------------------------------------------

#--------------------------------------Exclude Codec settings----------------------------
pcp_squeezelite_xcodec() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Exclude codec setting</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="XCODEC" value="'$XCODEC'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Explicitly exclude native support for one or more codecs (-e)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;codec1,codec2&gt;</p>'
	echo '                    <p>Known codecs:</p>'
	echo '                    <ul>'
	echo '                      <li>flac</li>'
	echo '                      <li>pcm</li>'
	echo '                      <li>mp3</li>'
	echo '                      <li>ogg</li>'
	echo '                      <li>aac</li>'
	echo '                      <li>wma</li>'
	echo '                      <li>alac</li>'
	echo '                      <li>dsd</li>'
	echo '                      <li>mad, mpg for specific mp3 codec</li>'
	echo '                    </ul>'
	echo '                    <p><b>Example: </b>dsd</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_squeezelite_xcodec
#----------------------------------------------------------------------------------------

#--------------------------------------Priority settings---------------------------------
pcp_squeezelite_priority() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">Priority setting</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="number" name="PRIORITY" value="'$PRIORITY'" min="1" max="99">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set real time priority of output thread (-p)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;priority&gt;</p>'
	echo '                    <p>Range: 1-99</p>'
	echo '                    <p>Default: 45</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_squeezelite_priority
#----------------------------------------------------------------------------------------

#--------------------------------------Max sample rate-----------------------------------
pcp_squeezelite_max_sample() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">Max sample rate</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="MAX_RATE" value="'$MAX_RATE'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Sample rates supported, allows output to be off when Squeezelite is started (-r)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;rates&gt;[:&lt;delay&gt;]</p>'
	echo '                    <ul>'
	echo '                      <li>rates = &lt;maxrate&gt;|&lt;minrate&gt;-&lt;maxrate&gt;|&lt;rate1&gt;,&lt;rate2&gt;,&lt;rate3&gt;</li>'
	echo '                      <li>delay = optional delay switching rates in ms</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_squeezelite_max_sample
#----------------------------------------------------------------------------------------

#--------------------------------------Upsample settings---------------------------------
pcp_squeezelite_upsample_settings() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">Upsample setting</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="UPSAMPLE" value="'$UPSAMPLE'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Resampling parameters (-R)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;recipe&gt;:&lt;flags&gt;:&lt;attenuation&gt;:&lt;precision&gt;:<br />'
	echo '                       &lt;passband_end&gt;:&lt;stopband_start&gt;:&lt;phase_response&gt;</p>'
	echo '                    <ul>'
	echo '                      <li>recipe = (v|h|m|l|q)(L|I|M)(s) [E|X]</li>'
	echo '                        <ul>'
	echo '                          <li>E = exception - resample only if native rate not supported</li>'
	echo '                          <li>X = async - resample to max rate for device, otherwise to max sync rate</li>'
	echo '                        </ul>'
	echo '                      <li>flags = num in hex</li>'
	echo '                      <li>attenuation = attenuation in dB to apply (default is -1db if not explicitly set)</li>'
	echo '                      <li>precision = number of bits precision (HQ = 20. VHQ = 28)</li>'
	echo '                      <li>passband_end = number in percent (0dB pt. bandwidth to preserve. nyquist = 100%)</li>'
	echo '                      <li>stopband_start = number in percent (Aliasing/imaging control. > passband_end)</li>'
	echo '                      <li>phase_response = 0-100 (0 = minimum / 50 = linear / 100 = maximum)</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_squeezelite_upsample_settings
#----------------------------------------------------------------------------------------

#--------------------------------------MAC address---------------------------------------
pcp_squeezelite_mac_address() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">MAC address</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="MAC_ADDRESS" value="'$MAC_ADDRESS'" pattern="^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set MAC address (-m)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;mac addr&gt;</p>'
	echo '                    <p>Format: ab:cd:ef:12:34:56</p>'
	echo '                    <p>This is used if you want to use a fake MAC address or you want to overwrite the default MAC address determined by Squeezelite.'
	echo '                       Usually you will not need to set a MAC address.</p>'
	echo '                    <p>By default Squeezelite will use one of the following MAC addresses:</p>'
	echo '                    <ul>'
	echo '                      <li>Physical MAC address: '$(pcp_eth0_mac_address)'</li>'
	echo '                      <li>Wireless MAC address: '$(pcp_wlan0_mac_address)'</li>'
	echo '                    </ul>'
	echo '                    <p><b>Note: </b>Squeezelite will ignore MAC addresses from the range 00:04:20:**:**:**</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_squeezelite_mac_address
#----------------------------------------------------------------------------------------

#--------------------------------------Squeezelite server IP-----------------------------
pcp_squeezelite_server_ip() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">LMS IP</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="SERVER_IP" value="'$SERVER_IP'" pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Connect to the specified LMS, otherwise autodiscovery will find the server (-s)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;server&gt;[:&lt;port&gt;]</p>'
	echo '                    <p>Default port: 3483</p>'
	echo '                    <p class="error"><b>Note:</b> Do not include the port number unless you have changed the default LMS port number.</p>'
	                          if [ "$LMSERVER" = "no" ]; then
	echo   '                    <p>Current LMS IP is:</p>'
	echo   '                    <ul>'
	echo   '                      <li>'$(pcp_lmsip)'</li>'
	echo   '                    </ul>'
	                          else
	echo   '                    <p>You have LMS enabled, if you also want to listen to music from this LMS on this pCP then use:</p>'
	echo   '                    <ul>'
	echo   '                      <li><b>127.0.0.1</b> in the LMS IP field</li>'
	echo   '                    </ul>'
	                          fi
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_squeezelite_server_ip
#----------------------------------------------------------------------------------------

#--------------------------------------Log level setting---------------------------------
pcp_squeezelite_log_level() {
	case "$LOGLEVEL" in
		all=info)         LOGLEVEL1="selected" ;;
		all=debug)        LOGLEVEL2="selected" ;;
		all=sdebug)       LOGLEVEL3="selected" ;;
		slimproto=info)   LOGLEVEL4="selected" ;;
		slimproto=debug)  LOGLEVEL5="selected" ;;
		slimproto=sdebug) LOGLEVEL6="selected" ;;
		stream=info)      LOGLEVEL7="selected" ;;
		stream=debug)     LOGLEVEL8="selected" ;;
		stream=sdebug)    LOGLEVEL9="selected" ;;
		decode=info)      LOGLEVEL10="selected" ;;
		decode=debug)     LOGLEVEL11="selected" ;;
		decode=sdebug)    LOGLEVEL12="selected" ;;
		output=info)      LOGLEVEL13="selected" ;;
		output=debug)     LOGLEVEL14="selected" ;;
		output=sdebug)    LOGLEVEL15="selected" ;;
		*)                LOGLEVEL0="selected" ;;
	esac

	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">Log level setting</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <select class="large15" name="LOGLEVEL">'
	echo '                    <option value="" '$LOGLEVEL0'>none</option>'
	echo '                    <option value="all=info" '$LOGLEVEL1'>all=info</option>'
	echo '                    <option value="all=debug" '$LOGLEVEL2'>all=debug</option>'
	echo '                    <option value="all=sdebug" '$LOGLEVEL3'>all=sdebug</option>'
	echo '                    <option value="slimproto=info" '$LOGLEVEL4'>slimproto=info</option>'
	echo '                    <option value="slimproto=debug" '$LOGLEVEL5'>slimproto=debug</option>'
	echo '                    <option value="slimproto=sdebug" '$LOGLEVEL6'>slimproto=sdebug</option>'
	echo '                    <option value="stream=info" '$LOGLEVEL7'>stream=info</option>'
	echo '                    <option value="stream=debug" '$LOGLEVEL8'>stream=debug</option>'
	echo '                    <option value="stream=sdebug" '$LOGLEVEL9'>stream=sdebug</option>'
	echo '                    <option value="decode=info" '$LOGLEVEL10'>decode=info</option>'
	echo '                    <option value="decode=debug" '$LOGLEVEL11'>decode=debug</option>'
	echo '                    <option value="decode=sdebug" '$LOGLEVEL12'>decode=sdebug</option>'
	echo '                    <option value="output=info" '$LOGLEVEL13'>output=info</option>'
	echo '                    <option value="output=debug" '$LOGLEVEL14'>output=debug</option>'
	echo '                    <option value="output=sdebug" '$LOGLEVEL15'>output=sdebug</option>'
	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set logging level (-d)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;log&gt;=&lt;level&gt;</p>'
	echo '                    <ul>'
	echo '                      <li>log: all|slimproto|stream|decode|output</li>'
	echo '                      <li>level: info|debug|sdebug</li>'
	echo '                    </ul>'
	echo '                    <p><b>Note:</b> Log file is /var/log/pcp_squeezelite.log</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_squeezelite_log_level
#----------------------------------------------------------------------------------------

#--------------------------------------Device supports DoP-------------------------------
pcp_squeezelite_dop() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">Device supports DoP</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="DSDOUT" value="'$DSDOUT'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Output device supports DSD over PCM (DoP) (-D)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;delay&gt;</p>'
	echo '                    <p>delay = optional delay switching between PCM and DoP in ms.</p>'
	echo '                    <p><b>Note: </b>LMS requires the DoP patch applied.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_squeezelite_dop
#----------------------------------------------------------------------------------------

#--------------------------------------Close output setting------------------------------
pcp_squeezelite_close_output() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">Close output setting</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="number" name="CLOSEOUT" value="'$CLOSEOUT'" min="1" max="1000">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set idle time before Squeezelite closes output (-C)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;timeout&gt;</p>'
	echo '                    <p>Value in seconds.</p>'
	echo '                    <p>Close output device when idle after timeout seconds, default is to keep it open while player is on.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_squeezelite_close_output
#----------------------------------------------------------------------------------------

#--------------------------------------Unmute ALSA control--------------------------------
pcp_squeezelite_unmute() {
	case "$UNMUTE" in
		PCM) UNMUTEYES="checked" ;;
		*) UNMUTENO="checked" ;;
	esac

	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">Unmute ALSA control</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="txt" name="UNMUTE" value="'$UNMUTE'">'
	echo '                </td>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set ALSA control to unmute and set to full volume (-U)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;control&gt;</p>'
	echo '                    <p>Unmute ALSA control and set to full volume.</p>'
	echo '                    <p><b>Note:</b> Not supported with -V option.</p>'

	echo '                    <p><b>You have the following audio cards:</b>' $(cat /proc/asound/cards | grep -Fr [ | awk '{print $1 " "  $4}')'</p>'
	echo '                    <p>For card 0 controls:' $(amixer scontrols -c0 | awk -F"'" '{print $2}')'</p>'
	echo '                    <p>For card 1 controls:' $(amixer scontrols -c1 | awk -F"'" '{print $2}')'</p>'
	echo '                    <p>For card 2 controls:' $(amixer scontrols -c2 | awk -F"'" '{print $2}')'</p>'

	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_squeezelite_unmute
#----------------------------------------------------------------------------------------

#--------------------------------------ALSA volume control-------------------------------
pcp_squeezelite_volume() {
	case "$ALSAVOLUME" in
		PCM) ALSAVOLUMEYES="checked" ;;
		*) ALSAVOLUMENO="checked" ;;
	esac

	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">ALSA volume control</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="txt" name="ALSAVOLUME" value="'$ALSAVOLUME'">'
	echo '                </td>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set ALSA control for volume adjustment (-V)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;control&gt;</p>'
	echo '                    <p>Use ALSA control for volume adjustment otherwise use software volume adjustment.</p>'

	echo '                    <p>Select and use the appropiate name of the possible controls from the list below.</p>'
	echo '                    <p><b>Note:</b> Not supported with -U option.</p>'
	echo '                    <p><b>You have the following audio cards:</b>' $(cat /proc/asound/cards | grep -Fr [ | awk '{print $1 " "  $4}')'</p>'
	echo '                    <p>For card 0 controls:' $(amixer scontrols -c0 | awk -F"'" '{print $2}')'</p>'
	echo '                    <p>For card 1 controls:' $(amixer scontrols -c1 | awk -F"'" '{print $2}')'</p>'
	echo '                    <p>For card 2 controls:' $(amixer scontrols -c2 | awk -F"'" '{print $2}')'</p>'

	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_BETA ] && pcp_squeezelite_volume
#----------------------------------------------------------------------------------------

#--------------------------------------Power On/Off GPIO---------------------------------
pcp_squeezelite_power_gpio() {
	if [ -n "$POWER_GPIO" ]; then
		case "$POWER_OUTPUT" in
			H) POH="checked" ;;
			L) POL="checked" ;;
		esac
	fi

	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">Power On/Off GPIO</p>'
	echo '                  <p class="row">Output is Active</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <p><input class="large15" type="number" name="POWER_GPIO" value="'$POWER_GPIO'" min="1"	max="40"></p>'
	echo '                  <input class="small1" type="radio" name="POWER_OUTPUT" value="H" '$POH'>High&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="POWER_OUTPUT" value="L" '$POL'>Low'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Power On/Off GPIO (-G)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;gpio&gt;:&lt;H|L&gt;</p>'
	echo '                    <p>Squeezelite will toggle this GPIO when the Power On/Off button is pressed.</p>'
	echo '                    <p>H or L to tell Squeezlite if the output should be active High or Low.</p>'
	echo '                    <p class="error"><b>WARNING:</b></p>'
	echo '                    <p class="error">Use caution when connecting to GPIOs. PERMANENT damage can occur.</p>'
	echo '                    <p class="error">If using mains voltages ensure you are FULLY QUALIFIED. DEATH can occur.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_BETA ] && [ $(pcp_squeezelite_build_option GPIO ) -eq 0 ] && pcp_squeezelite_power_gpio
#----------------------------------------------------------------------------------------

#--------------------------------------Power On/Off Script-------------------------------
pcp_squeezelite_power_script() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">Power On/Off Script</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="POWER_SCRIPT" value="'$POWER_SCRIPT'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Power On/Off Script (-S)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;/path/script.sh&gt;</p>'
	echo '                    <p>Squeezelite will run this script when the Power On/Off button is pressed.</p>'
	echo '                    <p class="error"><b>WARNING:</b></p>'
	echo '                    <p class="error">Use caution when connecting to GPIOs. PERMANENT damage can occur.</p>'
	echo '                    <p class="error">If using mains voltages ensure you are FULLY QUALIFIED. DEATH can occur.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_BETA ] && [ $(pcp_squeezelite_build_option GPIO) -eq 0 ] && pcp_squeezelite_power_script
#----------------------------------------------------------------------------------------

#--------------------------------------Various input-------------------------------------
pcp_squeezelite_various_input() {
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p class="row">Various input</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="OTHER" value="'$OTHER'">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Add another option&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Use this field to add options that are supported by Squeezelite but unavailable in the piCorePlayer web interface.</p>'
	echo '                    <p><b>Note: </b>Ensure to include the correct switch first, i.e. -n or -o etc</p>'
	echo '                    <p><b>Example: </b>-e dsd</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_squeezelite_various_input
#----------------------------------------------------------------------------------------

#--------------------------------------Submit button-------------------------------------
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td  class="column150">'
echo '                  <input type="submit" name="SUBMIT" value="Save">'
echo '                  <input type="hidden" name="FROM_PAGE" value="squeezelite">'
echo '                </td>'

if [ $MODE -ge $MODE_ADVANCED ]; then
	echo '                <td colspan="2">'
	echo '                  <p>Squeezelite command string&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Warning: </b>For advanced users only!</p>'
	echo '                    <p>'$STRING'</p>'
	echo '                    <p><b>Hint: </b>Triple click on command then press [Ctrl]+[c] to copy.</p>'
	echo '                    <p><b>Note: </b>Maximum length is 512 characters.</p>'
	echo '                  </div>'
	echo '                </td>'
fi

echo '              </tr>'
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

[ $DEBUG -eq 1 ] && pcp_show_config_cfg
pcp_footer
[ $MODE -ge $MODE_NORMAL ] && pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'
