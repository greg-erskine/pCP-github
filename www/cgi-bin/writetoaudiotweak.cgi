#!/bin/sh

# Version: 0.02 2014-12-10 GE
#	Using pcp_html_head now.
#	HTML5 formatting.

# Version: 0.01 2014-08-06 SBP
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Write to Audio Tweak" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#----------------------------------------------------------------------------------------
# ALSA OUTPUT LEVEL SECTION
#----------------------------------------------------------------------------------------
# Decode $ALSAlevelout using httpd, add quotes
ALSAlevelout=`sudo /usr/local/sbin/httpd -d \"$ALSAlevelout\"`
sudo sed -i "s/\(ALSAlevelout *=*\).*/\1$ALSAlevelout/" $CONFIGCFG
echo '<p class="info">[ INFO ] ALSAlevelout is set to: '$ALSAlevelout'</p>'

#----------------------------------------------------------------------------------------
# CMD SECTION
#----------------------------------------------------------------------------------------
# Decode $CMD using httpd, add quotes
CMD=`sudo /usr/local/sbin/httpd -d \"$CMD\"`
sudo sed -i "s/\(CMD *=*\).*/\1$CMD/" $CONFIGCFG

case "$CMD" in 
	\"Default\")
		echo '<p class="info">[ INFO ] CMD: '$CMD'</p>'
		sudo ./disableotg.sh
		;;
	\"Slow\")
		echo '<p class="info">[ INFO ] CMD: '$CMD'</p>'
		sudo ./enableotg.sh
		;;
	*)
		echo '<p class="error">[ ERROR ] CMD invalid: '$CMD'</p>'
		;;
esac

#----------------------------------------------------------------------------------------
# FIQ-SPILT SECTION
#----------------------------------------------------------------------------------------
# Decode $FIQ using httpd, add quotes
FIQ=`sudo /usr/local/sbin/httpd -d \"$FIQ\"`
sudo sed -i "s/\(FIQ *=*\).*/\1$FIQ/" $CONFIGCFG
pcp_backup
# Call FIQ script
sudo ./changeFIQ.sh
. $CONFIGCFG
echo '<p class="info">[ INFO ] FIQ is set to: '$FIQ'</p>'

#----------------------------------------------------------------------------------------
# ALSA OUTPUT LEVEL SECTION
#----------------------------------------------------------------------------------------
# Decode $ALSAlevelout using httpd, add quotes
ALSAlevelout=`sudo /usr/local/sbin/httpd -d \"$ALSAlevelout\"`
sudo sed -i "s/\(ALSAlevelout *=*\).*/\1$ALSAlevelout/" $CONFIGCFG
echo '<p class="info">[ INFO ] ALSAlevelout is set to: '$ALSAlevelout'</p>'

pcp_backup
[ $DEBUG = 1 ] && pcp_show_config_cfg
pcp_go_back_button

echo '</body>'
echo '</html>'