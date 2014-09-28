#!/bin/sh
echo "  "
echo "  "
#Read from config file. 
. /usr/local/sbin/config.cfg

read -p "Restrict codec use (Current codec restriction is: $CODEC)
- to keep current press ENTER.
- to remove all Codec settings, write x and ENTER  
- to change codec resriction write the new here (without '"-c"'):" t1
if [ -n "$t1" ]
then
CODEC="$t1"
else
CODEC="$CODEC"
fi

# adding "" around variable
CODEC="\"${CODEC}"\"    

#This will remove both "-a x" and "" 
if [ "CODEC" = '"x"' ] || [ "$CODEC" = '""' ]
then 
CODEC='""'
else break
fi


# Make changes in config file
echo "Codec is now restricted to: $CODEC"
sudo sed -i "s/\(CODEC *=*\).*/\1$CODEC/" /usr/local/sbin/config.cfg
echo "  "
echo "  "
exit 0
