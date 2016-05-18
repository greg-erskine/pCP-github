#!/bin/sh

# Version: 0.02 2016-05-17 GE
#	Major revision.

# Version: 0.01 2015-02-15 GE
#	Original version.

. pcp-functions
pcp_variables
. $CONFIGCFG

USER=""
TZ=""
CMDLINETXT=/mnt/mmcblk0p1/xxxcmdline.txt
DEBUG=1

pcp_html_head "xtras_bootcodes" "GE"

pcp_controls
pcp_banner
pcp_xtras
pcp_running_script
pcp_httpd_query_string

pcp_mount_mmcblk0p1

echo '<p><b>Note: </b>At the moment this page simply displays the contents of cmdline.txt and cmdline.'
echo '   In the future, it is intended to be able to modify the contents of cmdline.txt.</p>'

pcp_bootcode_add() {
	sed -i 's/'${1}'[ ]*//g' $CMDLINETXT
	[ $2 -eq 1 ] && sed -i '1 s/^/'${1}' /' $CMDLINETXT
}

pcp_bootcode_equal_add() {
	STR="$1=$2"
	sed -i 's/'${VARIABLE}'[\=a-zA-Z0-9]* //g' $CMDLINETXT
	[ x"" != x"$2" ] && sed -i '1 s/^/'${STR}' /' $CMDLINETXT
}

if [ "$SUBMIT" = "Save" ]; then
	case $VARIABLE in
		#--------------------------------------------------------------------------------
		# Standard Tiny Core bootcodes ( VARIABLE=value )
		#--------------------------------------------------------------------------------
		aoe)         pcp_bootcode_equal_add aoe "$AOE" ;;
		blacklist)   pcp_bootcode_equal_add blacklist "$BLACKLIST" ;;
		desktop)     pcp_bootcode_equal_add desktop "$DESKTOP" ;;
		home)        pcp_bootcode_equal_add home "$MYHOME" ;;
		host)        pcp_bootcode_equal_add host "$HOSTNAME" ;;
		httplist)    pcp_bootcode_equal_add httplist "$HTTPLIST" ;;
		icons)       pcp_bootcode_equal_add icons "$ICONS" ;;
		iso)         pcp_bootcode_equal_add iso "$ISO" ;;
		kmap)        pcp_bootcode_equal_add kmap "$KMAP" ;;
		lang)        pcp_bootcode_equal_add lang "$LANGUAGE" ;;
		mydata)      pcp_bootcode_equal_add mydata "$MYDATA" ;;
		nbd)         pcp_bootcode_equal_add nbd "$NBD" ;;
		nfsmount)    pcp_bootcode_equal_add nfsmount "$NFSMOUNT" ;;
		noicons)     pcp_bootcode_equal_add noicons "$NOICONS" ;;
		ntpserver)   pcp_bootcode_equal_add ntpserver "$NTPSERVER" ;;
		opt)         pcp_bootcode_equal_add opt "$MYOPT" ;;
		pretce)      pcp_bootcode_equal_add pretce "$PRETCE" ;;
		resume)      pcp_bootcode_equal_add resume "$RESUME" ;;
		rsyslog)     pcp_bootcode_equal_add rsyslog "$RSYSLOG" ;;
		swapfile)    pcp_bootcode_equal_add swapfile "$SWAPFILE" ;;
		tcvd)        pcp_bootcode_equal_add tcvd "$TCVD" ;;
		tftplist)    pcp_bootcode_equal_add tftplist "$TFTPLIST" ;;
		tz)          pcp_bootcode_equal_add tz "$tz" ;;
		user)        pcp_bootcode_equal_add user "$USER" ;;
		waitusb)     pcp_bootcode_equal_add waitusb "$WAITUSB" ;;
		xvesa)       pcp_bootcode_equal_add xvesa "$XVESA";;
		#--------------------------------------------------------------------------------
		# Standard Tiny Core bootcodes ( VARIABLE )
		#--------------------------------------------------------------------------------
		base)        pcp_bootcode_add base $BASE ;;
		cron)        pcp_bootcode_add cron $CRON ;;
		laptop)      pcp_bootcode_add laptop $LAPTOP ;;
		noautologin) pcp_bootcode_add noautologin $NOAUTOLOGIN ;;
		nodhcp)      pcp_bootcode_add nodhcp $NODHCP ;;
		nofstab)     pcp_bootcode_add nofstab $NOFSTAB ;;
		noicons)     pcp_bootcode_add noicons $NOICONS ;;
		norestore)   pcp_bootcode_add norestore $NORESTORE ;;
		nortc)       pcp_bootcode_add nortc $NORTC ;;
		noswap)      pcp_bootcode_add noswap $NOSWAP ;;
		noutc)       pcp_bootcode_add noutc $NOUTC ;;
		nozswap)     pcp_bootcode_add nozswap $NOZSWAP ;;
		pause)       pcp_bootcode_add pause $PAUSE ;;
		protect)     pcp_bootcode_add protect $PROTECT ;;
		secure)      pcp_bootcode_add secure $SECURE ;;
		showapps)    pcp_bootcode_add showapps $SHOWAPPS ;;
		superuser)   pcp_bootcode_add superuser $SUPERUSER ;;
		syslog)      pcp_bootcode_add syslog $SYSLOG ;;
		text)        pcp_bootcode_add text $TEXT ;;
		xonly)       pcp_bootcode_add xonly $XONLY ;;
		xsetup)      pcp_bootcode_add xsetup $XSETUP ;;
		#--------------------------------------------------------------------------------
		#
		#--------------------------------------------------------------------------------
	esac
