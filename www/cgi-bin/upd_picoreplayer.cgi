#!/bin/sh

# Version: 0.06 2015-01-23 GE
#	HTML5 formatted.
#	Increased width of update piCorePlayer button.
#	Minor html updates.

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

pcp_html_head "Update pCP" "SBP"

pcp_banner
pcp_navigation
pcp_running_script

echo '<p>[ INFO ] You are currently using piCorePlayer'$(pcp_picoreplayer_version)'</p>'

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
	echo '<table class="gbgrey">'
	echo '  <form name="insitu" action= "insitu.cgi" method="get">'
	echo '    <tr class="odd">'
	echo '      <td class="column150">'
	echo '        <select name="INSITU">'

	awk '{ print "<option value=\""$1"\">" $1"</option>" }' $UPD_PCP/insitu.cfg

	echo '        </select>'
	echo '      </td>'
	echo '      <td>'
	echo '        <p>Choose from Drop-Down list which version of piCorePlayer you would like to update/downgrade to.</p>'
	echo '      </td>'
	echo '    </tr>'
	echo '    <tr class="even">'
	echo '      <td class="column150">'
	echo '        <input class="large12" type="submit" value="Update piCorePlayer">'
	echo '      </td>'
	echo '      <td>'
	echo '        <p>Update may take a few minutes... please be patient. When the download has finished a new page will load.</p>'
	echo '      </td>'
	echo '    </tr>'
	echo '  </form>'
	echo '</table>'
fi

pcp_go_main_button

echo '</body>'
echo '</html>'