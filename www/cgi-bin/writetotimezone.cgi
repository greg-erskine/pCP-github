#!/bin/sh

# Version: 3.5.1 2018-04-02
#	Added pcp_redirect_button. GE.

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.

# Version: 0.01 2014-06-24
#	Original. GE.

. pcp-functions

pcp_html_head "Set Timezone" "GE"

pcp_banner
pcp_running_script
pcp_httpd_query_string

pcp_table_top "Changing timezone"
echo '<p class="info">[ INFO ] Setting Timezone to '$TIMEZONE'</p>'
pcp_save_to_config
pcp_mount_bootpart
pcp_set_timezone
pcp_umount_bootpart

[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Local time: '$(date)'</p>'

pcp_backup
pcp_table_middle
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 5
pcp_table_end

pcp_footer
pcp_copyright
pcp_reboot_required

echo '</body>'
echo '</html>'