fi

for i in `cat $CMDLINETXT`; do
	case $i in
		*=*)
			case $i in
				#---------------------------------------------------
				# Standard Tiny Core bootcodes
				#---------------------------------------------------
				aoe*) AOE=${i#*=} ;;
				blacklist*) BLACKLIST="$BLACKLIST ${i#*=}" ;;
				desktop*) DESKTOP=${i#*=} ;;
				home*) MYHOME=${i#*=} ;;
				host*) HOST=1; HOSTNAME=${i#*=} ;;
				httplist*) HTTPLIST=${i#*=} ;;
				icons*) ICONS=${i#*=} ;;
				iso*) ISOFILE=${i#*=} ;;
				kmap*) KEYMAP=${i#*=} ;;
				lang*) LANGUAGE=${i#*=} ;;
				mydata*) MYDATA=${i#*=} ;;
				nbd*) NBD=${i#*=} ;;
				nfsmount*) NFSMOUNT=${i#*=} ;;
				noicons*) NOICONS=${i#*=} ;;
				ntpserver*) NTPSERVER=${i#*=} ;;
				opt*) MYOPT=${i#*=} ;;
				pretce*) PRETCE=${i#*=} ;;
				resume*) RESUME=${i#*=} ;;
				rsyslog=*) RSYSLOG=${i#*=}; SYSLOG=1 ;;
				swapfile*) SWAPFILE=${i#*=} ;;
				tcvd*) TCVD=${i#*=} ;;
				tftplist*) TFTPLIST=${i#*=} ;;
				tz*) TZ=${i#*=} ;;
				user*) USER=${i#*=} ;;
				waitusb*) WAITUSB=${i#*=} ;;
				xvesa*) XVESA=${i#*=} ;;
				#---------------------------------------------------
			esac
		;;
		*)
			case $i in
				#---------------------------------------------------
				# Standard Tiny Core bootcodes
				#---------------------------------------------------
				base) ONLYBASE=1 ;;
				cron) CRON=1 ;;
				laptop) LAPTOP=1 ;;
				noautologin) NOAUTOLOGIN=1 ;;
				nodhcp) NODHCP=1 ;;
				nofstab) NOFSTAB=1 ;;
				noicons) NOICONS=1 ;;
				norestore) NORESTORE=1 ;;
				nortc) NORTC=1 ;;
				noswap) NOSWAP=1 ;;
				noutc) NOUTC=1 ;;
				nozswap) NOZSWAP=1 ;;
				pause) PAUSE=1 ;;
				protect) PROTECT=1 ;;
				secure) SECURE=1 ;;
				showapps) SHOWAPPS=1 ;;
				superuser) SUPERUSER=1 ;;
				syslog) SYSLOG=1 ;;
				text) TEXT=1 ;;
				xonly) XONLY=1 ;;
				xsetup) XSETUP=1 ;;
				#---------------------------------------------------
			esac
		;;
	esac
done

#----------------------------------------------------------------------------------------
pcp_start_row_shade
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>piCore bootcodes ( VARIABLE=value )</legend>'
echo '          <table class="bggrey percent100">'
#--------------------------------------Heading-------------------------------------------
echo '            <tr class="'$ROWSHADE'">'
echo '              <th class="column150">'
echo '                <p>Bootcode</p>'
echo '              </th>'
echo '              <th class="column210">'
echo '                <p>Value</p>'
echo '              </th>'
echo '              <th class="column150">'
echo '                <p>Save</p>'
echo '              </th>'
echo '              <th>'
echo '                <p>Description/Help</p>'
echo '              </th>'
echo '            </tr>'
#----------------------------------------------------------------------------------------

