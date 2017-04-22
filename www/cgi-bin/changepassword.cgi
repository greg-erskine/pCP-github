#!/bin/sh

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.

# Version: 0.03 2015-09-19 SBP
#	Removed httpd decoding.

# Version: 0.02 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014-06-24 GE
#	Original.

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