#!/bin/sh

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

# Check for squashfs-tools.tcz and download and install
if [ ! -f /mnt/mmcblk0p2/tce/optional/squashfs-tools.tcz ]; then
    sudo -u tc 'tce-load -w squashfs-tools.tcz'
fi
sudo -u tc 'tce-load -i squashfs-tools.tcz'

cd /tmp
mksquashfs pcpextension pcp.tcz

exit
