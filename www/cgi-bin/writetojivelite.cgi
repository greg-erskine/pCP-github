#!/bin/sh

# Version: 3.20 2017-03-08
#	Fixed pcp-xxx-functions issues. GE.

# Version: 3.10 2017-01-06
#	Enhanced formatting. GE.
#	Write jivelite.tcz.dep, instead of relying on it to be in base image. PH.
#	TODO: Move jivelite to repo with pcp-load.

# Version: 0.07 2016-05-09 GE
#	Fixed JIVELITE variable (YES/NO).

# Version: 0.06 2016-02-20 GE
#	Fixed sourceforge redirection issue.

# Version: 0.05 2015-12-19 GE
#	Added /bin/busybox to wget -s
#	Minor changes.

# Version: 0.04 2015-11-22 GE
#	Added code for VU Meters.
#	Revised jivelite download code.

# Version: 0.03 2015-08-29 SBP
#	Changed to touch-screen version.

# Version: 0.02 2015-05-08 GE
#	Revised.

# Version: 0.01 2015-03-15 SBP
#	Original version.

. pcp-functions
#. $CONFIGCFG

pcp_html_head "Write to Jivelite Tweak" "SBP" "150000" "tweaks.cgi"

pcp_banner
pcp_running_script
pcp_httpd_query_string

[ "$JIVELITE" = "yes" ] && VISUALISER="yes"
pcp_save_to_config

WGET="/bin/busybox wget"
JIVELITE_TCZ="jivelite_touch.tcz"
JIVELITE_MD5="jivelite_touch.tcz.md5.txt"
DEFAULT_VUMETER="VU_Meter_Kolossos_Oval.tcz"
AVAILABLE_VUMETERS=$($WGET $REPOSITORY -q -O - | grep -ow 'VU_Meter_\w*.tcz' | sort | uniq)

if [ $DEBUG -eq 1 ]; then
	echo '<p class="debug">[ DEBUG ] SUBMIT: '$SUBMIT'<br />'
	echo '                 [ DEBUG ] OPTION: '$OPTION'<br />'
	echo '                 [ DEBUG ] JIVELITE: '$JIVELITE'<br />'
	echo '                 [ DEBUG ] VISUALISER: '$VISUALISER'<br />'
	echo '                 [ DEBUG ] VUMETER: '$VUMETER'</p>'
	echo '<p class="debug">[ DEBUG ] REPOSITORY: '$REPOSITORY'<br />'
	echo '                 [ DEBUG ] JIVELITE_TCZ: '$JIVELITE_TCZ'<br />'
	echo '                 [ DEBUG ] JIVELITE_MD5: '$JIVELITE_MD5'<br />'
	echo '                 [ DEBUG ] DEFAULT_VUMETER: '$DEFAULT_VUMETER'<br />'
	echo '                 [ DEBUG ] AVAILABLE_VUMETERS: '$AVAILABLE_VUMETERS'</p>'
fi

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_download_jivelite() {
	cd /tmp
	sudo rm -f /tmp/${JIVELITE_TCZ}
	sudo rm -f /tmp/${JIVELITE_MD5}
	echo '<p class="info">[ INFO ] Downloading Jivelite from Ralphy'\''s repository...</p>'
	echo '<p class="info">[ INFO ] Downloading will take a few minutes. Please wait...</p>'

	$WGET -s ${REPOSITORY}/${JIVELITE_TCZ}
	if [ $? -eq 0 ]; then
		echo '<p class="info">[ INFO ] Downloading '$JIVELITE_TCZ'...'
		$WGET ${REPOSITORY}/${JIVELITE_TCZ} -O /tmp/${JIVELITE_TCZ}
		$WGET ${REPOSITORY}/${JIVELITE_MD5} -O /tmp/${JIVELITE_MD5}
		md5sum -c ${JIVELITE_MD5}
		if [ $? -eq 0 ]; then
			echo '<p class="ok">[ OK ] '$JIVELITE_TCZ' download successful.</p>'
			sudo cp /tmp/$JIVELITE_TCZ /mnt/mmcblk0p2/tce/optional/jivelite.tcz             #<-------------why do we rename jivelite extension????
			sudo chown tc:staff /mnt/mmcblk0p2/tce/optional/jivelite.tcz
			sudo cp /tmp/$JIVELITE_MD5 /mnt/mmcblk0p2/tce/optional/jivelite.tcz.md5.txt     #<-------------why do we rename jivelite extension????
			sudo chown tc:staff /mnt/mmcblk0p2/tce/optional/jivelite.tcz.md5.txt
			cat << EOF > /mnt/mmcblk0p2/tce/optional/jivelite.tcz.dep
touchscreen-KERNEL.tcz
libts.tcz
EOF
		else
			echo '<p class="error">[ ERROR ] Download unsuccessful, MD5 mismatch, try again later!</p>'
		fi
	else
		echo '<p class="error">[ ERROR ] '$TCZ' not available in repository, try again later!</p>'
	fi
}

