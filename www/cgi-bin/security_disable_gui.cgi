#!/bin/sh

# Version: 7.0.0 2020-05-27

#========================================================================================
# Disable web GUI
#----------------------------------------------------------------------------------------
STOP_HTTPD_SH="/tmp/stop_httpd.sh"

case $ACTION in
	Save\ GUI)
		pcp_save_to_config
		pcp_backup >/dev/null 2>&1
		REBOOT_REQUIRED=TRUE
	;;
	Abort\ GUI)
		sudo killall $STOP_HTTPD_SH
		REBOOT_REQUIRED=TRUE
	;;
	*)
		pcp_security_ssh
	;;
esac

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"
#---------------------------------------web GUI------------------------------------------
pcp_border_begin
pcp_heading5 "Disable web GUI"
echo '  <form id="GUI_Disable" name="GUI_Disable" action="'$0'" method="get">'
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <p>Disable web GUI</p>'
echo '      </div>'
echo '      <div class="'$COLUMN3_2'">'
echo '        <input class="form-control form-control-sm"'
echo '               type="text"'
echo '               name="GUI_DISABLE"'
echo '               value="'$GUI_DISABLE'"'
echo '               pattern="\d*"'
echo '               title="Use numbers."'
echo '        >'
echo '      </div>'
echo '      <div class="'$COLUMN3_3'">'
echo '        <p>Set disable web GUI time&nbsp;&nbsp;'
pcp_helpbadge
echo '        </p>'
echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '          <p>&lt;xx seconds&gt;</p>'
echo '          <p><b>Default: </b>0 = enable web GUI</p>'
echo '          <p>1 = never start web GUI</p>'
echo '          <p>&gt;20 = minimum value</p>'
echo '          <p>This sets the time, in seconds, between piCorePlayer booting and the web GUI being disabled.</p>'
echo '          <p>This increases security because it gives limited access window to the web GUI.</p>'
echo '        </div>'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN3_1'">'
echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Save GUI">Save</button>'
echo '        <input type="hidden" name="CALLED_BY" value="Disable GUI">'
echo '      </div>'
if [ -f $STOP_HTTPD_SH ]; then
	echo '      <div class="'$COLUMN3_1'">'
	echo '        <button class="'$BUTTON'" type="submit" name="ACTION" value="Abort GUI">Abort</button>'
	echo '      </div>'
fi
echo '    </div>'
#----------------------------------------------------------------------------------------
echo '  </form>'
pcp_border_end
#----------------------------------------------------------------------------------------
