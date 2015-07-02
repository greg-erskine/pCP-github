#!/bin/sh

# Version: 0.01 2015-06-16 GE
#   Original version.

#========================================================================================
# This script installs piCore extensions. ie. nano.tcz, wget.tcz, dialog.tcz
#
#   1. Type extension name
#   2. Search for extension
#   3. Check disk space
#   4. Check internet connection
#   5. Load/delete extension
#
# Complications:
#   1. Sufficient space, need to expand file system
#
# Future enhancements:
#   1. Search all 3.x, 4.x, 5.x, 6.x, arm6 and arm7 extension repositories
#   2. Pull-down list of all available extensions
#   3. Check for fastest repository mirror
#
#----------------------------------------------------------------------------------------

. /etc/init.d/tc-functions
getMirror
. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Add piCore extension" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_mode_lt_99

# Set variables
SUBMIT=Initial
EXTNFOUND=0

#========================================================================================
# Search, load and delete extension routines
#----------------------------------------------------------------------------------------
pcp_search_extn() {
	echo $EXTN | grep .tcz$ >/dev/null
	[ $? != 0  ] && EXTN=$EXTN.tcz
	pcp_init_search
	grep "$EXTN" /tmp/tags.db >/dev/null
	[ $? = 0 ] && EXTNFOUND=1
}

pcp_load_extn() {
	pcp_start_row_shade
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Installing '$EXTN' . . . </legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	                      pcp_textarea_inform "none" "sudo -u tc tce-load -iw $EXTN" 50
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
}

pcp_delete_extn() {
	pcp_start_row_shade
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Marking '$EXTN' and dependencies for deletion . . . </legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	echo '                <textarea class="inform" style="height:80px">'
	                        sudo -u tc tce-audit builddb
	                        echo
	                        echo After a reboot these extensions will be permanently deleted:
	                        sudo -u tc tce-audit delete $EXTN
	echo '                </textarea>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
}

#========================================================================================
# This routine uses the piCore search.sh script to update /tmp/tags.db
#----------------------------------------------------------------------------------------
pcp_init_search() {
	search.sh picoreplayer
}

pcp_free_space() {
	set -- `/bin/df -h | grep mmcblk0p2`
	echo $4
}

#========================================================================================
# Display debug information
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	if [ $DEBUG = 1 ]; then 
		echo '<p class="debug">[ DEBUG ] $EXTN: '$EXTN'<br />'
		echo '                 [ DEBUG ] $SUBMIT: '$SUBMIT'<br />'
		echo '                 [ DEBUG ] $MIRROR: '$MIRROR'</p>'
	fi
}

#========================================================================================
# The following section of code is based on piCore tce-ab script
#----------------------------------------------------------------------------------------
displayInfo() {
	if [ -n "$EXTN" ]; then
		sudo -u tc tce-fetch.sh "$EXTN".info
		if [ "$?" == 0 ]; then
			less "$EXTN".info
			rm "$EXTN".info
		else
			echo "$EXTN.info not found!"
		fi
	fi
}

displayDepends() {
	sudo -u tc tce-fetch.sh "$EXTN".dep
	if [ "$?" == 0 ]; then
		less "$EXTN".dep
		rm "$EXTN".dep
	else
		echo "$EXTN.dep not found!"
	fi
}

displayTree() {
	sudo -u tc tce-fetch.sh "$EXTN".tree
	if [ "$?" == 0 ]; then
		less "$EXTN".tree
		rm "$EXTN".tree
	else
		echo "$EXTN.tree not found!"
	fi
}

displaySize() {
	sudo -u tc tce-size "$EXTN"
}

displayFiles() {
	sudo -u tc tce-fetch.sh "$EXTN".list
	if [ "$?" == 0 ]; then
		less "$EXTN".list
		rm "$EXTN".list
	else
		echo "$EXTN.list not found!"
	fi
}

