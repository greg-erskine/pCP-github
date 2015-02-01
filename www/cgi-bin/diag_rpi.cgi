#!/bin/sh
# Raspberry Pi diagnostics script

# version: 0.01 2014-10-22 GE
#	Orignal.

. pcp-rpi-functions
. pcp-functions
pcp_variables

# Local variables
START="====================> Start <===================="
END="=====================> End <====================="
LOG="/tmp/diagrpi.log"
(echo $0; date) > $LOG

pcp_html_head "RasPi Diagnostics" "GE"

if [ $MODE -lt 5 ]; then
	echo '</body>'
	echo '</html>'
	exit 1
fi

pcp_footer
pcp_banner
pcp_diagnostics
pcp_running_script
pcp_refresh_button
pcp_go_main_button

echo '<p class="info">[ INFO ] Rev: '     $(pcp_rpi_revision)     '<br />'
echo '                [ INFO ] Model: '   $(pcp_rpi_model)        '<br />'
echo '                [ INFO ] PCB rev: ' $(pcp_rpi_pcb_revision) '<br />'
echo '                [ INFO ] memory: '  $(pcp_rpi_memory)       '<br />'

[ $(pcp_rpi_is_model_A) = 0 ] &&
echo '                [ INFO ] model A: Yes <br />' ||
echo '                [ INFO ] model A: No  <br />'

[ $(pcp_rpi_is_model_B) = 0 ] &&
echo '                [ INFO ] model B: Yes <br />' ||
echo '                [ INFO ] model B: No  <br />'

[ $(pcp_rpi_is_model_Bplus) = 0 ] &&
echo '                [ INFO ] model B+: Yes <br />' ||
echo '                [ INFO ] model B+: No  <br />'

[ $(pcp_rpi_is_memory_256) = 0 ] &&
echo '                [ INFO ] 256kB: Yes <br />' ||
echo '                [ INFO ] 256kB: No  <br />'

[ $(pcp_rpi_is_memory_512) = 0 ] &&
echo '                [ INFO ] 512kB: Yes </p>' ||
echo '                [ INFO ] 512kB: No  </p>'

pcp_footer
pcp_refresh_button

echo '</body>'
echo '</html>'

#=========================================================================================
# Add information to log file.
#-----------------------------------------------------------------------------------------
echo "[ INFO ] Rev: $(pcp_rpi_revision)" >> $LOG
echo "[ INFO ] Model: $(pcp_rpi_model)" >> $LOG
echo "[ INFO ] PCB rev: $(pcp_rpi_pcb_revision)" >> $LOG
echo "[ INFO ] memory: $(pcp_rpi_memory)" >> $LOG

[ $(pcp_rpi_is_model_A) = 0 ]     && echo "[ INFO ] model A: Yes" >> $LOG  || echo "[ INFO ] model A: No" >> $LOG
[ $(pcp_rpi_is_model_B) = 0 ]     && echo "[ INFO ] model B: Yes" >> $LOG  || echo "[ INFO ] model B: No" >> $LOG
[ $(pcp_rpi_is_model_Bplus) = 0 ] && echo "[ INFO ] model B+: Yes" >> $LOG || echo "[ INFO ] model B+: No" >> $LOG