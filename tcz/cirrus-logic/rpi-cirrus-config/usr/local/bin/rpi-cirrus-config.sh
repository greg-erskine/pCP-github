#!/bin/sh

# setup default mixer settings for Cirrus Logic Audio Card

if [ -r /home/tc/.config/rpi-cirrus-config.sh ] ; then
	echo "Setting up Cirrus Logic Audio Card with user config"
	sh /home/tc/.config/rpi-cirrus-config.sh
else
	echo "Setting up Cirrus Logic Audio Card"

	# load helper functions and definitions
	. /usr/local/lib/alsa/rpi-cirrus-functions.sh

	. /usr/local/etc/pcp/cirrus.conf

	[ $SPEAKERS -eq 1 ] && playback_to_speakers
	[ $SPDIF -eq 1 ] && playback_to_spdif
	[ $LINEOUT -eq 1 ] && playback_to_lineout
	[ $HEADSET -eq 1 ] && playback_to_headset
	mixer 'Noise Gate Switch' off
fi
