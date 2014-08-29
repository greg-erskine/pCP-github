#!/bin/sh
. pcp-functions
pcp_variables

# $UPD_PSP is defined in pcp-functions
# i.e. UPD_PCP=/tmp/upd_picoreplayer

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <title>pCP - InSitu upgrade</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="InSitu upgrade" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_script
pcp_httpd_query_string

# Decode variables using httpd
INSITU=`sudo /usr/local/sbin/httpd -d $INSITU`

if [ $DEBUG = 1 ]; then
	echo '<p class="debug">[ DEBUG ] QUERY_STRING: '$QUERY_STRING'<br />'
	echo '                 [ DEBUG ] INSITU: '$INSITU'<br />'
	echo '                 [ DEBUG ] UPD_PCP: '$UPD_PCP'</p>'
fi

#### This should be passed to do_updatepicoreplayer.cgi via hidden input field.
echo "INSITU="$INSITU > $UPD_PCP/version.cfg
#############################

echo '<h2>[ INFO ] You are currently using piCorePlayer version: '$(pcp_picoreplayer_version)'</h2>'
echo '<h2>[ INFO ] You have choosen to upgrade to: '$INSITU'</h2>'

# Make directories
sudo mkdir $UPD_PCP/boot
sudo mkdir $UPD_PCP/tce

# Download the boot files and the tce files and Break if errors in downloading boot files
echo '<p class="info">[ INFO ] Downloading '$INSITU'_boot.tar.gz...</p>'
wget -P "$UPD_PCP"/boot http://sourceforge.net/projects/picoreplayer/files/insitu/"$INSITU"/"$INSITU"_boot.tar.gz
result=$?
if [ $result -ne "0" ]; then
	echo '<p class="error">[ ERROR ] Error retrieving your boot files</p>'
	exit 1
else
	echo '<p class="ok">[ OK ] Success downloading boot files</p>'
fi

# Break if error in downloading tce files
echo '<p class="info">[ INFO ] Downloading '$INSITU'_tce.tar.gz...</p>'
wget -P "$UPD_PCP"/tce http://sourceforge.net/projects/picoreplayer/files/insitu/"$INSITU"/"$INSITU"_tce.tar.gz
if [ $result -ne "0" ]; then
	echo '<p class="error">[ ERROR ] Error retrieving your tce files</p>'
	exit 1
else
	echo '<p class="ok">[ OK ] Success downloading tce files</p>'
fi

echo '<h2>Please, do NOT TRY to update if you see any erors in the download. [The two lines above].</h2>'

echo '<table border="1" width="960">'
echo '  <form name="do_update" action= "do_updatepicoreplayer.cgi" method="get">'
echo '    <tr class="odd">'
echo '      <td width="150">'
echo '        <input type="submit" value='Update your piCorePlayer' />'
echo '      </td>'
echo '      <td width="800">'
echo '        <p>When you press the button, you will make the actual update with the downloaded files.'
echo '      </td>'  
echo '    </tr>'
echo '  </form>'
echo '</table>'

pcp_go_back_button

echo '</body>'
echo '</html>'