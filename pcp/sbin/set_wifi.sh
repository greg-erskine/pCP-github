#!/bin/sh

alias awk="busybox awk"
IFS=+
CONFIG=/usr/local/sbin/config.cfg

read TCUSER < /etc/sysconfig/tcuser
DB=/home/"$TCUSER"/wifi.db

set -- $(echo "" | awk -v dbfile="$DB" '
BEGIN {
        getline dbitem < dbfile
        split(dbitem,field,"\t")
        ssid = field[1]
        passwd = field[2]
        enc = field[3]
        close(dbfile)
}
END {
        print( "\"" ssid "\"" "+" "\"" passwd "\"" "+" "\"" enc "\"" )

} ' )

sudo sed -i "s/\(SSID *=*\).*/\1$1/" $CONFIG
sudo sed -i "s/\(PASSWORD *=*\).*/\1$2/" $CONFIG
sudo sed -i "s/\(ENCRYPTION *=*\).*/\1$3/" $CONFIG


