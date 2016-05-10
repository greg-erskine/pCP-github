#!/bin/sh

# Version: 0.03 2015-09-19 SBP
#	Removed httpd decoding.

# Version: 0.02 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions
pcp_variables

pcp_html_head "Change Password" "GE" "5" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

if [ "$NEWPASSWORD" = "$CONFIRMPASSWORD" ]; then
	[ $DEBUG -eq 1 ] && echo '<p class="info">[ INFO ] Passwords OK. '$NEWPASSWORD' = '$CONFIRMPASSWORD'</p>'
	echo '<p class="info">[ INFO ] '
	echo "tc:"$NEWPASSWORD | sudo chpasswd
	echo '</p>'
	pcp_backup
	#####################################
	# TODO. Add code to update httpd.conf
	#####################################
else
	echo '<p class="error">[ ERROR ] Passwords NOT OK. '$NEWPASSWORD' ne '$CONFIRMPASSWORD'</p>'
fi

pcp_go_back_button

echo '</body>'
echo '</html>'