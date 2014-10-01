#!/bin/sh
echo "  "
echo "  "
#Read from config file. 
. /usr/local/sbin/config.cfg

read -p "Change Buffer size (Current buffer size is: $BUFFER_SIZE)
- to keep current press ENTER.
- to remove all Buffer settings, write x and ENTER  
- to change Buffer size write the new here (without '"-b"'):" t1
if [ -n "$t1" ]
then
BUFFER_SIZE="$t1"
else
BUFFER_SIZE="$BUFFER_SIZE"
fi

# adding "" around variable
BUFFER_SIZE="\"${BUFFER_SIZE}"\"    

#This will remove both "-a x" and "" 
if [ "$BUFFER_SIZE" = '"x"' ] || [ "$BUFFER_SIZE" = '""' ]
then 
BUFFER_SIZE='""'
else break
fi

# Make changes in config file
echo
echo "Buffer size is now: $BUFFER_SIZE"
sudo sed -i "s/\(BUFFER_SIZE *=*\).*/\1$BUFER_SIZE/" /usr/local/sbin/config.cfg
echo "  "
echo "  "
exit 0
