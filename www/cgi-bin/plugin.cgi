#!/bin/sh


# Version: 0.01 SBP
#	Original.

. pcp-functions
. pcp-soundcard-functions
#. $CONFIGCFG


pcp_html_head "Plugin page" "SBP" 
 "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string
pcp_navigation

pcp_table_top "Third Party Plugins"

PLUGINDIR=/home/tc/www/cgi-bin/plugin
SCRIPTDIR=/cgi-bin

################################################
#Scan plugin directory and use each directory as a uniq name for each plugin button
################################################
I=1
PLUGINS=`ls "$PLUGINDIR"`
for DIR in $PLUGINS
do 
eval \ "PLUGIN${I}"="${DIR}"
I=$((I+1))
done

# check of result
#echo "plug1 er" $PLUGIN1
#echo "plug2 er" $PLUGIN2

################################################
#Next, read description for each pluin from the <PLUGIN>.conf file
################################################

		I=1
		while true; do
			eval PLUGIN="\${PLUGIN${I}}"
			if [ x"$PLUGIN" != x ]; then
		. "$PLUGINDIR"/"$PLUGIN"/"$PLUGIN".conf
		SHDESC=$(echo '$SHORT_DESCRIP')
		eval \ "SHDSCR${I}"="${SHDESC}"

		DESC=$(echo '$DESCRIPTION')
		eval \ "DSCR${I}"="${DESC}"

		PLNAME=$(echo '$PLUGIN_NAME')
		eval \ "PNAME${I}"="${PLNAME}"

		I=$((I+1))
			else
			break
		fi 
		done

# check of result
#echo "PLUGDSCR1 er" $DSCR1
#echo "PLUGDSCR2 er" $DSCR2

#---------------------------
# To make the initial plug tar and untar use:
#tar -cvf slimmer.tar  -C /home/tc/www/cgi-bin/plugin slimmer
#tar -xvf slimmer.tar -C /home/tc/www/cgi-bin/plugin 
#---------------------------



case "$ACTION" in
	Add)
		[ ! -d "$PLUGINDIR" ] && sudo mkdir "$PLUGINDIR"
		PL_REPO=$(echo "$PL_REPO_1" | rev | cut -d/ -f2- | rev)
		PLUG=$(basename "$PL_REPO")
		cd /tmp && wget "$PL_REPO" -O "$PLUG"
		echo "$PL_REPO"
		echo "$PLUG"
		tar -xvf "$PLUG" -C "$PLUGINDIR"

		# Now I would like to reset the variables and then refresh page - but the following does not work
		PL_REPO_1=""
		PLUG=""
		PL_REPO=""
		CMD=""

	;;
	Backup)
		pcp_backup
	;;
esac


#----------------------------------------------Third party plugins-----------------------------
		


# Now done in javascript below, 
# Quotes and & are not allowed, until writetoautostart.cgi is modified or we split out usercommands to only deal with encoded strings

# Decode variables using httpd, no quotes
#	USER_COMMAND_1=$(sudo $HTTPD -d $USER_COMMAND_1)
#	USER_COMMAND_1=$(echo $USER_COMMAND_1 | sed 's/"/\&quot;/g')

#	USER_COMMAND_2=$(sudo $HTTPD -d $USER_COMMAND_2)
#	USER_COMMAND_2=$(echo $USER_COMMAND_2 | sed 's/"/\&quot;/g')

#	USER_COMMAND_3=$(sudo $HTTPD -d $USER_COMMAND_3)
#	USER_COMMAND_3=$(echo $USER_COMMAND_3 | sed 's/"/\&quot;/g')

#	echo '<table class="bggrey">'
#	echo '  <tr>'
#	echo '    <td>'
#	echo '      <form name="setusercommands" action="writetoautostart.cgi" method="get">'
#	echo '        <div class="row">'
#	echo '          <fieldset>'
#	echo '            <legend>Third Party Add-on</legend>'
#	echo '            <table class="bggrey percent100">'
	pcp_incr_id
	pcp_start_row_shade

