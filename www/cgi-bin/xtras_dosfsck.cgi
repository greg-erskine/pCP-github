#!/bin/sh

# Version: 0.01 2014-12-27 GE
#   Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_dosfsck" "GE"

pcp_controls
pcp_banner
pcp_navigation
pcp_running_script
pcp_httpd_query_string

case "$SUBMIT" in
	fdis*)
		OPT=1
		;;
	resi*)
		OPT=2
		;;
esac

#========================================================================================
# Check for dosfstools.tcz and download and install
#========================================================================================


#cat /opt/.tce_dirIf you are running Core 4.2 or later, then you can find the tce directory by opening the terminal and typing 
#
#readlink /etc/sysconfig/tcedir


echo '<textarea class="inform">'

	if [ ! -f /mnt/mmcblk0p2/tce/optional/dosfstools.tcz ]; then
		tce-load -w dosfstools.tcz
		echo 'dosfstools.tcz not loaded'
	else
		echo 'dosfstools.tcz loaded'
	fi
	tce-load -i dosfstools.tcz

echo '</textarea>'

#========================================================================================
# fdisk routine
#----------------------------------------------------------------------------------------
pcp_fdisk() {
  echo '<textarea class="inform">'
  
  dosfsck -V /dev/mmcblk0p1
  
  echo '</textarea>'
}

#========================================================================================
# resize2fs routine
#----------------------------------------------------------------------------------------
pcp_resize2fs() {
  echo '<textarea class="inform" style="height:500px">'
  echo 'resize2fs can take a couple of minutes. Please wait...'
#  sudo resize2fs /dev/mmcblk0p2
  echo 'Finished. Please reboot now...'
  echo '</textarea>'
}

#========================================================================================
# fdisk and resize2fs buttons
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '        <legend>Resize partition</legend>'
echo '          <table class="bggrey percent100">'
echo '            <form name="increase" action="xtras_dosfsck.cgi" method="get" id="increase">'
echo '              <tr class="even">'
echo '                <td>'
echo '                  <p>Resizing the partition is a 2 step process</p>'
echo '                  <ol>'
echo '                    <li>Step 1 - fdisk, then reboot</li>'
echo '                    <li>Step 2 - resize2fs, then reboot</li>'
echo '                  </ol>'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="odd">'
echo '                <td>'
echo '                  <input type="submit" name="SUBMIT" value="fdisk" />&nbsp;&nbsp;fdisk to resize partition'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="even">'
echo '                <td>'

[ $OPT == 1 ] && pcp_fdisk

echo '                </td>'
echo '              </tr>'
echo '              <tr class="odd">'
echo '                <td>'
echo '                  <input type="submit" name="SUBMIT" value="resize2fs" />&nbsp;&nbsp;resize2fs to expand partition to fit file system'
echo '                </td>'
echo '              </tr>'
echo '              <tr class="even">'
echo '                <td>'

[ $OPT == 2 ] && pcp_resize2fs

echo '                </td>'
echo '              </tr>'
echo '            </form>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# Partition information
#----------------------------------------------------------------------------------------
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <form name="sd_information" method="get">'
echo '        <div class="row">'
echo '          <fieldset>'
echo '            <legend>Partition Information</legend>'
echo '            <table class="bggrey percent100">'
echo '              <tr class="odd">'
echo '                <td>'

pcp_textarea_inform "none" "fsck -h" 50

echo '                </td>'
echo '              </tr>'
echo '              <tr class="odd">'
echo '                <td>'

pcp_textarea_inform "none" "dosfsck -V /dev/mmcblk0p1" 120

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

pcp_footer

echo '</body>'
echo '</html>'