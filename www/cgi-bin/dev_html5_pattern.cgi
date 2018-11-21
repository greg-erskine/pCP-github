#!/bin/sh

# Version: 4.1.0 2018-09-20

# Title: HTML5 Pattern Test
# Description: Used for testing HTML regex pattern matching

. pcp-functions

pcp_html_head "HTML5 Pattern Test Page" "PH"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string_no_decode

#========================================================================================
# Main table
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>HTML5 Pattern Test</legend>'
pcp_start_row_shade
echo '          <form name="LMS" action="'$0'">'
echo '            <table class="bggrey percent100">'
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150 center">'
echo '                  <p>Submit</p>'
echo '                </td>'
echo '                <td class="column300">'
echo '                  <p>Enter HTML5 Pattern Here.</p>'
echo '                </td>'
echo '                <td class="column300">'
echo '                  <p>Type test strings here.</p>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150 center">'
echo '                  <button type="submit" name="ACTION" value="Submit">Submit</button>'
echo '                </td>'
echo '                <td class="column300">'
echo '                  <input id="PATTERN" class="large22" type="text" name="PATTERN" onchange="setpattern()">'
echo '                </td>'
echo '                <td class="column300">'
echo '                  <input id="TEST" class="large22" type="text" name="TEST" required pattern="" onclick="setpattern()">'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </form>'
echo '          <table class="bggrey percent100">'
pcp_toggle_row_shade
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150 center">'
echo '                <p>CGI Pattern Code</p>'
echo '              </td>'
echo '              <td>'
echo '                <p id="OUT">Enter HTML5 Pattern Here.</p>'
echo '              </td>'
echo '            </tr>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

echo '<script>'
echo '  var Box = "PATTERN";'
echo '  var Box1 = "TEST";'
echo '  var pattern = "'${PATTERN}'";'
echo '  var test = "'${TEST}'";'
echo '  document.getElementById(Box).value = decodeURIComponent(pattern.replace(/\+/g, "%20"));'
echo '  document.getElementById(Box1).value = decodeURIComponent(test.replace(/\+/g, "%20"));'
echo '  function setpattern() {'
echo '    document.getElementById(Box1).pattern = document.getElementById(Box).value;'
echo '  }'
echo '  function setout() {'
echo '    var tmp = "pattern=\"" + decodeURIComponent(pattern.replace(/\+/g, "%20")) + "\"";'
echo '    document.getElementById("OUT").innerHTML = tmp.replace(/\\/g, "\\\\");'
echo '  }'
echo '  setpattern();'
echo '  setout();'
echo '</script>'

pcp_footer
[ $MODE -ge $MODE_NORMAL ] && pcp_mode
pcp_copyright

echo '</body>'
echo '</html>'