#!/bin/sh

# Version: 0.01 2014-11-07 GE
#	Original.

status() {
	echo Status: $1
}

#sudo sh -c 'echo 17 > /sys/class/gpio/export'
#sudo sh -c 'echo "out" > /sys/class/gpio/gpio17/direction'
#sudo sh -c 'echo "0" > /sys/class/gpio/gpio17/active_low'

#cat /sys/class/gpio/gpio17/direction
#cat /sys/class/gpio/gpio17/value

. pcp-functions
pcp_variables
pcp_html_head "Relay" "GE"
pcp_banner

echo '<table border="1" bgcolor="d8d8d8" cellspacing="0" cellpadding="0" width="960">'

for i in 1 2 3 4
do
	echo '  <tr>'
	echo '    <td>'
	echo '      <p>Relay '$i'</p>'
	echo '    </td>'
	echo '    <td>'
	echo '      <form name="relay'$i'-on" action="relay_controls.cgi" method="get" id="relay'$i'-on">'
	echo '        <input type="hidden" name="RELAY" value="RLY'$i'"/>'
	echo '        <input type="hidden" name="ACTION" value="on"/>'
	echo '        <input type="submit" value="On" />'
	echo '      </form>'
	echo '    </td>'
	echo '    <td>'
	echo '      <form name="relay'$i'-off" action="relay_controls.cgi" method="get" id="relay'$i'-off">'
	echo '        <input type="hidden" name="RELAY" value="RLY'$i'"/>'
	echo '        <input type="hidden" name="ACTION" value="off"/>'
	echo '        <input type="submit" value="Off" />'
	echo '      </form>'
	echo '    </td>'
	echo '    <td>'
	echo '      <p>'$(status $i)'</p>'
	echo '    </td>'
	echo '  </tr>'
done

echo '</table>'

pcp_footer

echo '</body>'
echo '</html>'