#!/bin/sh
echo "  "
echo "  "
#Read from config file. 
. /usr/local/sbin/config.cfg

read -p "Change Output settings (Current setting is: $OUTPUT)
- to keep current press ENTER.
- to remove all Output settings, write x and ENTER 
- to change settings write the new here (without '"-o"'):" t1
if [ -n "$t1" ]
then
OUTPUT="$t1"
else
OUTPUT="$OUTPUT"
fi

# adding "" around variable
OUTPUT="\"${OUTPUT}"\"    

#This will remove both "-a x" and "" 
if [ "$OUTPUT" = '"x"' ] || [ "$OUTPUT" = '""' ]
then 
OUTPUT='""'
else break
fi


# Make changes in config file
echo "Output settings is now: $OUTPUT"
sudo sed -i "s/\(OUTPUT *=*\).*/\1$OUTPUT/" /usr/local/sbin/config.cfg
echo "  "
echo "  "
exit 0
