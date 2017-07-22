#!/bin/sh

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.

# Version: 0.05 2015-09-18 SBP
#	Added pcp_save_to_config, pcp_mount_bootpart and pcp_umount_bootpart.
#	Removed httpd decoding.

# Version: 0.04 2015-06-25 SBP
#	Removed reboot button - not needed anymore.

# Version: 0.03 2015-05-10 SBP
#	Fixed the saving command so that slashes are saved as well.

# Version: 0.03 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.02 2014-09-04 GE
#	Moved code to pcp_set_timezone routine.

# Version: 0.01 2014-06-24 GE
#	Original.

. pcp-functions

pcp_html_head "Set Timezone" "GE" "10" "tweaks.cgi"

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
pcp_go_back_button
pcp_table_end
pcp_footer
pcp_copyright
pcp_reboot_required

echo '</body>'
echo '</html>'