#!/bin/sh
echo "  "
echo "  "
#Read from config file.
#. /mnt/mmcblk0p1/tce/OliWeb-master/ivySox/picocgi/Config.cfg
. /usr/local/sbin/config.cfg
echo " "

echo "Change Squeezelite Settings"


echo " "
showMenu () {
echo "1)  Change Player name (Current name is: $NAME)"
echo "2)  Change Output setting (Current setting is: $OUTPUT)"
echo "3)  Change ALSA setting (Current setting is: $ALSA_PARAMS)"
echo "4)  Change MAC adress (Current adress is: $MAC_ADDRESS)"
echo "5)  Change Max sample rate (Current setting is: $MAX_RATE)"
echo " "
echo "6)  Change Buffer Size (Current setting is: $BUFFER_SIZE)"
echo "7)  Change Codec (Current Codec restriction is: $CODEC)"
echo "8)  Change Server (Current Server is: $SERVER)"
echo "9)  Change Priority level (Current Priority level is: $PRIORITY)"
#echo "10) Change Loglevel (Current loglevel is: $LOGLEVEL)"
echo "11) Change Upsample settings (Current Upsample setting is: $UPSAMPLE)"
echo "  "
echo "12) Make a backup of your Changes"
echo "13) Return to MAIN menu"




}



while [ 1 ]
do
showMenu
read CHOICE
case "$CHOICE" in

"1")
echo "NAME"
/usr/local/sbin/set_name.sh
;;


"2")
echo "OUTPUT"
/usr/local/sbin/set_output.sh
;;


"3")
echo "ALSA"
/usr/local/sbin/set_alsa.sh
;;


"4")
echo "MAC"
/usr/local/sbin/set_mac_add.sh
;;


"5")
echo "MAX RATE"
/usr/local/sbin/set_maxrate.sh
;;


"6")
echo "BUFFER SIZE"
/usr/local/sbin/set_buffer.sh
;;

"7")
echo "CODEC"
/usr/local/sbin/set_codec.sh
;;

"8")
echo "SERVER"
/usr/local/sbin/set_server.sh
;;

"9")
echo "PRIORITY"
/usr/local/sbin/set_priority.sh
;;

#"10")
#echo "LOGLEVEL"
#/usr/local/sbin/set_loglevel.sh
#;;

"11")
echo "UPSAMPLE"
/usr/local/sbin/upsample.sh
;;



"12")
echo "Saving your changes"
sudo filetool.sh -b
;;

"13")
exit


esac
done

