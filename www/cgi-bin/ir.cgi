#!/bin/sh

# Version: 0.01 2016-02-25 GE
#	Original.

. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

DEBUG=1

pcp_html_head "IR" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

WGET="/bin/busybox wget"
LIRC_REPOSITORY="https://raw.github.com/ralph-irving/tcz-lirc/master"
PICO_REPOSITORY="http://ralph_irving.users.sourceforge.net/pico"
IR_DOWNLOAD="/tmp/IR"
FAIL_MSG="ok"
RESULT=0

#========================================================================================
#irda-4.1.13-piCore+.tcz
#irda-4.1.13-piCore+.tcz.md5.txt
#irda-4.1.13-piCore_v7+.tcz
#irda-4.1.13-piCore_v7+.tcz.md5.txt
#lirc.tcz
#lirc.tcz.dep
#lirc.tcz.md5.txt
#libcofi.tcz
#libcofi.tcz.md5.txt
# --------
# 
#----------------------------------------------------------------------------------------
SPACE_REQUIRED=10000

#========================================================================================
# Check we have internet access - set FAIL_MSG if not accessible
#----------------------------------------------------------------------------------------
pcp_internet_indicator() {
	if [ $(pcp_internet_accessible) = 0 ]; then
		INTERNET_STATUS="Internet accessible."
	else
		INTERNET_STATUS="Internet not accessible!!"
		FAIL_MSG="Internet not accessible!!"
	fi
}

#========================================================================================
# Check we have sourceforge access - set FAIL_MSG if not accessible
#----------------------------------------------------------------------------------------
pcp_sourceforge_indicator() {
	if [ $(pcp_sourceforge_accessible) = 0 ]; then
		SOURCEFORGE_STATUS="Sourceforge repository accessible."
	else
		SOURCEFORGE_STATUS="Sourceforge repository not accessible!!"
		FAIL_MSG="Sourceforge not accessible!!"
	fi
}

#========================================================================================
# Check for free space - set FAIL_MSG if insufficient space is available
#----------------------------------------------------------------------------------------
pcp_enough_free_space() {
	REQUIRED_SPACE=$1
	FREE_SPACE=$(pcp_free_space k)
	if [ $FREE_SPACE -gt $REQUIRED_SPACE ]; then
		echo '[  OK  ] Free space: '$FREE_SPACE'k - Required space: '$REQUIRED_SPACE'k'
	else
		echo '[ ERROR ] Free space: '$FREE_SPACE'k - Required space: '$REQUIRED_SPACE'k'
		echo '[ ERROR ] Not enough free space - try expanding your partition.'
		FAIL_MSG="Not enough free space - try expanding your partition."
	fi
}

#========================================================================================
# Warning message
#----------------------------------------------------------------------------------------
pcp_warning_message() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Warning</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="warning">'
	echo '              <td>'
	echo '                <p style="color:white"><b>Warning:</b> Beta IR install.</p>'
	echo '                <ul>'
	echo '                  <li style="color:white">Probably will not work properly.</li>'
	echo '                </ul>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}

#========================================================================================
# Generate staus message and finish html page
#----------------------------------------------------------------------------------------
pcp_html_end() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Status</legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '                <p>'$FAIL_MSG'</p>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'

	pcp_footer
	pcp_copyright

	echo '</body>'
	echo '</html>'
	exit
}

#========================================================================================
# Get a file from a remote repository
#----------------------------------------------------------------------------------------
pcp_get_file() {
	[ $1 == "lirc" ] && REPOSITORY=${LIRC_REPOSITORY}
	[ $1 == "pico" ] && REPOSITORY=${PICO_REPOSITORY}
	echo -n '[ INFO ] Downloading '$2'... '
	$WGET --no-check-certificate ${REPOSITORY}/$2 -O ${IR_DOWNLOAD}/$2
	if [ $? = 0 ]; then
		echo "OK"
	else
		echo "FAILED"
		FAIL_MSG="Failed to download $1"
	fi
}

#========================================================================================
# Delete a file from the local repository
#----------------------------------------------------------------------------------------
pcp_delete_file() {
	echo -n '[ INFO ] Deleting '$1'...'
	echo "OK"
}

