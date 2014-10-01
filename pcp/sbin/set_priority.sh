#!/bin/sh
echo "  "
echo "  "
#Read from config file.
. /usr/local/sbin/config.cfg

read -p "Change priority level (Current priority level is: $PRIORITY)
- to keep current press ENTER.
- to remove all Priority settings, write x and ENTER  
- to change priority level write the new level here (without '"-p"'):" t1
if [ -n "$t1" ]
then
PRIORITY="$t1"
else
PRIORITY="$PRIORITY"
fi

# adding "" around variable
PRIORITY="\"${PRIORITY}"\"    

#This will remove both "-a x" and "" 
if [ "$PRIORITY" = '"x"' ] || [ "$PRIORITY" = '""' ]
then 
PRIORITY='""'
else break
fi


# Make changes in config file
echo "Priority is now set to: $PRIORITY"
sudo sed -i "s/\(PRIORITY *=*\).*/\1$PRIORITY/" /usr/local/sbin/config.cfg
echo "  "
echo "  "
exit 0
