#!/bin/sh

# Version: 4.2.0 2019-02-21

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
. pcp-functions
. pcp-lms-functions

pcp_html_head "Add piCore extension" "GE"

pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string
pcp_debug_info

#========================================================================================
# Set variables
#----------------------------------------------------------------------------------------
cd /tmp
TCELOAD="tce-load"
EXTNFOUND=0
LOG="${LOGDIR}/pcp_extensions.log"
PCP_REPO=${PCP_REPO}/
TAGS_PCP_DB="/tmp/tags_pcp.db"
TAGS_PICORE_DB="/tmp/tags_picore.db"

SIZELIST_PCP="/tmp/sizelist_pcp"
SIZELIST_PICORE="/tmp/sizelist_picore"

#========================================================================================
# Display debug information
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	echo '<!-- Start of debug info -->'
	pcp_debug_variables "html" EXTN SUBMIT MYMIRROR MIRROR PICORE_REPO_1 \
	PICORE_REPO_2 PCP_REPO CALLED_BY EXTNFOUND KERNELVER
	echo '<!-- End of debug info -->'
}

#========================================================================================
# Generate extensions report
#----------------------------------------------------------------------------------------
pcp_generate_report() {
	ORIG_PWD=$PWD
	(echo $0; date) > $LOG
	cat /etc/motd >>$LOG
	echo "" >>$LOG
	pcp_write_to_log "Installed extensions" "tce-status -i | sort -f"
	pcp_write_to_log "Uninstalled extensions" "tce-status -u | sort -f"
	pcp_write_to_log "Downloaded extensions" "cd $PACKAGEDIR; ls *.tcz | sort -f"
	pcp_write_to_log "onboot.lst" "cat $ONBOOTLST"
	pcp_write_to_log "Extension dependency tree" "pcp_full_dependency_tree text"
	cd $ORIG_PWD
}

#========================================================================================
# Search for extension in current tags database
#----------------------------------------------------------------------------------------
pcp_search_extn() {
	EXTN="${EXTN%.tcz}.tcz"
	grep -q "$EXTN" "$DB" && EXTNFOUND=1
}

#========================================================================================
# Find extension in both piCore and pCP tags databases.
# Note: pCP tags database has precedent.
#----------------------------------------------------------------------------------------
pcp_find_extn() {
	EXTNFOUND=0
	EXTN="${EXTN%.tcz}.tcz"
	if grep -q ${EXTN} $TAGS_PICORE_DB; then
		DB="$TAGS_PICORE_DB"
		MYMIRROR=$PICORE_REPO_1
		EXTNFOUND=1
	fi
	if grep -q ${EXTN} $TAGS_PCP_DB; then
		DB="$TAGS_PCP_DB"
		MYMIRROR=$PCP_REPO
		EXTNFOUND=1
	fi
	pcp_set_repository
}

#========================================================================================
# Set active repository to $MYMIRROR
#----------------------------------------------------------------------------------------
pcp_set_repository() {
	echo $MYMIRROR > /opt/tcemirror
}

#========================================================================================
# Download and install extension.
# Note: Extension will be added to onboot.lst
#----------------------------------------------------------------------------------------
pcp_load_extn() {
	pcp_table_top "Loading '$EXTN' . . . "
	                      pcp_textarea_inform "none" "sudo -u tc $TCELOAD -iw $EXTN" 50
	pcp_table_end
}

#========================================================================================
# Temporarily install extension.
# Note: Extension will need to be already downloaded.
#       Extension will not be added to onboot.lst
#----------------------------------------------------------------------------------------
pcp_install_extn() {
	pcp_table_top "Installing '$EXTN' . . . "
	                      pcp_textarea_inform "none" "sudo -u tc $TCELOAD -i $EXTN" 50
	pcp_table_end
}

#========================================================================================
# Uninstall extension.
# Note: This will remove the extension from onboot.lst but will not delete the extension.
#       NOT IMPLEMENTED.
#----------------------------------------------------------------------------------------
pcp_uninstall_extn() {
	pcp_table_top "Uninstalling '$EXTN' . . . "
#	                      pcp_textarea_inform "none" "sudo -u tc $TCELOAD -i $EXTN" 50
	pcp_table_end
}

