#!/bin/sh

# Version: 7.0.0 2020-05-12

. pcp-functions

pcp_html_head "Set Timezone" "GE"

pcp_navbar
pcp_httpd_query_string

pcp_heading5 "Changing timezone"
pcp_infobox_begin
pcp_message DEBUG "Local time: $(date)" "html"
pcp_save_to_config
pcp_mount_bootpart
pcp_set_timezone
pcp_umount_bootpart
pcp_backup
pcp_infobox_end

pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 5

pcp_html_end
