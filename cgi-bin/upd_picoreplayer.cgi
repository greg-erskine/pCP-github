#!/bin/sh

# Version: 0.05 2014-09-05 GE
#	Added INSITU_DOWNLOAD variable.

# version: 0.04 2014-08-12 GE
#	Added sudo to wget.

# version: 0.03 2014-07-19 GE
#	Fixed issue where downloading insitu.cfg always returned success message.
#	Improved error handling.
#	Added Main Page button so you can exit.
#	Modified a few comments.

# version: 0.02 2014-06-24 GE
#	Rewritten.

# version: 0.01 2014 SBP
#	Original.

# upd_picoreplayer.cgi -> insitu.cgi -> do_updatepicoreplayer.cgi

. pcp-functions
pcp_variables

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
pcp_navigation
pcp_running_script

echo '<h2>[ INFO ] You are currently using version: piCorePlayer'$(pcp_picoreplayer_version)'</h2>'

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Tidying up...</p>'
sudo rm -rf $UPD_PCP

[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Creating temporary update directory...</p>'
sudo mkdir -m 755 $UPD_PCP

# Download a list of available versions on Sourceforge
echo '<p class="info">[ INFO ] Downloading insitu.cfg...</p>'
[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Downloading '$INSITU_DOWNLOAD'/insitu.cfg...</p>'
sudo wget -P $UPD_PCP $INSITU_DOWNLOAD/insitu.cfg
result=$?
if [ $result = 0 ]; then
	echo '<p class="ok">[ OK ] Success downloading insitu.cfg</p>'
else
	echo '<p class="error">[ ERROR: '$result' ] Error downloading insitu.cfg</p>'
fi

if [ $result = 0 ]; then
	echo '<table border="0" width="960">'
	echo '  <form name="insitu" action= "insitu.cgi" method="get">'
	echo '    <tr class="odd">'
	echo '      <td width="150">'
	echo '        <select name="INSITU">'

	awk '{ print "<option value=\""$1"\">" $1"</option>" }' $UPD_PCP/insitu.cfg

	echo '      </td>'
	echo '      <td width="800"><p>Choose from Drop-Down list which version of piCorePlayer you would like to update/downgrade to.</p></td>'
	echo '    </tr>'
	echo '    <tr class="even">'
	echo '      <td width="150"><input type="submit" value="Update piCorePlayer"></td>'
	echo '      <td width="800"><p>Update may take a few minutes... please be patient. When the download has finished a new page will load.</p></td>'
	echo '    </tr>'
	echo '  </form>'
	echo '</table>'
fi

pcp_go_main_button

echo '</body>'
echo '</html>'
