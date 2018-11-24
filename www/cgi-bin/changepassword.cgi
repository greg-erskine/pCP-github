#!/bin/sh

# Version: 4.1.0 2018-09-19

. pcp-functions

pcp_html_head "Change Password" "GE" "5" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

pcp_table_top

if [ "$NEWPASSWORD" = "$CONFIRMPASSWORD" ]; then
	[ $DEBUG -eq 1 ] && echo '<p class="info">[ OK ] Passwords OK. '$NEWPASSWORD' = '$CONFIRMPASSWORD'</p>'
	echo '<p class="ok">[ OK ] '
	echo "tc:"$NEWPASSWORD | sudo chpasswd
	echo '.</p>'
	pcp_backup
	#####################################
	# TODO. Add code to update httpd.conf
	#####################################
else
	echo '<p class="error">[ ERROR ] Password not confirmed. Try again.</p>'
fi

pcp_table_middle
pcp_go_back_button
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'