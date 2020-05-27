#!/bin/sh

# Version: 7.0.0 2020-05-28

. pcp-functions
. pcp-lms-functions

pcp_html_head "Security" "GE"

pcp_controls
pcp_navbar
pcp_httpd_query_string

unset REBOOT_REQUIRED

[ x"" = x"$CALLED_BY" ] && CALLED_BY="tc password"

#========================================================================================
# Page tabs
#----------------------------------------------------------------------------------------
echo '<!-- Start of pcp_security_tabs toolbar -->'
echo '  <div>'
echo '    <ul class="nav nav-tabs navbar-dark mt-1">'

for TAB in "tc password" "httpd settings" "Disable SSH" # "Disable GUI"
do
	[ "$TAB" = "${CALLED_BY/+/ /}" ] && TAB_ACTIVE="active" || TAB_ACTIVE=""
	echo '      <li class="nav-item">'
	echo '        <a class="nav-link '$TAB_ACTIVE'" href="'$0'?CALLED_BY='${TAB/ /+}'" title="'$TAB'">'$TAB'</a>'
	echo '      </li>'
done

echo '    </ul>'
echo '  </div>'
echo '<!-- End of pcp_security_tabs toolbar -->'
#----------------------------------------------------------------------------------------
case "$CALLED_BY" in
	"tc password")    . security_tc_password.cgi;;
	"httpd settings") . security_httpd_settings.cgi;;
	"Disable GUI")    . security_disable_gui.cgi;;
	"Disable SSH")    . security_disable_ssh.cgi;;
esac
#----------------------------------------------------------------------------------------
pcp_footer
pcp_copyright
pcp_remove_query_string
[ $REBOOT_REQUIRED ] && pcp_reboot_required

echo '</body>'
echo '</html>'
exit
