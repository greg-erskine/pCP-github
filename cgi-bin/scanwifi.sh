#!/bin/sh
killall -9 wpa_supplicant
sudo iwlist wlan0 scanning > /tmp/wifiscan #save scan results to a temp file
scan_ok=$(grep "wlan" /tmp/wifiscan) #check if the scanning was ok with wlan0
if [ -z "$scan_ok" ]; then
    killall -9 wpa_supplicant
    iwlist wlan0-1 scanning > /tmp/wifiscan
fi
scan_ok=$(grep "wlan" /tmp/wifiscan) #check if the scanning was ok
if [ -z "$scan_ok" ]; then #if scan was not ok, finish the script
    echo -n "
WIFI scanning failed.
    
"
    exit
fi
if [ -f /tmp/ssids ]; then
    rm /tmp/ssids
fi
n_results=$(grep -c "ESSID:" /tmp/wifiscan) #save number of scanned cell
i=1
while [ "$i" -le "$n_results" ]; do
        if [ $i -lt 10 ]; then
                cell=$(echo "Cell 0$i - Address:")
        else
                cell=$(echo "Cell $i - Address:")
        fi
        j=`expr $i + 1`
        if [ $j -lt 10 ]; then
                nextcell=$(echo "Cell 0$j - Address:")
        else
                nextcell=$(echo "Cell $j - Address:")
        fi
        awk -v v1="$cell" '$0 ~ v1 {p=1}p' /tmp/wifiscan | awk -v v2="$nextcell" '$0 ~ v2 {exit}1' > /tmp/onecell #store only one cell info in a temp file

        ##################################################
        ## Uncomment following line to show mac address ##

        #oneaddress=$(grep " Address:" /tmp/onecell | awk '{print $5}')

        onessid=$(grep "ESSID:" /tmp/onecell | awk '{ sub(/^[ \t]+/, ""); print }' | awk '{gsub("ESSID:", "");print}')
        oneencryption=$(grep "Encryption key:" /tmp/onecell | awk '{ sub(/^[ \t]+/, ""); print }' | awk '{gsub("Encryption key:on", "(secure)");print}' | awk '{gsub("Encryption key:off", "(open)  ");print}')
        onepower=$(grep "Quality=" /tmp/onecell | awk '{ sub(/^[ \t]+/, ""); print }' | awk '{gsub("Quality=", "");print}' | awk -F '/70' '{print $1}')
        onepower=$(awk -v v3=$onepower 'BEGIN{ print v3 * 10 / 7}')
        onepower=${onepower%.*}
        onepower="(Signal strength: $onepower%)"
        if [ -n "$oneaddress" ]; then                                                                                                            
                echo "$onessid  $oneaddress $oneencryption $onepower" >> /tmp/ssids                                                              
        else                                                                                                                                     
                echo "$onessid  $oneencryption $onepower" >> /tmp/ssids                                                                          
        fi
        i=`expr $i + 1`
done
rm /tmp/onecell
awk '{printf("%5d : %s\n", NR,$0)}' /tmp/ssids > /tmp/sec_ssids #add numbers at beginning of line
grep ESSID /tmp/wifiscan | awk '{ sub(/^[ \t]+/, ""); print }' | awk '{printf("%5d : %s\n", NR,$0)}' | awk '{gsub("ESSID:", "");print}' > /tmp/ssids #generate file with only numbers and names
echo -n "Available WIFI networks:
"
cat /tmp/sec_ssids #show ssids list
echo -n "Enter the numeric option for your selected network: "
read nsel
pattern=$(echo " $nsel : ")
wifissid=$(grep "$pattern" /tmp/ssids)
wifissid=$(echo "$wifissid" | awk -v pat="$pattern" '{gsub(pat, "");print}' | awk '{ sub(/^[ \t]+/, ""); print }')
wifissid=${wifissid:1:`expr ${#wifissid} - 2`}  #several commands to get clean name of ssid
if [ $nsel -lt 10 ]; then
    cell=$(echo "Cell 0$nsel - Address:")
else
    cell=$(echo "Cell $nsel - Address:")
fi
nextsel=`expr $nsel + 1`
if [ $nextsel -lt 10 ]; then
    nextcell=$(echo "Cell 0$nextsel - Address:")
else
    nextcell=$(echo "Cell $nextsel - Address:")
fi
awk -v v1="$cell" '$0 ~ v1 {p=1}p' /tmp/wifiscan | awk -v v2="$nextcell" '$0 ~ v2 {exit}1' > /tmp/cellinfo0 #store only the selected cell info in a temp file
grep -v ESSID /tmp/cellinfo0 > /tmp/cellinfo # delete ESSID line to avoid later grep mistakes
rm /tmp/cellinfo0
wifichannel=$(grep " Channel:" /tmp/cellinfo)
wifichannel=$(echo "$wifichannel" | awk '{gsub(" Channel:", "");print}' | awk '{ sub(/^[ \t]+/, ""); print }') #get clean wifi channel
wifimode=$(grep " WEP" /tmp/cellinfo) #check if encryption mode is WEP
if [ -n "$wifimode" ]; then   #check if $wifimode is not an empty string
    wifimode="wep"
else
    wifimode=$(grep "WPA2 " /tmp/cellinfo) #check if encryption mode is WPA2
    if [ -n "$wifimode" ]; then
        wifimode="psk2"
    else
        wifimode=$(grep "WPA " /tmp/cellinfo) #check if encryption mode is WPA
        if [ -n "$wifimode" ]; then
            wifimode="psk"
        else
            wifimode="none"
        fi
    fi
fi
encryp_on=$(grep " Encryption key:on" /tmp/cellinfo)
if [[ "$wifimode" == "none" && -n "$encryp_on" ]]; then
    echo " "
    echo "Impossible to detect wifi security mode automatically."
    echo "Please specify the seurity mode of the network."
    echo " 1: WPA"
    echo " 2: WPA2"
    echo " 3: WEP"
    echo " 4: Undefined"
    echo -n "Enter the numeric option for your security mode: "
    read sel_mode
    case "$sel_mode" in
        1)
            wifimode="psk"
            ;;
        2)
            wifimode="psk2"
            ;;
        3)
            wifimode="wep"
            ;;
        4)
            wifimode="none"
            ;;
    esac
fi
if [ "$wifimode" != "none" ]; then #ask for passwork when needed
    echo -n "Enter password of the selected WIFI network: "
    read wifipass
fi
rm /tmp/cellinfo
rm /tmp/ssids
rm /tmp/sec_ssids
rm /tmp/wifiscan
#write results in the wireless config file and reset wifi interface
uci set wireless.radio0.channel=$wifichannel
uci set wireless.wificlient.ssid="$wifissid"
uci set wireless.wificlient.encryption=$wifimode
uci set wireless.wificlient.key=$wifipass
uci commit wireless
echo -n "

Trying to connect to WIFI network.
(Wait a few seconds and check status with: iwconfig )


"
wifi down
wifi