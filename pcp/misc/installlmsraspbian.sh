#!/bin/bash

# This script install LMS on Raspbian.
# Reference: http://wiki.slimdevices.com/index.php/DebianPackage

latest_lms=$(wget -q -O - "http://www.mysqueezebox.com/update/?version=7.8.0&revision=1&geturl=1&os=deb")
echo $latest_lms
mkdir -p /sources
cd /sources
wget $latest_lms
lms_deb=$(echo $latest_lms | cut -d "/" -f5)
echo $lms_deb
dpkg -i $lms_deb
#ls /sources/logi* -1t | tail -3 | xargs -d '\n' rm -f
