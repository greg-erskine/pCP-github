#!/bin/sh
echo "  "
echo "  "
#Read from config file. 
. /usr/local/sbin/config.cfg

read -p "Change Upsample settings (Current setting is: $UPSAMPLE)
- to keep current press ENTER.
- to remove all Output settings, write x and ENTER 
- to change settings write the new here (without '"-u"'):" t1
if [ -n "$t1" ]
then
UPSAMPLE="$t1"
else
UPSAMPLE="$UPSAMPLE"
fi

# adding "" around variable
UPSAMPLE="\"${UPSAMPLE}"\"    

#This will remove both "-a x" and "" 
if [ "$UPSAMPLE" = '"x"' ] || [ "$UPSAMPLE" = '""' ]
then 
UPSAMPLE='""'
else break
fi


# Make changes in config file
echo "Upsample settings is now: $UPSAMPLE"
sudo sed -i "s/\(UPSAMPLE *=*\).*/\1$UPSAMPLE/" /usr/local/sbin/config.cfg
echo "  "
echo "  "
exit 0
