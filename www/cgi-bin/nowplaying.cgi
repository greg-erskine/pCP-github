#!/bin/sh

# This page is meant to be embedded in an IFRAME

. pcp-functions
. pcp-lms-functions

echo 'Content-Type: text/html'
echo ''
echo '<!DOCTYPE html>'
echo '<!-- Start of pcp_html_head -->'
echo '<!-- Code and style taken from https://github.com/Logitech/slimserver -->'
echo '<!-- Logitech Media Server Copyright 2001-2009 Logitech -->'
echo '<html lang="en">'
echo '<head>'
echo '  <meta charset="UTF-8">'
echo '  <title>pCP - NowPlaying</title>'
echo '  <meta name="author" content="PH">'
echo '  <meta name="description" content="NowPlaying">'
echo '  <link rel="icon" href="../images/pCP.png" type="image/x-icon" />'
echo '  <script src="../js/piCorePlayer.js"></script>'
echo '  <script src="../js/NowPlaying.js"></script>'
echo '  <link rel="stylesheet" type="text/css" href="../css/NowPlaying.css?'$(date -r ../css/NowPlaying.css +%H%M%S)'">'
echo '</head>'
echo ''
echo '<body>'
echo '<!-- End of pcp_html_head -->'

[ x"" = x"$LMSWEBPORT" ] && LMSPORT=9000 || LMSPORT=$LMSWEBPORT 
LMSIP=$(pcp_lmsip)

echo '<body>'
echo ' <div id="playerbox">'
echo '  <table id="ctrlBar" border="0" cellspacing="0" cellpadding="0">'
echo '   <tr>'
echo '    <td width="50%">'
echo '     <table style="border-collapse:collapse; border:0px; border-spacing:0px; padding:0px;">'
echo '      <tr>'

