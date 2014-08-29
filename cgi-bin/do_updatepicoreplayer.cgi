#!/bin/sh
. pcp-functions
pcp_variables
. $CONFIGCFG



# Version: 0.02 2014-08-23 SBP
#      Added function so that onboot.lst will not be overwritten
#	Added function so that new needed packages for piCorePlayer will be added to onboot.lst from list in the new piCorePlayer home

# Version: 0.01 2014-06-25 GE
#	Original

# $UPD_PSP is defined in pcp-functions
# i.e. UPD_PCP=/tmp/upd_picoreplayer
# Read the version from the temp file
. $UPD_PCP/version.cfg

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
echo '  <script language="Javascript" src="../js/piCorePlayer.js"></script>'
echo '</head>'
echo ''
echo '<body>'

pcp_banner
pcp_running_script
pcp_mount_mmcblk0p1

# Delete all files from the boot partition
sudo rm -rf /mnt/mmcblk0p1/* 

# Copy the config file to boot partition
sudo cp -f /usr/local/sbin/config.cfg /mnt/mmcblk0p1/newconfig.cfg 
sudo dos2unix -u /mnt/mmcblk0p1/newconfig.cfg
echo '<p class="info">[ INFO ] Your config has been saved so your current settings will used be after updating piCorePlayer</p>'

# Untar and overwrite the boot files
echo '<p class="info">[ INFO ] Untarring '$INSITU'_boot.tar.gz...</p>'
echo '<textarea name="TextBox" cols="120" rows="8">'
sudo tar -zxvf $UPD_PCP/boot/"$INSITU"_boot.tar.gz -C /
echo '</textarea>'
[ $DEBUG = 1 ] && result=$? && echo '<p class="info">[ INFO ] boot tar: '$result'</p>'

pcp_umount_mmcblk0p1


#First delete all the kernel specific files in optional directory so no stray files are left
sudo rm -rf /mnt/mmcblk0p2/tce/optional/*piCore*.*

# Untar and overwrite the tce files
echo '<p class="info">[ INFO ] Untarring '$INSITU'_tce.tar.gz...</p>'
echo '<textarea name="TextBox" cols="120" rows="8">'
#sudo tar -zxvf $UPD_PCP/tce/"$INSITU"_tce.tar.gz -C /
sudo tar -zxvf $UPD_PCP/tce/"$INSITU"_tce.tar.gz -C / --exclude='mnt/mmcblk0p2/tce/onboot.lst'
echo '</textarea>'
[ $DEBUG = 1 ] && result=$? && echo '<p class="info">[ INFO ] tce tar: '$result'</p>'

# add eventual missing packages to onboot.lst. It is important if different versions of piCorePlayer have different needs.  
fgrep -vxf /mnt/mmcblk0p2/tce/onboot.lst /mnt/mmcblk0p2/tce/piCorePlayer.dep >> /mnt/mmcblk0p2/tce/onboot.lst


echo '<h2>piCorePlayer has been updated, please reboot now. And then you should have: '$INSITU'</h2>'
echo '<table border="0" cellspacing="0" cellpadding="0" width="960">'
echo '  <tr height="30">'
echo '    <td width="150" align="center">'
echo "      <form name=\"Reboot\" action=\"javascript:pcp_confirm('Reboot piCorePlayer?','reboot.cgi')\" method=\"get\" id=\"Reboot\">"
echo '      <input type="submit" value="     Reboot      " /></form>'
echo '    </td>'
echo '    <td valign="top">'
echo '      <p>Reboot - in order to finalize the update</p>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
echo '</body>'
echo '</html>'