#========================================================================================
# IR install
#----------------------------------------------------------------------------------------
pcp_ir_install() {
	echo '[ INFO ] Preparing download directory...'
	if [ -d $IR_DOWNLOAD ]; then
		sudo rm -rf $IR_DOWNLOAD
		[ $? != 0 ] && FAIL_MSG="Can not remove directory $IR_DOWNLOAD"
	fi
	sudo mkdir -m 755 $IR_DOWNLOAD
	[ $? != 0 ] && FAIL_MSG="Can not make directory $IR_DOWNLOAD"

#	[ $FAIL_MSG = "ok" ] && pcp_get_file lirc irda-4.1.13-piCore+.tcz
#	[ $FAIL_MSG = "ok" ] && pcp_get_file lirc irda-4.1.13-piCore+.tcz.md5.txt
# 	[ $FAIL_MSG = "ok" ] && pcp_get_file lirc irda-4.1.13-piCore_v7+.tcz
# 	[ $FAIL_MSG = "ok" ] && pcp_get_file lirc irda-4.1.13-piCore_v7+.tcz.md5.txt
#	[ $FAIL_MSG = "ok" ] && pcp_get_file lirc lirc.tcz
# 	[ $FAIL_MSG = "ok" ] && pcp_get_file lirc lirc.tcz.dep
 	[ $FAIL_MSG = "ok" ] && pcp_get_file lirc lirc.tcz.md5.txt

	if [ ! -f /mnt/mmcblk0p2/tce/optional/libcofi.tcz ]; then
		[ $FAIL_MSG = "ok" ] && pcp_get_file pico libcofi.tcz
		[ $FAIL_MSG = "ok" ] && pcp_get_file pico libcofi.tcz.md5.txt
	fi

	echo -n '[ INFO ] Installing files...'
	[ $FAIL_MSG = "ok" ] && sudo chown tc:staff $IR_DOWNLOAD/*
	[ $? = 0 ] || FAIL_MSG="Can not change ownership."
	[ $FAIL_MSG = "ok" ] && sudo chmod u=rw,g=rw,o=r $IR_DOWNLOAD/*
	[ $? = 0 ] || FAIL_MSG="Can not change permissions."
	[ $FAIL_MSG = "ok" ] && sudo cp -af $IR_DOWNLOAD/* /mnt/mmcblk0p2/tce/optional/
	[ $? = 0 ] || FAIL_MSG="Can not copy to tce/optional."
	[ $FAIL_MSG = "ok" ] && echo "OK" || echo "FAILED"

	echo -n '[ INFO ] Updating configuration files...'
	[ $FAIL_MSG = "ok" ] && IR_LIRC="yes" && pcp_save_to_config
	[ $FAIL_MSG = "ok" ] && echo "OK" || echo "FAILED"

	

}

#========================================================================================
# IR uninstall
#----------------------------------------------------------------------------------------
pcp_ir_uninstall() {
	[ $FAIL_MSG = "ok" ] && pcp_delete_file irda-4.1.13-piCore+.tcz
	[ $FAIL_MSG = "ok" ] && pcp_delete_file irda-4.1.13-piCore+.tcz.md5.txt
 	[ $FAIL_MSG = "ok" ] && pcp_delete_file irda-4.1.13-piCore_v7+.tcz
 	[ $FAIL_MSG = "ok" ] && pcp_delete_file irda-4.1.13-piCore_v7+.tcz.md5.txt
	[ $FAIL_MSG = "ok" ] && pcp_delete_file lirc.tcz
 	[ $FAIL_MSG = "ok" ] && pcp_delete_file lirc.tcz.dep
 	[ $FAIL_MSG = "ok" ] && pcp_delete_file lirc.tcz.md5.txt

	if [ $SHAIRPORT = "no" ]; then
		[ $FAIL_MSG = "ok" ] && pcp_delete_file libcofi.tcz
		[ $FAIL_MSG = "ok" ] && pcp_delete_file libcofi.tcz.md5.txt
	fi

	IR_LIRC="no" && pcp_save_to_config
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
case $ACTION in
	Install)
		pcp_warning_message
		;;
	Uninstall)
		pcp_warning_message
		;;
	*)
		ACTION=Initial
		pcp_warning_message
		pcp_internet_indicator
		[ $FAIL_MSG = "ok" ] || pcp_html_end
		pcp_sourceforge_indicator
		[ $FAIL_MSG = "ok" ] || pcp_html_end
		;;
esac

#========================================================================================
# Start Initial table
#----------------------------------------------------------------------------------------
if [ $ACTION = "Initial" ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>IR</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <form name="IR" action="'$0'" method="get">'
	#------------------------------------------Install/Unintall IR---------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Column 1</p>'
	echo '                </td>'
	echo '                <td class="column150 center">'
	[ $IR_LIRC = "no" ] &&
	echo '                  <input type="submit" name="ACTION" value="Install" />'
	[ $IR_LIRC = "yes" ] &&
	echo '                  <input type="submit" name="ACTION" value="Uninstall" />'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Install/Uninstall IR&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Install/Uninstall IR from repo.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------IR GPIO---------------------------------------
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Column 1</p>'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input class="large15" type="text" name="IR_GPIO" value="'$IR_GPIO'">'  
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>IR GPIO&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>IR GPIO.</p>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------
	echo '            </form>'
	#----------------------------------------------------------------------------------------
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi
#----------------------------------------------------------------------------------------

#========================================================================================
# xxx table
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>'$STEP'</legend>'
echo '          <table class="bggrey percent100">'
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'

#----------------------------------------------------------------------------------------
if [ $ACTION = "Initial" ]; then
	echo '                  <textarea class="inform" style="height:100px">'
	echo '[ INFO ] '$INTERNET_STATUS
	echo '[ INFO ] '$SOURCEFORGE_STATUS
	pcp_enough_free_space $SPACE_REQUIRED
fi
#----------------------------------------------------------------------------------------
if [ $ACTION = "Install" ]; then
	echo '                  <textarea class="inform" style="height:200px">'
	pcp_enough_free_space $SPACE_REQUIRED
	[ $FAIL_MSG = "ok" ] && pcp_ir_install
fi
#----------------------------------------------------------------------------------------
if [ $ACTION = "Uninstall" ]; then
	echo '                  <textarea class="inform" style="height:80px">'
	[ $FAIL_MSG = "ok" ] && pcp_ir_uninstall
fi
#----------------------------------------------------------------------------------------
echo '                  </textarea>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

pcp_html_end