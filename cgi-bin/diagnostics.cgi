#!/bin/sh
# Diagnostics script

. pcp-functions
pcp_variables

# Local variables
START="====================> Start <===================="
END="=====================> End <====================="

echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
echo '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
echo ''
echo '<head>'
echo '  <meta http-equiv="Cache-Control" content="no-cache" />'
echo '  <meta http-equiv="Pragma" content="no-cache" />'
echo '  <meta http-equiv="Expires" content="0" />'
echo '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
echo '  <title>pCP - Diagnostics</title>'
echo '  <meta name="author" content="Steen" />'
echo '  <meta name="description" content="Diagnostics" />'
echo '  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css" />'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_navigation
pcp_running_script

echo '<h2>[ INFO ] piCore version: '$(pcp_picore_version)'</h2>'
echo '<textarea name="TextBox4" cols="120" rows="2">'
version
echo '</textarea>'

echo '<h2>[ INFO ] piCorePlayer version: '$(pcp_picoreplayer_version)'</h2>'
echo '<textarea name="TextBox4" cols="120" rows="5">'
echo $START
cat /usr/local/sbin/piversion.cfg
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Squeezelite version and license: '$(pcp_squeezelite_version)'</h2>'
echo '<textarea name="TextBox" cols="120" rows="15">'
echo $START
/mnt/mmcblk0p2/tce/squeezelite-armv6hf -t
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] ALSA output devices</h2>'
echo '<textarea name="TextBox" cols="120" rows="15">'
echo $START
/mnt/mmcblk0p2/tce/squeezelite-armv6hf -l
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Squeezelite help</h2>'
#echo '<p style="font-size:10px">'
echo '<textarea name="TextBox" cols="120" rows="20">'
sudo /mnt/mmcblk0p2/tce/squeezelite-armv6hf -h
echo '</textarea>'

# Check if mmcblk0p1 is mounted otherwise mount it

pcp_mount_mmcblk0p1
dmesg | tail -1

if mount | grep $VOLUME; then
	pcp_show_config_txt
	pcp_show_cmdline_txt
	pcp_umount_mmcblk0p1
	sleep 2
	dmesg | tail -1
fi

pcp_show_config_cfg

echo '<h2>[ INFO ] Current bootsync.sh</h2>'
echo '<textarea name="TextBox4" cols="120" rows="8">'
echo $START
cat $BOOTSYNC
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Current bootlocal.sh</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
echo $START
cat $BOOTLOCAL
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Current shutdown.sh</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
echo $START
cat $SHUTDOWN
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] dmesg</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
dmesg
echo '</textarea>'

# These files are created by the backup process
#	/tmp/backup_done
#	/tmp/backup_status

echo '<h2>[ INFO ] Current /opt/.filetool.lst</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
echo $START
cat /opt/.filetool.lst
echo $END
echo '</textarea>'

echo '<h2>[ INFO ] Current /opt/.xfiletool.lst</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
echo $START
cat /opt/.xfiletool.lst
echo $END
echo '</textarea>'
 
echo '<h2>[ INFO ] Backup mydata</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
tar tzf /mnt/mmcblk0p2/tce/mydata.tgz
echo '</textarea>'

echo '<h2>[ INFO ] lsmod</h2>'
echo '<textarea name="TextBox4" cols="120" rows="15">'
lsmod
echo '</textarea>'

echo '<h2>[ INFO ] Directory of www/cgi-bin</h2>'
echo '<pre>'
ls -al
echo '</pre>'

pcp_refresh_button

echo '</body>'
echo '</html>'