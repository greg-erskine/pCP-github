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


TCE_REPO="http://repo.tinycorelinux.net"
PCP_REPO="https://sourceforge.net/projects/picoreplayer/files/repo"

#This list does not include kernel modules
TCE_EXT="alsa-utils alsa busybox-httpd dialog openssh openssl readline libedit \
firmware-atheros firmware-ralinkwifi firmware-rpi3-wireless libiw libnl ncurses wifi wireless_tools wpa_supplicant"

PCP_EXT="libasound pcp-libogg pcp-libmpg123 pcp-libfaad2 pcp-libsoxr pcp-libmad pcp-libvorbis pcp-libflac pcp-squeezelite"

#TCE_EXT="readline busybox-httpd"
#PCP_EXT="pcp-libflac"

for I in $TCE_EXT; do
	echo "${BLUE}[ INFO ] Checking ${I}"
	for FILE_EXT in $(echo "tcz.dep tcz.md5.txt tcz"); do
		DL_PATH=`pwd`
		DL_FILE="${DL_PATH}/${I}.${FILE_EXT}"
		if [ ! -e $DL_FILE ]; then
			echo "${BLUE}    [ INFO ] Downloading ${I}.${FILE_EXT}"
			wget $TCE_REPO/8.x/armv7/tcz/${I}.${FILE_EXT} -O ${DL_FILE} >/dev/null 2>&1
			if [ $? -ne 0 ]; then
				case ${I}.${FILE_EXT} in
					*.dep) echo "${YELLOW}    ${I}.${FILE_EXT} not found.${YELLOW}";;
					*.txt) echo "${RED}    Error on ${DL_FILE}${YELLOW}";;
					*.tcz) echo "${RED}    Error on ${DL_FILE}${YELLOW}";;
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
	for FILE_EXT in $(echo "tcz.dep tcz.md5.txt tcz"); do
		DL_PATH=`pwd`
		DL_FILE="${DL_PATH}/${I}.${FILE_EXT}"
		if [ ! -e $DL_FILE ]; then
			echo "${BLUE}    [ INFO ] Downloading ${I}.${FILE_EXT}"
			wget $PCP_REPO/8.x/armv7/tcz/${I}.${FILE_EXT} -O ${DL_FILE} >/dev/null 2>&1
			if [ $? -ne 0 ]; then
				case ${I}.${FILE_EXT} in
					*.dep) echo "${YELLOW}    ${I}.${FILE_EXT} not found.${YELLOW}";;
					*.txt) echo "${RED}    Error on ${DL_FILE}${YELLOW}";;
					*.tcz) echo "${RED}    Error on ${DL_FILE}${YELLOW}";;
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

echo
echo "${BLUE} [ INFO ] Checking Dependancies."
for I in `ls -1 *.dep`; do
	echo -n "${BLUE}    [ INFO ] Checking $I."
	FAIL=1
	while read -r LINE; do
		case $LINE in
			*.tcz)
				[ -e "$LINE" ] && FAIL=0 || FAIL=1
			;;
		esac
	[ $FAIL -eq 0 ] || echo -n "${RED} ERROR on $LINE."
	done < $I
	[ $FAIL -eq 0 ] && echo "${GREEN} OK." || echo "${RED} ERROR"
done
