#!/bin/sh
echo "  "
echo "  "
echo "Your physical MAC adress is: "
MAC=$(ifconfig eth0 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}')
echo "$MAC"
echo "  "

#Currently used MAC adress read from config file 
. /usr/local/sbin/config.cfg


read -p "Change MAC adress? (Current used MAC adress is: $MAC_ADDRESS)
- to keep current press ENTER.
- to remove all MAC settings, write x and ENTER 
- to change settings write the new here (without '"-m"'):" t1
if [ -n "$t1" ]
then
MAC_ADDRESS="$t1"
else
MAC_ADDRESS="$MAC_ADDRESS"
fi

# adding "" around variable
MAC_ADDRESS="\"${MAC_ADDRESS}"\"    

#This will remove both "-a x" and "" 
if [ "$MAC_ADDRESS" = '"x"' ] || [ "$MAC_ADDRESS" = '""' ]
then 
MAC_ADDRESS='""'
else break
fi

# Make changes in config file
echo "MAC adress is now: $MAC_ADDRESS"
sudo sed -i "s/\(MAC_ADDRESS *=*\).*/\1$MAC_ADDRESS/" /usr/local/sbin/config.cfg
echo "  "
echo "  "
exit 0


