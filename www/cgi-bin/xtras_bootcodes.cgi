#!/bin/sh

# Version: 3.00 2016-07-28
#	Fixed issue with pcp_bootcode_equal_add. GE.
#	Revised handling of multiple spaces. GE.
#	Added cmdline.txt functions buttons. GE.

# Version: 0.02 2016-06-03
#	Major revision. GE.

# Version: 0.01 2015-02-15
#	Original version. GE.

. pcp-functions
pcp_variables
. $CONFIGCFG

USER=""
TZ=""
REBOOT_REQUIRED="no"

# Define red cross
RED='&nbsp;<span class="indicator_red">&#x2718;</span>'
RED=""
# Define green tick
GREEN='&nbsp;<span class="indicator_green">&#x2714;</span>'

pcp_html_head "xtras_bootcodes" "GE"

pcp_controls
pcp_banner
pcp_xtras
pcp_running_script
pcp_httpd_query_string

#========================================================================================
# Missing bootcodes - add these sometime in the future?
#----------------------------------------------------------------------------------------
# local={hda1|sda1}          Specify PPI directory or loopback file
# vga=7xx                    7xx from table above
# settime                    Set UTC time at boot, internet required
# embed                      Stay on initramfs
# bkg=image.{jpg|png|gif}    Set background from /opt/backgrounds
# multivt                    Allows for multiple virtual terminals
# lst=yyy.lst                Load alternate yyy.lst on boot. yyy.lst is expected to reside
#                            in $DRIVE/tce where $DRIVE is the drive specified by the tce= bootcode.  
# console=ttyAMA0,115200
# console=tty1
#----------------------------------------------------------------------------------------

#========================================================================================
# Routines
#----------------------------------------------------------------------------------------
pcp_backup_cmdlinetxt() {
	cp ${CMDLINETXT} ${CMDLINETXT}.bak
}

pcp_restore_cmdlinetxt() {
	[ -f ${CMDLINETXT}.bak ] && cp ${CMDLINETXT}.bak ${CMDLINETXT}
}

pcp_clean_cmdlinetxt() {
	# Remove carriage return, add a space to end of file, then remove multiple spaces.
	cat $CMDLINETXT | tr -d "\n" > /tmp/cmdline.txt
	cp /tmp/cmdline.txt $CMDLINETXT
	sed -i '$s/$/ /' $CMDLINETXT
	sed -i 's/ \{1,\}/ /g' $CMDLINETXT
}

pcp_bootcode_add() {
	REBOOT_REQUIRED="yes"
	pcp_clean_cmdlinetxt
	sed -i 's/'${1}'[ ]*//g' $CMDLINETXT
	[ $2 -eq 1 ] && sed -i '1 s/^/'${1}' /' $CMDLINETXT
}

pcp_bootcode_equal_add() {
	REBOOT_REQUIRED="yes"
	pcp_clean_cmdlinetxt
	STR="$1=$2"
	sed -i 's/'${VARIABLE}'[=][^ ]* //g' $CMDLINETXT
	[ x"" != x"$2" ] && sed -i '1 s/^/'${STR}' /' $CMDLINETXT
}

#========================================================================================
# Generate warning message
#----------------------------------------------------------------------------------------
pcp_warning_message() {
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Warning</legend>'
	echo '          <table class="bggrey percent100">'
	echo '            <tr class="warning">'
	echo '              <td>'
	echo '                <p style="color:white"><b>Warning:</b> It can be dangerous to play with bootcodes.</p>'
	echo '                <ul>'
	echo '                  <li style="color:white">Only suitable for Advanced users who want to experiment with bootcodes.</li>'
	echo '                  <li style="color:white">Use at your own risk.</li>'
	echo '                  <li style="color:white">Some of the tinycore bootcodes may not work with piCorePlayer.</li>'
	echo '                  <li style="color:white">Only a small subset of bootcodes are available on this page.</li>'
	echo '                  <li style="color:white">Requests for activating additional bootcodes welcome.</li>'
	echo '                  <li style="color:white">A reboot is required to make changed bootcodes active.</li>'
	echo '                </ul>'
	echo '              </td>'
	echo '            </tr>'
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}

#========================================================================================
# Generate html end code
#----------------------------------------------------------------------------------------
pcp_html_end(){
	pcp_footer
	pcp_copyright

	echo '</body>'
	echo '</html>'
}

# Backup cmdline.txt if one does not exist.
pcp_mount_mmcblk0p1_nohtml >/dev/null 2>&1
[ ! -f ${CMDLINETXT}.bak ] && pcp_backup_cmdlinetxt

case "$SUBMIT" in
	Restore) pcp_restore_cmdlinetxt ;;
	Backup) pcp_backup_cmdlinetxt ;;
	Clean) pcp_clean_cmdlinetxt ;;
esac