#--------------------------------------aoe-----------------------------------------
pcp_bootcode_aoe() {
	echo '            <form name="aoe" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>aoe</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="AOE" value="'$AOE'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="aoe">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for aoe&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_aoe
#----------------------------------------------------------------------------------------

#--------------------------------------blacklist-----------------------------------------
pcp_bootcode_blacklist() {
	echo '            <form name="blacklist" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>blacklist</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="BLACKLIST" value="'$BLACKLIST'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="blacklist">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Blacklist module&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;blacklist=ssb&gt;</p>'
	echo '                    <p>Blacklist a single module.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_blacklist
#----------------------------------------------------------------------------------------

#--------------------------------------desktop----------------------------------------------
pcp_bootcode_desktop() {
	echo '            <form name="desktop" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>desktop</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="DESKTOP" value="'$DESKTOP'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="desktop">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for desktop&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_desktop
#----------------------------------------------------------------------------------------

#--------------------------------------home-----------------------------------------
pcp_bootcode_home() {
	echo '            <form name="home" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>home</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="MYHOME" value="'$MYHOME'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="home">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for home&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_home
#----------------------------------------------------------------------------------------

#--------------------------------------host-----------------------------------------
pcp_bootcode_host() {
	echo '            <form name="host" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>host</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="HOSTNAME" value="'$HOSTNAME'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="host">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for host&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_host
#----------------------------------------------------------------------------------------

#--------------------------------------httplist-----------------------------------------
pcp_bootcode_httplist() {
	echo '            <form name="httplist" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>httplist</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="HTTPLIST" value="'$HTTPLIST'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="httplist">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for httplist&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_httplist
#----------------------------------------------------------------------------------------

#--------------------------------------icons-----------------------------------------
pcp_bootcode_icons() {
	echo '            <form name="icons" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>icons</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="ICONS" value="'$ICONS'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="icons">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for icons&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_icons
#----------------------------------------------------------------------------------------

#--------------------------------------iso-----------------------------------------
pcp_bootcode_iso() {
	echo '            <form name="iso" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>iso</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="ISOFILE" value="'$ISOFILE'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="iso">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for iso&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_iso
#----------------------------------------------------------------------------------------

#--------------------------------------kmap----------------------------------------------
pcp_bootcode_kmap() {
	echo '            <form name="kmap" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>kmap</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="KEYMAP" value="'$KEYMAP'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="kmap">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for kmap&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_kmap
#----------------------------------------------------------------------------------------

#--------------------------------------lang----------------------------------------------
pcp_bootcode_lang() {
	echo '            <form name="lang" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>lang</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="LANGUAGE" value="'$LANGUAGE'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="lang">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for lang&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_lang
#----------------------------------------------------------------------------------------

#--------------------------------------mydata-----------------------------------------
pcp_bootcode_mydata() {
	echo '            <form name="mydata" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>mydata</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="MYDATA" value="'$MYDATA'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="mydata">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for mydata&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_mydata
#----------------------------------------------------------------------------------------

#--------------------------------------nbd-----------------------------------------
pcp_bootcode_nbd() {
	echo '            <form name="nbd" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>nbd</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="NBD" value="'$NBD'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="nbd">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for nbd&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_nbd
#----------------------------------------------------------------------------------------

#--------------------------------------nfsmount-----------------------------------------
pcp_bootcode_nfsmount() {
	echo '            <form name="nfsmount" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>nfsmount</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="NFSMOUNT" value="'$NFSMOUNT'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="nfsmount">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for nfsmount&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_nfsmount
#----------------------------------------------------------------------------------------

#--------------------------------------noicons-----------------------------------------
pcp_bootcode_noicons() {
	echo '            <form name="noicons" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>noicons</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="NOICONS" value="'$NOICONS'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="noicons">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for noicons&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_noicons
#----------------------------------------------------------------------------------------

#--------------------------------------ntpserver-----------------------------------------
pcp_bootcode_ntpserver() {
	echo '            <form name="ntpserver" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>ntpserver</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="NTPSERVER" value="'$NTPSERVER'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="ntpserver">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for ntpserver&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_ntpserver
#----------------------------------------------------------------------------------------

#--------------------------------------opt-----------------------------------------
pcp_bootcode_opt() {
	echo '            <form name="opt" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>opt</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="MYOPT" value="'$MYOPT'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="opt">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for opt&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_opt
#----------------------------------------------------------------------------------------

#--------------------------------------pretce-----------------------------------------
pcp_bootcode_pretce() {
	echo '            <form name="pretce" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>pretce</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="PRETCE" value="'$PRETCE'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="pretce">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for pretce&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_pretce
#----------------------------------------------------------------------------------------

#--------------------------------------resume-----------------------------------------
pcp_bootcode_resume() {
	echo '            <form name="resume" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>resume</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="RESUME" value="'$RESUME'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="resume">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for resume&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_resume
#----------------------------------------------------------------------------------------

#--------------------------------------rsyslog-----------------------------------------
pcp_bootcode_rsyslog() {
	echo '            <form name="rsyslog" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>rsyslog</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="RSYSLOG" value="'$RSYSLOG'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="rsyslog">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for rsyslog&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_rsyslog
#----------------------------------------------------------------------------------------

#--------------------------------------swapfile-----------------------------------------
pcp_bootcode_swapfile() {
	echo '            <form name="swapfile" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>swapfile</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="SWAPFILE" value="'$SWAPFILE'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="swapfile">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for swapfile&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_swapfile
#----------------------------------------------------------------------------------------

#--------------------------------------tcvd-----------------------------------------
pcp_bootcode_tcvd() {
	echo '            <form name="tcvd" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>tcvd</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="TCVD" value="'$TCVD'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="tcvd">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for tcvd&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_tcvd
#----------------------------------------------------------------------------------------

#--------------------------------------tftplist-----------------------------------------
pcp_bootcode_tftplist() {
	echo '            <form name="tftplist" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>tftplist</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="TFTPLIST" value="'$TFTPLIST'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="tftplist">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for tftplist&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_tftplist
#----------------------------------------------------------------------------------------

#--------------------------------------tz----------------------------------------------
pcp_bootcode_tz() {
	echo '            <form name="tz" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>tz</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="TZ" value="'$TZ'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="tz">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for tz&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_tz
#----------------------------------------------------------------------------------------

#--------------------------------------user-----------------------------------------
pcp_bootcode_user() {
	echo '            <form name="user" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>user</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="USER" value="'$USER'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="user">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for user&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_user
#----------------------------------------------------------------------------------------

#--------------------------------------waitusb-------------------------------------------
pcp_bootcode_waitusb() {
	echo '            <form name="waitusb" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>waitusb</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="WAITUSB" value="'$WAITUSB'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="waitusb">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Wait for USB&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;waitusb=X&gt;</p>'
	echo '                    <p>Wait X seconds for slow USB devices.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_waitusb
#----------------------------------------------------------------------------------------

#--------------------------------------xvesa-----------------------------------------
pcp_bootcode_xvesa() {
	echo '            <form name="xvesa" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>xvesa</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="large15" type="text" name="XVESA" value="'$XVESA'">'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="xvesa">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for xvesa&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_xvesa
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
pcp_start_row_shade
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>piCore bootcodes ( VARIABLE )</legend>'
echo '          <table class="bggrey percent100">'
#--------------------------------------Heading-------------------------------------------
echo '            <tr class="'$ROWSHADE'">'
echo '              <th class="column150">'
echo '                <p>Bootcode</p>'
echo '              </th>'
echo '              <th class="column210">'
echo '                <p>Set</p>'
echo '              </th>'
echo '              <th class="column150">'
echo '                <p>Save</p>'
echo '              </th>'
echo '              <th>'
echo '                <p>Description/Help</p>'
echo '              </th>'
echo '            </tr>'
#----------------------------------------------------------------------------------------

#--------------------------------------base-------------------------------------------
pcp_bootcode_base() {
	[ $ONLYBASE -eq 1 ] && ONLYBASEyes="checked" || ONLYBASEno="checked"

	echo '            <form name="base" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>base</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="ONLYBASE" value="1" '$ONLYBASEyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="ONLYBASE" value="0" '$ONLYBASEno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="base">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set base&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_base
#----------------------------------------------------------------------------------------

#--------------------------------------cron-------------------------------------------
pcp_bootcode_cron() {
	[ $CRON -eq 1 ] && CRONyes="checked" || CRONno="checked"

	echo '            <form name="cron" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>cron</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="CRON" value="1" '$CRONyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="CRON" value="0" '$CRONno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="cron">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set cron&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_cron
#----------------------------------------------------------------------------------------

#--------------------------------------laptop-------------------------------------------
pcp_bootcode_laptop() {
	[ $LAPTOP -eq 1 ] && LAPTOPyes="checked" || LAPTOPno="checked"

	echo '            <form name="laptop" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>laptop</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="LAPTOP" value="1" '$LAPTOPyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="LAPTOP" value="0" '$LAPTOPno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="laptop">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set laptop&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_laptop
#----------------------------------------------------------------------------------------

#--------------------------------------noautologin-------------------------------------------
pcp_bootcode_noautologin() {
	[ $NOAUTOLOGIN -eq 1 ] && NOAUTOLOGINyes="checked" || NOAUTOLOGINno="checked"

	echo '            <form name="noautologin" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>noautologin</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="NOAUTOLOGIN" value="1" '$NOAUTOLOGINyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="NOAUTOLOGIN" value="0" '$NOAUTOLOGINno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="noautologin">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set noautologin&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_noautologin
#----------------------------------------------------------------------------------------

#--------------------------------------nodhcp-------------------------------------------
pcp_bootcode_nodhcp() {
	[ $NODHCP -eq 1 ] && NODHCPyes="checked" || NODHCPno="checked"

	echo '            <form name="nodhcp" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>nodhcp</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="NODHCP" value="1" '$NODHCPyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="NODHCP" value="0" '$NODHCPno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="nodhcp">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set nodhcp&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_nodhcp
#----------------------------------------------------------------------------------------

#--------------------------------------nofstab-------------------------------------------
pcp_bootcode_nofstab() {
	[ $NOFSTAB -eq 1 ] && NOFSTAByes="checked" || NOFSTABno="checked"

	echo '            <form name="nofstab" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>nofstab</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="NOFSTAB" value="1" '$NOFSTAByes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="NOFSTAB" value="0" '$NOFSTABno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="nofstab">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set nofstab&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_nofstab
#----------------------------------------------------------------------------------------

#--------------------------------------noicons-------------------------------------------
pcp_bootcode_noicons() {
	[ $NOICONS -eq 1 ] && NOICONSyes="checked" || NOICONSno="checked"

	echo '            <form name="noicons" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>noicons</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="NOICONS" value="1" '$NOICONSyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="NOICONS" value="0" '$NOICONSno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="noicons">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set noicons&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_noicons
#----------------------------------------------------------------------------------------

#--------------------------------------norestore-------------------------------------------
pcp_bootcode_norestore() {
	[ $NORESTORE -eq 1 ] && NORESTOREyes="checked" || NORESTOREno="checked"

	echo '            <form name="norestore" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>norestore</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="NORESTORE" value="1" '$NORESTOREyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="NORESTORE" value="0" '$NORESTOREno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="norestore">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set norestore&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_norestore
#----------------------------------------------------------------------------------------

#--------------------------------------nortc-------------------------------------------
pcp_bootcode_nortc() {
	[ $NORTC -eq 1 ] && NORTCyes="checked" || NORTCno="checked"

	echo '            <form name="nortc" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>nortc</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="NORTC" value="1" '$NORTCyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="NORTC" value="0" '$NORTCno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="nortc">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set nortc&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_nortc
#----------------------------------------------------------------------------------------

#--------------------------------------noswap-------------------------------------------
pcp_bootcode_noswap() {
	[ $NOSWAP -eq 1 ] && NOSWAPyes="checked" || NOSWAPno="checked"

	echo '            <form name="noswap" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>noswap</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="NOSWAP" value="1" '$NOSWAPyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="NOSWAP" value="0" '$NOSWAPno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="noswap">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set noswap&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_noswap
#----------------------------------------------------------------------------------------

#--------------------------------------noutc-------------------------------------------
pcp_bootcode_noutc() {
	[ $NOUTC -eq 1 ] && NOUTCyes="checked" || NOUTCno="checked"

	echo '            <form name="noutc" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>noutc</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="NOUTC" value="1" '$NOUTCyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="NOUTC" value="0" '$NOUTCno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="noutc">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set noutc&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_noutc
#----------------------------------------------------------------------------------------

#--------------------------------------nozswap-------------------------------------------
pcp_bootcode_nozswap() {
	[ $NOZSWAP -eq 1 ] && NOZSWAPyes="checked" || NOZSWAPno="checked"

	echo '            <form name="nozswap" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>nozswap</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="NOZSWAP" value="1" '$NOZSWAPyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="NOZSWAP" value="0" '$NOZSWAPno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="nozswap">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set nozswap&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_nozswap
#----------------------------------------------------------------------------------------

#--------------------------------------pause-------------------------------------------
pcp_bootcode_pause() {
	[ $PAUSE -eq 1 ] && PAUSEyes="checked" || PAUSEno="checked"

	echo '            <form name="pause" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>pause</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="PAUSE" value="1" '$PAUSEyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="PAUSE" value="0" '$PAUSEno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="pause">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set pause&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_pause
#----------------------------------------------------------------------------------------

#--------------------------------------protect-------------------------------------------
pcp_bootcode_protect() {
	[ $PROTECT -eq 1 ] && PROTECTyes="checked" || PROTECTno="checked"

	echo '            <form name="protect" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>protect</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="PROTECT" value="1" '$PROTECTyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="PROTECT" value="0" '$PROTECTno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="protect">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set protect&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_protect
#----------------------------------------------------------------------------------------

#--------------------------------------secure-------------------------------------------
pcp_bootcode_secure() {
	[ $SECURE -eq 1 ] && SECUREyes="checked" || SECUREno="checked"

	echo '            <form name="secure" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>secure</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="SECURE" value="1" '$SECUREyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="SECURE" value="0" '$SECUREno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="secure">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set secure&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_secure
#----------------------------------------------------------------------------------------

#--------------------------------------showapps-------------------------------------------
pcp_bootcode_showapps() {
	[ $SHOWAPPS -eq 1 ] && SHOWAPPSyes="checked" || SHOWAPPSno="checked"

	echo '            <form name="showapps" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>showapps</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="SHOWAPPS" value="1" '$SHOWAPPSyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="SHOWAPPS" value="0" '$SHOWAPPSno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="showapps">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set showapps&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_showapps
#----------------------------------------------------------------------------------------

#--------------------------------------superuser-------------------------------------------
pcp_bootcode_superuser() {
	[ $SUPERUSER -eq 1 ] && SUPERUSERyes="checked" || SUPERUSERno="checked"

	echo '            <form name="superuser" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>superuser</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="SUPERUSER" value="1" '$SUPERUSERyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="SUPERUSER" value="0" '$SUPERUSERno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="superuser">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set superuser&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_superuser
#----------------------------------------------------------------------------------------

#--------------------------------------syslog-------------------------------------------
pcp_bootcode_syslog() {
	[ $SYSLOG -eq 1 ] && SYSLOGyes="checked" || SYSLOGno="checked"

	echo '            <form name="syslog" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>syslog</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="SYSLOG" value="1" '$SYSLOGyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="SYSLOG" value="0" '$SYSLOGno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="syslog">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set syslog&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_syslog
#----------------------------------------------------------------------------------------

#--------------------------------------text-------------------------------------------
pcp_bootcode_text() {
	[ $TEXT -eq 1 ] && TEXTyes="checked" || TEXTno="checked"

	echo '            <form name="text" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>text</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="TEXT" value="1" '$TEXTyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="TEXT" value="0" '$TEXTno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="text">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set text&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_text
#----------------------------------------------------------------------------------------

#--------------------------------------xonly-------------------------------------------
pcp_bootcode_xonly() {
	[ $XONLY -eq 1 ] && XONLYyes="checked" || XONLYno="checked"

	echo '            <form name="xonly" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>xonly</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="XONLY" value="1" '$XONLYyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="XONLY" value="0" '$XONLYno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="xonly">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set xonly&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_xonly
#----------------------------------------------------------------------------------------

#--------------------------------------xsetup-------------------------------------------
pcp_bootcode_xsetup() {
	[ $XSETUP -eq 1 ] && XSETUPyes="checked" || XSETUPno="checked"

	echo '            <form name="xsetup" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="column150">'
	echo '                  <p>xsetup</p>'
	echo '                </td>'
	echo '                <td class="column210">'
	echo '                  <input class="small1" type="radio" name="XSETUP" value="1" '$XSETUPyes'>Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	echo '                  <input class="small1" type="radio" name="XSETUP" value="0" '$XSETUPno'>No'
	echo '                </td>'
	echo '                <td class="column150 center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="xsetup">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set xsetup&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> </p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_xsetup
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
# $CMDLINETXT - /mnt/mmcblkop1/cmdline.txt
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