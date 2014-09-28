#!/bin/sh
echo "  "
echo "  "
#Read from config file.
. /usr/local/sbin/config.cfg

read -p "Change ALSA settings (Current setting is: $ALSA_PARAMS)
- to keep current press ENTER:
- to remove all ALSA settings, write x and ENTER  
- to change settings write the new here (without '"-a"'): " t1
if [ -n "$t1" ]
then
ALSA_PARAMS="$t1"
else
ALSA_PARAMS="$ALSA_PARAMS"
fi

# adding "" around variable
ALSA_PARAMS="\"${ALSA_PARAMS}"\"

#This will remove both "-a x" and "" 
if [ "$ALSA_PARAMS" = '"x"' ] || [ "$ALSA_PARAMS" = '""' ]
then 
ALSA_PARAMS='""'
else break
fi


# Make changes in config file    
echo "ALSA setting is now: $ALSA_PARAMS"
sed -i "s/\(ALSA_PARAMS *=*\).*/\1$ALSA_PARAMS/" /usr/local/sbin/config.cfg
echo "  "
echo "  "
exit 0