#========================================================================================
# Process bootcodes in cmdline.txt
#----------------------------------------------------------------------------------------
if [ "$SUBMIT" = "Save" ]; then
	case $VARIABLE in
		#--------------------------------------------------------------------------------
		# Standard Tiny Core bootcodes ( VARIABLE=value )
		#--------------------------------------------------------------------------------
		aoe)         pcp_bootcode_equal_add aoe "$AOE" ;;
		blacklist)   pcp_bootcode_equal_add blacklist "$BLACKLIST" ;;
		desktop)     pcp_bootcode_equal_add desktop "$DESKTOP" ;;
		home)        pcp_bootcode_equal_add home "$MYHOME" ;;
		host)        pcp_bootcode_equal_add host "$MYHOST" ;;
		httplist)    pcp_bootcode_equal_add httplist "$HTTPLIST" ;;
		icons)       pcp_bootcode_equal_add icons "$ICONS" ;;
		iso)         pcp_bootcode_equal_add iso "$ISO" ;;
		kmap)        pcp_bootcode_equal_add kmap "$KMAP" ;;
		lang)        pcp_bootcode_equal_add lang "$MYLANG" ;;
		mydata)      pcp_bootcode_equal_add mydata "$MYDATA" ;;
		nbd)         pcp_bootcode_equal_add nbd "$NBD" ;;
		nfsmount)    pcp_bootcode_equal_add nfsmount "$NFSMOUNT" ;;
		noicons)     pcp_bootcode_equal_add noicons "$NOICONS" ;;
		ntpserver)   pcp_bootcode_equal_add ntpserver "$NTPSERVER" ;;
		opt)         pcp_bootcode_equal_add opt "$MYOPT" ;;
		pretce)      pcp_bootcode_equal_add pretce "$PRETCE" ;;
		restore)     pcp_bootcode_equal_add restore "$RESTORE" ;;
		resume)      pcp_bootcode_equal_add resume "$RESUME" ;;
		rsyslog)     pcp_bootcode_equal_add rsyslog "$RSYSLOG" ;;
		swapfile)    pcp_bootcode_equal_add swapfile "$SWAPFILE" ;;
		tce)         pcp_bootcode_equal_add mytce "$MYTCE" ;;
		tcvd)        pcp_bootcode_equal_add tcvd "$TCVD" ;;
		tftplist)    pcp_bootcode_equal_add tftplist "$TFTPLIST" ;;
		tz)          pcp_bootcode_equal_add tz "$tz" ;;
		user)        pcp_bootcode_equal_add user "$USER" ;;
		waitusb)     pcp_bootcode_equal_add waitusb "$WAITUSB" ;;
		xvesa)       pcp_bootcode_equal_add xvesa "$XVESA";;
		#--------------------------------------------------------------------------------
		# Kernel bootcodes ( VARIABLE=value )
		#--------------------------------------------------------------------------------
		consoleblank)         pcp_bootcode_equal_add consoleblank "$CONSOLEBLANK" ;;
		dwc_otg.fiq_fsm_mask) pcp_bootcode_equal_add iq_fsm_mask "$IQ_FSM_MASK" ;;
		dwc_otg.lpm_enable)   pcp_bootcode_equal_add lpm_enable "$LPM_ENABLE" ;;
		elevator)             pcp_bootcode_equal_add elevator "$ELEVATOR" ;;
		loglevel)             pcp_bootcode_equal_add loglevel "$LOGLEVEL" ;;
		root)                 pcp_bootcode_equal_add root "$ROOT" ;;
		smsc95xx.turbo_mode)  pcp_bootcode_equal_add turbo_mode "$TURBO_MODE" ;;
		#--------------------------------------------------------------------------------
		# Standard Tiny Core bootcodes ( VARIABLE )
		#--------------------------------------------------------------------------------
		base)        pcp_bootcode_add base $ONLYBASE ;;
		cron)        pcp_bootcode_add cron $CRON ;;
		laptop)      pcp_bootcode_add laptop $LAPTOP ;;
		noautologin) pcp_bootcode_add noautologin $NOAUTOLOGIN ;;
		nodhcp)      pcp_bootcode_add nodhcp $NODHCP ;;
		noembed)     pcp_bootcode_add noembed $NOEMBED ;;
		nofstab)     pcp_bootcode_add nofstab $NOFSTAB ;;
		noicons)     pcp_bootcode_add noicons $NOICONS ;;
		norestore)   pcp_bootcode_add norestore $NORESTORE ;;
		nortc)       pcp_bootcode_add nortc $NORTC ;;
		noswap)      pcp_bootcode_add noswap $NOSWAP ;;
		noutc)       pcp_bootcode_add noutc $NOUTC ;;
		nozswap)     pcp_bootcode_add nozswap $NOZSWAP ;;
		pause)       pcp_bootcode_add pause $PAUSE ;;
		protect)     pcp_bootcode_add protect $PROTECT ;;
		safebackup)  pcp_bootcode_add safebackup $SAFEBACKUP ;;
		secure)      pcp_bootcode_add secure $SECURE ;;
		showapps)    pcp_bootcode_add showapps $SHOWAPPS ;;
		superuser)   pcp_bootcode_add superuser $SUPERUSER ;;
		syslog)      pcp_bootcode_add syslog $SYSLOG ;;
		text)        pcp_bootcode_add text $TEXT ;;
		xonly)       pcp_bootcode_add xonly $XONLY ;;
		xsetup)      pcp_bootcode_add xsetup $XSETUP ;;
		#--------------------------------------------------------------------------------
		# Kernel bootcodes ( VARIABLE )
		#--------------------------------------------------------------------------------
		quiet)       pcp_bootcode_add quiet $QUIET ;;
		rootwait)    pcp_bootcode_add rootwait $ROOTWAIT ;;
	esac
fi