#========================================================================================
# Loaded extensions on /mnt/mmcblk0p2/tce/optional/
#----------------------------------------------------------------------------------------
if [ $MODE = $MODE_DEVELOPER ]; then
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Loaded Extensions</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150">'
	echo '                <p>Loaded extensions</p>'
	echo '              </td>'
	echo '              <td class="column300">'
	echo '                <select class="large22" name="XXXX">'
	                        EXTNLST=$(ls /usr/local/tce.installed/ | sed 's/\/usr\/local\/tce.installed\///g')
	                        for i in $EXTNLST
	                        do
	                          echo '<option value="'$i'">'$i'</option>'
	                        done
	echo '                </select>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>List of loaded extensions in /usr/local/tce.installed/</p>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

#========================================================================================
# Downloaded extensions on /mnt/mmcblk0p2/tce/optional/
#----------------------------------------------------------------------------------------
if [ $MODE = $MODE_DEVELOPER ]; then
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Downloaded Extensions</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150">'
	echo '                <p>Downloaded extensions</p>'
	echo '              </td>'
	echo '              <td class="column300">'
	echo '                <select class="large22" name="XXXXX">'
	                        EXTNLST=$(ls /mnt/mmcblk0p2/tce/optional/*.tcz | sed 's/\/mnt\/mmcblk0p2\/tce\/optional\///g')
	                        for i in $EXTNLST
	                        do
	                          echo '<option value="'$i'">'$i'</option>'
	                        done
	echo '                </select>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>List of downloaded extensions in /mnt/mmcblk0p2/tce/optional/</p>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

#========================================================================================
# Available extensions from tags.db
#----------------------------------------------------------------------------------------
if [ $MODE = $MODE_DEVELOPER ]; then
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Available Extensions</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column150">'
	echo '                <p>Available extensions</p>'
	echo '              </td>'
	echo '              <td class="column300">'
	echo '                <select class="large22" name="XXXXXX">'
	                        [ -f /tmp/tags.db ] || pcp_init_search
	                        EXTNLST=$(cat /tmp/tags.db | awk '{print $1}')
	                        for i in $EXTNLST
	                        do
	                          echo '<option value="'$i'">'$i'</option>'
	                        done
	echo '                </select>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p>List of extensions available for download from the piCore repository.</p>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'

pcp_running_script
pcp_httpd_query_string
pcp_debug_info

EXTN=`sudo $HTPPD -d $EXTN`

case "$SUBMIT" in
	Initial)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Initial pass. Get extension...</p>'
		EXTN=""
		;;
	Search)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Searching for '$EXTN'...</p>'
		[ "$EXTN" == "" ] || [ "$EXTN" == ".tcz" ] || pcp_search_extn
		;;
	Load)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Loading '$EXTN'...</p>'
		pcp_load_extn
		;;
	Delete)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Marking '$EXTN' for deletion...</p>'
		pcp_delete_extn
		;;
	*)
		[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Invalid option '$SUBMIT'...</p>'
		;;
esac

echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Start table
#----------------------------------------------------------------------------------------
pcp_start_row_shade
pcp_toggle_row_shade
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="extension" action="xtras_extensions.cgi" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Extension '$EXTN'</legend>'
echo '            <table class="bggrey percent100">'
pcp_incr_id
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p class="row">Extension name</p>'
echo '                </td>'
echo '                <td class="column300">'
echo '                  <input class="large22" type="text" name="EXTN" value="'$EXTN'">'
echo '                </td>'
echo '                <td>'
echo '                  <p>Search, load or delete piCore extension&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>This option will load or delete a piCore extension and dependencies.</p>'
echo '                    <p><b>Step:</b></p>'
echo '                    <ol>'
echo '                      <li>Search for extension - this ensures you have selected a valid extension.</li>'
echo '                      <li>Check free space and download size before loading.</li>'
echo '                      <li>Load or delete - this loads or marks for deletion extensions and dependencies.</li>'
echo '                    </ol>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade

if [ $EXTNFOUND = 0 ] && [ $SUBMIT = "Search" ]; then 
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p></p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p class="error">Extension not found!</p>'
	echo '                </td>'
	echo '              </tr>'
fi

echo '              <tr>'
echo '                <td colspan="3">'

if [ $EXTNFOUND = 1 ]; then 
	echo '                  <input type="submit" name="SUBMIT" value="Load">'
	echo '                  <input type="submit" name="SUBMIT" value="Delete">'
fi

echo '                  <input type="submit" name="SUBMIT" value="Search">'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Check for internet and piCore repository access
#----------------------------------------------------------------------------------------
if [ $SUBMIT = "Initial" ]; then
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Internet</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'
	                  if [ $(pcp_internet_accessible) = 0 ]; then
	                    IMAGE="green.png"
	                    STATUS="Internet accessible..."
	                  else
	                    IMAGE="red.png"
	                    STATUS="Internet not accessible!!"
	                  fi
	echo '              <td class="column150">'
	echo '                <p class="centre"><img src="../images/'$IMAGE'" alt="'$STATUS'"></p>'
	echo '              </td>'
	echo '              <td class="column150">'
	echo '                <p>'$STATUS'</p>'
	echo '              </td>'
	echo '              <td class="column150">'
	echo '                <p></p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p></p>'
	echo '              </td>'
	                    if [ $(pcp_picore_accessible) = 0 ]; then
	                      IMAGE="green.png"
	                      STATUS="piCore repository accessible..."
	                    else
	                      IMAGE="red.png"
	                      STATUS="piCore repository not accessible!!"
	                    fi
	echo '              <td class="column150">'
	echo '                <p class="centre"><img src="../images/'$IMAGE'" alt="'$STATUS'"></p>'
	echo '              </td>'
	echo '              <td class="column210">'
	echo '                <p>'$STATUS'</p>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

if [ $MODE = $MODE_DEVELOPER ] && [ $EXTNFOUND = 1 ] && [ $SUBMIT != "Initial" ]; then
	#========================================================================================
	# Display disk space using df
	#----------------------------------------------------------------------------------------
	pcp_toggle_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="diskspace" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Free space</legend>'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "pcp_free_space" 20
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'

	if [ $DEBUG = 1 ]; then
		#========================================================================================
		# Display tce mirror using 
		#----------------------------------------------------------------------------------------
		pcp_start_row_shade
		pcp_toggle_row_shade
		echo '<table class="bggrey">'
		echo '  <tr>'
		echo '    <td>'
		echo '      <form name="tce_mirror" method="get">'
		echo '        <div class="row">'
		echo '          <fieldset>'
		echo '            <legend>Current tce mirror</legend>'
		echo '            <table class="bggrey percent100">'
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		                        pcp_textarea_inform "none" "cat /opt/tcemirror" 20
		echo '                </td>'
		echo '              </tr>'
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		                        RESULT=$(ls -al /etc/sysconfig | grep tcedir)
		                        pcp_textarea_inform "none" "echo $RESULT" 25
		echo '                </td>'
		echo '              </tr>'
		echo '            </table>'
		echo '          </fieldset>'
		echo '        </div>'
		echo '      </form>'
		echo '    </td>'
		echo '  </tr>'
		echo '</table>'
	fi

	#========================================================================================
	# Display Extension size using tce-size
	#----------------------------------------------------------------------------------------
	pcp_start_row_shade

	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="Extension_size" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Extension: '$EXTN'</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p><b>Information:</b></p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "displayInfo" 200
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p><b>Dependencies:</b></p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "displayDepends" 100
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p><b>Tree:</b></p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "displayTree" 100
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p><b>Size:</b></p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "displaySize" 100
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <p><b>Files:</b></p>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        pcp_textarea_inform "none" "displayFiles" 100
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
	#----------------------------------------------------------------------------------------
fi

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'