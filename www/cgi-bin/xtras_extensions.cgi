#!/bin/sh

# Version: 7.0.0 2020-05-04

#========================================================================================
# This script downloads, installs, deletes, updates and reports on extensions.
#
# Complications:
#   1. Juggling multiple repositories that aren't mirrors.
#   2. Uses tce-load and /opt/tcemirror to store current repository.
#   3. Trying to incorporate BOTH $PCP_CUR_REPO and /opt/tcemirror.
#   4. tags_*.db are an attempt to work out which repository the extension was
#      downloaded from. Half implemented.
#   5. Sufficient space, need to expand file system.
#----------------------------------------------------------------------------------------

. /etc/init.d/tc-functions
. pcp-functions
. pcp-lms-functions

pcp_html_head "Add piCore extension" "GE"

pcp_controls
pcp_navbar
pcp_httpd_query_string
pcp_debug_info

#========================================================================================
# Set variables
#----------------------------------------------------------------------------------------
cd /tmp
TCELOAD="tce-load"
EXTNFOUND=0
LOG="${LOGDIR}/pcp_extensions.log"
PCP_REPO_1="${PCP_REPO_1%/}/"
PCP_REPO_2="${PCP_REPO_2%/}/"
[ $PCP_CUR_REPO -eq 1 ] && PCP_REPO="$PCP_REPO_1" || PCP_REPO="$PCP_REPO_2"
TAGS_PCP_DB="/tmp/tags_pcp.db"
TAGS_PICORE_DB="/tmp/tags_picore.db"
SIZELIST_PCP="/tmp/sizelist_pcp"
SIZELIST_PICORE="/tmp/sizelist_picore"
KERNEL="$(uname -r)"

ACCCESSIBLETXT="/tmp/accessible.txt"
sudo chmod 777 $ACCCESSIBLETXT
[ -f /tmp/accessible.txt ] && . /tmp/accessible.txt

#========================================================================================
# Display debug information
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	if [ $DEBUG -eq 1 ]; then
		echo '<!-- Start of debug info -->'
		echo '<div>' #"Debug"
		pcp_debug_variables "html" EXTN SUBMIT MYMIRROR MIRROR LOG \
			PCP_CUR_REPO PCP_REPO PCP_REPO_1 PCP_REPO_2 PICORE_REPO_1 PICORE_REPO_2 \
			CALLED_BY EXTNFOUND KERNELVER PACKAGEDIR KERNEL
		echo '</div>'
		echo '<!-- End of debug info -->'
	fi
}

#========================================================================================
# Generate extensions report
#----------------------------------------------------------------------------------------
pcp_generate_report() {
	ORIG_PWD="$PWD"
	(echo $0; date) > $LOG
	cat /etc/motd >> $LOG
	echo "" >> $LOG
	pcp_write_to_log "Installed extensions" "tce-status -i | sort -f"
	pcp_write_to_log "Uninstalled extensions" "tce-status -u | sort -f"
	pcp_write_to_log "Downloaded extensions" "cd $PACKAGEDIR; ls *.tcz | sort -f"
	pcp_write_to_log "onboot.lst" "cat $ONBOOTLST"
	pcp_write_to_log "Extension dependency tree" "pcp_full_dependency_tree text"
	cd "$ORIG_PWD"
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
		[ $PCP_CUR_REPO -eq 1 ] && MYMIRROR="$PICORE_REPO_1" || MYMIRROR="$PICORE_REPO_2"
		EXTNFOUND=1
	fi
	pcp_set_repository
}

#========================================================================================
# Set active repository to $MYMIRROR
#----------------------------------------------------------------------------------------
pcp_set_repository() {
	echo $MYMIRROR > /opt/tcemirror

	case ${MYMIRROR%/} in
		"${PICORE_REPO_1%/}") PCP_CUR_REPO=1; pcp_save_to_config;;
		"${PICORE_REPO_2%/}") PCP_CUR_REPO=2; pcp_save_to_config;;
	esac
}