for i in `cat $CMDLINETXT`; do
	case $i in
		*=*)
			case $i in
				#---------------------------------------------------
				# Standard Tiny Core bootcodes ( VARIABLE=value )
				#---------------------------------------------------
				aoe*)       AOE=${i#*=} ;;
				blacklist*) BLACKLIST="$BLACKLIST ${i#*=}" ;;
				desktop*)   DESKTOP=${i#*=} ;;
				home*)      MYHOME=${i#*=} ;;
				host*)      MYHOST=${i#*=}; HOST=1 ;;
				httplist*)  HTTPLIST=${i#*=} ;;
				icons*)     ICONS=${i#*=} ;;
				iso*)       ISOFILE=${i#*=} ;;
				kmap*)      KEYMAP=${i#*=} ;;
				lang*)      MYLANG=${i#*=} ;;
				mydata*)    MYDATA=${i#*=} ;;
				nbd*)       NBD=${i#*=} ;;
				nfsmount*)  NFSMOUNT=${i#*=} ;;
				noicons*)   NOICONS=${i#*=} ;;
				ntpserver*) NTPSERVER=${i#*=} ;;
				opt*)       MYOPT=${i#*=} ;;
				pretce*)    PRETCE=${i#*=} ;;
				restore*)   RESTORE=${i#*=} ;;
				resume*)    RESUME=${i#*=} ;;
				rsyslog*)   RSYSLOG=${i#*=}; SYSLOG=1 ;;
				swapfile*)  SWAPFILE=${i#*=} ;;
				tce*)       MYTCE=${i#*=} ;;
				tcvd*)      TCVD=${i#*=} ;;
				tftplist*)  TFTPLIST=${i#*=} ;;
				tz*)        TZ=${i#*=} ;;
				user*)      USER=${i#*=} ;;
				waitusb*)   WAITUSB=${i#*=} ;;
				xvesa*)     XVESA=${i#*=} ;;
				#---------------------------------------------------
				# Kernel bootcodes ( VARIABLE=value )
				#---------------------------------------------------
				consoleblank*)         CONSOLEBLANK=${i#*=} ;;
				dwc_otg.fiq_fsm_mask*) FIQ_FSM_MASK=${i#*=} ;;
				dwc_otg.lpm_enable*)   LPM_ENABLE=${i#*=} ;;
				elevator*)             ELEVATOR=${i#*=} ;;
				loglevel*)             LOGLEVEL=${i#*=} ;;
				root*)                 ROOT=${i#*=} ;;
				smsc95xx.turbo_mode*)  TURBO_MODE=${i#*=} ;;
			esac
		;;
		*)
			case $i in
				#---------------------------------------------------
				# Standard Tiny Core bootcodes ( VARIABLE )
				#---------------------------------------------------
				base)        ONLYBASE=1 ;;
				cron)        CRON=1 ;;
				laptop)      LAPTOP=1 ;;
				noautologin) NOAUTOLOGIN=1 ;;
				nodhcp)      NODHCP=1 ;;
				noembed)     NOEMBED=1 ;;
				nofstab)     NOFSTAB=1 ;;
				noicons)     NOICONS=1 ;;
				norestore)   NORESTORE=1 ;;
				nortc)       NORTC=1 ;;
				noswap)      NOSWAP=1 ;;
				noutc)       NOUTC=1 ;;
				nozswap)     NOZSWAP=1 ;;
				pause)       PAUSE=1 ;;
				protect)     PROTECT=1 ;;
				safebackup)  SAFEBACKUP=1 ;;
				secure)      SECURE=1 ;;
				showapps)    SHOWAPPS=1 ;;
				superuser)   SUPERUSER=1 ;;
				syslog)      SYSLOG=1 ;;
				text)        TEXT=1 ;;
				xonly)       XONLY=1 ;;
				xsetup)      XSETUP=1 ;;
				#---------------------------------------------------
				# Kernel bootcodes ( VARIABLE )
				#---------------------------------------------------
				quiet)       QUIET=1 ;;
				rootwait)    ROOTWAIT=1 ;;
			esac
		;;
	esac
done

pcp_warning_message
[ $MODE -le $MODE_NORMAL ] && pcp_html_end && exit
[ $MODE -lt $MODE_DEVELOPER ] && [ "$REBOOT_REQUIRED" = "yes" ] && pcp_reboot_required

#----------------------------------------------------------------------------------------
# cmdline.txt functions
#----------------------------------------------------------------------------------------
pcp_start_row_shade
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>cmdline.txt functions</legend>'
echo '          <table class="bggrey percent100">'
echo '            <form name="functions" action="'$0'" method="get">'
echo '            <tr class="'$ROWSHADE'">'
echo '              <td class="'$COL1' right">'
echo '                <input type="submit" name="SUBMIT" value="Clean" title="Clean cmdline.txt">'
echo '                <input type="submit" name="SUBMIT" value="Backup" title="Backup cmdline.txt">'
echo '                <input type="submit" name="SUBMIT" value="Restore" title="Restore cmdline.txt">'
echo '              </td>'
echo '            </tr>'
echo '            </form>'
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

COL1="column150"
COL2="column210"
COL3="column150"
COL4="column210"

#----------------------------------------------------------------------------------------
# piCore bootcodes ( VARIABLE=value )
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
echo '              <th class="'$COL1'">'
echo '                <p>Bootcode</p>'
echo '              </th>'
echo '              <th class="'$COL2'">'
echo '                <p>Value</p>'
echo '              </th>'
echo '              <th class="'$COL3'">'
echo '                <p>Save</p>'
echo '              </th>'
echo '              <th class="'$COL4'">'
echo '                <p>Description/Help</p>'
echo '              </th>'
echo '            </tr>'
#----------------------------------------------------------------------------------------

