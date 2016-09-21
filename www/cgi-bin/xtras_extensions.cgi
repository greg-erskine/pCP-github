#!/bin/sh

# Version: 3.02 2016-09-21
#	Added default button. SBP.
#	Added more help txt. SBP.
#	Added repo indicator. SBP.
#	Extensive update. GE.

# Version: 3.00 2016-07-08
#	Removed pcp_mode_lt_beta. GE.

# Version: 0.06 2016-05-28 GE
#	Major update.

# Version: 0.05 2016-03-05 GE
#	Changed indicators to tick and cross.

# Version: 0.04 2016-01-06 GE
#	Deleted pcp_free_space.

# Version: 0.03 2015-11-15 GE
#	Minor updates.

# Version: 0.02 2015-08-25 GE
#	Added link to Tiny Core Linux Repository browser.

# Version: 0.01 2015-06-16 GE
#	Original version.

#========================================================================================
# This script installs piCore extensions ie. nano.tcz, wget.tcz, dialog.tcz
#
# Complications:
#   1. Sufficient space, need to expand file system.
#
# Future enhancements:
#   1. Search all 3.x, 4.x, 5.x, 6.x, 7.x, arm6 and arm7 extension repositories.
#   2. Check for fastest repository mirror.
#----------------------------------------------------------------------------------------

. /etc/init.d/tc-functions
. pcp-lms-functions
. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Add piCore extension" "GE"

pcp_banner
pcp_navigation

# Set variables
TCELOAD="tce-load"
SUBMIT="Initial"
ORPHAN=""
EXTNFOUND=0
MYMIRROR=$(cat /opt/tcemirror)
LOG="${LOGDIR}/pcp_extensions.log"
PCP_REPO=${PCP_REPO}/

#========================================================================================
# Search, load, install and delete extension routines
#----------------------------------------------------------------------------------------
pcp_search_extn() {
	EXTN="${EXTN%.tcz}.tcz"
	pcp_init_search
	grep -q "$EXTN" /tmp/tags.db && EXTNFOUND=1
}

pcp_load_extn() {
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Installing '$EXTN' . . . </legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	                      pcp_textarea_inform "none" "sudo -u tc $TCELOAD -iw $EXTN" 50
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
}

pcp_install_extn() {
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Installing '$EXTN' . . . </legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td>'
	                      pcp_textarea_inform "none" "sudo -u tc $TCELOAD -i $EXTN" 50
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
}

