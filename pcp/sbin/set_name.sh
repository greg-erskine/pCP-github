#!/bin/sh
echo "  "
echo "  "
#Read from config file. 
. /usr/local/sbin/config.cfg

read -p "Change name of player (Current name is: $NAME)
- to keep current press ENTER.
- to remove the Name, write x and ENTER  
- to change name write the new here (without '"-n"'):" t1
if [ -n "$t1" ]
then
NAME="$t1"
else
NAME="$NAME"
fi

# adding "" around variable
NAME="\"${NAME}"\"    

#This will remove both "-a x" and "" 
if [ "$NAME" = '"x"' ] || [ "$NAME" = '""' ]
then 
NAME='""'
else break
fi


# Make changes in config file
echo "Name of player is now: $NAME"
sudo sed -i "s/\(NAME *=*\).*/\1$NAME/" /usr/local/sbin/config.cfg
echo "  "
echo "  "
exit 0