#========================================================================================
# Delete extension.
# Note: This will delete the extension and its dependencies.
#       Reboot required.
#----------------------------------------------------------------------------------------
pcp_delete_extn() {
	pcp_table_top "Marking '$EXTN' and dependencies for deletion . . . "
	echo '                <textarea class="inform" style="height:80px">'
	                        sudo -u tc tce-audit builddb
	                        echo
	                        echo 'After a reboot these extensions will be permanently deleted:'
	                        sudo -u tc tce-audit delete $EXTN
	echo '                </textarea>'
	pcp_table_end
}

#========================================================================================
# Update extension.
#----------------------------------------------------------------------------------------
pcp_update_extn() {
	pcp_table_top "Updating '$EXTN' . . . "
	                      pcp_textarea_inform "none" "sudo -u tc pcp-update $EXTN" 50
	pcp_table_end
}

#========================================================================================
# This routine uses the piCore's search.sh script to update /tmp/tags.db
# Note: This downloads tag.db from both the piCore and pCP repositories.
#       Tag databases will only be downloaded if they don't exist or are older than 2 hours.
#----------------------------------------------------------------------------------------
pcp_init_search() {
	ORIG_MYMIRROR=$(cat /opt/tcemirror)
	MINUTES="+120"

	ANSWER=$(find $TAGS_PICORE_DB -mmin $MINUTES)
	if [ $ANSWER != "" ] || [ ! -f $TAGS_PICORE_DB ]; then
		echo $PICORE_REPO_1 > /opt/tcemirror
		search.sh picoreplayer
		sudo mv /tmp/tags.db $TAGS_PICORE_DB

#		tce-size picoreplayer
#		sudo mv /tmp/sizelist $SIZELIST_PICORE

	fi

	ANSWER=$(find $TAGS_PCP_DB -mmin $MINUTES)
	if [ $ANSWER != "" ] || [ ! -f $TAGS_PCP_DB ]; then
		echo $PCP_REPO > /opt/tcemirror
		search.sh picoreplayer
		sudo mv /tmp/tags.db $TAGS_PCP_DB

		tce-size picoreplayer
		sudo mv /tmp/sizelist $SIZELIST_PCP

	fi

#	cat $SIZELIST_PICORE > /tmp/sizelist
#	cat $SIZELIST_PCP >> /tmp/sizelist

	echo $ORIG_MYMIRROR > /opt/tcemirror
}