#========================================================================================
# Download and install extension.
# Note: Extension will be added to onboot.lst
#----------------------------------------------------------------------------------------
pcp_load_extn() {
	echo '<div>'
	pcp_textarea "Loading '$EXTN'" "sudo -u tc $TCELOAD -iw $EXTN" 10
	echo '</div>'
}

#========================================================================================
# Temporarily install extension.
# Note: Extension will need to be already downloaded.
#       Extension will not be added to onboot.lst
#----------------------------------------------------------------------------------------
pcp_install_extn() {
	echo '<div>'
	pcp_textarea "Installing '$EXTN'" "sudo -u tc $TCELOAD -i $EXTN" 10
	echo '</div>'
}

#========================================================================================
# Uninstall extension.
# Note: This will remove the extension from onboot.lst but will not delete the extension.
#       NOT IMPLEMENTED.
#----------------------------------------------------------------------------------------
#pcp_uninstall_extn() {
#	pcp_table_top "Uninstalling '$EXTN' . . . "
#	pcp_textarea "none" "sudo -u tc $TCELOAD -i $EXTN" 50
#	pcp_table_end
#}

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
	pcp_textarea "none" "sudo -u tc pcp-update $EXTN" 50
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
#		tce-size picoreplayer
#		sudo mv /tmp/sizelist $SIZELIST_PCP
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
	rm -f /tmp/tags.db
	rm -f /tmp/*.tree
	rm -f /tmp/sizelist
}

#========================================================================================
# This routine creates /opt/localmirrors
#----------------------------------------------------------------------------------------
pcp_create_localmirrors() {
	echo $PCP_REPO > /opt/localmirrors
	echo $PICORE_REPO_1 >> /opt/localmirrors
}

#========================================================================================
# Repository/extension information message
#----------------------------------------------------------------------------------------
pcp_information_message() {
	echo '<div>'  # "Information"
	echo '                <p><b>piCorePlayer</b> uses 3 repositories for downloading extensions:</p>'
	echo '                <ul>'
	echo '                  <li><b>piCorePlayer main repository</b> - maintained by the piCorePlayer team (default).</li>'
	echo '                  <li><b>piCorePlayer mirror repository</b> - maintained by the piCorePlayer team.</li>'
	echo '                  <li><b>Official piCore repository</b> - maintained by the piCore/TinyCore team.</li>'
	echo '                </ul>'
	echo '                <p><b>Extensions</b> can be:</p>'
	echo '                <ul>'
	echo '                  <li><b>Available</b> - the extension is available for download from the above repositories.</li>'
	echo '                  <li><b>Installed</b> - the extension has been downloaded to local storage and installed.</li>'
	echo '                  <li><b>Uninstalled</b> - the extension has been downloaded to local storage but not installed.</li>'
#	echo '                  <li><b>Downloaded</b> - the extension has been downloaded to local storage.</li>'
	echo '                </ul>'
	echo '</div>'
}

#========================================================================================
# The following section of code is based on piCore tce-ab script
#----------------------------------------------------------------------------------------
pcp_display_info() {
		sudo -u tc tce-fetch.sh "${EXTN}.info"
		if [ $? -eq 0 ]; then
			cat "${EXTN}.info"
#			rm -f "${EXTN}.info"
		else
			echo "${EXTN}.info not found!"
		fi
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
		sudo sed -i "s/KERNEL/${KERNEL}/" ${EXTN}.tree
		cat "${EXTN}.tree"
#		sudo chmod 444 "${EXTN}.tree"
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

		echo '      <form name="Extension_size" method="get">'
		echo '        <div class="row">'

		echo "            <h5>Information for '$EXTN'. . . </h5>"
		echo '            <table class="bggrey percent100">'
		#--------------------------------------------------------------------------------

		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		echo '                  <p><b>Information:</b></p>'
		echo '                </td>'
		echo '              </tr>'

		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		                        pcp_textarea "none" "pcp_display_info" 200
		echo '                </td>'
		echo '              </tr>'
		#--------------------------------------------------------------------------------
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		echo '                  <p><b>Dependencies:</b></p>'
		echo '                </td>'
		echo '              </tr>'

		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		                        pcp_textarea "none" "pcp_display_depends" 100
		echo '                </td>'
		echo '              </tr>'
		#--------------------------------------------------------------------------------

		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		echo '                  <p><b>Tree:</b></p>'
		echo '                </td>'
		echo '              </tr>'

		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		                        pcp_textarea "none" "pcp_display_tree" 100
		echo '                </td>'
		echo '              </tr>'
		#--------------------------------------------------------------------------------

		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		echo '                  <p><b>Size:</b></p>'
		echo '                </td>'
		echo '              </tr>'

		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		                        pcp_textarea "none" "pcp_display_size" 100
		echo '                </td>'
		echo '              </tr>'
		#--------------------------------------------------------------------------------

		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		echo '                  <p><b>Files:</b></p>'
		echo '                </td>'
		echo '              </tr>'

		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td>'
		                        pcp_textarea "none" "pcp_display_files" 100
		echo '                </td>'
		echo '              </tr>'
		#--------------------------------------------------------------------------------

		echo '        </div>'
		echo '      </form>'

	fi
}

#========================================================================================
# Check for access to the Internet, piCorePlayer and piCore repositories
#----------------------------------------------------------------------------------------
pcp_internet() {
	if [ $(pcp_internet_accessible) -eq 0 ]; then
		pcp_green_tick "Internet accessible."
		echo "[  OK  ] Internet accessible." >> $LOG
		echo "INTERNET_ACCESSIBLE=true" > $ACCCESSIBLETXT
	else
		pcp_red_cross "Internet not accessible."
		echo "[ ERROR ] Internet not accessible." >> $LOG
		echo "unset INTERNET_ACCESSIBLE" > $ACCCESSIBLETXT
	fi
}

pcp_dns() {
	if [ $(pcp_dns_accessible) -eq 0 ]; then
		pcp_green_tick "DNS accessible."
		echo "[  OK  ] DNS accessible." >> $LOG
		echo "DNS_ACCESSIBLE=true" >> $ACCCESSIBLETXT
	else
		pcp_red_cross "DNS not accessible."
		echo "[ ERROR ] DNS not accessible." >> $LOG
		echo "unset DNS_ACCESSIBLE" >> $ACCCESSIBLETXT
	fi
}

pcp_pcp_repo_1() {
	if [ $(pcp_pcp_repo_1_accessible) -eq 0 ]; then
		pcp_green_tick "piCorePlayer main repository accessible ($PCP_REPO_1)."
		echo "[  OK  ] piCorePlayer main repository accessible. ($PCP_REPO_1)" >> $LOG
		echo "PCP_REPO_1_ACCESSIBLE=true" >> $ACCCESSIBLETXT
	else
		pcp_red_cross "piCorePlayer main repository not accessible ($PCP_REPO_1)."
		echo "[ ERROR ] piCorePlayer main repository not accessible. ($PCP_REPO_1)" >> $LOG
		echo "unset PCP_REPO_1_ACCESSIBLE" >> $ACCCESSIBLETXT
	fi
}

pcp_pcp_repo_2() {
	if [ $(pcp_pcp_repo_2_accessible) -eq 0 ]; then
		pcp_green_tick "piCorePlayer mirror repository accessible ($PCP_REPO_2)."
		echo "[  OK  ] piCorePlayer mirror repository accessible. ($PCP_REPO_2)" >> $LOG
		echo "PCP_REPO_2_ACCESSIBLE=true" >> $ACCCESSIBLETXT
	else
		pcp_red_cross "piCorePlayer mirror repository not accessible ($PCP_REPO_2)."
		echo "[ ERROR ] piCorePlayer mirror repository not accessible. ($PCP_REPO_2)" >> $LOG
		echo "unset PCP_REPO_2_ACCESSIBLE" >> $ACCCESSIBLETXT
	fi
}

pcp_picore_repo_1() {
	if [ $(pcp_picore_repo_1_accessible) -eq 0 ]; then
		pcp_green_tick "Official piCore repository accessible ($PICORE_REPO_1)."
		echo "[  OK  ] Official piCore repository accessible. ($PICORE_REPO_1)" >> $LOG
		echo "PICORE_REPO_1_ACCESSIBLE=true" >> $ACCCESSIBLETXT
	else
		pcp_red_cross "Official piCore repository not accessible ($PICORE_REPO_1)."
		echo "[ ERROR ] Official piCore repository not accessible. ($PICORE_REPO_1)" >> $LOG
		echo "unset PICORE_REPO_1_ACCESSIBLE" >> $ACCCESSIBLETXT
	fi
}

pcp_picore_repo_2() {
	if [ $(pcp_picore_repo_2_accessible) -eq 0 ]; then
		pcp_green_tick "Official piCore mirror repository accessible ($PICORE_REPO_2)."
		echo "[  OK  ] Official piCore mirror repository accessible. ($PICORE_REPO_2)" >> $LOG
		echo "PICORE_REPO_2_ACCESSIBLE=true" >> $ACCCESSIBLETXT
	else
		pcp_red_cross "Official piCore mirror repository not accessible ($PICORE_REPO_2)."
		echo "[ ERROR ] Official piCore mirror repository not accessible. ($PICORE_REPO_2)" >> $LOG
		echo "unset PICORE_REPO_2_ACCESSIBLE" >> $ACCCESSIBLETXT
	fi
}

pcp_indicator_js() {
	echo '<script>'
	echo 'var theIndicator = document.querySelector("#indicator'$ID'");'
	echo '	theIndicator.classList.add("'$CLASS'");'
	echo '	document.getElementById("indicator'$ID'").innerHTML = "'$INDICATOR'";'
	echo '	document.getElementById("status'$ID'").innerHTML = "'$STATUS'";'
	echo '</script> '
}

#----------------------------------------------------------------------------------------
# Internet, DNS and repository accessibility indicators.
#----------------------------------------------------------------------------------------
pcp_internet_check() {

	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Checking Internet and repository accessiblity. . . </legend>'
	#--------------------------------Internet accessible---------------------------------
	pcp_incr_id

	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column50 center">'
	echo '                <p id="indicator'$ID'">?</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p id="status'$ID'">Checking internet...</p>'
	echo '              </td>'
	echo '            </tr>'
	pcp_internet
	pcp_indicator_js
	#-----------------------------------DNS accessible-----------------------------------
	pcp_incr_id

	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column50 center">'
	echo '                <p id="indicator'$ID'">?</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p id="status'$ID'">Checking DNS...</p>'
	echo '              </td>'
	echo '            </tr>'
	pcp_dns
	pcp_indicator_js
	#-------------------------piCorePlayer repository 1 accessible-----------------------
	pcp_incr_id

	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column50 center">'
	echo '                <p id="indicator'$ID'">?</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p id="status'$ID'">Checking piCorePlayer repository...</p>'
	echo '              </td>'
	echo '            </tr>'
	pcp_pcp_repo_1
	pcp_indicator_js
	#-------------------------piCorePlayer repository 2 accessible-----------------------
	pcp_incr_id

	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column50 center">'
	echo '                <p id="indicator'$ID'">?</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p id="status'$ID'">Checking piCorePlayer miror repository...</p>'
	echo '              </td>'
	echo '            </tr>'
	pcp_pcp_repo_2
	pcp_indicator_js
	#------------------------Official piCore repository accessible-----------------------
	pcp_incr_id

	echo '            <tr class="'$ROWSHADE'">'
	echo '              <td class="column50 center">'
	echo '                <p id="indicator'$ID'">?</p>'
	echo '              </td>'
	echo '              <td>'
	echo '                <p id="status'$ID'">Checking piCore repository...</p>'
	echo '              </td>'
	echo '            </tr>'
	pcp_picore_repo_1
	pcp_indicator_js
	#--------------------Official piCore mirror repository accessible--------------------
	if [ $MODE -ge $MODE_DEVELOPER ]; then
		pcp_incr_id

		echo '            <tr class="'$ROWSHADE'">'
		echo '              <td class="column50 center">'
		echo '                <p id="indicator'$ID'">?</p>'
		echo '              </td>'
		echo '              <td>'
		echo '                <p id="status'$ID'">Checking piCore mirror repository...</p>'
		echo '              </td>'
		echo '            </tr>'
		pcp_picore_repo_2
		pcp_indicator_js
	fi
	#------------------------------------------------------------------------------------
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'

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
	echo '            <legend>Check free space. . . </legend>'
	echo '            <table class="bggrey percent100">'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column210 center">'
	echo '                  <p>'$(pcp_free_space)' free space</p>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p><b>WARNING:</b> Check there is sufficient free space before downloading extensions.</p>'
	echo '                  <p>Use [ Main Page ] > <a href="xtras_resize.cgi">[ Resize FS ]</a> to increase the size of partition 2 (if required).</p>'
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

	echo '      <form name="tce_mirror" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Current tcemirror/tcedir</legend>'
	echo '            <table class="bggrey percent100">'
	pcp_start_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td>'
	                        read MIRROR < /opt/tcemirror
	                        pcp_textarea "none" 'echo "$MIRROR"' 15
	                        RESULT=$(ls -al /etc/sysconfig | grep tcedir)
	                        pcp_textarea "none" 'echo "$RESULT"' 15
	echo '                </td>'
	echo '              </tr>'
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'

}

#========================================================================================
# Select repository
#----------------------------------------------------------------------------------------
pcp_set_repo_status() {
	read MYMIRROR < /opt/tcemirror

	case "${MYMIRROR%/}" in
		"${PCP_REPO_1%/}")
			SELECTED_PCP_1="selected"
			STATUS="piCorePlayer main repository"
			DB="$TAGS_PCP_DB"
			PCP_CUR_REPO=1
			pcp_save_to_config
		;;
		"${PCP_REPO_2%/}")
			SELECTED_PCP_2="selected"
			STATUS="piCorePlayer mirror repository"
			DB="$TAGS_PCP_DB"
			PCP_CUR_REPO=2
			pcp_save_to_config
		;;
		"${PICORE_REPO_1%/}")
			SELECTED_PICORE="selected"
			STATUS="Official piCore repository"
			DB="$TAGS_PICORE_DB"
		;;
	esac
}

pcp_select_repository() {
	pcp_set_repo_status

	echo '      <form name="current_repository" action="'$0'" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Set extension repository</legend>'
	pcp_debug_variables "html" INTERNET_ACCESSIBLE DNS_ACCESSIBLE CALLED_BY PCP_CUR_REPO MYMIRROR PCP_REPO PCP_REPO_1 PCP_REPO_2 PICORE_REPO_1
	echo '            <table class="bggrey percent100">'
	#------------------------------------------------------------------------------------
	pcp_incr_id
	pcp_start_row_shade

	if [ $INTERNET_ACCESSIBLE -a $DNS_ACCESSIBLE ]; then
		if [ $PCP_REPO_1_ACCESSIBLE ]; then
			PCP_REPO_1_ACCESS="(Accessible)"
		else
			PCP_REPO_1_ACCESS="(Not Accessible)"
			PCP_REPO_1_DISABLED="disabled"
		fi
		if [ $PCP_REPO_2_ACCESSIBLE ]; then
			PCP_REPO_2_ACCESS="(Accessible)"
		else
			PCP_REPO_2_ACCESS="(Not Accessible)"
			PCP_REPO_2_DISABLED="disabled"
		fi
		if [ $PICORE_REPO_1_ACCESSIBLE ]; then
			PICORE_REPO_1_ACCESS="(Accessible)"
		else
			PICORE_REPO_1_ACCESS="(Not Accessible)"
			PICORE_REPO_1_DISABLED="disabled"
		fi
	else
		PCP_REPO_1_ACCESS="(Not Accessible)"
		PCP_REPO_1_DISABLED="disabled"
		PCP_REPO_2_ACCESS="(Not Accessible)"
		PCP_REPO_2_DISABLED="disabled"
		PICORE_REPO_1_ACCESS="(Not Accessible)"
		PICORE_REPO_1_DISABLED="disabled"
	fi

	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>Current repository</p>'
	echo '                </td>'
	echo '                <td class="column300">'
	echo '                  <select class="large22" name="MYMIRROR">'
	echo '                    <option value="'$PCP_REPO_1'" '$SELECTED_PCP_1' '$PCP_REPO_1_DISABLED'>piCorePlayer main repository '$PCP_REPO_1_ACCESS'</option>'
	echo '                    <option value="'$PCP_REPO_2'" '$SELECTED_PCP_2' '$PCP_REPO_2_DISABLED' >piCorePlayer mirror repository '$PCP_REPO_2_ACCESS'</option>'
	echo '                    <option value="'$PICORE_REPO_1'" '$SELECTED_PICORE' '$PICORE_REPO_1_DISABLED'>Official piCore repository '$PICORE_REPO_1_ACCESS'</option>'
	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Select extension repository&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Select the required extension repository:</p>'
	echo '                    <ul>'
	echo '                      <li>piCorePlayer main repository (default)</li>'
	echo '                      <li>piCorePlayer mirror repository</li>'
	echo '                      <li>Official piCore repository.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------

	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Set">'
	echo '                  <input type="hidden" name="CALLED_BY" value="'$CALLED_BY'">'
	echo '                </td>'
	echo '              </tr>'
	if [ "$SELECTED_PCP_1" != "selected" ]; then
		echo '              <tr class="'$ROWSHADE'">'
		echo '                <td class="column150">'
		echo '                  <input type="submit" name="SUBMIT" value="Reset">'
		echo '                </td>'
		echo '                <td colspan="2">'
		echo '                  <p><b>WARNING:</b> Remember to press [Reset] before leaving this page.</p>'
		echo '                </td>'
		echo '              </tr>'
	fi
	#------------------------------------------------------------------------------------
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'

}

#========================================================================================
# Available extensions from current tags_*.db
#----------------------------------------------------------------------------------------
pcp_show_available_extns() {

	echo '      <form name="available" action="'$0'" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Available extensions in the '$STATUS'</legend>'
	echo '            <table class="bggrey percent100">'
	#------------------------------------------------------------------------------------
	pcp_incr_id

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
	echo '                  <p>List of '$(cat $DB | wc -l)' extensions available in the '$STATUS'&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>Lists all '$(cat $DB | wc -l)' extensions that are currently available for download from '$STATUS'</li>'
	echo '                    </ul>'
	echo '                    <p>Buttons:</p>'
	echo '                    <ul>'
	echo '                      <li><b>[Info]</b> will display information about the selected extension.</li>'
	echo '                      <li><b>[Load]</b> will load and install the selected extension.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
	echo '                  <input type="submit" name="SUBMIT" value="Info">'
	echo '                  <input type="submit" name="SUBMIT" value="Load">'
	echo '                  <input type="hidden" name="CALLED_BY" value="'$CALLED_BY'">'
	echo '                  <input type="hidden" name="DB" value="'$DB'">'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'

}

#========================================================================================
# Installed extensions - tce-status -i
#----------------------------------------------------------------------------------------
pcp_show_installed_extns() {

	echo '      <form name="installed" action="'$0'" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Installed extensions</legend>'
	echo '            <table class="bggrey percent100">'
	#------------------------------------------------------------------------------------
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
	echo '                  <p>List of '$(tce-status -i | wc -l)' installed extensions&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>Lists all extensions that are currently installed.</li>'
	echo '                      <li>These extensions are usually loaded at boot via '$ONBOOTLST'.</li>'
	echo '                      <li>There are '$(find /usr/local/tce.installed -not -type d | wc -l)' extensions in the tce.installed directory.</li>'
	echo '                    </ul>'
	echo '                    <p>Buttons:</p>'
	echo '                    <ul>'
#	echo '                      <li><b>[Info]</b> will display additional information about the extension.</li>'
	echo '                      <li><b>[Update]</b> will check for a new version and update the selected extension if needed.</li>'
	echo '                      <li><b>[Delete]</b> will delete the selected extension and dependencies on reboot.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
#	echo '                  <input type="submit" name="SUBMIT" value="Info">'
	echo '                  <input type="submit" name="SUBMIT" value="Update">'
	echo '                  <input type="submit" name="SUBMIT" value="Delete">'
	echo '                  <input type="hidden" name="CALLED_BY" value="Installed">'
	echo '                  <input type="hidden" name="DB" value="'$DB'">'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'

}

#========================================================================================
# Uninstalled extensions - tce-status -u
#----------------------------------------------------------------------------------------
pcp_show_uninstalled_extns() {

	echo '      <form name="uninstalled" action="'$0'" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Uninstalled extensions</legend>'
	echo '            <table class="bggrey percent100">'
	#------------------------------------------------------------------------------------
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
	echo '                  <p>List of '$(tce-status -u | wc -l)' uninstalled extensions&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>Lists all extensions that are currently downloaded but not installed.</li>'
	echo '                    </ul>'
	echo '                    <p>Buttons:</p>'
	echo '                    <ul>'
#	echo '                      <li><b>[Info]</b> will display additional information about the extension.</li>'
#	echo '                      <li><b>[Install]</b> will install the extension.</li>'
	echo '                      <li><b>[Update]</b> will check for a new version and update the extension if needed.</li>'
	echo '                      <li><b>[Delete]</b> will delete the extension and dependencies on reboot.</li>'
	echo '                    </ul>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan="3">'
#	echo '                  <input type="submit" name="SUBMIT" value="Info">'
#	echo '                  <input type="submit" name="SUBMIT" value="Install">'
	echo '                  <input type="submit" name="SUBMIT" value="Update">'
	echo '                  <input type="submit" name="SUBMIT" value="Delete">'
	echo '                  <input type="hidden" name="CALLED_BY" value="Uninstalled">'
	echo '                  <input type="hidden" name="DB" value="'$DB'">'
	echo '                </td>'
	echo '              </tr>'
	#------------------------------------------------------------------------------------
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'

}

#========================================================================================
# Downloaded extensions in /mnt/mmcblk0p2/tce/optional/ on SD card
# GE - NOT USED.
#----------------------------------------------------------------------------------------
pcp_show_downloaded_extns() {
	pcp_set_repo_status

	echo '      <form name="downloaded" action="'$0'" method="get">'
	echo '        <div class="row">'
	echo '          <fieldset>'
	echo '            <legend>Downloaded extensions</legend>'
	echo '            <table class="bggrey percent100">'
	#------------------------------------------------------------------------------------
	pcp_incr_id

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
	#------------------------------------------------------------------------------------
#	pcp_toggle_row_shade
#	echo '              <tr class="'$ROWSHADE'">'
#	echo '                <td colspan="3">'
#	echo '                  <input type="submit" name="SUBMIT" value="Info">'
#	echo '                  <input type="hidden" name="CALLED_BY" value="Downloaded">'
#	echo '                  <input type="hidden" name="DB" value="'$DB'">'
#	echo '                </td>'
#	echo '              </tr>'
	#------------------------------------------------------------------------------------
	echo '            </table>'
	echo '          </fieldset>'
	echo '        </div>'
	echo '      </form>'

}

#========================================================================================
# Show current onboot.lst - these are the extensions loaded during a boot.
#----------------------------------------------------------------------------------------
pcp_show_onboot_lst() {
	echo '<div>'
	pcp_textarea "Current $ONBOOTLST" "cat $ONBOOTLST" 50
	echo '</div>'
}

#========================================================================================
# Extension dependency tree
#----------------------------------------------------------------------------------------
pcp_dependency_tree() {
	if [ -n "$1" ]; then
		APP="${1%.tcz}.tcz"
		INDENT=""
		pcp_get_dependencies $APP
	fi
}

pcp_get_dependencies() {
	APP="${1//KERNEL/$KERNEL}"
	echo -n "$INDENT"
	echo -n "-----"
	echo "$APP"
	for DEPAPP in $(cat ${PACKAGEDIR}/${APP}.dep)
	do
		INDENT="${INDENT}     |"
		pcp_get_dependencies $DEPAPP
	done
	INDENT="${INDENT%     |}"
}

pcp_full_dependency_tree() {
#	[ "$1" != "text" ] && pcp_table_textarea_top "Extension dependency tree" "" "300"
	for E in $(cat $ONBOOTLST)
	do
		pcp_dependency_tree $E
		echo ""
	done >/var/log/pcp_dependency_tree.log
#	[ "$1" != "text" ] && pcp_table_textarea_end

	echo '<div>'
	pcp_textarea "Extension dependency tree" "cat /var/log/pcp_dependency_tree.log" 15
	echo '</div>'
}

#========================================================================================
# Main.
#----------------------------------------------------------------------------------------
pcp_debug_info

echo '<!-- Start of pcp_extension_tabs toolbar -->'
echo '  <div>'
echo '    <ul class="nav nav-tabs navbar-dark mt-1">'

[ x"" = x"$CALLED_BY" ] && CALLED_BY="Information"
for TAB in Information Available Installed Uninstalled onboot.lst
do
	[ "$TAB" = "$CALLED_BY" ] && TAB_ACTIVE="active" || TAB_ACTIVE=""
	echo '      <li class="nav-item">'
	echo '        <a class="nav-link '$TAB_ACTIVE'" href="'$0'?CALLED_BY='$TAB'" title="'$TAB'">'$TAB'</a>'
	echo '      </li>'
done

echo '    </ul>'
echo '  </div>'
echo '<!-- End of pcp_extension_tabs toolbar -->'

case "$CALLED_BY" in
	Information)
		pcp_information_message
		pcp_generate_report
		pcp_internet_check
		pcp_init_search
		[ $DEBUG -eq 1 ] && pcp_tce_mirror
	;;
	Available)
		case "$SUBMIT" in
			Set)   pcp_set_repository;   pcp_cleanup;;
			Reset) pcp_reset_repository; pcp_cleanup;;
		esac
		pcp_select_repository
		pcp_show_available_extns
		pcp_search_extn
		case "$SUBMIT" in
			Info) pcp_display_information;;
			Load) pcp_load_extn;;
		esac
		pcp_free_space_check
	;;
	Installed)
		pcp_show_installed_extns
		case "$SUBMIT" in
#			Info)   pcp_find_extn; pcp_display_information;;
			Update) pcp_update_extn;;
			Delete) pcp_delete_extn;;
		esac
	;;
	Uninstalled)
		pcp_show_uninstalled_extns
		case "$SUBMIT" in
#			Info)    pcp_find_extn; pcp_display_information;;
			Install) pcp_install_extn;;
			Update)  pcp_update_extn;;
			Delete)  pcp_delete_extn;;
		esac
	;;
	Downloaded)
		pcp_show_downloaded_extns
		case "$SUBMIT" in
#			Info)   pcp_find_extn; pcp_display_information;;
			Delete) pcp_delete_extn;;
		esac
	;;
	onboot.lst)
		pcp_show_onboot_lst
		pcp_full_dependency_tree html
	;;
esac
#----------------------------------------------------------------------------------------

pcp_html_end
exit