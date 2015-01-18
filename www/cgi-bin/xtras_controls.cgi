#!/bin/sh

# Version: 0.01 2014-10-22 GE
#	Original.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "Controls Adv" "GE"

pcp_favorites

pcp_banner
pcp_navigation
pcp_running_script
pcp_refresh_button

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] LMS IP: '$(pcp_lmsip)'<br />'
	echo '                 [ DEBUG ] MAC: '$(pcp_controls_mac_address)'</p>'
fi

echo '<h1>User Commands experiment</h1>' 

echo 	'<textarea>'
echo $COMMAND_1
pcp_user_commands
echo 	'</textarea>'


#========================================================================================
echo '<h1>Favorite toolbar experiment #0</h1>'

FAVLIST=`( echo "$(pcp_controls_mac_address) favorites items 0 100"; echo "exit" ) | nc $(pcp_lmsip) 9090 | sed 's/ /\+/g'`
FAVLIST=`sudo /usr/local/sbin/httpd -d $FAVLIST`

		echo '<!-- Start of pcp_favorites -->'
		echo '<table class="bgblack">'
		echo '  <tr>'
		echo '    <td>'
		echo '      <p>'

echo $FAVLIST | awk '
BEGIN {
	RS="id:"
	FS=":"
	i = 0
}
#main
{
	i++
	split($1,a," ")
	id[i]=a[1]
	split(id[i],b,".")
	num[i]=b[2]
	name[i]=$2
	gsub(" type","",name[i])
	hasitems[i]=$5
	gsub("count","",hasitems[i])
	if ( hasitems[i] != "0 " ) {
		i--
	}
}
END {
	for (j=1; j<=7; j++) {
#		printf "<option value=\"%s\" id=\"%10s\">%s - %s - :%s:</option>",id[j],id[j],num[j],name[j],hasitems[j]
		printf "        <a class=\"nav2\" href=\"favorites.cgi?STARTFAV=%s\" title=\"%s\">%s</a>",id[j],id[j],name[j]
	}
} '

		echo '      </p>'
		echo '    </td>'
		echo '  </tr>'
		echo '</table>'
		echo '<!-- End of pcp_favorites -->'
echo '<br /><br />'

#------------------------------------------------------------------------------

#========================================================================================
echo '<h1>Favorite experiment #1</h1>'

FAVLIST=`( echo "$(pcp_controls_mac_address) favorites items 0 100"; echo "exit" ) | nc $(pcp_lmsip) 9090 | sed 's/ /\+/g'`

echo '#1<br />'
echo $FAVLIST
echo '<br /><br />'

FAVLIST=`sudo /usr/local/sbin/httpd -d $FAVLIST`

echo '#2<br />'
echo $FAVLIST
echo '<br /><br />'

echo '#3<br />'
echo '<br />'
echo '<select name="FAVORITES">'

#b8:27:eb:c7:e0:61 favorites items 0 100 title:Favorites id:
#00517dec.0 name:On mysqueezebox.com isaudio:0 hasitems:1 id:
#00517dec.1 name:A Hundred Million Suns type:audio isaudio:1 hasitems:0 id:
#00517dec.2 name:Affirmation type:audio isaudio:1 hasitems:0

FAVLIST=`echo $FAVLIST | awk '
BEGIN {
	RS="id:"
	FS=":"
	i = 0
}
#main
{
	i++
	split($1,a," ")
	id[i]=a[1]
	split(id[i],b,".")
	num[i]=b[2]
	name[i]=$2
	gsub(" type","",name[i])
	hasitems[i]=$5
	gsub("count","",hasitems[i])
	if ( hasitems[i] != "0 " ) {
		i--
	}
}
END {
	for (j=1; j<=i; j++) {
		printf "<option value=\"%s\" id=\"%10s\">%s - %s - :%s:</option>",id[j],id[j],num[j],name[j],hasitems[j]
	}
} ' `

echo $FAVLIST
echo '</select>'

echo '<br /><br />'

#------------------------------------------------------------------------------
echo '<h1>Favorite experiment #2</h1>'


pcp_autofav_id() {

AUTOSTARTFAV=`sudo /usr/local/sbin/httpd -d $AUTOSTARTFAV`

FAVLIST=`( echo "$(pcp_controls_mac_address) favorites items 0 100"; echo "exit" ) | nc $(pcp_lmsip) 9090 | sed 's/ /\+/g'`
FAVLIST=`sudo /usr/local/sbin/httpd -d $FAVLIST`

echo $FAVLIST | awk -v autostartfav="$AUTOSTARTFAV" '
BEGIN {
	RS="id:"
	FS=":"
	i = 0
}
# main
{
	i++
	split($1,a," ")
	id[i]=a[1]
	name[i]=$2
	gsub(" type","",name[i])
	if ( name[i] == autostartfav ) {
		result=id[i]
	}
	hasitems[i]=$5
	gsub("count","",hasitems[i])
	if ( hasitems[i] != "0 " ) {
		i--
	}
}
END {
	printf "%s",result
} '

}

echo '<p>'$(pcp_autofav_id)'</p>'

#========================================================================================
echo '<h1>Playlist experiment</h1>'

PLAYLISTS=`( echo "$(pcp_controls_mac_address) playlists 0 5"; echo "exit" ) | nc $(pcp_lmsip) 9090 | sed 's/ /\+/g'`

echo '#1<br />'
echo $PLAYLISTS
echo '<br /><br />'

PLAYLISTS=`sudo /usr/local/sbin/httpd -d $PLAYLISTS`

echo '#2<br />'
echo $PLAYLISTS
echo '<br /><br />'

echo '#3<br />'
echo '<br />'
echo '<select name="PLAYLISTS">'


SEARCH="Affirmation"

PLAYLISTS=`echo $PLAYLISTS | awk -v search=$SEARCH '
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
	printf "</select><p>Search: %s</p>", search
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