#========================================================================================
# Cleanup temporary files.
# Note: Temporary files are written to /tmp so they will be deleted by a reboot.
#----------------------------------------------------------------------------------------
pcp_cleanup() {
#	rm -f /tmp/tags.db
	rm -f /tmp/*.treeXXX
	rm -f /tmp/sizelistXXX
}

#========================================================================================
# This routine creates /opt/localmirrors
#----------------------------------------------------------------------------------------
pcp_create_localmirrors() {
	echo $PICORE_REPO_1 > /opt/localmirrors
	echo $PCP_REPO >> /opt/localmirrors
}

#========================================================================================
# Repository/extension information message
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
	echo '                  <li><b>piCorePlayer repository</b> - maintained by the piCorePlayer team.</li>'
	echo '                </ul>'
	echo '                <p><b>Extensions</b> can be:</p>'
	echo '                <ul>'
	echo '                  <li><b>Available</b> - the extension is available for download from the above repositories.</li>'
	echo '                  <li><b>Installed</b> - the extension has been downloaded to local storage and installed.</li>'
	echo '                  <li><b>Uninstalled</b> - the extension has been downloaded to local storage but not installed.</li>'
	echo '                  <li><b>Downloaded</b> - the extension has been downloaded to local storage.</li>'
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
# The following section of code is based on piCore tce-ab script
#----------------------------------------------------------------------------------------
pcp_display_info() {
#	if [ -n "$EXTN" ]; then
		sudo -u tc tce-fetch.sh "${EXTN}.info"
		if [ $? -eq 0 ]; then
			cat "${EXTN}.info"
#			rm -f "${EXTN}.info"
		else
			echo "${EXTN}.info not found!"
		fi
#	fi
}

pcp_display_depends() {
	sudo -u tc tce-fetch.sh "${EXTN}.dep"
	if [ $? -eq 0 ]; then
		cat "${EXTN}.dep"
#		rm -f "${EXTN}.dep"
	else
		echo "${EXTN}.dep not found!"
	fi
}

pcp_display_tree() {
	sudo -u tc tce-fetch.sh "${EXTN}.tree"
	if [ $? -eq 0 ]; then
		cat "${EXTN}.tree"
#		rm -f "${EXTN}.tree"
	else
		echo "${EXTN}.tree not found!"
	fi
}

# Downloads sizelist
pcp_display_size() {
	sudo -u tc tce-size "$EXTN"
}

pcp_display_files() {
	sudo -u tc tce-fetch.sh "${EXTN}.list"
	if [ $? -eq 0 ]; then
		cat "${EXTN}.list"
#		rm -f "${EXTN}.list"
	else
		echo "${EXTN}.list not found!"
	fi
}

#========================================================================================
# Display Extension information - information, dependences, tree, size, files
#----------------------------------------------------------------------------------------
pcp_display_information() {
	if [ $EXTNFOUND -eq 1 ]; then
		pcp_start_row_shade
		echo '<table class="bggrey">'
		echo '  <tr>'
		echo '    <td>'
		echo '      <form name="Extension_size" method="get">'
		echo '        <div class="row">'
		echo '          <fieldset>'
		echo "            <legend>Information for '$EXTN'. . . </legend>"
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
	fi
}

#========================================================================================
# Check for internet, TinyCore and piCore repository access
#----------------------------------------------------------------------------------------
pcp_internet_check() {
	INTERNET=TRUE
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
		INTERNET=FALSE
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
		INTERNET=FALSE
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
		pcp_green_tick "piCorePlayer repository accessible."
	else
		pcp_red_cross "piCorePlayer repository not accessible."
		INTERNET=FALSE
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
}

#========================================================================================
# Display disk space using df
#----------------------------------------------------------------------------------------
pcp_free_space_check() {
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <form name="diskspace" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Checking free space. . . </legend>'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column210 center">'
	echo '                  <p>'$(pcp_free_space)' free space</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p><b>WARNING:</b> Check you have sufficient free space before you download the required extension.</p>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}

#========================================================================================
# Display tce mirror
#----------------------------------------------------------------------------------------
pcp_tce_mirror() {
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
}

#========================================================================================
# Select repository
#----------------------------------------------------------------------------------------
pcp_set_repo_status() {
	MYMIRROR=$(cat /opt/tcemirror)

	case "$MYMIRROR" in
		"$PICORE_REPO_1")
			SELECTED_PICORE="selected"
			STATUS="Official piCore repository"
			DB="$TAGS_PICORE_DB"
		;;
		"$PCP_REPO")
			SELECTED_PCP="selected"
			STATUS="piCorePlayer repository"
			DB="$TAGS_PCP_DB"
		;;
	esac
}

pcp_select_repository() {
	pcp_set_repo_status
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
	echo '                    <option value="'$PICORE_REPO_1'" '$SELECTED_PICORE'>Official piCore repository</option>'
	echo '                    <option value="'$PCP_REPO'" '$SELECTED_PCP'>piCorePlayer repository</option>'
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
	echo '                      <li>piCorePlayer repository.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#----------------------------------------------------------------------------------------
	pcp_toggle_row_shade
	if [ "$SELECTED_PICORE" = "selected" ]; then
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td colspan="3">'
		echo '                  <input type="submit" name="SUBMIT" value="Set">'
		echo '                  <input type="hidden" name="CALLED_BY" value="'$CALLED_BY'">'
		echo '                </td>'
		echo '              </tr>'
	else
		echo '              <tr class="warning">'
		echo '                <td class="column150">'
		echo '                  <input type="submit" name="SUBMIT" value="Reset">'
		echo '                  <input type="hidden" name="CALLED_BY" value="'$CALLED_BY'">'
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
}

#========================================================================================
# Available extensions from current tags_*.db
#----------------------------------------------------------------------------------------
pcp_show_available_extns() {
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

	                          for E in $(cat $DB | awk '{print $1}')
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
	echo '                      <li>If the <b>Official piCore repository</b> is selected, only piCore extensions are listed.</li>'
	echo '                      <li>If the <b>piCorePlayer repository</b> is selected, only piCorePlayer extensions are listed.</li>'
	echo '                    </ul>'
	echo '                    <p>Buttons:</p>'
	echo '                    <ul>'
	echo '                      <li><b>[Info]</b> will display additional information about the extension.</li>'
	echo '                      <li><b>[Load]</b> will load and install the extension.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Info">'
	echo '                  <input type="submit" name="SUBMIT" value="Load">'
	echo '                  <input type="hidden" name="CALLED_BY" value="'$CALLED_BY'">'
	echo '                  <input type="hidden" name="DB" value="'$DB'">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}

#========================================================================================
# Installed extensions - tce-status -i
#----------------------------------------------------------------------------------------
pcp_show_installed_extns() {
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

	                          for i in $(tce-status -i | sort -f)
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
	echo '                      <li>These extensions are usually loaded at boot via '$ONBOOTLST'.</li>'
	echo '                    </ul>'
	echo '                    <p>Buttons:</p>'
	echo '                    <ul>'
	echo '                      <li><b>[Info]</b> will display additional information about the extension.</li>'
	echo '                      <li><b>[Update]</b> will check for a new version and update the extension if needed.</li>'
	echo '                      <li><b>[Delete]</b> will delete the extension and dependencies on reboot.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
#	echo '                  <input type="submit" name="SUBMIT" value="Info">'
#	echo '                  <input type="submit" name="SUBMIT" value="Update">'
	echo '                  <input type="submit" name="SUBMIT" value="Delete">'
	echo '                  <input type="hidden" name="CALLED_BY" value="Installed">'
	echo '                  <input type="hidden" name="DB" value="'$DB'">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}

#========================================================================================
# Uninstalled extensions - tce-status -u
#----------------------------------------------------------------------------------------
pcp_show_uninstalled_extns() {
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

	                          for i in $(tce-status -u | sort -f)
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
	echo '                    <p>Buttons:</p>'
	echo '                    <ul>'
	echo '                      <li><b>[Info]</b> will display additional information about the extension.</li>'
	echo '                      <li><b>[Install]</b> will install the extension.</li>'
	echo '                      <li><b>[Delete]</b> will delete the extension and dependencies on reboot.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
#	echo '                  <input type="submit" name="SUBMIT" value="Info">'
#	echo '                  <input type="submit" name="SUBMIT" value="Install">'
	echo '                  <input type="submit" name="SUBMIT" value="Delete">'
	echo '                  <input type="hidden" name="CALLED_BY" value="Uninstalled">'
	echo '                  <input type="hidden" name="DB" value="'$DB'">'
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}

#========================================================================================
# Downloaded extensions in /mnt/mmcblk0p2/tce/optional/ on SD card
#----------------------------------------------------------------------------------------
pcp_show_downloaded_extns() {
	pcp_set_repo_status
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

	                          for E in $(ls $PACKAGEDIR/*.tcz | awk -F 'optional/' '{print $2}' | sort -f)
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
	echo '                    <p>Buttons:</p>'
	echo '                    <ul>'
	echo '                      <li><b>[Info]</b> will display additional information about the extension.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
#	pcp_toggle_row_shade
#	echo '              <tr class="'$ROWSHADE'">'
#	echo '                <td colspan="3">'
#	echo '                  <input type="submit" name="SUBMIT" value="Info">'
#	echo '                  <input type="hidden" name="CALLED_BY" value="Downloaded">'
#	echo '                  <input type="hidden" name="DB" value="'$DB'">'
#	echo '                </td>'
#	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}

#========================================================================================
# Show current onboot.lst - these are the extensions loaded during a boot.
#----------------------------------------------------------------------------------------
pcp_show_onboot_lst() {
	pcp_table_top "Current $ONBOOTLST"
	                      pcp_textarea_inform "none" "cat $ONBOOTLST" 50
	pcp_table_end
}

#========================================================================================
# Extension dependency tree
#----------------------------------------------------------------------------------------
pcp_dependency_tree() {
	if [ -n "$1" ]; then
		app=${1%.tcz}
		app="$app.tcz"
		localtce="/mnt/mmcblk0p2/tce/optional"
		kernel=$(uname -r)
		indent=""
		pcp_get_dependencies $app
	fi
}

pcp_get_dependencies() {
	app=${1//KERNEL/$kernel}
	echo -n "$indent"
	echo -n "-----"
	echo "$app"
	deplist=$(cat /mnt/mmcblk0p2/tce/optional/"$app.dep" 2>/dev/null)
	for depapp in $deplist; do
		indent="${indent}     |"
		pcp_get_dependencies $depapp
	done
	indent=${indent%     |}
}

pcp_full_dependency_tree() {
	[ "$1" != "text" ] && pcp_table_textarea_top "Extension dependency tree" "" "300"
	for E in $(cat $ONBOOTLST); do
		pcp_dependency_tree $E
		echo ""
	done
	[ "$1" != "text" ] && pcp_table_textarea_end
}

#========================================================================================
# Tabs.
#----------------------------------------------------------------------------------------
pcp_generate_report
pcp_debug_info

echo '<!-- Start of pcp_extension_tabs toolbar -->'
echo '<p style="margin-top:8px;">'

[ x"" = x"$CALLED_BY" ] && CALLED_BY="Information"
for tab in Information Available  Installed Uninstalled Downloaded onboot.lst; do
	[ "$tab" = "$CALLED_BY" ] && TAB_STYLE="tab7a" || TAB_STYLE="tab7"
	echo '  <a class="'$TAB_STYLE'" href="'$0'?CALLED_BY='$tab'" title="'$tab'">'$tab'</a>'
done

echo '</p>'
echo '<div class="tab7end" style="margin-bottom:10px;">pCP</div>'
echo '<!-- End of pcp_extension_tabs toolbar -->'

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
case "$CALLED_BY" in
	Information)
		pcp_information_message
		pcp_free_space_check
		pcp_internet_check
		pcp_init_search
		[ $DEBUG -eq 1 ] && pcp_tce_mirror
	;;
	Available)
		case "$SUBMIT" in
			Set) pcp_set_repository; pcp_cleanup;;
			Reset) pcp_reset_repository; pcp_cleanup;;
		esac
		pcp_select_repository
		pcp_show_available_extns
		pcp_search_extn
		case "$SUBMIT" in
			Info) pcp_display_information;;
			Load) pcp_load_extn;;
		esac
	;;
	Installed)
		pcp_show_installed_extns
		case "$SUBMIT" in
#			Info) pcp_find_extn; pcp_display_information;;
#			Update) pcp_update_extn;;
			Delete) pcp_delete_extn;;
		esac
	;;
	Uninstalled)
		pcp_show_uninstalled_extns
		case "$SUBMIT" in
#			Info) pcp_find_extn; pcp_display_information;;
			Install) pcp_install_extn;;
			Delete) pcp_delete_extn;;
		esac
	;;
	Downloaded)
		pcp_show_downloaded_extns
		case "$SUBMIT" in
#			Info) pcp_find_extn; pcp_display_information;;
			Delete) pcp_delete_extn;;
		esac
	;;
	onboot.lst)
		pcp_show_onboot_lst
		pcp_full_dependency_tree html
	;;
esac
#----------------------------------------------------------------------------------------

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