pcp_third_party_add_ons() {
	I=1
	while true; do
		eval PLUGIN="\${PLUGIN${I}}"
		if [ x"$PLUGIN" != x ]; then 

		eval DSCR="\${DSCR${I}}"


		eval SHDSCR="\${SHDSCR${I}}"



		eval PNAME="\${PNAME${I}}"

	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
 	echo '                   <input type="checkbox" name=mybox value="yes" checked>'
#	echo '                  <p>Shairport-sync</p>'
#	echo '                  <p>'"$PNAME"'</p>'
	echo '                </td>'
#	echo '                <td class="column210">'

#	echo '                  <p>'"$PNAME"'</p>'
# 	echo '                   <input type="checkbox" name=mybox value="1" checked>'
#	echo '                  <input class="small1" type="radio" name="SHAIRPORT" value="yes" '$SHAIRPORTyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
#	echo '                  <input class="small1" type="radio" name="SHAIRPORT" value="no" '$SHAIRPORTno'>No'
	echo '                </td>'
	echo '                <td>'

	echo '                <p>'"$SHDSCR"':&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                  ' $DSCR
#	echo '                    <p>Automatically start Shairport when pCP starts to stream audio from your iDevice.</p>'
	echo '                  </div>'
	echo '                </td>'

	echo '                <td>'
#	echo '                  <input type="submit" name="SUBMIT" value="Install">'
#	echo '                  <input type="submit" name="SUBMIT" value="Config">'
#	echo '                  <input class="small1" type="radio" name="RESTART" value="Enabled" '$RESTART_Y'>Enabled'
#	echo '                  <input class="small1" type="radio" name="RESTART" value="Disabled" '$RESTART_N'>Disabled'
	echo ' <FORM METHOD="LINK" ACTION='"$SCRIPTDIR"/plugin/"$PLUGIN"/"$PLUGIN"'.sh>'
#	echo ' <INPUT TYPE="submit" VALUE='"$PLUGIN"'>'
	echo ' <INPUT TYPE="submit" VALUE=Install>'
#	echo ' </FORM>'

	echo ' <FORM METHOD="LINK" ACTION='"$SCRIPTDIR"/plugin/"$PLUGIN"/"$PLUGIN"'.cgi>'
#	echo ' <INPUT TYPE="submit" VALUE='"$PLUGIN"'>'
	echo ' <INPUT TYPE="submit" VALUE=Configure>'

	echo ' <FORM METHOD="LINK" ACTION='"$SCRIPTDIR"/plugin/"$PLUGIN"/"$PLUGIN"'_remove.sh>'
#	echo ' <INPUT TYPE="submit" VALUE='"$PLUGIN"'>'
	echo ' <INPUT TYPE="submit" VALUE=Remove>'
	echo ' </FORM>'
	echo '                </td>'


	echo '              </tr>'
	pcp_incr_id
	pcp_toggle_row_shade


		else
			break
		fi
I=$((I+1))
done

#---------------------------
# End looping here
#----------------------------

#========================================
# Add repo section
#========================================
pcp_add_repo() {

#	echo '<table class="bggrey">'
#	echo '  <tr>'
#	echo '    <td>'
#	echo '      <form name="setusercommands" action="writetoautostart.cgi" method="get">'
#	echo '        <div class="row">'
#	echo '          <fieldset>'
#	echo '            <legend>Provide Repo</legend>'
#	echo '            <table class="bggrey percent100">'




pcp_incr_id


#	pcp_toggle_row_shade
#Start New functions
echo '            <form name="manual_adjust" action="'$0'" method="get">'

	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">Add Plugin repo:</td>'
	echo '                <td>'
	echo '                  <input class="large60"'
	echo '                         type="text"'
	echo '                         id="PL_REPO_1"'
	echo '                         name="PL_REPO_1"'
	echo '                         value="'$PL_REPO_1'"'
	echo '                         maxlength="254"'
	echo '                         title="Invalid characters: &amp &quot"'
	echo '                         pattern="[^\&\x22]+"'
	echo '                  >'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade

	echo '              <script type="text/javascript">'
	echo '                 var cmd1 = "'$PL_REPO_1'";'
	echo '                 document.getElementById("PL_REPO_1").value = decodeURIComponent(cmd1.replace(/\+/g, "%20"));'
	echo '              </script>'
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150"></td>'
	echo '                <td>'
	echo '                  <p>Adds Third Party Plugins to piCorePlayer&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This feature allows to add third part Plugins if the developer have made a package for piCorePlayer.'
	echo '                    <p><b>Warning:</b> As piCorePlayer automatically will download software from the repositories you define, please verify that you trust the owner of the repository.'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td colspan=2>'
	echo '                  <input type="hidden" name="AUTOSTART" value="CMD"/>'
	echo '                  <input type="submit" name="ACTION" value="'Add'">'
#	echo '                  <input type="submit" name="SUBMIT" value="Clear">'





	echo '                </td>'
	echo '              </tr>'
}

pcp_add_repo


#	echo '            </table>'
#	echo '          </fieldset>'
#	echo '        </div>'
#	echo '      </form>'
#	echo '    </td>'
#	echo '  </tr>'
#	echo '</table>'
}
[ $MODE -ge $MODE_NORMAL ] && pcp_third_party_add_ons





#pcp_table_middle
#pcp_go_back_button
pcp_table_end

pcp_footer
pcp_copyright

[ $CHANGED ] && pcp_reboot_required

echo '</body>'
echo '</html>'

echo '</html>'