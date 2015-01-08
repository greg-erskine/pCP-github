#!/bin/sh

# Version: 0.01 2014-10-22 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Controls Adv" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_refresh_button

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] LMS IP: '$(pcp_lmsip)'<br />'
	echo '                 [ DEBUG ] MAC: '$(pcp_controls_mac_address)'</p>'
fi


#========================================================================================

FAVS=`( echo "$(pcp_controls_mac_address) favorites items 0 100"; echo "exit" ) | nc $(pcp_lmsip) 9090 | sed 's/ /\+/g'`

echo '#1'
echo $FAVS
echo '<br /><br />'

FAVS=`sudo /usr/local/sbin/httpd -d $FAVS`

echo '#2'
echo $FAVS
echo '<br /><br />'

echo '#3'
echo '<br />'
echo '<select name="FAVORITES">'

FAVS=`echo $FAVS | awk '
BEGIN {
	RS="id:"
	FS=":"
	i = 0
}
#main
{
	split($1,c," ")
	id[i]=c[1]
	name[i]=$2
	gsub(" type","",name[i])
	i++
}
END {
	for (j=2; j<NR; j++) {
		printf "<option value=\"%s\" id=\"%10s\">%s - %s</option>",id[j],id[j],id[j],name[j]
	}
} ' `

echo $FAVS
echo '</select>'

echo '<br /><br />'

#------------------------------------------------------------------------------


#========================================================================================

PLAYLISTS=`( echo "$(pcp_controls_mac_address) playlists 0 5"; echo "exit" ) | nc $(pcp_lmsip) 9090 | sed 's/ /\+/g'`

echo '#1'
echo $PLAYLISTS
echo '<br /><br />'

PLAYLISTS=`sudo /usr/local/sbin/httpd -d $PLAYLISTS`

echo '#2'
echo $PLAYLISTS
echo '<br /><br />'

echo '#3'
echo '<br />'
echo '<select name="PLAYLISTS">'

PLAYLISTS=`echo $PLAYLISTS | awk '
BEGIN {
	RS="id:"
	FS=":"
	i = 0
}
#main
{
	split($1,c," ")
	id[i]=c[1]
	playlist[i]=$2
	i++
}
END {
	for (j=1; j<NR; j++) {
		printf "<option value=\"%s\" id=\"%10s\">%s - %s</option>",id[j],id[j],id[j],playlist[j]
	}
} ' `

echo $PLAYLISTS
echo '</select>'


echo '<br /><br />'

#------------------------------------------------------------------------------


echo '<br />'
echo '<br />'

exit

CONNECTED=$(pcp_lms_get "connected")
echo '<div>'
echo '<p>Connected: '$CONNECTED'</p>'
echo '</div>'

ARTIST=$(pcp_lms_get "artist")
echo '<div>'
echo '<p>Artist: '$ARTIST'</p>'
echo '</div>'

TITLE=$(pcp_lms_get "title")
echo '<div>'
echo '<p>Song: '$TITLE'</p>'
echo '</div>'

ALBUM=$(pcp_lms_get "album")
echo '<div>'
echo '<p>Album: '$ALBUM'</p>'
echo '</div>'

INFORMATION="$ARTIST - $TITLE - $ALBUM"
echo '<br />'
echo '<div style="width: 400px; border:1px solid black; ">'
echo '<marquee behavior="scroll" direction="left">'$INFORMATION'</marquee>'
echo '</div>'
echo '<br />'

echo '<div>'
echo '<img src="http://'$(pcp_lmsip)':9000/music/current/cover.jpg" alt="Currently playing" style="height: 250px; width: 250px; border:1px solid black;"/>'
echo '</div>'

echo '<br />'

pcp_footer

echo '</body>'
echo '</html>'