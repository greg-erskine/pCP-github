#!/bin/sh

# Version: 0.01 2015-02-15 GE
#	Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

pcp_html_head "xtras_bootcodes" "GE"

pcp_controls
pcp_banner
pcp_xtras
pcp_running_script

pcp_mount_mmcblk0p1_nohtml

echo '<p><b>Note: </b>At the moment this page simply displays the contents of cmdline.txt and cmdline.'
echo '   In the future, it is intended to be able to modify the contents of cmdline.txt.</p>'

USER=""
TZ=""

for i in `cat $CMDLINETXT`; do
	case $i in
		*=*)
			case $i in
				waitusb*) WAITUSB=${i#*=} ;;
				lang*) LANGUAGE=${i#*=} ;;
				kmap*) KEYMAP=${i#*=} ;;
				tz* ) TZ=${i#*=} ;;
				desktop*) DESKTOP=${i#*=} ;;
				ntpserver*) NTPSERVER=${i#*=} ;;
				icons*) ICONS=${i#*=} ;;
				noicons*) NOICONS=${i#*=} ;;
				user*) USER=${i#*=} ;;
				home*) MYHOME=${i#*=} ;;
				tcvd*) TCVD=${i#*=} ;;
				opt*) MYOPT=${i#*=} ;;
				swapfile*) SWAPFILE=${i#*=} ;;
				resume*) RESUME=${i#*=} ;;
				host*) HOST=1 ;;
				nfsmount* ) NFSMOUNT=${i#*=} ;;
				tftplist* ) TFTPLIST=${i#*=} ;;
				httplist* ) HTTPLIST=${i#*=} ;;
				aoe* ) AOE=${i#*=} ;;
				nbd* ) NBD=${i#*=} ;;
				mydata* ) MYDATA=${i#*=} ;;
				pretce* ) PRETCE=${i#*=} ;;
				xvesa* ) XVESA=${i#*=} ;;
				rsyslog=* ) RSYSLOG=${i#*=}; SYSLOG=1 ;;
				blacklist* ) BLACKLIST="$BLACKLIST ${i#*=}" ;;
				iso* ) ISOFILE=${i#*=} ;;
			esac
		;;
		*)
			case $i in
				nozswap) NOZSWAP=1 ;;
				nofstab) NOFSTAB=1 ;;
				nortc) NORTC=1 ;;
				syslog) SYSLOG=1 ;;
				noutc) NOUTC=1 ;;
				nodhcp) NODHCP=1 ;;
				noicons) NOICONS=1 ;;
				text) TEXT=1 ;;
				xonly) XONLY=1 ;;
				superuser) SUPERUSER=1 ;;
				noswap) NOSWAP=1 ;;
				secure) SECURE=1 ;;
				protect) PROTECT=1 ;;
				cron) CRON=1 ;;
				xsetup) XSETUP=1 ;;
				laptop) LAPTOP=1 ;;
				base) ONLYBASE=1 ;;
				showapps) SHOWAPPS=1 ;;
				norestore) NORESTORE=1 ;;
				noautologin) NOAUTOLOGIN=1 ;;
				pause) PAUSE=1 ;;
			esac
		;;
	esac
done

pcp_bootcode_line() {
	pcp_toggle_row_shade
	echo '  <tr class="'$ROWSHADE'">'
	echo '    <td class="column150">'
	echo '      <p>'$1'</p>'
	echo '    </td>'
	echo '    <td class="column300">'
	echo '      <p>'$(echo $2)'</p>'
	echo '    </td>'
	echo '  </tr>'
}

pcp_start_row_shade

echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Possible piCore bootcodes</legend>'
echo '          <table class="bggrey percent100">'

echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="column150">'
echo '                <p>Title 1</p>'
echo '              </td>'
echo '              <td class="column300">'
echo '                <p>Title 2</p>'
echo '              </td>'
echo '            </tr>'

pcp_bootcode_line waitusb $WAITUSB
pcp_bootcode_line lang $LANGUAGE
pcp_bootcode_line kmap $KEYMAP
pcp_bootcode_line tz $TZ
pcp_bootcode_line desktop $DESKTOP
pcp_bootcode_line ntpserver $NTPSERVER
pcp_bootcode_line icons $ICONS
pcp_bootcode_line noicons $NOICONS
pcp_bootcode_line user $USER
pcp_bootcode_line home $MYHOME
pcp_bootcode_line tcvd $TCVD
pcp_bootcode_line opt $MYOPT
pcp_bootcode_line swapfile $SWAPFILE
pcp_bootcode_line resume $RESUME
pcp_bootcode_line host $HOS
pcp_bootcode_line nfsmount $NFSMOUNT
pcp_bootcode_line tftplist $TFTPLIST
pcp_bootcode_line httplist $HTTPLIST
pcp_bootcode_line aoe $AOE
pcp_bootcode_line nbd $NBD
pcp_bootcode_line mydata $MYDATA
pcp_bootcode_line pretce $PRETCE
pcp_bootcode_line xvesa $XVESA
pcp_bootcode_line rsyslog $RSYSLOG
pcp_bootcode_line blacklist $BLACKLIST
pcp_bootcode_line iso $ISOFILE

pcp_bootcode_line nozswap $NOZSWAP
pcp_bootcode_line nofstab $NOFSTAB
pcp_bootcode_line nortc $NORTC
pcp_bootcode_line syslog $SYSLOG
pcp_bootcode_line noutc $NOUTC
pcp_bootcode_line nodhcp $NODHCP
pcp_bootcode_line noicons $NOICONS
pcp_bootcode_line text $TEXT
pcp_bootcode_line xonly $XONLY
pcp_bootcode_line superuser $SUPERUSER
pcp_bootcode_line noswap $NOSWAP
pcp_bootcode_line secure $SECURE
pcp_bootcode_line protect $PROTECT
pcp_bootcode_line cron $CRON
pcp_bootcode_line xsetup $XSETUP
pcp_bootcode_line laptop $LAPTOP
pcp_bootcode_line base $ONLYBASE
pcp_bootcode_line showapps $SHOWAPPS
pcp_bootcode_line norestore $NORESTORE
pcp_bootcode_line noautologin $NOAUTOLOGIN
pcp_bootcode_line pause $PAUSE

echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'

#========================================================================================
# /mnt/mmcblkop1/cmdline.txt
#----------------------------------------------------------------------------------------

pcp_textarea "" "cat $CMDLINETXT" 50

echo '<h1>Bootcodes:</h1>'

cat $CMDLINETXT | awk '
	BEGIN {
		RS=" "
		FS="="
		i = 0
	}
	# main
	{
		bootcode[i]=$0
		i++
	}
	END {
		for (j=0; j<i; j++) {
			printf "%s. %s<br />\n",j+1,bootcode[j]
		}
	} '

pcp_umount_mmcblk0p1

#========================================================================================
# /proc/cmdline
#----------------------------------------------------------------------------------------
pcp_textarea "" "cat /proc/cmdline" 100

echo '<h1>Bootcodes:</h1>'

cat /proc/cmdline | sed 's/  / /g' | awk '
	BEGIN {
		RS=" "
		FS="="
		i = 0
	}
	# main
	{
		bootcode[i]=$0
		i++
	}
	END {
		for (j=0; j<i; j++) {
			printf "%s. %s<br />\n",j+1,bootcode[j]
		}
	} '

#----------------------------------------------------------------------------------------

echo '<br />'

pcp_footer
pcp_copyright

echo '</body>'
echo '</html>'