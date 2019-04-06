#/bin/sh

# ANSI COLORS
CRE="$(echo -e '\r\033[K')"
RED="$(echo -e '\033[1;31m')"
GREEN="$(echo -e '\033[1;32m')"
YELLOW="$(echo -e '\033[1;33m')"
BLUE="$(echo -e '\033[1;34m')"
MAGENTA="$(echo -e '\033[1;35m')"
CYAN="$(echo -e '\033[1;36m')"
WHITE="$(echo -e '\033[1;37m')"
NORMAL="$(echo -e '\033[0;39m')"

red='\e[1;31m'
green='\e[1;32m'
yellow='\e[1;33m'
blue='\e[1;34m'
magenta='\e[1;35m'
cyan='\e[1;36m'
end='\e[0m'

TCE_REPO="http://repo.tinycorelinux.net"
PCP_REPO="http://repo.picoreplayer.org/repo"
#For now use the armv7 repo
TCE_VER="10.x/armv7/tcz"

#This list does not include kernel modules
#TCE_EXT="alsa-utils alsa dialog openssh openssl readline libedit \
#firmware-atheros firmware-ralinkwifi libiw libnl ncurses \
#wireless_tools"

PCP_EXT="pcp pcp-base libasound pcp-libogg pcp-libmpg123 pcp-libfaad2 pcp-libsoxr \
pcp-libmad pcp-libvorbis pcp-libflac pcp-squeezelite firmware-rtlwifi firmware-brcmwifi wiringpi \
wpa_supplicant crda ca-certificates firmware-rpi-wifi alsa-utils alsa dialog openssh openssl readline libedit \
firmware-atheros firmware-ralinkwifi libiw libnl ncurses \
wireless_tools"

archive(){
	echo "${YELLOW}*****************************************************************"
	echo " Archiving current state"
	echo "*****************************************************************"
	echo "${BLUE}"
	
	DATESTAMP=$(date +%m%d%Y%H%M)
	tar -zc --exclude="archive*" -f archive/extentions-${DATESTAMP}.tgz *

	echo " Archive contains"
	echo ""
	tar tvf archive/extentions-${DATESTAMP}.tgz
	echo ""

	echo "${YELLOW}*****************************************************************"
	echo " Done Archiving"
	echo "*****************************************************************"
	echo ""
}

download_extensions() {
	echo "${YELLOW}*****************************************************************"
	echo " Downloading Extensions"
	echo "*****************************************************************"
	echo ""

	#TCE_EXT="readline busybox-httpd"
	#PCP_EXT="pcp-libflac"

	for I in $TCE_EXT; do
		echo "${BLUE}[ INFO ] Checking ${I}"
		for FILE_EXT in $(echo "tcz.dep tcz.md5.txt tcz.info tcz.list tcz"); do
			DL_PATH=`pwd`
			DL_FILE="${DL_PATH}/${I}.${FILE_EXT}"
			if [ ! -e $DL_FILE ]; then
				echo "${BLUE}    [ INFO ] Downloading ${I}.${FILE_EXT}"
				wget ${TCE_REPO}/${TCE_VER}/${I}.${FILE_EXT} -O ${DL_FILE} >/dev/null 2>&1
				if [ $? -ne 0 ]; then
					case ${I}.${FILE_EXT} in
						*.dep) echo "${YELLOW}    ${I}.${FILE_EXT} not found.${YELLOW}";;
						*) echo "${RED}    Error on ${DL_FILE}${YELLOW}";;
					esac
				fi
				chmod 664 $DL_FILE
				[ -s $DL_FILE ] || rm -f $DL_FILE
			fi
		done
		echo -n "${BLUE}    [ INFO ] Checking md5 of ${I}.tcz. "
		md5sum -c --quiet ${I}.tcz.md5.txt
		[ $? -eq 0 ] && echo "${GREEN}OK" || echo "${RED}ERROR"
	done

	for I in $PCP_EXT; do
		echo "${BLUE}[ INFO ] Checking ${I}"
		for FILE_EXT in $(echo "tcz.dep tcz.md5.txt tcz.info tcz.list tcz"); do
			DL_PATH=`pwd`
			DL_FILE="${DL_PATH}/${I}.${FILE_EXT}"
			if [ ! -e $DL_FILE ]; then
				echo "${BLUE}    [ INFO ] Downloading ${I}.${FILE_EXT}"
				wget $PCP_REPO/${TCE_VER}/${I}.${FILE_EXT} -O ${DL_FILE} >/dev/null 2>&1
				if [ $? -ne 0 ]; then
					case ${I}.${FILE_EXT} in
						*.dep) echo "${YELLOW}    ${I}.${FILE_EXT} not found.${YELLOW}";;
						*) echo "${RED}    Error on ${DL_FILE}${YELLOW}";;
					esac
				fi
				chmod 664 $DL_FILE
				[ -s $DL_FILE ] || rm -f $DL_FILE
			fi
		done
		echo -n "${BLUE}    [ INFO ] Checking md5 of ${I}.tcz. "
		md5sum -c --quiet ${I}.tcz.md5.txt
		[ $? -eq 0 ] && echo "${GREEN}OK" || echo "${RED}ERROR"
	done

	echo "${YELLOW}*****************************************************************"
	echo " Done Downloading"
	echo "*****************************************************************"
	echo ""
	
}

