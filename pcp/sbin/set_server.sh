#!/bin/sh
echo "  "
echo "  "
#Read from config file.
. /usr/local/sbin/config.cfg

read -p "Change Server(Current Server is: $SERVER_IP)
- to keep current press ENTER.
- to remove all Server settings, write x and ENTER    
- to change Server write the new here (without '"-s"'):" t1
if [ -n "$t1" ]
then
SERVER_IP="$t1"
else
SERVER_IP="$SERVER_IP"
fi

# adding "" around variable
SERVER_IP="\"${SERVER_IP}"\"    

#This will remove both "-a x" and "" 
if [ "$SERVER_IP" = '"x"' ] || [ "$SERVER_IP" = '""' ]
then 
SERVER_IP='""'
else break
fi


# Make changes in config file
echo "Server is now set to: $SERVER_IP"
sudo sed -i "s/\(SERVER_IP *=*\).*/\1$SERVER_IP/" /usr/local/sbin/config.cfg
echo "  "
echo "  "
exit 0
