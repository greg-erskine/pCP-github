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

pcp_table_top "Available plugins"

PLUGINDIR=/home/tc/www/cgi-bin/plugin

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
		DESC=$(echo '$DESCRIPTION')
		eval \ "DSCR${I}"="${DESC}"
		I=$((I+1))
			else
			break
		fi 
		done

# check of result
#echo "PLUGDSCR1 er" $DSCR1
#echo "PLUGDSCR2 er" $DSCR2



################################################
# Make a button for each plugin that will load the <PLUGIN>.cgi file 
# that can be used for setup of the plugin 
################################################


	I=1
	while true; do
		eval PLUGIN="\${PLUGIN${I}}"
		if [ x"$PLUGIN" != x ]; then 

		eval DSCR="\${DSCR${I}}"

	pcp_toggle_row_shade
	pcp_incr_id
	echo '            <tr class="'$ROWSHADE'">'
	echo ' <FORM METHOD="LINK" ACTION='"$PLUGINDIR"/"$PLUGIN"/"$PLUGIN"'.cgi>'
	echo ' <INPUT TYPE="submit" VALUE='"$PLUGIN"'>'
	echo ' </FORM>'
	echo '                <p>Info about the Plug-in:&nbsp;&nbsp;'
	echo '                  <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                </p>'
	echo '                <div id="'$ID'" class="less">'
	echo '                  ' $DSCR
	echo '                  <ul>'

		else
			break
		fi
I=$((I+1))
done



pcp_table_middle
pcp_go_back_button
pcp_table_end

pcp_footer
pcp_copyright

[ $CHANGED ] && pcp_reboot_required

echo '</body>'
echo '</html>'

echo '</html>'