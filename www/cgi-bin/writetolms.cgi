#!/bin/sh

# Version: 0.01 2016-01-30 SBP
#	Original version.

. pcp-functions
pcp_variables

# Store the original values so we can see if they are changed
ORIG_LMS="$LMS"
ORIG_SAMBA="$SAMBA"

pcp_html_head "Write to Audio Tweak" "SBP" "15" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

#LMS="slimserver*"
SAMBA="samba.tcz"
WGET="/bin/busybox wget"
LMSREPOSITORY="http://sourceforge.net/projects/picoreplayer/files/tce/7.x/LMS/"

# Only offer reboot option if needed
REBOOT_REQUIRED=0



#========================================================================================================
# Routines
#--------------------------------------------------------------------------------------------------------
pcp_download_lms() {
#	pcp_sufficient_free_space 2000
	cd /tmp
	sudo rm -f /tmp/LMS
	sudo mkdir /tmp/LMS
	echo '<p class="info">[ INFO ] Downloading LMS from repository...</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Repo: '${LMSREPOSITORY}'</p>'
	echo '<p class="info">[ INFO ] Download will take a few minutes. Please wait...</p>'

	$WGET -s ${LMSREPOSITORY}slimserver-CPAN-armv6.tcz
	if [ $? = 0 ]; then
		RESULT=0
		echo '<p class="info">[ INFO ] Downloading Logitech Media Server LMS...'
		$WGET -P /tmp/LMS ${LMSREPOSITORY}slimserver-CPAN-armv6.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/LMS ${LMSREPOSITORY}slimserver-CPAN-armv6.tcz.dep
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/LMS ${LMSREPOSITORY}slimserver-CPAN-armv6.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/LMS ${LMSREPOSITORY}slimserver.tcz.md5.txt
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/LMS ${LMSREPOSITORY}slimserver.tcz.dep
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)
		$WGET -P /tmp/LMS ${LMSREPOSITORY}slimserver.tcz
		[ $? = 0 ] && echo -n . || (echo $?; RESULT=1)

		sudo -u tc tce-load -w gcc_libs.tcz
		sudo -u tc tce-load -w perl5.tcz
		
		if [ $RESULT = 0 ]; then
			echo '<p class="ok">[ OK ] Download successful.</p>'
			sudo /usr/local/etc/init.d/slimserver stop >/dev/null 2>&1
			sudo chown -R tc:staff /tmp/LMS
			sudo chmod -R 755 /tmp/LMS
			sudo cp -a /tmp/LMS/. /mnt/mmcblk0p2/tce/optional/
			sudo rm -f /tmp/LMS
		else
			echo '<p class="error">[ ERROR ] LMS download unsuccessful, try again!</p>'
		fi

	else
		echo '<p class="error">[ ERROR ] LMS not available in repository, try again later!</p>'
	fi

#	SPACE=$(pcp_free_space k)
#	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] Free space: '$SPACE'k</p>'
}

pcp_install_lms() {
	echo '<p class="info">[ INFO ] Installation of LMS.</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] LMS is added to onboot.lst</p>'
	sudo sed -i '/slimserver.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
	sudo echo 'slimserver.tcz' >> /mnt/mmcblk0p2/tce/onboot.lst
}

pcp_remove_lms() {
	sudo /usr/local/etc/init.d/slimserver stop >/dev/null 2>&1
	sudo rm -f /mnt/mmcblk0p2/tce/optional/slimserver-CPAN-armv6*
	sudo rm -f /mnt/mmcblk0p2/tce/optional/slimserver.tcz*
	sudo rm -f /mnt/mmcblk0p2/tce/optional/gcc_libs.tcz
	sudo rm -f /mnt/mmcblk0p2/tce/optional/perl5.tcz
	sudo sed -i '/slimserver.tcz/d' /mnt/mmcblk0p2/tce/onboot.lst
}

#========================================================================================
# LMS section
#----------------------------------------------------------------------------------------
# Only do something if variable is changed
#if [ $ORIG_LMS != $LMS ]; then
	REBOOT_REQUIRED=1
	echo '<hr>'
	echo '<p class="info">[ INFO ] LMS is set to: '$LMS'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] ORIG_LMS is: '$ORIG_LMS'</p>'
	[ $DEBUG = 1 ] && echo '<p class="debug">[ DEBUG ] LMS is: '$LMS'</p>'

	case "$LMS" in
		yes)
			echo '<p class="info">[ INFO ] LMS will be downloaded and enabled.</p>'
			pcp_download_lms
			pcp_install_lms
			;;
		no)
			echo '<p class="info">[ INFO ] LMS will be disabled and removed.</p>'
			pcp_remove_lms
			;;
		*)
			echo '<p class="error">[ ERROR ] LMS selection invalid: '$LMS'</p>'
			;;
	esac
	echo '<hr>'
#else
#	echo '<p class="info">[ INFO ] LMS variable unchanged.</p>'
#fi




echo '<hr>'
pcp_save_to_config
pcp_backup

[ $DEBUG = 1 ] && pcp_textarea "Current $ONBOOTLST" "cat $ONBOOTLST" 150
[ $DEBUG = 1 ] && pcp_textarea "Current $CONFIGCFG" "cat $CONFIGCFG" 150

[ $REBOOT_REQUIRED = 1 ] && pcp_reboot_required



pcp_go_back_button

echo '</body>'
echo '</html>'