function readfile(){
    while read -r line
    do
        if [[ $line =~ ^\ +$ ]] || [ -z $line ] ;then
            nothing=0
        else
			j=1
            EXT="$line"
            while [ $j -ne $TABLEVEL ]; do
                echo -n "  "
                let j=j+1
            done
			echo -n "${BLUE}   $EXT "
			if [[ $line =~ .*KERNEL.* ]]; then
				echo "${GREEN}KERNEL MODULE - OK${NORMAL}"
			elif [ -e $EXT ]; then
					echo "${GREEN}OK${NORMAL}"
			else
				FAIL=1
				echo "${RED}Fail${NORMAL}"
			fi
            let TABLEVEL=TABLEVEL+1
            getdep $EXT
            let TABLEVEL=TABLEVEL-1
        fi
    done < "$1"
}

function getdep(){
    [ -e ${1}.dep ] && readfile ${1}.dep
}

dependancy_check(){
	echo "${YELLOW}*****************************************************************"
	echo " Checking all dependancies"
	echo "*****************************************************************"
	echo ""
	TABLEVEL=0
	FAIL=0
	for I in `ls -1 *.dep|sort -f`; do
		echo "${BLUE}[ INFO ] Checking $I."
		let TABLEVEL=TABLEVEL+1
		readfile $I
		TABLEVEL=0
	done

	echo "${YELLOW}*****************************************************************"
	echo " Done checking dependancies"
	[ $FAIL -ne 0 ] && echo "${RED} There was an ERROR on at least one dependency${YELLOW}"
	echo "*****************************************************************"
	echo ""
}

check_updates(){
	echo "${YELLOW}*****************************************************************"
	echo " Checking for Updates"
	echo "*****************************************************************"
	echo ""
	REPOS=(TCE PCP)
	
	for R in ${REPOS[@]}; do
		eval REPO_ADDR=\${${R}_REPO} 
		eval EXTENSIONS=\${${R}_EXT}
		echo "${BLUE}[ INFO ] Checking files from $R Repo: ${REPO_ADDR}"
		for I in ${EXTENSIONS}; do
			printf "${blue}  [ INFO] Checking: %-25s" "${I}"
			rm -f /tmp/${I}*
			wget ${REPO_ADDR}/${TCE_VER}/${I}.tcz.md5.txt -P /tmp >/dev/null 2>&1
			if [ $? -ne 0 ]; then
				echo "${RED}ERROR downloading ${REPO_ADDR}/${TCE_VER}/${I}.tcz.md5.txt"
			else		
				diff -q ${I}.tcz.md5.txt /tmp/${I}.tcz.md5.txt >/dev/null 2>&1
				if [ $? -ne 0 ]; then
					echo -e "${YELLOW} Different md5 signature found."
					echo "${BLUE}"
					while true; do
						read -p "Do you want to update Extension? (y/n)" yn
						case $yn in
							[Yy]* ) UPDATE=1; break;;
							[Nn]* ) UPDATE=0; break;;
							* ) echo "Please answer yes or no.";;
						esac
					done
					if [ $UPDATE -eq 1 ]; then
						FAIL=0
						for FILE_EXT in $(echo "tcz.dep tcz.info tcz.list tcz"); do
							wget ${REPO_ADDR}/${TCE_VER}/${I}.${FILE_EXT} -P /tmp >/dev/null 2>&1
							if [ $? -ne 0 ]; then
								case ${I}.${FILE_EXT} in
									*.dep) echo "${YELLOW}    ${I}.${FILE_EXT} not found.${YELLOW}";;
									*) FAIL=1; echo "${RED}    Error on ${I}.${FILE_EXT}${YELLOW}";;
								esac
							fi
						done
						if [ $FAIL -eq 0 ]; then
							cd /tmp
							md5sum -c --quiet ${I}.tcz.md5.txt
							[ $? -eq 0 ] && mv -f /tmp/${I}* ${EXTENSION_DIR} || FAIL=1
							cd ${EXTENSION_DIR}
						fi
						if [ $FAIL -ne 0 ]; then
							echo "${RED} Error downloading part of ${I}, extension not updated.{$YELLOW}"
						fi
					fi
					if [ $UPDATE -eq 0 ] || [ $FAIL -ne 0 ]; then  
						rm -f /tmp/${I}*
					fi
				else
					echo -e "${GREEN} Extension version Matches"
				fi
			fi
		done
	done
	echo "${YELLOW}*****************************************************************"
	echo " Done checking for updates"
	echo "*****************************************************************"
	echo ""
}

########################### Main ######################################
cd tcz-for-img
EXTENSION_DIR=$(pwd)

while true; do
	read -p "Do you wish to archive files? (y/n)" yn
	case $yn in
			[Yy]* ) archive; break;;
			[Nn]* ) break;;
			* ) echo "Please answer yes or no.";;
		esac
done
echo ""

while true; do
	read -p "Do you wish to update extensions? (y/n)" yn
	case $yn in
			[Yy]* ) check_updates; break;;
			[Nn]* ) break;;
			* ) echo "Please answer yes or no.";;
		esac
done
echo ""

dependancy_check
