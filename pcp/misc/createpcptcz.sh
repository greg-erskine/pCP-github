#!/bin/sh -x
# Script to create pcp.tcz

# Version: 0.02 2015-07-08 SBP
#	Added the other files as well.

# Version: 0.01 2014-04-23 GE
#	Added to git.

. /etc/init.d/tc-functions
checkroot

WWWROOT=/home/tc
#WWWROOT=/var/xxxx # Future location

pcp_extension_report() {
	ls -al /tmp/pcp.tcz
	echo "" >> /tmp/pcp.tcz.txt
	mkdir /tmp/tempmount
	sudo mount /tmp/pcp.tcz /tmp/tempmount -t squashfs -o loop,ro,bs=4096
	ls -alR /tmp/tempmount/*
	sudo umount /tmp/tempmount
}

echo -n "${BLUE}Removing previous pcp.tcz files... ${NORMAL}"
rm -rf /tmp/pcpextension
rm -f /tmp/pcp.tcz
rm -rf /tmp/tempmount
echo "${GREEN}Done.${NORMAL}"

cat /etc/motd > /tmp/pcp.tcz.txt

#########################################################################################
# STEEN, WARNING !! Changing original files and directories !!
# Prepare directory and file ownership and permissions.
# First step to setting proper permissions.
#----------------------------------------------------------------------------------------
# As the files are getting copied back and forth, edited etc their permissions are
# getting changed, resulting in inconsistencies. Let's fix it here.
# These are not the final permissions. Ideally, the web server needs to run as a 
# non-root user... tc?? One day. Also, write permissions should be removed.
#########################################################################################
echo -n "${BLUE}Setting ${WWWROOT}/www permissions... ${NORMAL}"
chown -R tc:staff /home/tc/www
chmod u=rwx,g=rx,o= /home/tc/www/cgi-bin/*
chmod u=rw,g=r,o= /home/tc/www/css/*
chmod u=rw,g=r,o= /home/tc/www/images/*
chmod u=rw,g=r,o= /home/tc/www/js/*
chmod u=r,g=r,o= /home/tc/www/index.html
echo "${GREEN}Done.${NORMAL}"

#########################################################################################
# GREG Tidy up code here. Does it make a difference in directory ownership and
# permissions doing it this long handed way?
#########################################################################################
echo -n "${BLUE}Copying ${WWWROOT}/www files... ${NORMAL}"
cd /tmp
mkdir pcpextension
cd pcpextension
mkdir -p home/tc/www
cd home/tc/www
mkdir -p cgi-bin
mkdir -p css
mkdir -p images
mkdir -p js
cd /home/tc
cp -rp www/* /tmp/pcpextension/home/tc/www
echo "${GREEN}Done.${NORMAL}"

#========================================================================================
# Create pcp extension autorun script
#----------------------------------------------------------------------------------------
echo -n "${BLUE}Copying autorun script... ${NORMAL}"
mkdir -p /tmp/pcpextension/usr/local/tce.installed
cp ~/pcp /tmp/pcpextension/usr/local/tce.installed
sudo chown -R root:staff /tmp/package/usr/local/tce.installed
sudo chmod -R u=rwx,g=rwx,o=rx /tmp/package/usr/local/tce.installed
echo "${GREEN}Done.${NORMAL}"

#========================================================================================
# Copy pCP files from /etc directory
#----------------------------------------------------------------------------------------
echo -n "${BLUE}Copying /etc files... ${NORMAL}"
mkdir -p /tmp/pcpextension/etc

# -rwxr-xr-x 1 root root /etc/asound.conf
chown root:root /etc/asound.conf
chmod u=rwx,g=rx,o=rx /etc/asound.conf
cp -rp /etc/asound.conf /tmp/pcpextension/etc/asound.conf.sample

# -rw-r--r-- 1 root root /etc/group
chown root:root /etc/group
chmod u=rw,g=r,o=r /etc/group
cp -rp /etc/group /tmp/pcpextension/etc/group.sample

# -rwxr-xr-x 1 root root /etc/modprobe.conf
chown root:root /etc/modprobe.conf
chmod u=rwx,g=rx,o=rx /etc/modprobe.conf
cp -rp /etc/modprobe.conf /tmp/pcpextension/etc/modprobe.conf.sample

# -rw-r--r-- 1 root root /etc/motd
chown root:root /etc/motd
chmod u=rw,g=r,o=r /etc/motd
cp -rp /etc/motd /tmp/pcpextension/etc/motd.sample

# -rw-r--r-- 1 root root /etc/passwd
chown root:root /etc/passwd
chmod u=rw,g=r,o=r /etc/passwd
cp -rp /etc/passwd /tmp/pcpextension/etc/passwd.sample

# -rw-r----- 1 root root /etc/shadow - piCore
# -rw-r----- 1 root shadow /etc/shadow - Rasbian
chown root:root /etc/shadow
chmod u=rw,g=r,o= /etc/shadow
cp -rp /etc/shadow /tmp/pcpextension/etc/shadow.sample
echo "${GREEN}Done.${NORMAL}"

#========================================================================================
# Copy pCP files from /usr/local/ directory
#----------------------------------------------------------------------------------------
echo -n "${BLUE}Copying /usr/local files... ${NORMAL}"
mkdir -p /tmp/pcpextension/usr/local/sbin

# -rwxr-xr-x 1 root root setup
chown root:root /usr/local/sbin/setup
chmod u=rwx,g=rx,o=rx /usr/local/sbin/setup
cp -rp /usr/local/sbin/setup /tmp/pcpextension/usr/local/sbin

# -rwxr-xr-x 1 root root webgui
chown root:root /usr/local/sbin/webgui
chmod u=rwx,g=rx,o=rx /usr/local/sbin/webgui
cp -rp /usr/local/sbin/webgui /tmp/pcpextension/usr/local/sbin

# -rwxr-xr-x 1 root root config.cfg
chown root:root /usr/local/sbin/config.cfg
chmod u=rwx,g=rx,o=rx /usr/local/sbin/config.cfg
cp -rp /usr/local/sbin/config.cfg /tmp/pcpextension/usr/local/sbin

# -rw-r--r-- 1 root root piversion.cfg
chown root:root /usr/local/sbin/piversion.cfg
chmod u=rw,g=r,o=r /usr/local/sbin/piversion.cfg
cp -rp /usr/local/sbin/piversion.cfg /tmp/pcpextension/usr/local/sbin

#########################################################################################
# STEEN, SHOULD THESE BE INCLUDED??? SHOULD BE GENERATED THE FIRST TIME YOU ACCESS SSH.
#########################################################################################
#mkdir -p /tmp/pcpextension/usr/local/etc
#cp -rp /usr/local/etc/dropbear/dropbear_dss_host_key /tmp/pcpextension/usr/local/etc
#cp -rp /usr/local/etc/dropbear/dropbear_rsa_host_key /tmp/pcpextension/usr/local/etc
#########################################################################################

mkdir -p /tmp/pcpextension/usr/local/etc/init.d
# -rwxr-xr-x 1 root root squeezelite
chown root:root /usr/local/etc/init.d/squeezelite
chmod u=rwx,g=rx,o=rx /usr/local/etc/init.d/squeezelite
cp -rp /usr/local/etc/init.d/squeezelite /tmp/pcpextension/usr/local/etc/init.d

# -rwxr-xr-x 1 root root httpd
chown root:root /usr/local/etc/init.d/httpd
chmod u=rwx,g=rx,o=rx /usr/local/etc/init.d/httpd
cp -rp /usr/local/etc/init.d/httpd /tmp/pcpextension/usr/local/etc/init.d
echo "${GREEN}Done.${NORMAL}"

#========================================================================================
# Copy mmcblk0p2 files
#----------------------------------------------------------------------------------------
echo -n "${BLUE}Copying /mnt/mmcblk0p2 files... ${NORMAL}"
mkdir -p /tmp/pcpextension/mnt/mmcblk0p2/tce

#########################################################################################
# STEEN, QUESTIONABLE OWNERSHIP AND PERMISSIONS
#########################################################################################
# -rwxrwxr-x 1 tc staff onboot.lst
chown tc:staff /mnt/mmcblk0p2/tce/onboot.lst
chmod u=rwx,g=rwx,o=rx /mnt/mmcblk0p2/tce/onboot.lst
cp -rp /mnt/mmcblk0p2/tce/onboot.lst /tmp/pcpextension/mnt/mmcblk0p2/tce

#########################################################################################
# STEEN, QUESTIONABLE OWNERSHIP AND PERMISSIONS
#########################################################################################
# -rwxrwxr-x 1 tc staff piCorePlayer.dep
chown tc:staff /mnt/mmcblk0p2/tce/piCorePlayer.dep
chmod u=rwx,g=rwx,o=rx /mnt/mmcblk0p2/tce/piCorePlayer.dep
cp -rp /mnt/mmcblk0p2/tce/piCorePlayer.dep /tmp/pcpextension/mnt/mmcblk0p2/tce

#########################################################################################
# STEEN, QUESTIONABLE OWNERSHIP AND PERMISSIONS
#########################################################################################
# Might be possible to download or make a squeezelite.tcz
# -rwxrw-r-- 1 tc staff squeezelite-armv6hf
chown tc:staff /mnt/mmcblk0p2/tce/piCorePlayer.dep
chmod u=rwx,g=rw,o=r /mnt/mmcblk0p2/tce/piCorePlayer.dep
cp -rp /mnt/mmcblk0p2/tce/squeezelite-armv6hf /tmp/pcpextension/mnt/mmcblk0p2/tce
echo "${GREEN}Done.${NORMAL}"

#========================================================================================
# Copy misc files
#----------------------------------------------------------------------------------------
echo -n "${BLUE}Copying miscellaneous files... ${NORMAL}"

#########################################################################################
# STEEN, SHOULD THESE BE INCLUDED??? USER SETTINGS.
#########################################################################################
mkdir -p /tmp/pcpextension/var/lib/alsa
cp -rp /var/lib/alsa/asound.state /tmp/pcpextension/var/lib/alsa

#########################################################################################
# STEEN, SHOULD THESE BE INCLUDED??? CRONTAB SHOULD BE EMPTY.
#########################################################################################
#mkdir -p /tmp/pcpextension/var/spool/cron/crontabs
#cp -rp /var/spool/cron/crontabs /tmp/pcpextension/var/spool/cron

echo "${GREEN}Done.${NORMAL}"

#========================================================================================
# Check for squashfs-tools.tcz and download and install
#----------------------------------------------------------------------------------------
echo -n "${BLUE}Loading squashfs-tools.tcz...  ${NORMAL}"
if [ ! -f /mnt/mmcblk0p2/tce/optional/squashfs-tools.tcz ]; then
	sudo -u tc tce-load -w squashfs-tools.tcz >> /tmp/pcp.tcz.txt 2>&1
fi
sudo -u tc tce-load -i squashfs-tools.tcz >> /tmp/pcp.tcz.txt 2>&1
echo "" >> /tmp/pcp.tcz.txt
echo "${GREEN}Done.${NORMAL}"

#========================================================================================
# Create pcp.tcz extension
#----------------------------------------------------------------------------------------
echo -n "${BLUE}Creating pcp.tcz extension... ${NORMAL}"
cd /tmp
mksquashfs pcpextension pcp.tcz >> /tmp/pcp.tcz.txt
echo "" >> /tmp/pcp.tcz.txt
echo "${GREEN}Done.${NORMAL}"

echo -n "${BLUE}Generating report... ${NORMAL}"
pcp_extension_report >> /tmp/pcp.tcz.txt
echo "${GREEN}Done.${NORMAL}"

exit 0