pcp_install_jivelite() {
	echo '<p class="info">[ INFO ] Jivelite is installed.</p>'
	sudo -u tc tce-load -i jivelite.tcz                                            #<--------------if doing a reboot is this necessary???
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is added to onboot.lst</p>'
	sudo sed -i '/jivelite.tcz/d' $ONBOOTLST
	sudo echo 'jivelite.tcz' >> $ONBOOTLST

	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is added to .xfiletool.lst</p>'
	sudo sed -i '/^opt\/jivelite/d' /opt/.xfiletool.lst
	sudo echo 'opt/jivelite' >> /opt/.xfiletool.lst
}

pcp_delete_jivelite() {
	echo '<p class="info">[ INFO ] Jivelite is removed from piCorePlayer.</p>'
	sudo rm -f /mnt/mmcblk0p2/tce/optional/jivelite.tcz
	sudo rm -f /mnt/mmcblk0p2/tce/optional/jivelite.tcz.md5.txt
	sudo rm -rf /home/tc/.jivelite

	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is removed from onboot.lst</p>'
	sudo sed -i '/jivelite.tcz/d' $ONBOOTLST

	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Jivelite is removed from .xfiletool.lst</p>'
	sudo sed -i '/^opt\/jivelite/d' /opt/.xfiletool.lst

	[ "$JIVELITE" = "no" ] && VISUALISER="no"
	pcp_save_to_config
}

pcp_remove_temp() {
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Removing previous Jivelite downloads from /tmp directory.</p>'
	sudo rm -f /tmp/$JIVELITE_TCZ
	sudo rm -f /tmp/$JIVELITE_MD5
	sudo rm -f /tmp/VU_Meter*
}

pcp_download_vumeters() {
	cd /tmp
	sudo rm -f VU_Meter*
	echo '<p class="info">[ INFO ] Downloading VU Meters from Ralphy'\''s repository...</p>'

	for i in $AVAILABLE_VUMETERS
	do
		TCZ=${i}
		MD5=${i}.md5.txt

		$WGET -s ${REPOSITORY}/${TCZ}
		if [ $? -eq 0 ]; then
			echo '<p class="info">[ INFO ] Downloading '$TCZ'...'
			$WGET ${REPOSITORY}/${TCZ} -O /tmp/${TCZ}
			$WGET ${REPOSITORY}/${MD5} -O /tmp/${MD5}
			md5sum -c ${MD5}
			if [ $? -eq 0 ]; then
				echo '<p class="ok">[ OK ] '$TCZ' download successful.</p>'
				sudo cp /tmp/${TCZ} /mnt/mmcblk0p2/tce/optional/
				sudo chown tc:staff /mnt/mmcblk0p2/tce/optional/${TCZ}
				sudo cp /tmp/${MD5} /mnt/mmcblk0p2/tce/optional/
				sudo chown tc:staff /mnt/mmcblk0p2/tce/optional/${MD5}
			else
				echo '<p class="error">[ ERROR ] Download unsuccessful, MD5 mismatch, try again later!</p>'
			fi
		else
			echo '<p class="error">[ ERROR ] '$TCZ' not available in repository, try again later!</p>'
		fi
	done
}