#  Play/Next Buttons
echo '       <td id="ctrlPrevious">'
echo '        <table border="0" cellpadding="0" cellspacing="0" id="ext-gen3" class="btn-previous">'
echo '         <tbody>'
echo '          <tr>'
echo '           <td></td>'
echo '           <td>'
echo '            <button type="button" style="padding: 0px; width: 31px;" class="x-btn-22" id="ext-gen4" onclick="lms_controls_send('\'''$LMSIP''\'', '\'''$LMSPORT''\'', '\'''$NAME''\'', '\''playlist'\'', '\''jump'\'', '\''-1'\'')" title="Previous"></button>'
echo '           </td>'
echo '           <td></td>'
echo '          </tr>'
echo '         </tbody>'
echo '        </table>'
echo '       </td>'

echo '       <td id="ctrlTogglePlay">'
echo '        <table border="0" cellpadding="0" cellspacing="0" id="toggleplay" class="btn-pause">'
echo '         <tbody>'
echo '          <tr>'
echo '           <td></td>'
echo '           <td>'
echo '            <button type="button" style="padding: 0px; width: 31px;" class="x-btn-22" id="btn-toggle-play" onclick="togglePause();" title="Pause"></button>'
echo '           </td>'
echo '           <td></td>'
echo '          </tr>'
echo '         </tbody>'
echo '        </table>'
echo '       </td>'

echo '       <td id="ctrlNext">'
echo '        <table border="0" cellpadding="0" cellspacing="0" id="ext-gen7" class="btn-next">'
echo '         <tbody>'
echo '          <tr>'
echo '           <td></td>'
echo '           <td>'
echo '            <button type="button" style="padding: 0px; width: 31px;" class="x-btn-22" id="ext-gen8" onclick="lms_controls_send('\'''$LMSIP''\'', '\'''$LMSPORT''\'', '\'''$NAME''\'', '\''playlist'\'', '\''jump'\'', '\''+1'\'')" title="Next"></button>'
echo '           </td>'
echo '           <td></td>'
echo '          </tr>'
echo '         </tbody>'
echo '        </table>'
echo '       </td>'

echo '       <td><img src="../images/spacer.gif" alt="" border="0" width="8" /></td>'

# Repeat/Shuffle
echo '       <td id="ctrlRepeat">'
echo '        <table border="0" cellpadding="0" cellspacing="0" id="btn-repeat" class="btn-repeat-0">'
echo '         <tbody>'
echo '          <tr>'
echo '           <td></td>'
echo '           <td>'
echo '            <button type="button" style="padding: 0px; width: 31px;" class="x-btn-22" id="btn-repeat-text" onclick="updateRepeat(123);" title="Repeat off"></button>'
echo '           </td>'
echo '           <td></td>'
echo '          </tr>'
echo '         </tbody>'
echo '        </table>'
echo '       </td>'

echo '       <td id="ctrlShuffle">'
echo '        <table border="0" cellpadding="0" cellspacing="0" id="btn-shuffle" class="btn-shuffle-0">'
echo '         <tbody>'
echo '          <tr>'
echo '           <td></td>'
echo '           <td>'
echo '             <button type="button" style="padding: 0px; width: 31px;" class="x-btn-22" id="btn-shuffle-text" onclick="updateShuffle(123);" title="Shuffle - Don'\''t Shuffle Playlist"></button>'
echo '           </td>'
echo '           <td></td>'
echo '          </tr>'
echo '         </tbody>'
echo '        </table>'
echo '       </td>'

echo '       <td><img src="../images/spacer.gif" alt="" border="0" width="8" /></td>'

# RandomPlay Button
echo '       <td id="ctrlRandom">'
echo '        <table border="0" cellpadding="0" cellspacing="0" id="btn-random" class="btn-random">'
echo '         <tbody>'
echo '          <tr>'
echo '           <td></td>'
echo '           <td>'
echo '            <button type="button" style="padding: 0px; width: 31px;" class="x-btn-22" id="btn-random" onclick="RandomPlay();" title="Random Play"></button>'
echo '           </td>'
echo '           <td></td>'
echo '          </tr>'
echo '         </tbody>'
echo '        </table>'
echo '       </td>'

echo '      </tr>'
echo '     </table>'
echo '    </td>'

### Volume Section
echo '    <td style="width:30%;">'
echo '     <table style="border-collapse:collapse; border:0px; border-spacing:0px; padding:0px; float:right;">'
echo '      <tr>'

echo '       <td id="ctrlVolumeDown" class="ctrlVolume">'
echo '        <table id="ext-gen13" class="btn-volume-decrease">'
echo '         <tbody>'
echo '          <tr>'
echo '           <td></td>'
echo '           <td >'
echo '            <button type="button" style="padding: 0px; width: 27px;" class="x-btn-22" id="ext-gen14" onclick="lms_controls_send('\'''$LMSIP''\'', '\'''$LMSPORT''\'', '\'''$NAME''\'', '\''mixer'\'', '\''volume'\'', '\''-5'\'')" title="Softer"></button>'
echo '          </td>'
echo '          <td></td>'
echo '          </tr>'
echo '         </tbody>'
echo '        </table>'
echo '       </td>'

echo '       <td id="ctrlVolume" class="ctrlVolume5">'
echo '        <img src="../images/spacer.gif" alt="" style="display:block;" onclick="setVolume(event);">'
echo '       </td>'

echo '       <td id="ctrlVolumeUp" class="ctrlVolume">'
echo '        <table id="ext-gen15" class="btn-volume-increase">'
echo '         <tbody>'
echo '          <tr>'
echo '           <td></td>'
echo '           <td>'
echo '            <button type="button" style="padding: 0px; width: 27px;" class="x-btn-22" id="ext-gen16" onclick="lms_controls_send('\'''$LMSIP''\'', '\'''$LMSPORT''\'', '\'''$NAME''\'', '\''mixer'\'', '\''volume'\'', '\''+5'\'')" title="Louder"></button>'
echo '           </td>'
echo '           <td></td>'
echo '          </tr>'
echo '         </tbody>'
echo '        </table>'
echo '       </td>'
echo '      </tr>'
echo '     </table>'
echo '    </td>'

### Power Button
echo '    <td style="width:25%;">'
echo '     <span id="ctrlPower" style="float:right">'
echo '      <table border="0" cellpadding="0" cellspacing="0" id="btn-pwr" class="btn-power">'
echo '       <tbody>'
echo '        <tr>'
echo '         <td></td>'
echo '         <td>'
echo '          <button type="button" style="padding: 0px; width: 24px;" class="x-btn-24" id="btn-pwr-text" title="Power: on" onclick="lms_controls_send('\'''$LMSIP''\'', '\'''$LMSPORT''\'', '\'''$NAME''\'', '\''power'\''); Power(1);"></button>'
echo '         </td>'
echo '         <td></td>'
echo '        </tr>'
echo '       </tbody>'
echo '      </table>'
echo '     </span>'
echo '    </td>'

echo '    <td><img src="../images/spacer.gif" alt="" height="10" width="5" border="0" /></td>'
echo '    <td align="right" valign="top">'
echo '     <table border="0" cellspacing="0" cellpadding="0">'
echo '      <tr>'
echo '       <td>'
echo '        <div id="ctrlUndock" style="visibility:hidden"></div>'
echo '       </td>'
echo '      </tr>'
echo '      <tr>'
echo '       <td>'
echo '        <div id="ctrlCollapse"></div>'
echo '        <div id="ctrlExpand"></div>'
echo '       </td>'
echo '      </tr>'
echo '     </table>'
echo '    </td>'
echo '   </tr>'
echo '  </table>'

echo '  <div id="expandedPlayerPanel">'
echo '   <div id="ctrlCurrentArt">'
echo '    <img id="image" src="" alt="" height="96" width="96" border="0"/>'
echo '   </div>'
echo '   <div id="ctrlCurrentSongInfo">'
echo '    <div id="ctrlCurrentTitle"></div>'
echo '    <div id="ctrlTrackInfo" class="currentTrackInfo">'
echo '     <div id="ctrlCurrentArtist"></div>'
echo '     <div id="ctrlCurrentAlbum"></div>'
echo '     <div id="ctrlBitrate"></div>'
echo '    </div>'
echo '    <div id="ctrlPlaytimePanel">'
echo '     <div id="ctrlPlaytime"></div>'
echo '     <div>'
echo '      <div id="ctrlProgress">'
echo '       <img src="../images/spacer.gif" onclick="setProgress(event);" class="progressLeft"/><img id="fill_left" src="../images/spacer.gif" onclick="setProgress(event);" class="progressFillLeft"/><img src="../images/spacer.gif" onclick="setProgress(event);" class="progressIndicator"/><img id="fill_right" src="../images/spacer.gif" onclick="setProgress(event);" class="progressFillRight"/><img src="../images/spacer.gif" onclick="setProgress(event);" class="progressRight"/>'
echo '      </div>'
echo '     </div>'
echo '     <div id="ctrlPlaytimeRight">'
echo '      <span id="ctrlRemainingTime"></span>'
echo '      &nbsp;(<span id="ctrlPlayNum"></span>&nbsp;of&nbsp;<span id="ctrlSongCount"></span>)'
echo '     </div>'
echo '    </div>'
echo '   </div>'
echo '  </div>'
echo ' </div>'

echo '<script>'
echo '  url = "http://'$LMSIP':'$LMSPORT'";'
echo '  playerName = "'$NAME'";'
echo '  function checkIfVisible(){'
echo '    if (document.getElementById("playerbox").offsetHeight > 0) {'
echo '      SetUpdates(true);'
echo '    } else {'
echo '      SetUpdates(false);'
echo '    }'
echo '  setTimeout("checkIfVisible()",1000);'
echo '  }'
echo '  checkIfVisible();'

echo '  function generate_lms_command (...restArgs) {'
echo '    var args = makeArgs("'$LMSIP'", "'$LMSPORT'", "'$NAME'");'
echo '    Array.prototype.push.apply(args, restArgs);'
echo '    lms_controls_send.apply(this, args);'
echo '  };'

echo '</script>'
echo '</body>'
echo '</html>'
