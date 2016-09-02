#!/bin/sh

# Version: 3.02 2016-09-02
#	Added default button. SBP.
#	Added more help txt
#	Added repo indicator

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
getMirror
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

pcp_set_mirror() {
	echo $MYMIRROR > /opt/tcemirror
}

pcp_cleanup() {
	rm -f /tmp/tags.db
	rm -f /tmp/*.tree
	rm -f /tmp/sizelist
}

pcp_create_localmirrors() {
	echo https://sourceforge.net/projects/picoreplayer/files/repo/ > /opt/localmirrors
	echo https://sourceforge.net/projects/picoreplayer/files/tce/ >> /opt/localmirrors	# FIX
}

#========================================================================================
# Display debug information
#----------------------------------------------------------------------------------------
pcp_debug_info() {
	if [ $DEBUG -eq 1 ]; then
		echo '<p class="debug">[ DEBUG ] $EXTN: '$EXTN'<br />'
		echo '                 [ DEBUG ] $SUBMIT: '$SUBMIT'<br />'
		echo '                 [ DEBUG ] $MIRROR: '$MIRROR'</p>'
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
# Main
#----------------------------------------------------------------------------------------
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
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Setting mirror repository...</p>'
		pcp_set_mirror
		pcp_cleanup
	;;
	Default)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Setting repository to Default piCore repo...</p>'
		MYMIRROR='http://repo.tinycorelinux.net/'
		pcp_set_mirror
		pcp_cleanup
	;;

	*)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Invalid option '$SUBMIT'...</p>'
	;;
esac

echo '    </td>'
echo '  </tr>'
echo '</table>'

if [ $DEBUG -eq 1 ]; then
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

if [ $MODE -ge $MODE_BETA ]; then
#========================================================================================
# Show available piCore remote mirrors
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
                          echo '                  <input type="submit" name="SUBMIT" value="Default">'
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
# Show piCore local mirrors
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="local_mirrors" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>piCorePlayer Sourceforge repository</legend>'
echo '            <table class="bggrey percent100">'
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Local mirror</p>'
echo '                </td>'
echo '                <td class="column300">'
echo '                  <select class="large22" name="MYMIRROR">'

                          if [ -f /opt/localmirrors ]; then
                            for LM in $(cat "/opt/localmirrors")
                            do
                              echo '                    <option value="'$LM'">'$LM'</option>'
                            done
                          else
                            echo '                    <option value="none">'/opt/localmirrors not found!'</option>'
                          fi

echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>Select local mirror repository&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Local mirrors are only available if /opt/localmirrors is found.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'

                        if [ -f /opt/localmirrors ]; then
                          echo '                  <input type="submit" name="SUBMIT" value="Set">'
                        else
                          echo '                  <input type="submit" name="SUBMIT" value="Create">'
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

#========================================================================================
# Installed extensions - tce-status -i
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="installed" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Locally installed extensions</legend>'
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
	                        echo '<option value="'$i'.tcz">'$i'.tcz</option>'
	                      done
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>List of installed extensions&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Lists all piCore extensions that are currently installed.</li>'
echo '                      <li>These extensions are loaded at boot via /mnt/mmcblk0p2/tce/onboot.lst.</li>'
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
echo '            <legend>Locally downloaded extensions</legend>'
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
                            echo '<option value="'$i'">'$i'</option>'
                          done
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>List of uninstalled extensions&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Lists all piCore extensions that are currently downloaded but not (yet) installed.</li>'
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
	echo '            <legend>Locally orphaned extensions</legend>'
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
	                            echo '<option value="'$i'">'$i'</option>'
	                          done
	echo '                  </select>'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>List of Orphaned extensions&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <ul>'
	echo '                      <li>Lists all orphaned extensions installed.</li>'
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
# Loaded extensions in /mnt/mmcblk0p2/tce/optional/ on SD card
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="loaded" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Locally loaded extensions</legend>'
echo '            <table class="bggrey percent100">'
pcp_incr_id
pcp_start_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td class="column150">'
echo '                  <p>Loaded extensions</p>'
echo '                </td>'
echo '                <td class="column300">'
echo '                  <select class="large22" name="EXTN">'
                          for E in $(ls /mnt/mmcblk0p2/tce/optional/*.tcz | sed 's/\/mnt\/mmcblk0p2\/tce\/optional\///g')
                          do
                            [ "$E" = "$EXTN" ] && SELECTED="selected" || SELECTED=""
                            echo '<option value="'$E'" '$SELECTED'>'$E'</option>'
                          done
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>List of loaded extensions&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Lists all piCore extensions that are currently loaded.</li>'
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
# Available extensions from tags.db
#----------------------------------------------------------------------------------------
INDICATOR=$HEAVY_CHECK_MARK
CLASS="indicator_green"
echo "mymirror" "$MYMIRROR"

#This will find the correct value of MYMIRROR if not set by this page
if [ x"$MYMIRROR" = x"" ]; then
MYMIRROR=$(cat /opt/tcemirror)
fi

echo "mymirror" "$MYMIRROR"
case "$MYMIRROR" in
	https://sourceforge.net/projects/picoreplayer/files/repo/*)
		STATUS="<b>piCorePlayer Sourceforge repository is selected</b>"
		;;
	http://repo.tinycorelinux.net/*)
		STATUS="<b>Officiel piCore repository is selected</b>"
		;;
#	http://repo.xxxx.xx/*)                                                   #<--- I don't know if it is possible to parse all official mirrors from the mirror.tcz and use them here?
#		STATUS="<b>Officiel piCore mirror is selected</b>"
#		;;	
	none*)
		STATUS="<b>No repository is selected</b>"             
		;;
		*)
		STATUS="<b>Possibly you are using a mirrored repo</b>"           #<----For now used as a proxi for the use of mirrors. It is clearly not the correct way
	;;
esac	


echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="available" action="'$0'" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Available extensions</legend>'
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
                            echo '<option value="'$E'" '$SELECTED'>'$E'</option>'
                          done
echo '                  </select>'
echo '                </td>'
echo '                <td>'
echo '                  <p>List of extensions available from the selected piCore repository&nbsp;&nbsp;'
echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
echo '                  </p>'
echo '                  <div id="'$ID'" class="less">'
echo '                    <ul>'
echo '                      <li>Lists all piCore extensions that are currently available for download from the selected piCore repository.</li>'
echo '                      <li>If the <b>Remote official piCore repository</b> is selected official piCore packages are listed here.</li>'
echo '                      <li>If the <b>piCorePlayer Sourceforge respository</b> is selected special piCorePlayer packages are listed here.</li>'
echo '                      <li>Both sort of packages are fine, but sometime piCorePlayer needs a package not available at the official repo.</li>'
echo '                    </ul>'
echo '                  </div>'
echo '                </td>'
echo '              </tr>'
pcp_toggle_row_shade
echo '              <tr class="'$ROWSHADE'">'
echo '                <td>'
echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
echo '              </td>'
echo '              <td>'
echo '                <p>&nbsp;&nbsp;'$STATUS'</p>'
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
	echo '                    <p>This option will load or delete a piCore extension and dependencies.</p>'
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

#========================================================================================
# Check for internet and piCore repository access
#----------------------------------------------------------------------------------------
if [ "$SUBMIT" = "Initial" ]; then
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Internet</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="'$ROWSHADE'">'

	                  if [ $(pcp_internet_accessible) -eq 0 ]; then
	                      INDICATOR=$HEAVY_CHECK_MARK
	                      CLASS="indicator_green"
	                      STATUS="Internet accessible..."
	                  else
	                      INDICATOR=$HEAVY_BALLOT_X
	                      CLASS="indicator_red"
	                      STATUS="Internet not accessible!!"
	                  fi

	echo '              <td class="column150 center">'
	echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
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

	                    if [ $(pcp_picore_accessible) -eq 0 ]; then
	                        INDICATOR=$HEAVY_CHECK_MARK
	                        CLASS="indicator_green"
	                        STATUS="piCore repository accessible..."
	                    else
	                        INDICATOR=$HEAVY_BALLOT_X
	                        CLASS="indicator_red"
	                        STATUS="piCore repository not accessible!!"
	                    fi

	echo '              <td class="column150 center">'
	echo '                <p class="'$CLASS'">'$INDICATOR'</p>'
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

if [ $MODE -ge $MODE_BETA ] && [ $EXTNFOUND -eq 1 ] && [ "$SUBMIT" != "Initial" ]; then
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

echo '</body>'
echo '</html>'