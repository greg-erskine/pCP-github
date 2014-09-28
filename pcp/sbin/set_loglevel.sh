#!/bin/sh
echo "  "
echo "  "
#Read from config file.
. /usr/local/sbin/config.cfg

read -p "Change Log level(Current Log level is: $LOGLEVEL)
- to keep current press ENTER.
- to remove all Loglevel settings, write x and ENTER  
- to change Log level write the new level here (without '"-d"'):" t1
if [ -n "$t1" ]
then
LOGLEVEL="$t1"
else
LOGLEVEL="$LOGLEVEL"
fi

# adding "" around variable
LOGLEVEL="\"${LOGLEVEL}"\"    

#This will remove both "-a x" and "" 
if [ "$LOGLEVEL" = '"x"' ] || [ "$LOGLEVEL" = '""' ]
then 
LOGLEVEL='""'
else break
fi


# Make changes in config file
echo "Log level is now set to: $LOGLEVEL"
sudo sed -i "s/\(LOGLEVEL *=*\).*/\1$LOGLEVEL/" /usr/local/sbin/config.cfg

LOGFILE="-f logfile.log"
LOGFILE="\"${LOGFILE}"\"
sudo sed -i "s/\(LOGFILE *=*\).*/\1$LOGFILE/" /usr/local/sbin/config.cfg
echo "Log is saved in /mnt/mmcblk0p1/tce/logfile.log"
echo "  "
echo "  "
echo
exit 0