pcp_delete_extn() {
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Marking '$EXTN' and dependencies for deletion . . . </legend>'
	echo '          <table class="bggrey percent100">'
	pcp_start_row_shade
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
# This routine uses the piCore's search.sh script to update /tmp/tags.db
#----------------------------------------------------------------------------------------
pcp_init_search() {
	search.sh picoreplayer
}

pcp_set_repository() {
	echo $MYMIRROR > /opt/tcemirror
}

pcp_cleanup() {
	rm -f /tmp/tags.db
	rm -f /tmp/*.tree
	rm -f /tmp/sizelist
}

#========================================================================================
# This routine creates /opt/localmirrors
#----------------------------------------------------------------------------------------
pcp_create_localmirrors() {
	echo $PICORE_REPO_1 > /opt/localmirrors
	echo $PCP_REPO >> /opt/localmirrors
}

#========================================================================================
# Generate warning message
#----------------------------------------------------------------------------------------
pcp_information_message() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Information</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr>'
	echo '              <td>'
	echo '                <p><b>piCorePlayer</b> uses two repositories for downloading extensions:</p>'
	echo '                <ul>'
	echo '                  <li><b>Official piCore repository</b> - maintained by the piCore/TinyCore team.</li>'
	echo '                  <li><b>piCorePlayer sourceforge repository</b> - maintained by the piCorePlayer team.</li>'
	echo '                </ul>'
	echo '                <p><b>Extensions</b> can be:</p>'
	echo '                <ul>'
	echo '                  <li><b>downloaded</b> - the extension has been downloaded onto the SD card.</li>'
	echo '                  <li><b>installed</b> - the extension is downloaded and installed.</li>'
	echo '                  <li><b>uninstalled</b> - the extension is downloaded but not installed.</li>'
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
# Display debug information
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	if [ $DEBUG -eq 1 ]; then
		echo '<p class="debug">[ DEBUG ] $EXTN: '$EXTN'<br />'
		echo '                 [ DEBUG ] $SUBMIT: '$SUBMIT'<br />'
		echo '                 [ DEBUG ] $MYMIRROR: '$MYMIRROR'<br />'
		echo '                 [ DEBUG ] $MIRROR: '$MIRROR'<br />'
		echo '                 [ DEBUG ] $PICORE_REPO_1: '$PICORE_REPO_1'<br />'
		echo '                 [ DEBUG ] $PICORE_REPO_2: '$PICORE_REPO_2'<br />'
		echo '                 [ DEBUG ] $PCP_REPO: '$PCP_REPO'</p>'
	fi
}

#========================================================================================
# The following section of code is based on piCore tce-ab script
#----------------------------------------------------------------------------------------
pcp_display_info() {
	if [ -n "$EXTN" ]; then
		sudo -u tc tce-fetch.sh "${EXTN}.info"
		if [ $? -eq 0 ]; then
			cat "${EXTN}.info"
			rm -f "${EXTN}.info"
		else
			echo "${EXTN}.info not found!"
		fi
	fi
}

pcp_display_depends() {
	sudo -u tc tce-fetch.sh "${EXTN}.dep"
	if [ $? -eq 0 ]; then
		cat "${EXTN}.dep"
		rm -f "${EXTN}.dep"
	else
		echo "${EXTN}.dep not found!"
	fi
}

pcp_display_tree() {
	sudo -u tc tce-fetch.sh "${EXTN}.tree"
	if [ $? -eq 0 ]; then
		cat "${EXTN}.tree"
		rm -f "${EXTN}.tree"
	else
		echo "${EXTN}.tree not found!"
	fi
}

pcp_display_size() {
	sudo -u tc tce-size "$EXTN"
}

pcp_display_files() {
	sudo -u tc tce-fetch.sh "${EXTN}.list"
	if [ $? -eq 0 ]; then
		cat "${EXTN}.list"
		rm -f "${EXTN}.list"
	else
		echo "${EXTN}.list not found!"
	fi
}

#========================================================================================
# Generate report log
#----------------------------------------------------------------------------------------
pcp_generate_report() {
	(echo $0; date) > $LOG
	cat /etc/motd >>$LOG
	echo "" >>$LOG
	pcp_write_to_log "Downloaded extensions" "ls /mnt/mmcblk0p2/tce/optional/*.tcz | sed 's/\/mnt\/mmcblk0p2\/tce\/optional\///g'"
	pcp_write_to_log "Installed extensions" "tce-status -i"
	pcp_write_to_log "Uninstalled extensions" "tce-status -u"
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_information_message
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'

pcp_running_script
pcp_httpd_query_string
pcp_debug_info

case "$SUBMIT" in
	Initial)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Initial pass. Get extension...</p>'
		EXTN=""
	;;
	Info)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Searching for '$EXTN'...</p>'
		[ "$EXTN" = "" ] || [ "$EXTN" = ".tcz" ] || pcp_search_extn
	;;
	Load)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Loading '$EXTN'...</p>'
		pcp_load_extn
	;;
	Get)
		EXTN="mirrors.tcz"
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Getting '$EXTN'...</p>'
		pcp_load_extn
	;;
	Create)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Creating localmirrors  '$EXTN'...</p>'
		pcp_create_localmirrors
	;;
	Delete)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Marking '$EXTN' for deletion...</p>'
		pcp_delete_extn
	;;
	Set)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Setting repository...</p>'
		pcp_set_repository
		pcp_cleanup
	;;
	Reset)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Resetting repository to Official piCore repository...</p>'
		pcp_reset_repository
		pcp_cleanup
	;;
	*)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Invalid option '$SUBMIT'...</p>'
	;;
esac

echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Check for internet and piCore repository access
#----------------------------------------------------------------------------------------
if [ "$SUBMIT" = "Initial" ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Checking Internet accessiblity. . . </legend>'
	echo '          <table class="bggrey percent100">'
	#------------------------------------------------------------------------------------
	if [ $(pcp_internet_accessible) -eq 0 ]; then
	  pcp_green_tick "Internet accessible."
	else
	  pcp_red_cross "Internet not accessible."
	fi
	pcp_start_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column50 center">'
	echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
	echo '              </td>'
	echo '              <td class="column300">'
	echo '                <p>'$STATUS'</p>'
	echo '              </td>'
	echo '              <td class="column150">'
	echo '                <p></p>'
	echo '              </td>'
	echo '            </tr>'
	#------------------------------------------------------------------------------------
	if [ $(pcp_picore_repo_1_accessible) -eq 0 ]; then
	  pcp_green_tick "Official piCore repository accessible."
	else
	  pcp_red_cross "Official piCore repository not accessible."
	fi
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column50 center">'
	echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
	echo '              </td>'
	echo '              <td class="column300">'
	echo '                <p>'$STATUS'</p>'
	echo '              </td>'
	echo '              <td class="column150">'
	echo '                <p></p>'
	echo '              </td>'
	echo '            </tr>'
	#------------------------------------------------------------------------------------
	if [ $(pcp_pcp_repo_accessible) -eq 0 ]; then
	  pcp_green_tick "piCorePlayer sourceforge repository accessible."
	else
	  pcp_red_cross "piCorePlayer sourceforge repository not accessible."
	fi
	pcp_toggle_row_shade
	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column50 center">'
	echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
	echo '              </td>'
	echo '              <td class="column300">'
	echo '                <p>'$STATUS'</p>'
	echo '              </td>'
	echo '              <td class="column150">'
	echo '                <p></p>'
	echo '              </td>'
	echo '            </tr>'
	#------------------------------------------------------------------------------------
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
fi

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
echo '            <legend>Checking free space. . . </legend>'
echo '            <table class="bggrey percent100">'
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
                        pcp_textarea_inform "none" "pcp_free_space" 20
echo '                </td>'
echo '              </tr>'
echo '              <tr>'
echo '                <td>'
echo '                  <p><b>WARNING:</b> Check you have sufficient free space before you download your required extension.</p>'
echo '                </td>'
echo '              </tr>'
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

if [ $DEBUG -eq 1 ]; then
	#========================================================================================
	# Display tce mirror using
	#----------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="tce_mirror" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Current tcemirror/tcedir</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        read MIRROR < /opt/tcemirror
	                        pcp_textarea_inform "none" 'echo "$MIRROR"' 15
	                        RESULT=$(ls -al /etc/sysconfig | grep tcedir)
	                        pcp_textarea_inform "none" 'echo "$RESULT"' 15
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

if [ $MODE -ge $MODE_DEVELOPER ]; then
	#========================================================================================
	# Show available piCore/TinyCore remote mirrors - needs mirrors.tcz installed.
	#
	# Note: The piCore/Tiny Core remote mirrors are generally slow, incomplete and not
	#       up to date. I don't recommend using them.
	#----------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="remote_mirrors" action="'$0'" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Remote official piCore repository</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Remote mirror</p>'
	echo '                </td>'
	echo '                <td class="column300">'
	echo '                  <select class="large22" name="MYMIRROR">'

                              if [ $(pcp_extn_is_installed mirrors) -eq 0 ]; then
                                read MIRROR < /opt/tcemirror
                                for M in $(cat "/usr/local/share/mirrors")
                                do
                                  [ "$M" = "$MIRROR" ] && SELECTED="selected" || SELECTED=""
                                  echo '                    <option value="'$M'" '$SELECTED'>'$M'</option>'
                                done
                              else
                                echo '                    <option value="none">'mirrors.tcz not installed!'</option>'
                              fi

	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Select remote mirror repository&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>Remote mirrors are only available if mirrors.tcz is loaded.</li>'
	echo '                      <li>To return from any repo to the default repo press the <b>"Default button"</b>.</li>'
	echo '                      <li>Remote mirrors are listed in /usr/local/share/mirrors.</li>'
	echo '                      <li><b>Note:</b> Not all remote mirrors are are up to date.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'

                            if [ $(pcp_extn_is_installed mirrors) -eq 0 ]; then
                              echo '                  <input type="submit" name="SUBMIT" value="Set">'
                            else
                              echo '                  <input type="submit" name="SUBMIT" value="Get">'
                            fi

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
# Set repository
#----------------------------------------------------------------------------------------
MYMIRROR=$(cat /opt/tcemirror)

case "$MYMIRROR" in
	"$PICORE_REPO_1")
		SELECTED_1="selected"
		STATUS="Official piCore repository"
	;;
	"$PCP_REPO")
		SELECTED_2="selected"
		STATUS="piCorePlayer sourceforge repository"
	;;
esac

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="current_repository" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Set extension repository</legend>'
echo '            <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Current repository</p>'
echo '                </td>'
echo '                <td class="column300">'
echo '                  <select class="large22" name="MYMIRROR">'
echo '                    <option value="'$PICORE_REPO_1'" '$SELECTED_1'>Official piCore repository</option>'
echo '                    <option value="'$PCP_REPO'" '$SELECTED_2'>piCorePlayer sourceforge repository</option>'
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Select repository&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <p>Select either:</p>'
echo '                    <ul>'
echo '                      <li>Official piCore repository, or</li>'
echo '                      <li>piCorePlayer sourceforge repository.</li>'
echo '                    </ul>'
echo '                    <p><b>WARNING:</b> Remember to press [Reset] before leaving this page.</p>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td colspan="3">'
echo '                  <input type="submit" name="SUBMIT" value="Set">'
echo '                </td>'
echo '              </tr>'
#----------------------------------------------------------------------------------------
if [ "$SELECTED_2" = "selected" ]; then
	echo '              <tr class="warning">'
	echo '                <td class="column150">'
	echo '                  <input type="submit" name="SUBMIT" value="Reset">'
	echo '                </td>'
	echo '                <td colspan="2">'
	echo '                  <p style="color:white"><b>WARNING:</b> Remember to press [Reset] before leaving this page.</p>'
	echo '                </td>'
	echo '              </tr>'
fi
#----------------------------------------------------------------------------------------
echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Available extensions from tags.db
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="available" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Available extensions in the '$STATUS'</legend>'
echo '            <table class="bggrey percent100">'
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Available extensions</p>'
echo '                </td>'
echo '                <td class="column300">'
echo '                  <select class="large22" name="EXTN">'
                          [ -f /tmp/tags.db ] || pcp_init_search
                          for E in $(cat /tmp/tags.db | awk '{print $1}')
                          do
                            [ "$E" = "$EXTN" ] && SELECTED="selected" || SELECTED=""
                            echo '                    <option value="'$E'" '$SELECTED'>'$E'</option>'
                          done
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>List of extensions available in the '$STATUS'&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Lists all extensions that are currently available for download from '$STATUS'</li>'
echo '                      <li>If the <b>Official piCore repository</b> is selected, official piCore extensions are listed.</li>'
echo '                      <li>If the <b>piCorePlayer Sourceforge repository</b> is selected, special piCorePlayer extensions are listed.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                  <input type="submit" name="SUBMIT" value="Info">'
echo '                  <input type="submit" name="SUBMIT" value="Load">'
echo '                </td>'
echo '              </tr>'

echo '            </table>'
echo '          </fieldset>'
echo '        </div>'
echo '      </form>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

if [ $MODE -ge $MODE_BETA ]; then
	#========================================================================================
	# Loaded extensions in /mnt/mmcblk0p2/tce/optional/ on SD card
	#----------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="downloaded" action="'$0'" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Downloaded extensions</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Downloaded extensions</p>'
	echo '                </td>'
	echo '                <td class="column300">'
	echo '                  <select class="large22" name="EXTN">'

                              for E in $(ls /mnt/mmcblk0p2/tce/optional/*.tcz | sed 's/\/mnt\/mmcblk0p2\/tce\/optional\///g')
                              do
                                [ "$E" = "$EXTN" ] && SELECTED="selected" || SELECTED=""
                                echo '                    <option value="'$E'" '$SELECTED'>'$E'</option>'
                              done

	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>List of downloaded extensions&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>Lists all extensions that are currently downloaded.</li>'
	echo '                      <li>These extensions may be installed or uninstalled.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <input type="submit" name="SUBMIT" value="Info">'
	echo '                  <input type="submit" name="SUBMIT" value="Delete">'
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
	# Installed extensions - tce-status -i
	#----------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="installed" action="'$0'" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Installed extensions</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Installed extensions</p>'
	echo '                </td>'
	echo '                <td class="column300">'
	echo '                  <select class="large22" name="EXTN">'

                              for i in $(tce-status -i)
                              do
                                echo '                    <option value="'$i'.tcz">'$i'.tcz</option>'
                              done

	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>List of installed extensions&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>Lists all extensions that are currently installed.</li>'
	echo '                      <li>These extensions are usually loaded at boot via /mnt/mmcblk0p2/tce/onboot.lst.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <input type="submit" name="SUBMIT" value="Info">'
	echo '                  <input type="submit" name="SUBMIT" value="Delete">'
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
	# Uninstalled extensions - tce-status -u
	#----------------------------------------------------------------------------------------
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="uninstalled" action="'$0'" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Uninstalled extensions</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Uninstalled extensions</p>'
	echo '                </td>'
	echo '                <td class="column300">'
	echo '                  <select class="large22" name="EXTN">'

                              for i in $(tce-status -u)
                              do
                                echo '                    <option value="'$i'">'$i'</option>'
                              done

	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>List of uninstalled extensions&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>Lists all extensions that are currently downloaded but not (yet) installed.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	echo '                  <input type="submit" name="SUBMIT" value="Info">'
	echo '                  <input type="submit" name="SUBMIT" value="Install">'
	echo '                  <input type="submit" name="SUBMIT" value="Delete">'
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
	# Orphaned extensions - tce-status -o  WARNING: very slow!
	#----------------------------------------------------------------------------------------
	if [ "$ORPHAN" = "yes" ]; then
		echo '<table class="bggrey">'
		echo '  <tr>'
		echo '    <td>'
		echo '      <form name="orphan" action="'$0'" method="get">'
		echo '        <div class="row">'
		echo '          <fieldset>'
		echo '            <legend>Orphaned extensions</legend>'
		echo '            <table class="bggrey percent100">'
		pcp_incr_id
		pcp_start_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150">'
		echo '                  <p>Orphaned extensions</p>'
		echo '                </td>'
		echo '                <td class="column300">'
		echo '                  <select class="large22" name="EXTN">'

                                  for i in $(tce-status -o | grep '.tcz ' | sed 's/ not found!//' )
                                  do
                                    echo '                    <option value="'$i'">'$i'</option>'
                                  done

		echo '                  </select>'
		echo '                </td>'
		echo '                <td>'
		echo '                  <p>List of Orphaned extensions&nbsp;&nbsp;'
		echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
		echo '                  </p>'
		echo '                  <div id="'$ID'" class="less">'
		echo '                    <ul>'
		echo '                      <li>Lists all orphaned extensions.</li>'
		echo '                    </ul>'
		echo '                  </div>'
		echo '                </td>'
		echo '              </tr>'
		pcp_toggle_row_shade
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		echo '                  <input type="submit" name="SUBMIT" value="Info">'
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
fi

#========================================================================================
# Manual search for extension
#----------------------------------------------------------------------------------------
if [ $MODE -eq $MODE_DEVELOPER ] && [ $DEBUG -eq 1 ]; then
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="extension" action="'$0'" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Extension '$EXTN'</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade
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
	echo '                    <p>This option will load or delete an extension and its dependencies.</p>'
	echo '                    <p><b>Step:</b></p>'
	echo '                    <ol>'
	echo '                      <li>Search for extension - this ensures you have selected a valid extension.</li>'
	echo '                      <li>Check free space and download size before loading.</li>'
	echo '                      <li>Load or delete - this loads or marks for deletion extensions and dependencies.</li>'
	echo '                    </ol>'
	echo '                    <p>For more information - see <a href="http://packages.tinycorelinux.net/" target="_new">Tiny Core Linux Repository browser</a>.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade

	if [ $EXTNFOUND -eq 0 ] && [ "$SUBMIT" = "Info" ]; then
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

	if [ $EXTNFOUND -eq 1 ]; then
		echo '                  <input type="submit" name="SUBMIT" value="Load">'
		echo '                  <input type="submit" name="SUBMIT" value="Delete">'
	fi

	echo '                  <input type="submit" name="SUBMIT" value="Info">'
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

if [ $MODE -ge $MODE_ADVANCED ] && [ $EXTNFOUND -eq 1 ] && [ "$SUBMIT" != "Initial" ]; then
	#========================================================================================
	# Display Extension information
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
	                        pcp_textarea_inform "none" "pcp_display_info" 200
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
	                        pcp_textarea_inform "none" "pcp_display_depends" 100
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
	                        pcp_textarea_inform "none" "pcp_display_tree" 100
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
	                        pcp_textarea_inform "none" "pcp_display_size" 100
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
	                        pcp_textarea_inform "none" "pcp_display_files" 100
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

[ "$SUBMIT" = "Initial" ] && pcp_generate_report

echo '</body>'
echo '</html>'