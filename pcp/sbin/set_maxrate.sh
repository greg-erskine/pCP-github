#!/bin/sh
echo "  "
echo "  "
#Read from config file.
. /usr/local/sbin/config.cfg

read -p "Change Max sample rate (Current Max rate is: $MAX_RATE)
- to keep current press ENTER.
- to remove all Alsa settings, write x and ENTER 
- to change max sample rate write the new level here (without '"-r"'):" t1
if [ -n "$t1" ]
then
MAX_RATE="$t1"
else
MAX_RATE="$MAX_RATE"
fi

# adding "" around variable
MAX_RATE="\"${MAX_RATE}"\"    

#This will remove both "-a x" and "" 
if [ "$MAX_RATE" = '"x"' ] || [ "$MAX_RATE" = '""' ]
then 
MAX_RATE='""'
else break
fi


# Make changes in config file
echo "Max sample rate is now set to: $MAX_RATE"
sudo sed -i "s/\(MAX_RATE *=*\).*/\1$MAX_RATE/" /usr/local/sbin/config.cfg
echo "  "
echo "  "
exit 0
