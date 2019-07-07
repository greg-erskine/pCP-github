#!/bin/sh

# Version: 6.0.0 2019-06-21

. pcp-functions
. pcp-lms-functions

pcp_html_head "Security" "GE"

pcp_running_script
pcp_httpd_query_string
pcp_picoreplayers_toolbar
pcp_controls
pcp_banner
pcp_navigation

unset REBOOT_REQUIRED

[ x"" = x"$CALLED_BY" ] && CALLED_BY="tc password"

#========================================================================================
# Page tabs
#----------------------------------------------------------------------------------------
echo '<!-- Start of pcp_security_tabs toolbar -->'
echo '<p style="margin-top:8px;">'

#for TAB in "tc password" "httpd settings" "Disable GUI" "Disable SSH"

for TAB in "tc password" "httpd settings"
do
	[ "$TAB" = "$CALLED_BY" ] && TAB_STYLE="tab7a" || TAB_STYLE="tab7"
	echo '  <a class="'$TAB_STYLE'" href="'$0'?CALLED_BY='$TAB'" title="'$TAB'">'$TAB'</a>'
done

echo '</p>'
echo '<div class="tab7end" style="margin-bottom:10px;">pCP</div>'
echo '<!-- End of pcp_security_tabs toolbar -->'
#----------------------------------------------------------------------------------------
case $CALLED_BY in
	tc\ password)    . security_tc_password.cgi;;
	httpd\ settings) . security_httpd_settings.cgi;;
	Disable\ GUI)    . security_disable_gui.cgi;;
	Disable\ SSH)    . security_disable_ssh.cgi;;
esac
#----------------------------------------------------------------------------------------
pcp_footer
pcp_copyright
pcp_remove_query_string
[ $REBOOT_REQUIRED ] && pcp_reboot_required

echo '</body>'
echo '</html>'
exit