pcp_install_default_vumeter() {
	echo '<p class="info">[ INFO ] Installing default VU Meter...</p>'
	sudo -u tc tce-load -i $DEFAULT_VUMETER
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Adding default VU Meter to onboot.lst...</p>'
	sudo sed -i '/VU_Meter/d' $ONBOOTLST
	sudo echo $DEFAULT_VUMETER >> $ONBOOTLST
}

pcp_install_vumeter() {
	echo '<p class="info">[ INFO ] Installing VU Meter...</p>'

	# Unmount all loop mounted VU_Meters (Note: should be only zero or one)
	MOUNTED_METERS=$(df | grep VU_Meter | awk '{print $6}' )
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] '$MOUNTED_METERS'</p>'

	for i in $MOUNTED_METERS
	do
		sudo umount $i
	done

	rm -f /usr/local/tce.installed/VU_Meter*
	sudo rm /opt/jivelite/share/jive/applets/JogglerSkin/images/UNOFFICIAL/VUMeter/vu_analog_25seq_w.png
	sudo -u tc tce-load -i $VUMETER >/dev/null 2>&1
	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] VU Meter is added to onboot.lst</p>'
	sudo sed -i '/VU_Meter/d' $ONBOOTLST
	sudo echo $VUMETER >> $ONBOOTLST
}

pcp_delete_vumeters() {
	echo '<p class="info">[ INFO ] Removing VU Meters...</p>'
	sudo rm -f /mnt/mmcblk0p2/tce/optional/VU_Meter*.tcz
	sudo rm -f /mnt/mmcblk0p2/tce/optional/VU_Meter*.tcz.md5.txt

	[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Removing VU Meter from onboot.lst...</p>'
	sudo sed -i '/VU_Meter/d' $ONBOOTLST
}

pcp_lirc_popup() {
	if [ "$IR_LIRC" = "yes" ]; then
		STRING1='INFO: LIRC is enabled; you might need to remove/install LIRC again to fix problems. But first press [OK] to reboot now'
		SCRIPT1='reboot.cgi'
		pcp_confirmation_required
	else
		pcp_reboot_required
	fi
}

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
pcp_table_top "Jivelite"

case "$OPTION" in
	JIVELITE)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Doing OPTION: '$OPTION'<br />'
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Doing with SUBMIT: '$SUBMIT'<br />'
		case "$SUBMIT" in
			Save)
				case "$JIVELITE" in
					yes)
						pcp_download_jivelite
						pcp_install_jivelite
						pcp_download_vumeters
						pcp_install_default_vumeter
						pcp_remove_temp
					;;
					no)
						pcp_delete_jivelite
						pcp_delete_vumeters
						pcp_remove_temp
					;;
					*)
						[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] JIVELITE: '$JIVELITE'<br />'
					;;
				esac
				pcp_backup
				echo '<p class="info">[ INFO ] A reboot is needed in order to finalize!</p>'
				pcp_lirc_popup
			;;
			Reset)
				echo '<p class="info">[ INFO ] Resetting Jivelite Configuration......</p>'
				rm -f /home/tc/.jivelite/userpath/settings/*.lua
				pcp_backup
				pkill -SIGTERM jivelite
				echo '<p class="info">[ INFO ] Jivelite has been reset and restarted. Reconfigure Jivelite and then Backup Changes !</p>'
			;;
			*)
				echo '<p class="error">[ ERROR ] JIVELITE: '$JIVELITE', Bad SUBMIT:'$SUBMIT'<br />'
			;;
		esac
		[ $DEBUG -eq 1 ] && pcp_show_config_cfg
	;;
	VUMETER)
		[ $DEBUG -eq 1 ] && echo '<p class="debug">[ DEBUG ] Doing OPTION: '$OPTION'<br />'
		case "$SUBMIT" in
			Save)
				pcp_install_vumeter
				echo '<p class="info">[ INFO ] A restart of Jivelite is needed in order to finalize!</p>'
				echo '<p class="info">[ INFO ] Jivelite will now restart!</p>'
				sudo killall jivelite
			;;
			Download)
				pcp_download_vumeters
			;;
		esac
	;;
esac

pcp_table_middle
pcp_go_back_button
pcp_table_end
pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'
