#!/bin/sh
. pcp-functions
pcp_variables

# Defined in pcp-functions
#UPD_PCP=/tmp/upd_picoreplayer

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <title>pCP - Update pCP</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Update pCP" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_script

echo '<h2>[ INFO ] You are currently using piCorePlayer version: '$(pcp_picoreplayer_version)'</h2>'

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Tidying up...</p>'
sudo rm -rf $UPD_PCP

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Creating temporary update directory...</p>'
sudo mkdir -m 777 $UPD_PCP

# Download a list of available versions on Sourceforge - coming from this file insitu.cfg
echo '<p class="info">[ INFO ] Downloading insitu.cfg...</p>'
wget -P $UPD_PCP http://sourceforge.net/projects/picoreplayer/files/insitu/insitu.cfg
result=$?
if [ $result -ne "0" ]; then
	echo '<p class="error">[ ERROR ] Error retrieving insitu.cfg</p>'
	exit 1
else
	echo '<p class="ok">[ OK ] Success downloading insitu.cfg</p>'
fi

echo '<h2>Choose from Drop-Down list which version of piCorePlayer you will update to ...... or downgrade to</h2>'

echo '<table border="0" width="960">'
echo '  <form name="insitu" action= "insitu.cgi" method="get">'
echo '    <tr class="odd">'
echo '      <td width="150">'
echo '        <select name="INSITU">'

awk '{ print "<option value=\""$1"\">" $1"</option>" }' $UPD_PCP/insitu.cfg

echo '      </td>'
echo '      <td width="800"><p>Please note that it takes a long time. Please be patient, when download is finished the new page will load.'
echo '    </tr>'
echo '    <tr class="even">'
echo '      <td colspan="2"><input type="submit" value="Update your piCorePlayer"></td>'
echo '    </tr>'
echo '  </form>'
echo '</table>'

echo '</body>'
echo '</html>'
