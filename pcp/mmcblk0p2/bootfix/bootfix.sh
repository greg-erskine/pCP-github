#!/bin/sh
# Script run early in do_rebootstuff to fix issues occurring after an insitu update.

# Version: pCP2.05 0.01 2014-06-25 SBP 

. /home/tc/www/cgi-bin/pcp-functions


#Awk program to read bootlocal line by line and add the separator field
#    also removes the extra do_rebootstuff line added by insitu_update.cgi v2.04
#	 Maybe we should just remove that Green color escape sequence from bootlocal.....10 lines of code to rebuild the escape sequence
rebuild_bootlocal() {
	awk '
	function myrebuild(){
		infile="/opt/bootlocal.sh"
		outfile="/tmp/bootlocal.sh"
		while (getline line < infile > 0){
			if ( line ~ /do_rebootstuff/ ){
				if ( line ~ /tee/ ){
					system("echo \47#pCPstart------\47 >> "outfile)
					system("echo \47"line"\47 >> "outfile)
					system("echo \47#pCPstop------\47 >> "outfile)
				}
			}
			else if ( line ~ /GREEN=/ ){
				system("printf GREEN= >>"outfile)
				system("printf \47\42\44\50echo -e \47 >> "outfile)
				system("printf \42\47\42 >>"outfile)
				system("printf \47\134\47 >>"outfile)
				system("printf 033[1 >>"outfile)
				system("printf \47;\47 >>"outfile)
				system("printf 32m >>"outfile)
				system("printf \42\47\51\42 >>"outfile)
				system("printf \47\42\47 >> "outfile)
				system("echo \"\" >>"outfile)
			}
			else{
				system("printf \47"line"\47 >> "outfile)
				system("echo \"\" >>"outfile)
			}
		}
		close(infile)
	}
	BEGIN {myrebuild();}
	'
}

#--------------------------------------------------------------
# Fixes needed in order to update to pCP2.05
# Files that need to be in this folder are
#    bootfix.sh
#    pcp-load
#
mv /mnt/mmcblk0p2/tce/bootfix/pcp-load /usr/local/sbin/
rebuild_bootlocal
rm /opt/bootlocal.sh
mv /tmp/bootlocal.sh /opt/bootlocal.sh
chmod 775 /opt/bootlocal.sh
chown tc:staff /opt/bootlocal.sh

#The follwing will replace lines between #pCPstart and #cPCstop with REPLACEMENT
# We/I need to figure out how to use REPLACEMENT as a variable. It doesn't work yet

#REPLACEMET=${/home/tc/www/cgi-bin/do_rebootstuff.sh | tee -a /var/log/pcp_boot.log}

#sed -i -n '/#pCPstart/{p;:a;N;/#pCPstop/!ba;s/.*\n/REPLACEMENT\n/};p' /opt/bootlocal.sh

#--------------------------------------------------------------

#fixes needed in order to update to pCPversion - add below