#!/bin/sh

# Version: 0.02 2015-07-07 SBP
#	Added the other files as well.

# Version: 0.01 2014-04-23 GE
#	Added to git.

# Script to create pcp.tcz
# Only does www section of pcp at the moment.

set -x

rm -rf /tmp/pcpextension
rm -f /tmp/pcp.tcz

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


#copy from etc direktory pCP files motd, asound.conf files and password files
mkdir -p /tmp/pcpextension/etc
cp -rp /etc/motd /tmp/pcpextension/etc
cp -rp /etc/asound.conf /tmp/pcpextension/etc
cp -rp /etc/passwd /tmp/pcpextension/etc
cp -rp /etc/shadow /tmp/pcpextension/etc
cp -rp /etc/group /tmp/pcpextension/etc
cp -rp /etc/modprobe.conf /tmp/pcpextension/etc

#copy pCP files from usr directory
mkdir -p /tmp/pcpextension/usr/local/sbin
cp -rp /usr/local/sbin/setup /tmp/pcpextension/usr/local/sbin
cp -rp /usr/local/sbin/webgui /tmp/pcpextension/usr/local/sbin
cp -rp /usr/local/sbin/config.cfg /tmp/pcpextension/usr/local/sbin
cp -rp /usr/local/sbin/piversion.cfg /tmp/pcpextension/usr/local/sbin
mkdir -p /tmp/pcpextension/usr/local/etc
cp -rp /usr/local/etc/dropbear/dropbear_dss_host_key /tmp/pcpextension/usr/local/etc
cp -rp /usr/local/etc/dropbear/dropbear_rsa_host_key /tmp/pcpextension/usr/local/etc
mkdir -p /tmp/pcpextension/usr/local/etc/init.d
cp -rp /usr/local/etc/init.d/squeezelite /tmp/pcpextension/usr/local/etc/init.d
cp -rp /usr/local/etc/init.d/httpd /tmp/pcpextension/usr/local/etc/init.d

#copy to mmcblk0p2
mkdir -p /tmp/pcpextension/mnt/mmcblk0p2/tce
cp -rp /mnt/mmcblk0p2/tce/onboot.lst /tmp/pcpextension/mnt/mmcblk0p2/tce
cp -rp /mnt/mmcblk0p2/tce/piCorePlayer.dep /tmp/pcpextension/mnt/mmcblk0p2/tce
#might be possible to download or make a squeezelite.tcz
cp -rp /mnt/mmcblk0p2/tce/squeezelite-armv6hf /tmp/pcpextension/mnt/mmcblk0p2/tce

#copy misc files
mkdir -p /tmp/pcpextension/var/lib/alsa
cp -rp /var/lib/alsa/asound.state /tmp/pcpextension/var/lib/alsa
mkdir -p /tmp/pcpextension/var/spool/cron/crontabs
cp -rp /var/spool/cron/crontabs /tmp/pcpextension/var/spool/cron



# Check for squashfs-tools.tcz and download and install
if [ ! -f /mnt/mmcblk0p2/tce/optional/squashfs-tools.tcz ]; then
sudo -u tc tce-load -w squashfs-tools.tcz
fi
sudo -u tc tce-load -i squashfs-tools.tcz

cd /tmp
mksquashfs pcpextension pcp.tcz

exit