#--------------------------------------aoe-----------------------------------------------
pcp_bootcode_aoe() {
	[ x"" = x"$AOE" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="aoe" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>aoe=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="AOE"'
	echo '                         value="'$AOE'"'
	echo '                         title="No spaces"'
	echo '                         pattern="[^\s]*"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save" title="Save AOE">'
	echo '                  <input type="hidden" name="VARIABLE" value="aoe">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for aoe&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>TODO</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_aoe
#----------------------------------------------------------------------------------------

#--------------------------------------blacklist-----------------------------------------
pcp_bootcode_blacklist() {
	[ x"" = x"$BLACKLIST" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="blacklist" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>blacklist=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="BLACKLIST"'
	echo '                         value="'$BLACKLIST'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
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
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_blacklist
#----------------------------------------------------------------------------------------

#--------------------------------------desktop-------------------------------------------
pcp_bootcode_desktop() {
	[ x"" = x"$DESKTOP" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="desktop" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>desktop=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="DESKTOP"'
	echo '                         value="'$DESKTOP'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="desktop">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify alternate window manager&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;desktop=yyy&gt;</p>'
	echo '                    <p>Specify alternate window manager yyy.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_desktop
#----------------------------------------------------------------------------------------

#--------------------------------------home----------------------------------------------
pcp_bootcode_home() {
	[ x"" = x"$MYHOME" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="home" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>home=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="MYHOME"'
	echo '                         value="'$MYHOME'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="home">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify persistent home directory&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;home=hda1|sda1&gt;</p>'
	echo '                    <p>Specify persistent home directory.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_home
#----------------------------------------------------------------------------------------

#--------------------------------------host----------------------------------------------
pcp_bootcode_host() {
	[ x"" = x"$MYHOST" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="host" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>host=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="MYHOST"'
	echo '                         value="'$MYHOST'"'
	echo '                         readonly'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '                  <input type="hidden" name="VARIABLE" value="host">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set hostname&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;host=xxxx&gt;</p>'
	echo '                    <p>Set hostname to xxxx.</p>'
	echo '                    <p><b>Note:</b> Use [Tweaks] page to set.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_host
#----------------------------------------------------------------------------------------

#--------------------------------------httplist------------------------------------------
pcp_bootcode_httplist() {
	[ x"" = x"$HTTPLIST" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="httplist" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>httplist=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="HTTPLIST"'
	echo '                         value="'$HTTPLIST'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="httplist">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for httplist&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_httplist
#----------------------------------------------------------------------------------------

#--------------------------------------icons---------------------------------------------
pcp_bootcode_icons() {
	[ x"" = x"$ICONS" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="icons" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>icons=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="ICONS"'
	echo '                         value="'$ICONS'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="icons">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for icons&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_icons
#----------------------------------------------------------------------------------------

#--------------------------------------iso-----------------------------------------------
pcp_bootcode_iso() {
	[ x"" = x"$ISOFILE" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="iso" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>iso=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="ISOFILE"'
	echo '                         value="'$ISOFILE'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="iso">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify device to search and boot an iso&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;iso=hda1|sda1&gt;</p>'
	echo '                    <p>Specify device to search and boot an iso.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_iso
#----------------------------------------------------------------------------------------

#--------------------------------------kmap----------------------------------------------
pcp_bootcode_kmap() {
	[ x"" = x"$KEYMAP" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="kmap" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>kmap=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="KEYMAP"'
	echo '                         value="'$KEYMAP'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="kmap">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set the default console keymap&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;kmap=us&gt;</p>'
	echo '                    <p>If you have kmaps.tcz installed, you can use this bootcode to set the default console keymap.</p>'
	echo '                    <p><b>Default:</b> US.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_kmap
#----------------------------------------------------------------------------------------

#--------------------------------------lang----------------------------------------------
pcp_bootcode_lang() {
	[ x"" = x"$MYLANG" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="lang" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>lang=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="MYLANG"'
	echo '                         value="'$MYLANG'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="lang">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Use the preferred locale&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;lang=en&gt;</p>'
	echo '                    <p>You need to generate your preferred locale using the getlocale.tcz extension.</p>'
	echo '                    <p><b>Default:</b> C locale is used (US English, ASCII)</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_lang
#----------------------------------------------------------------------------------------

#--------------------------------------mydata--------------------------------------------
pcp_bootcode_mydata() {
	[ x"" = x"$MYDATA" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="mydata" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>mydata=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="MYDATA"'
	echo '                         value="'$MYDATA'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="mydata">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify alternative name for mydata&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;mydata=configuration&gt;</p>'
	echo '                    <p>Defines an alternative saved configation name.</p>'
	echo '                    <p><b>Default:</b> mydata.tgz</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_mydata
#----------------------------------------------------------------------------------------

#--------------------------------------nbd-----------------------------------------------
pcp_bootcode_nbd() {
	[ x"" = x"$NBD" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="nbd" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>nbd=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="NBD"'
	echo '                         value="'$NBD'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="nbd">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for nbd&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_nbd
#----------------------------------------------------------------------------------------

#--------------------------------------nfsmount------------------------------------------
pcp_bootcode_nfsmount() {
	[ x"" = x"$NFSMOUNT" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="nfsmount" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>nfsmount=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="NFSMOUNT"'
	echo '                         value="'$NFSMOUNT'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="nfsmount">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Define nfsmount&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_nfsmount
#----------------------------------------------------------------------------------------

#--------------------------------------noicons-------------------------------------------
pcp_bootcode_noicons() {
	[ x"" = x"$NOICONS" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="noicons" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>noicons=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="NOICONS"'
	echo '                         value="'$NOICONS'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="noicons">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Do not use icons&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Do not use icons.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_noicons
#----------------------------------------------------------------------------------------

#--------------------------------------ntpserver-----------------------------------------
pcp_bootcode_ntpserver() {
	[ x"" = x"$NTPSERVER" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="ntpserver" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>ntpserver=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="NTPSERVER"'
	echo '                         value="'$NTPSERVER'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="ntpserver">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Define alternative Network Time Protocol (ntp) server&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;ntpserver=xxx.xxx.xxx.xxx&gt; or &lt;ntpserver=FQDN&gt;</p>'
	echo '                    <p><b>Default:</b> pool.ntp.org</p>'
	echo '                    <p><b>Hint:</b> Use "ntpdc -c monlist" on ntp server to confirm bootcode is working.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_ntpserver
#----------------------------------------------------------------------------------------

#--------------------------------------opt-----------------------------------------------
pcp_bootcode_opt() {
	[ x"" = x"$MYOPT" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="opt" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>opt=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="MYOPT"'
	echo '                         value="'$MYOPT'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="opt">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify persistent opt directory&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;opt=hda1|sda1&gt;</p>'
	echo '                    <p>Specify persistent opt directory.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_opt
#----------------------------------------------------------------------------------------

#--------------------------------------pretce--------------------------------------------
pcp_bootcode_pretce() {
	[ x"" = x"$PRETCE" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="pretce" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>pretce=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="PRETCE"'
	echo '                         value="'$PRETCE'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="pretce">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for pretce&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_pretce
#----------------------------------------------------------------------------------------

#--------------------------------------restore-------------------------------------------
pcp_bootcode_restore() {
	[ x"" = x"$RESTORE" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="restore" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>restore=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="RESTORE"'
	echo '                         value="'$RESTORE'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="restore">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify saved configuration location&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;restore={hda1|sda1|floppy}&gt;</p>'
	echo '                    <p>If you wish to store the backup in a separate location (ie. not under the'
	echo '                       tce directory), you need to use the restore bootcode.</p>'
	echo '                    <p></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_restore
#----------------------------------------------------------------------------------------

#--------------------------------------resume--------------------------------------------
pcp_bootcode_resume() {
	[ x"" = x"$RESUME" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="resume" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>resume=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="RESUME"'
	echo '                         value="'$RESUME'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="resume">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for resume&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_resume
#----------------------------------------------------------------------------------------

#--------------------------------------rsyslog-------------------------------------------
pcp_bootcode_rsyslog() {
	[ x"" = x"$RSYSLOG" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="rsyslog" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>rsyslog=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="RSYSLOG"'
	echo '                         value="'$RSYSLOG'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="rsyslog">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for rsyslog&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_rsyslog
#----------------------------------------------------------------------------------------

#--------------------------------------swapfile------------------------------------------
pcp_bootcode_swapfile() {
	[ x"" = x"$SWAPFILE" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="swapfile" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>swapfile=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="SWAPFILE"'
	echo '                         value="'$SWAPFILE'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="swapfile">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify swapfile&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;swapfile=hda1&gt;</p>'
	echo '                    <p>Scan for or Specify swapfile.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_swapfile
#----------------------------------------------------------------------------------------

#--------------------------------------tce-----------------------------------------------
pcp_bootcode_tce() {
	[ x"" = x"$MYTCE" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="tce" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>tce=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="MYTCE"'
	echo '                         value="'$MYTCE'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="tce">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify Restore TCE apps directory&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;tce={hda1|sda1}&gt;</p>'
	echo '                    <p>Specifies where to locate and store the extensions and backup.'
	echo '                       If it’s not given, the system will scan all drives for a first-level directory called /tce.'
	echo '                       Thus it may improve boot time to specify where it is.</p>'
	echo '                    <p><b>Example:</b></p>'
	echo '                    <ul>'
	echo '                      <li>tce=sda1</li>'
	echo '                      <li>tce=sda1/mydir</li>'
	echo '                    <p></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_tce
#----------------------------------------------------------------------------------------

#--------------------------------------tcvd----------------------------------------------
pcp_bootcode_tcvd() {
	[ x"" = x"$TCVD" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="tcvd" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>tcvd=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="TCVD"'
	echo '                         value="'$TCVD'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="tcvd">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Virtual disk support&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Virtual disk support (tcvd, tiny core virtual disk).</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_tcvd
#----------------------------------------------------------------------------------------

#--------------------------------------tftplist------------------------------------------
pcp_bootcode_tftplist() {
	[ x"" = x"$TFTPLIST" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="tftplist" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>tftplist=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="TFTPLIST"'
	echo '                         value="'$TFTPLIST'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="tftplist">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enter value for tftplist&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_tftplist
#----------------------------------------------------------------------------------------

#--------------------------------------tz------------------------------------------------
pcp_bootcode_tz() {
	[ x"" = x"$TZ" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="tz" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>tz=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="TZ"'
	echo '                         value="'$TZ'"'
	echo '                         readonly'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '                  <input type="hidden" name="VARIABLE" value="tz">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify Timezone&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;tz=GMT+8&gt;</p>'
	echo '                    <p>Timezone tz=PST+8PDT,M3.2.0/2,M11.1.0/2</p>'
	echo '                    <p>Timezone is automatically set during the first boot.</p>'
	echo '                    <p><b>Note:</b> Use [Tweaks] page to modify or delete.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_tz
#----------------------------------------------------------------------------------------

#--------------------------------------user----------------------------------------------
pcp_bootcode_user() {
	[ x"" = x"$USER" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="user" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>user=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="USER"'
	echo '                         value="'$USER'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="user">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify alternate user&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;user=xxx&gt;</p>'
	echo '                    <p>Specify alternate user xxx.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_user
#----------------------------------------------------------------------------------------

#--------------------------------------waitusb-------------------------------------------
pcp_bootcode_waitusb() {
	[ x"" = x"$WAITUSB" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="waitusb" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>waitusb=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="number"'
	echo '                         name="WAITUSB"'
	echo '                         value="'$WAITUSB'"'
	echo '                         min="1"'
	echo '                         max="120"'
	echo '                         title="waitsub ( 1 -120 )"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="waitusb">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Wait for USB&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;waitusb=x&gt;</p>'
	echo '                    <p>During boot process, wait x seconds for slow USB devices.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_waitusb
#----------------------------------------------------------------------------------------

#--------------------------------------xvesa---------------------------------------------
pcp_bootcode_xvesa() {
	[ x"" = x"$XVESA" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="xvesa" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>xvesa=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="XVESA"'
	echo '                         value="'$XVESA'"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="xvesa">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set Xvesa default screen resolution&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;xvesa=800x600x32&gt;</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_xvesa
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

COL11="column20"
COL12="column100"
COL13="column150"
COL14="column210"

#----------------------------------------------------------------------------------------
# piCore bootcodes ( VARIABLE )
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
echo '              <th class="column100">'
echo '                <p>Save</p>'
echo '              </th>'
echo '              <th class="column210">'
echo '                <p>Description/Help</p>'
echo '              </th>'
echo '            </tr>'
#----------------------------------------------------------------------------------------

#--------------------------------------base----------------------------------------------
pcp_bootcode_base() {
	if [ $ONLYBASE -eq 1 ]; then ONLYBASEyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="base" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="ONLYBASE" value="1" '$ONLYBASEyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>base&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL13' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="base">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Only load base system&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Skip loading extensions, only load the base system.</p>'
	echo '                    <p><b>Note:</b> Can also be used with norestore bootcode to load a base system with no configuration.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_base
#----------------------------------------------------------------------------------------

#--------------------------------------cron----------------------------------------------
pcp_bootcode_cron() {
	if [ $CRON -eq 1 ]; then CRONyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="cron" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="CRON" value="1" '$CRONyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>cron&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="cron">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Start cron daemon&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Start the cron daemon at boot.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_cron
#----------------------------------------------------------------------------------------

#--------------------------------------laptop--------------------------------------------
pcp_bootcode_laptop() {
	if [ $LAPTOP -eq 1 ]; then LAPTOPyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="laptop" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="LAPTOP" value="1" '$LAPTOPyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>laptop&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="laptop">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Force load laptop related modules&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Force load laptop related modules.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_laptop
#----------------------------------------------------------------------------------------

#--------------------------------------noautologin---------------------------------------
pcp_bootcode_noautologin() {
	if [ $NOAUTOLOGIN -eq 1 ]; then NOAUTOLOGINyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="noautologin" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="NOAUTOLOGIN" value="1" '$NOAUTOLOGINyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>noautologin&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="noautologin">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>No automatic login&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Skip automatic login at boot.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_noautologin
#----------------------------------------------------------------------------------------

#--------------------------------------nodhcp--------------------------------------------
pcp_bootcode_nodhcp() {
	if [ $NODHCP -eq 1 ]; then NODHCPyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="nodhcp" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="NODHCP" value="1" '$NODHCPyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>nodhcp&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="nodhcp">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>No dhcp request&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Skip the dhcp request at boot.</p>'
	echo '                    <p>This is used when a static IP is set.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_nodhcp
#-----------------------------------------------------------------------------------------

#--------------------------------------noembed--------------------------------------------
pcp_bootcode_noembed() {
	if [ $NOEMBED -eq 1 ]; then NOEMBEDyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="noembed" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="NOEMBED" value="1" '$NOEMBEDyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>noembed&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="noembed">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Use a separate tmpfs&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>This is an advanced option that changes where in RAM Core is run from.</p>'
	echo '                    <p><b>Default:</b> Core uses the tmpfs setup by the kernel; with this bootcode, Core will setup a new tmpfs file system, and use that instead.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_noembed
#----------------------------------------------------------------------------------------

#--------------------------------------nofstab-------------------------------------------
pcp_bootcode_nofstab() {
	if [ $NOFSTAB -eq 1 ]; then NOFSTAByes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="nofstab" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="NOFSTAB" value="1" '$NOFSTAByes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>nofstab&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="nofstab">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set nofstab&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_nofstab
#----------------------------------------------------------------------------------------

#--------------------------------------noicons-------------------------------------------
pcp_bootcode_noicons() {
	if [ $NOICONS -eq 1 ]; then NOICONSyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="noicons" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="NOICONS" value="1" '$NOICONSyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>noicons&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="noicons">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Do not use icons&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Do not use icons.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_noicons
#----------------------------------------------------------------------------------------

#--------------------------------------norestore-----------------------------------------
pcp_bootcode_norestore() {
	if [ $NORESTORE -eq 1 ]; then NORESTOREyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="norestore" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="NORESTORE" value="1" '$NORESTOREyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>norestore&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="norestore">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Turn off the restoring the configuration file&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Prevent the loading of the configuration file (mydata.tgz)</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_norestore
#----------------------------------------------------------------------------------------

#--------------------------------------nortc---------------------------------------------
pcp_bootcode_nortc() {
	if [ $NORTC -eq 1 ]; then NORTCyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="nortc" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="NORTC" value="1" '$NORTCyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>nortc&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="nortc">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set no Real Time Clock (nortc)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>The Raspberry Pi does not have a Real Time Clock.</p>'
	echo '                    <p>The time is set during each boot from a ntp server.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_nortc
#----------------------------------------------------------------------------------------

#--------------------------------------noswap--------------------------------------------
pcp_bootcode_noswap() {
	if [ $NOSWAP -eq 1 ]; then NOSWAPyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="noswap" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="NOSWAP" value="1" '$NOSWAPyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>noswap&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="noswap">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Do not use swap partition&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> The system will use all Linux swap partitions automatically.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_noswap
#----------------------------------------------------------------------------------------

#--------------------------------------noutc---------------------------------------------
pcp_bootcode_noutc() {
	if [ $NOUTC -eq 1 ]; then NOUTCyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="noutc" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="NOUTC" value="1" '$NOUTCyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>noutc&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="noutc">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>BIOS is using localtime&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>BIOS is using localtime.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_noutc
#----------------------------------------------------------------------------------------

#--------------------------------------nozswap-------------------------------------------
pcp_bootcode_nozswap() {
	if [ $NOZSWAP -eq 1 ]; then NOZSWAPyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="nozswap" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="NOZSWAP" value="1" '$NOZSWAPyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>nozswap&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="nozswap">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Disable compressed swap in RAM&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Default:</b> Core uses a RAM compression technique allowing you to use more RAM than you actually have.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_nozswap
#----------------------------------------------------------------------------------------

#--------------------------------------pause---------------------------------------------
pcp_bootcode_pause() {
	if [ $PAUSE -eq 1 ]; then PAUSEyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="pause" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="PAUSE" value="1" '$PAUSEyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>pause&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="pause">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Wait for a keypress before completing boot&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>By waiting for an enter key press before completing the boot, this bootcode lets you view the system boot messages more easily.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_pause
#----------------------------------------------------------------------------------------

#--------------------------------------protect-------------------------------------------
pcp_bootcode_protect() {
	if [ $PROTECT -eq 1 ]; then PROTECTyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="protect" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="PROTECT" value="1" '$PROTECTyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>protect&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="protect">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Use password encrypted backup&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>For added security, use a password encrypted backup.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_protect
#----------------------------------------------------------------------------------------

#--------------------------------------safebackup----------------------------------------
pcp_bootcode_safebackup() {
	if [ $SAFEBACKUP -eq 1 ]; then SAFEBACKUPyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="safebackup" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="SAFEBACKUP" value="1" '$SAFEBACKUPyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>safebackup&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="safebackup">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Enable safe backup (mydatabk.tgz)&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>A copy of your previous backup is made before doing a new backup (mydatabk.tgz).</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_safebackup
#----------------------------------------------------------------------------------------

#--------------------------------------secure--------------------------------------------
pcp_bootcode_secure() {
	if [ $SECURE -eq 1 ]; then SECUREyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="secure" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="SECURE" value="1" '$SECUREyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>secure&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="secure">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set password on boot&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>If you need to set the password on boot, for example on a first run.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_secure
#----------------------------------------------------------------------------------------

#--------------------------------------showapps------------------------------------------
pcp_bootcode_showapps() {
	if [ $SHOWAPPS -eq 1 ]; then SHOWAPPSyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="showapps" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="SHOWAPPS" value="1" '$SHOWAPPSyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>showapps&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="showapps">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Display application names when booting&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Show each extension by name when loading it.'
	echo '                       It slightly delays the boot, but it’s useful to find which extension has trouble loading.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_showapps
#----------------------------------------------------------------------------------------

#--------------------------------------superuser-----------------------------------------
pcp_bootcode_superuser() {
	if [ $SUPERUSER -eq 1 ]; then SUPERUSERyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="superuser" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="SUPERUSER" value="1" '$SUPERUSERyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>superuser&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="superuser">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Textmode as user root&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Textmode as user root.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_superuser
#----------------------------------------------------------------------------------------

#--------------------------------------syslog--------------------------------------------
pcp_bootcode_syslog() {
	if [ $SYSLOG -eq 1 ]; then SYSLOGyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="syslog" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="SYSLOG" value="1" '$SYSLOGyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>syslog&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="syslog">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Start syslog daemon&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Start syslog daemon at boot.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_syslog
#----------------------------------------------------------------------------------------

#--------------------------------------text----------------------------------------------
pcp_bootcode_text() {
	if [ $TEXT -eq 1 ]; then TEXTyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="text" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="TEXT" value="1" '$TEXTyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>text&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="text">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Boot to text mode&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>In case an X server is installed, do not boot to graphical mode.'
	echo '                       If an X server is not installed, the system will always boot to text mode.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_text
#----------------------------------------------------------------------------------------

#--------------------------------------xonly---------------------------------------------
pcp_bootcode_xonly() {
	if [ $XONLY -eq 1 ]; then XONLYyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="xonly" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="XONLY" value="1" '$XONLYyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>xonly&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="xonly">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set xonly&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p></p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_xonly
#----------------------------------------------------------------------------------------

#--------------------------------------xsetup--------------------------------------------
pcp_bootcode_xsetup() {
	if [ $XSETUP -eq 1 ]; then XSETUPyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="xsetup" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="XSETUP" value="1" '$XSETUPyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>xsetup&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="xsetup">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set xsetup&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>...</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_xsetup
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
# Kernel bootcodes ( VARIABLE=value )
#----------------------------------------------------------------------------------------
pcp_start_row_shade
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Kernel bootcodes ( VARIABLE=value )</legend>'
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

#--------------------------------------consoleblank--------------------------------------
pcp_bootcode_consoleblank() {
	[ x"" = x"$CONSOLEBLANK" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="consoleblank" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>consoleblank=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="CONSOLEBLANK"'
	echo '                         value="'$CONSOLEBLANK'"'
	echo '                         readonly'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '                  <input type="hidden" name="VARIABLE" value="consoleblank">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Display consoleblank&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Note:</b> Use [Tweaks] page to set.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_consoleblank
#----------------------------------------------------------------------------------------

#--------------------------------------dwc_otg.fiq_fsm_mask------------------------------
pcp_bootcode_fiq_fsm_mask() {
	[ x"" = x"$FIQ_FSM_MASK" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="fiq_fsm_mask" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>dwc_otg.fiq_fsm_mask=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="FIQ_FSM_MASK"'
	echo '                         value="'$FIQ_FSM_MASK'"'
	echo '                         readonly'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '                  <input type="hidden" name="VARIABLE" value="fiq_fsm_mask">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Display dwc_otg.fiq_fsm_mask&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Note:</b> Use [Tweaks] page to set.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_fiq_fsm_mask
#----------------------------------------------------------------------------------------

#--------------------------------------dwc_otg.lpm_enable--------------------------------
pcp_bootcode_lpm_enable() {
	[ x"" = x"$LPM_ENABLE" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="lpm_enable" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>dwc_otg.lpm_enable=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="LPM_ENABLE"'
	echo '                         value="'$LPM_ENABLE'"'
	echo '                         readonly'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '                  <input type="hidden" name="VARIABLE" value="lpm_enable">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Display dwc_otg.lpm_enable&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Note:</b> Use [Tweaks] page to set.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_lpm_enable
#----------------------------------------------------------------------------------------

#--------------------------------------elevator------------------------------------------
pcp_bootcode_elevator() {
	[ x"" = x"$ELEVATOR" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="elevator" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>elevator=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="ELEVATOR"'
	echo '                         value="'$ELEVATOR'"'
	echo '                         readonly'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '                  <input type="hidden" name="VARIABLE" value="elevator">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Display elevator&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;elevator=cfq|deadline|noop&gt;</p>'
	echo '                    <p>See https://www.kernel.org/doc/Documentation/block/deadline-iosched.txt and'
	echo '                       https://www.kernel.org/doc/Documentation/block/deadline-iosched.txt for details.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_elevator
#----------------------------------------------------------------------------------------

#--------------------------------------loglevel------------------------------------------
pcp_bootcode_loglevel() {
	[ x"" = x"$LOGLEVEL" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="loglevel" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>loglevel=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="number"'
	echo '                         name="LOGLEVEL"'
	echo '                         value="'$LOGLEVEL'"'
	echo '                         min="0"'
	echo '                         max="7"'
	echo '                         title="logelevel ( 0 - 7 )"'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="loglevel">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Set the default console log level&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;loglevel=x&gt;</p>'
	echo '                    <p>Specify the initial console log level:</p>'
	echo '                    <p>Specify the initial console log level:</p>'
	echo '                    <ul>'
	echo '                      <li>0 (KERN_EMERG) The system is unusable.</li>'
	echo '                      <li>1 (KERN_ALERT) Actions that must be taken care of immediately.</li>'
	echo '                      <li>2 (KERN_CRIT) Critical conditions.</li>'
	echo '                      <li>3 (KERN_ERR) Noncritical error conditions.</li>'
	echo '                      <li>4 (KERN_WARNING) Warning conditions that should be taken care of.</li>'
	echo '                      <li>5 (KERN_NOTICE) Normal, but significant events.</li>'
	echo '                      <li>6 (KERN_INFO) Informational messages that require no action.</li>'
	echo '                      <li>7 (KERN_DEBUG) Kernel debugging messages, output by the kernel
                                    if the developer enabled debugging at compile time.</li>'
	echo '                    </ul>'
	echo '                    <p><b>Default:</b> 3</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_loglevel
#----------------------------------------------------------------------------------------

#--------------------------------------root----------------------------------------------
pcp_bootcode_root() {
	[ x"" = x"$ROOT" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="root" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>root=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="ROOT"'
	echo '                         value="'$ROOT'"'
	echo '                         readonly'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '                  <input type="hidden" name="VARIABLE" value="root">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Specify the root filesystem to boot from&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>&lt;root=device&gt;</p>'
	echo '                    <p>Tell the kernel which disk device the root filesystem image is on.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_root
#----------------------------------------------------------------------------------------

#--------------------------------------smsc95xx.turbo_mode-------------------------------
pcp_bootcode_turbo_mode() {
	[ x"" = x"$TURBO_MODE" ] && INDICATOR=$RED || INDICATOR=$GREEN
	echo '            <form name="turbo_mode" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL1' right">'
	echo '                  <p>smsc95xx.turbo_mode=</p>'
	echo '                </td>'
	echo '                <td class="'$COL2'">'
	echo '                  <input class="large15"'
	echo '                         type="text"'
	echo '                         name="TURBO_MODE"'
	echo '                         value="'$TURBO_MODE'"'
	echo '                         readonly'
	echo '                  >'$INDICATOR
	echo '                </td>'
	echo '                <td class="'$COL3' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '                  <input type="hidden" name="VARIABLE" value="turbo_mode">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Display smsc95xx.turbo_mode&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p><b>Note:</b> Use [Tweaks] page to set.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_turbo_mode
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
# Kernel bootcodes ( VARIABLE )
#----------------------------------------------------------------------------------------
pcp_start_row_shade
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Kernel bootcodes ( VARIABLE )</legend>'
echo '          <table class="bggrey percent100">'
#--------------------------------------Heading-------------------------------------------
echo '            <tr class="'$ROWSHADE'">'
echo '              <th class="column150">'
echo '                <p>Bootcode</p>'
echo '              </th>'
echo '              <th class="column100">'
echo '                <p>Save</p>'
echo '              </th>'
echo '              <th class="column210">'
echo '                <p>Description/Help</p>'
echo '              </th>'
echo '            </tr>'
#----------------------------------------------------------------------------------------

#--------------------------------------quiet---------------------------------------------
pcp_bootcode_quiet() {
	if [ $QUIET -eq 1 ]; then QUIETyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="quiet" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="QUIET" value="1" '$QUIETyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>quiet&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL13' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="quiet">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Disable all log messages&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Set the default kernel log level to KERN_WARNING (4),
                                 which suppresses all messages during boot except extremely serious ones.</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_quiet
#----------------------------------------------------------------------------------------

#--------------------------------------rootwait------------------------------------------
pcp_bootcode_rootwait() {
	if [ $ROOTWAIT -eq 1 ]; then ROOTWAITyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	echo '            <form name="rootwait" action="'$0'" method="get">'
	pcp_incr_id
	pcp_toggle_row_shade
	echo '              <tr class="'$ROWSHADE'">'
	echo '                <td class="'$COL11'">'
	echo '                  <input class="small1" type="checkbox" name="ROOTWAIT" value="1" '$ROOTWAITyes'>'
	echo '                </td>'
	echo '                <td class="'$COL12'">'
	echo '                  <p>rootwait&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '                </td>'
	echo '                <td class="'$COL13' center">'
	echo '                  <input type="submit" name="SUBMIT" value="Save">'
	echo '                  <input type="hidden" name="VARIABLE" value="rootwait">'
	echo '                </td>'
	echo '                <td>'
	echo '                  <p>Wait for root device&nbsp;&nbsp;'
	echo '                    <a id="'$ID'a" class="moreless" href=# onclick="return more('\'''$ID''\'')">more></a>'
	echo '                  </p>'
	echo '                  <div id="'$ID'" class="less">'
	echo '                    <p>Wait (indefinitely) for root device to show up.'
	echo '                       Useful for devices that are detected asynchronously (e.g. USB and MMC devices)</p>'
	echo '                  </div>'
	echo '                </td>'
	echo '              </tr>'
	echo '            </form>'
}
[ $MODE -ge $MODE_ADVANCED ] && pcp_bootcode_rootwait
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
pcp_start_row_shade
echo '<table class="bggrey">'
echo '  <tr>'
echo '    <td>'
echo '      <div class="row">'
echo '        <fieldset>'
echo '          <legend>Current: '$CMDLINETXT'</legend>'
echo '          <table class="bggrey percent100">'
#----------------------------------------------------------------------------------------

pcp_textarea_inform "" "cat $CMDLINETXT" 60

echo '<h1>[ INFO ] Bootcodes:</h1>'
echo '<textarea class="inform" style="height:250px">'

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
			printf "%s. %s\n",j+1,bootcode[j]
		}
	} '

echo '</textarea>'

pcp_umount_mmcblk0p1_nohtml >/dev/null 2>&1

#----------------------------------------------------------------------------------------
echo '          </table>'
echo '        </fieldset>'
echo '      </div>'
echo '    </td>'
echo '  </tr>'
echo '</table>'
#----------------------------------------------------------------------------------------

#========================================================================================
# /proc/cmdline
#----------------------------------------------------------------------------------------
pcp_proc_cmdline() {
	pcp_start_row_shade
	echo '<table class="bggrey">'
	echo '  <tr>'
	echo '    <td>'
	echo '      <div class="row">'
	echo '        <fieldset>'
	echo '          <legend>Current: /proc/cmdline</legend>'
	echo '          <table class="bggrey percent100">'
	#------------------------------------------------------------------------------------

	pcp_textarea_inform "" "cat /proc/cmdline" 100

	echo '<h1>[ INFO ] Bootcodes:</h1>'
	echo '<textarea class="inform" style="height:280px">'

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
				printf "%s. %s\n",j+1,bootcode[j]
			}
		} '

	echo '</textarea>'

	#------------------------------------------------------------------------------------
	echo '          </table>'
	echo '        </fieldset>'
	echo '      </div>'
	echo '    </td>'
	echo '  </tr>'
	echo '</table>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_proc_cmdline
#----------------------------------------------------------------------------------------

pcp_html_end
