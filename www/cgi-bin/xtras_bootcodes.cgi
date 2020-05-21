#!/bin/sh

# Version: 7.0.0 2020-05-21
# Title: Bootcodes
# Description: Set/adjust bootcodes in cmdline.txt

. pcp-functions

USER=""
TZ=""

#========================================================================================
# Define green tick and red cross
#----------------------------------------------------------------------------------------
RED='&nbsp;<span class="indicator_red">&#x2718;</span>'
RED=""
GREEN='&nbsp;<span class="indicator_green">&#x2714;</span>'

pcp_html_head "xtras_bootcodes" "GE"

pcp_controls
pcp_xtras
pcp_httpd_query_string

#========================================================================================
# Missing bootcodes - add these sometime in the future?
#----------------------------------------------------------------------------------------
# local={hda1|sda1}          Specify directory or loopback file
# settime                    Set UTC time at boot, internet required
# embed                      Stay on initramfs
# bkg=image.{jpg|png|gif}    Set background from /opt/backgrounds
# multivt                    Allows for multiple virtual terminals
# lst=yyy.lst                Load alternate yyy.lst on boot. yyy.lst is expected to reside
#                            in $DRIVE/tce where $DRIVE is the drive specified by the tce=bootcode.
#----------------------------------------------------------------------------------------

#========================================================================================
# Generate warning message
#----------------------------------------------------------------------------------------
pcp_warning_message() {
	echo '  <div class="'$BORDER'">'
	echo '    <div class="row">'
	echo '      <div class="col-12 mx-1">'
	echo '        <p><b>Warning:</b> It can be dangerous to play with bootcodes.</p>'
	echo '        <ul>'
	echo '          <li>Use at your own risk.</li>'
	echo '          <li>Some of the Tiny Core Linux bootcodes may not work with piCorePlayer.</li>'
	echo '          <li>Only a small subset of bootcodes are available on this page.</li>'
	echo '          <li>Requests for activating additional bootcodes welcome.</li>'
	echo '          <li>A reboot is required to make changed bootcodes active.</li>'
	echo '        </ul>'
	echo '      </div>'
	echo '    </div>'
	echo '  </div>'
}

#========================================================================================
# Generate html end code
#----------------------------------------------------------------------------------------
# Backup cmdline.txt if one does not exist. Use ssh to restore.
pcp_mount_bootpart >/dev/null 2>&1
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
		iso)         pcp_bootcode_equal_add iso "$ISOFILE" ;;
		kmap)        pcp_bootcode_equal_add kmap "$KEYMAP" ;;
		lang)        pcp_bootcode_equal_add lang "$MYLANG" ;;
		mydata)      pcp_bootcode_equal_add mydata "$MYDATA" ;;
		nbd)         pcp_bootcode_equal_add nbd "$NBD" ;;
		nfsmount)    pcp_bootcode_equal_add nfsmount "$NFSMOUNT" ;;
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
		tz)          pcp_bootcode_equal_add tz "$tz" ;; #<==GE $TZ ??
		user)        pcp_bootcode_equal_add user "$USER" ;;
		waitusb)     pcp_bootcode_equal_add waitusb "$WAITUSB" ;;
		xvesa)       pcp_bootcode_equal_add xvesa "$XVESA";;
		#--------------------------------------------------------------------------------
		# Kernel bootcodes ( VARIABLE=value )
		#--------------------------------------------------------------------------------
		console)              pcp_bootcode_equal_add2 console "$CONSOLE" ;;
		consoleblank)         pcp_bootcode_equal_add consoleblank "$CONSOLEBLANK" ;;
		dwc_otg.fiq_fsm_mask) pcp_bootcode_equal_add iq_fsm_mask "$IQ_FSM_MASK" ;;
		dwc_otg.lpm_enable)   pcp_bootcode_equal_add lpm_enable "$LPM_ENABLE" ;;
		elevator)             pcp_bootcode_equal_add elevator "$ELEVATOR" ;;
		fbcon)                pcp_bootcode_equal_add2 fbcon "$FBCON" ;;
		isolcpus)             pcp_bootcode_equal_add isolcpus "$ISOLCPUS" ;;
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
		logo.nologo) pcp_bootcode_add logo.nologo $NOLOGO ;;
		quiet)       pcp_bootcode_add quiet $QUIET ;;
		rootwait)    pcp_bootcode_add rootwait $ROOTWAIT ;;
	esac
fi

BLACKLIST=""
CONSOLE=""
FBCON=""

for i in $(cat $CMDLINETXT); do
	case $i in
		*=*)
			case $i in
				#---------------------------------------------------
				# Standard Tiny Core bootcodes
				# ( VARIABLE=value ) or ( VARIABLE=value value)
				#---------------------------------------------------
				aoe*)       AOE=${i#*=} ;;
				blacklist*) BLACKLIST="$BLACKLIST ${i#*=}" ;;
				desktop*)   DESKTOP=${i#*=} ;;
				home*)      MYHOME=${i#*=} ;;
				host*)      MYHOST=${i#*=}; HOST=1 ;;
				httplist*)  HTTPLIST=${i#*=} ;;
				icons*)     ICONS=${i#*=} ;;
				iso=*)      ISOFILE=${i#*=} ;;
				kmap*)      KEYMAP=${i#*=} ;;
				lang*)      MYLANG=${i#*=} ;;
				mydata*)    MYDATA=${i#*=} ;;
				nbd*)       NBD=${i#*=} ;;
				nfsmount*)  NFSMOUNT=${i#*=} ;;
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
				# Kernel bootcodes
				# ( VARIABLE=value ) or ( VARIABLE=value value)
				#---------------------------------------------------
				console=*)             CONSOLE="$CONSOLE ${i#*=}" ;;
				consoleblank*)         CONSOLEBLANK=${i#*=} ;;
				dwc_otg.fiq_fsm_mask*) FIQ_FSM_MASK=${i#*=} ;;
				dwc_otg.lpm_enable*)   LPM_ENABLE=${i#*=} ;;
				elevator*)             ELEVATOR=${i#*=} ;;
				fbcon*)                FBCON="$FBCON ${i#*=}" ;;
				isolcpus*)             ISOLCPUS=${i#*=} ;;
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
				logo.nologo) NOLOGO=1 ;;
				quiet)       QUIET=1 ;;
				rootwait)    ROOTWAIT=1 ;;
			esac
		;;
	esac
done

pcp_warning_message
[ $MODE -lt $MODE_DEVELOPER ] && [ "$REBOOT_REQUIRED" ] && pcp_reboot_required

#----------------------------------------------------------------------------------------
# cmdline.txt functions
#----------------------------------------------------------------------------------------
pcp_incr_id
echo '  <div class="'$BORDER'">'
pcp_heading5 "cmdline.txt functions"

echo '    <form name="functions" action="'$0'" method="get">'
echo '      <div class="row mx-1">'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Clean" title="Clean cmdline.txt">'
echo '        </div>'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Backup" title="Backup cmdline.txt">'
echo '        </div>'
echo '        <div class="col-2">'
echo '          <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Restore" title="Restore cmdline.txt">'
echo '        </div>'
echo '        <div class="col-6">'
echo '          <p>&nbsp;&nbsp;'
echo '            <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
echo '          </p>'
echo '          <div id="dt'$ID'" class="'$COLLAPSE'">'
echo '            <ul>'
echo '              <li><b>Clean</b> - remove stray spaces from cmdline.txt.</li>'
echo '              <li><b>Backup</b> - make a backup of cmdline.txt.</li>'
echo '              <li><b>Restore</b> - restore cmdline.txt from backup.</li>'
echo '            </ul>'
echo '          </div>'
echo '        </div>'
echo '      </div>'
echo '    </form>'
echo '  </div>'
#----------------------------------------------------------------------------------------

COLUMN4_1="col-sm-1 text-sm-right"
COLUMN4_2="col-sm-3"
COLUMN4_3="col-sm-2"
COLUMN4_4="col-sm-6"
#----------------------------------------------------------------------------------------
# piCore bootcodes ( VARIABLE=value )
#----------------------------------------------------------------------------------------
echo '  <div class="'$BORDER'">'
pcp_heading5 "piCore bootcodes ( VARIABLE=value )"
#--------------------------------------Headings------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN4_1'">'
echo '        <pclass="text-bold">Bootcode</p>'
echo '      </div>'
echo '      <div class="'$COLUMN4_2'">'
echo '        <p>Value</p>'
echo '      </div>'
echo '      <div class="'$COLUMN4_3'">'
echo '        <p>Save</p>'
echo '      </div>'
echo '      <div class="'$COLUMN4_4'">'
echo '        <p>Description/Help</p>'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------

#--------------------------------------aoe-----------------------------------------------
pcp_bootcode_aoe() {
	[ x"" = x"$AOE" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>aoe=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="aoe" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="AOE"'
	echo '                 value="'$AOE'"'
	echo '                 pattern="[^\s]*"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="aoe">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="aoe" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Enter value for aoe&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_aoe
#----------------------------------------------------------------------------------------

#--------------------------------------blacklist-----------------------------------------
pcp_bootcode_blacklist() {
	[ x"" = x"$BLACKLIST" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>blacklist=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="blacklist" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="BLACKLIST"'
	echo '                 value="'$BLACKLIST'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="blacklist">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="blacklist" type="submit" name="SUBMIT" value="Save" disabled>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Blacklist module&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;blacklist=ssb&gt;</p>'
	echo '          <p>Blacklist a single module.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_blacklist
#----------------------------------------------------------------------------------------

#--------------------------------------desktop-------------------------------------------
pcp_bootcode_desktop() {
	[ x"" = x"$DESKTOP" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>desktop=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="desktop" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="DESKTOP"'
	echo '                 value="'$DESKTOP'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="desktop">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="desktop" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Specify alternate window manager&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;desktop=yyy&gt;</p>'
	echo '          <p>Specify alternate window manager yyy.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_desktop
#----------------------------------------------------------------------------------------

#--------------------------------------home----------------------------------------------
pcp_bootcode_home() {
	[ x"" = x"$MYHOME" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>home=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="home" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="MYHOME"'
	echo '                 value="'$MYHOME'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="home">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="home" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Specify persistent home directory&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;home=hda1|sda1&gt;</p>'
	echo '          <p>Specify persistent home directory.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_home
#----------------------------------------------------------------------------------------

#--------------------------------------host----------------------------------------------
pcp_bootcode_host() {
	[ x"" = x"$MYHOST" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>host=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="host" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="MYHOST"'
	echo '                 value="'$MYHOST'"'
	echo '                 readonly'
	echo '          >'
	echo '          <input class="'$BUTTON'" form="host" type="hidden" name="VARIABLE" value="host">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set hostname&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;host='$COLUMN4_4'&gt;</p>'
	echo '          <p>Set hostname to '$COLUMN4_4'.</p>'
	echo '          <p><b>Note:</b> Use [Tweaks] page to set.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_host
#----------------------------------------------------------------------------------------

#--------------------------------------httplist------------------------------------------
pcp_bootcode_httplist() {
	[ x"" = x"$HTTPLIST" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>httplist=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="httplist" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="HTTPLIST"'
	echo '                 value="'$HTTPLIST'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="httplist">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="httplist" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Enter value for httplist&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_httplist
#----------------------------------------------------------------------------------------

#--------------------------------------icons---------------------------------------------
pcp_bootcode_icons() {
	[ x"" = x"$ICONS" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>icons=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="icons" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="ICONS"'
	echo '                 value="'$ICONS'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="icons">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="icons" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Enter value for icons&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_icons
#----------------------------------------------------------------------------------------

#--------------------------------------iso-----------------------------------------------
pcp_bootcode_iso() {
	[ x"" = x"$ISOFILE" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>iso=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="iso" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="ISOFILE"'
	echo '                 value="'$ISOFILE'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="iso">'
	echo '       </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="iso" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Specify device to search and boot an iso&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;iso=hda1|sda1&gt;</p>'
	echo '          <p>Specify device to search and boot an iso.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_iso
#----------------------------------------------------------------------------------------

#--------------------------------------kmap----------------------------------------------
pcp_bootcode_kmap() {
	[ x"" = x"$KEYMAP" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>kmap=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="kmap" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="KEYMAP"'
	echo '                 value="'$KEYMAP'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="kmap">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="kmap" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set the default console keymap&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;kmap=us&gt;</p>'
	echo '          <p>If you have kmaps.tcz installed, you can use this bootcode to set the default console keymap.</p>'
	echo '          <p><b>Default:</b> US.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_kmap
#----------------------------------------------------------------------------------------

#--------------------------------------lang----------------------------------------------
pcp_bootcode_lang() {
	[ x"" = x"$MYLANG" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>lang=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="lang" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="MYLANG"'
	echo '                 value="'$MYLANG'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="lang">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="lang" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Use the preferred locale&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;lang=en&gt;</p>'
	echo '          <p>You need to generate your preferred locale using the getlocale.tcz extension.</p>'
	echo '          <p><b>Default:</b> C locale is used (US English, ASCII)</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_lang
#----------------------------------------------------------------------------------------

#--------------------------------------mydata--------------------------------------------
pcp_bootcode_mydata() {
	[ x"" = x"$MYDATA" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>mydata=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="mydata" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="MYDATA"'
	echo '                 value="'$MYDATA'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="mydata">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="mydata" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Specify alternative name for mydata&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;mydata=configuration&gt;</p>'
	echo '          <p>Defines an alternative saved configation name.</p>'
	echo '          <p><b>Default:</b> mydata.tgz</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_mydata
#----------------------------------------------------------------------------------------

#--------------------------------------nbd-----------------------------------------------
pcp_bootcode_nbd() {
	[ x"" = x"$NBD" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>nbd=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="nbd" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="NBD"'
	echo '                 value="'$NBD'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="nbd">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="nbd" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Enter value for nbd&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_nbd
#----------------------------------------------------------------------------------------

#--------------------------------------nfsmount------------------------------------------
pcp_bootcode_nfsmount() {
	[ x"" = x"$NFSMOUNT" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>nfsmount=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="nfsmount" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="NFSMOUNT"'
	echo '                 value="'$NFSMOUNT'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="nfsmount">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="nfsmount" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Define nfsmount&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_nfsmount
#----------------------------------------------------------------------------------------

#--------------------------------------ntpserver-----------------------------------------
pcp_bootcode_ntpserver() {
	[ x"" = x"$NTPSERVER" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>ntpserver=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="ntpserver" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="NTPSERVER"'
	echo '                 value="'$NTPSERVER'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="ntpserver">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="ntpserver" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Define alternative Network Time Protocol (ntp) server&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;ntpserver=xxx.xxx.xxx.xxx&gt; or &lt;ntpserver=FQDN&gt;</p>'
	echo '          <p><b>Default:</b> pool.ntp.org</p>'
	echo '          <p><b>Hint:</b> Use "ntpdc -c monlist" on ntp server to confirm bootcode is working.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_SERVER ] && pcp_bootcode_ntpserver
#----------------------------------------------------------------------------------------

#--------------------------------------opt-----------------------------------------------
pcp_bootcode_opt() {
	[ x"" = x"$MYOPT" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>opt=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="opt" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="MYOPT"'
	echo '                 value="'$MYOPT'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="opt">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="opt" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Specify persistent opt directory&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;opt=hda1|sda1&gt;</p>'
	echo '          <p>Specify persistent opt directory.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_opt
#----------------------------------------------------------------------------------------

#--------------------------------------pretce--------------------------------------------
pcp_bootcode_pretce() {
	[ x"" = x"$PRETCE" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>pretce=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="pretce" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="PRETCE"'
	echo '                 value="'$PRETCE'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="pretce">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="pretce" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Enter value for pretce&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_pretce
#----------------------------------------------------------------------------------------

#--------------------------------------restore-------------------------------------------
pcp_bootcode_restore() {
	[ x"" = x"$RESTORE" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>restore=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="restore" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="RESTORE"'
	echo '                 value="'$RESTORE'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="restore">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="restore" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Specify saved configuration location&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;restore={hda1|sda1|floppy}&gt;</p>'
	echo '          <p>If you wish to store the backup in a separate location (ie. not under the'
	echo '             tce directory), you need to use the restore bootcode.</p>'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_restore
#----------------------------------------------------------------------------------------

#--------------------------------------resume--------------------------------------------
pcp_bootcode_resume() {
	[ x"" = x"$RESUME" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>resume=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="resume" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="RESUME"'
	echo '                 value="'$RESUME'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="resume">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="resume" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Enter value for resume&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_resume
#----------------------------------------------------------------------------------------

#--------------------------------------rsyslog-------------------------------------------
pcp_bootcode_rsyslog() {
	[ x"" = x"$RSYSLOG" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>rsyslog=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="rsyslog" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="RSYSLOG"'
	echo '                 value="'$RSYSLOG'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="rsyslog">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="rsyslog" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Enter value for rsyslog&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_rsyslog
#----------------------------------------------------------------------------------------

#--------------------------------------swapfile------------------------------------------
pcp_bootcode_swapfile() {
	[ x"" = x"$SWAPFILE" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>swapfile=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="swapfile" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="SWAPFILE"'
	echo '                 value="'$SWAPFILE'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="swapfile">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="swapfile" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Specify swapfile&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;swapfile=hda1&gt;</p>'
	echo '          <p>Scan for or Specify swapfile.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_swapfile
#----------------------------------------------------------------------------------------

#--------------------------------------tce-----------------------------------------------
pcp_bootcode_tce() {
	[ x"" = x"$MYTCE" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>tce=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="tce" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="MYTCE"'
	echo '                 value="'$MYTCE'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="tce">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="tce" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Specify Restore TCE apps directory&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;tce={hda1|sda1}&gt;</p>'
	echo '          <p>Specifies where to locate and store the extensions and backup.'
	echo '             If it’s not given, the system will scan all drives for a first-level directory called /tce.'
	echo '             Thus it may improve boot time to specify where it is.</p>'
	echo '          <p><b>Example:</b></p>'
	echo '          <ul>'
	echo '            <li>tce=sda1</li>'
	echo '            <li>tce=sda1/mydir</li>'
	echo '          </ul>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_tce
#----------------------------------------------------------------------------------------

#--------------------------------------tcvd----------------------------------------------
pcp_bootcode_tcvd() {
	[ x"" = x"$TCVD" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>tcvd=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="tcvd" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="TCVD"'
	echo '                 value="'$TCVD'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="tcvd">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="tcvd" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Virtual disk support&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Virtual disk support (tcvd, tiny core virtual disk).</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_tcvd
#----------------------------------------------------------------------------------------

#--------------------------------------tftplist------------------------------------------
pcp_bootcode_tftplist() {
	[ x"" = x"$TFTPLIST" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>tftplist=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="tftplist" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="TFTPLIST"'
	echo '                 value="'$TFTPLIST'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="tftplist">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="tftplist" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Enter value for tftplist&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_tftplist
#----------------------------------------------------------------------------------------

#--------------------------------------tz------------------------------------------------
pcp_bootcode_tz() {
	[ x"" = x"$TZ" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>tz=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="tz" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="TZ"'
	echo '                 value="'$TZ'"'
	echo '                 readonly'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="tz">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="tz" type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Specify Timezone&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;tz=GMT+8&gt;</p>'
	echo '          <p>Timezone tz=PST+8PDT,M3.2.0/2,M11.1.0/2</p>'
	echo '          <p>Timezone is automatically set during the first boot.</p>'
	echo '          <p><b>Note:</b> Use [Tweaks] page to modify or delete.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_tz
#----------------------------------------------------------------------------------------

#--------------------------------------user----------------------------------------------
pcp_bootcode_user() {
	[ x"" = x"$USER" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>user=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="user" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="USER"'
	echo '                 value="'$USER'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="user">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="user" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Specify alternate user&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;user=xxx&gt;</p>'
	echo '          <p>Specify alternate user xxx.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_user
#----------------------------------------------------------------------------------------

#--------------------------------------waitusb-------------------------------------------
pcp_bootcode_waitusb() {
	[ x"" = x"$WAITUSB" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>waitusb=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="waitusb" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="number"'
	echo '                 name="WAITUSB"'
	echo '                 value="'$WAITUSB'"'
	echo '                 min="1"'
	echo '                 max="120"'
	echo '                 title="waitsub ( 1 -120 )"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="waitusb">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="waitusb" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Wait for USB&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;waitusb=x&gt;</p>'
	echo '          <p>During boot process, wait x seconds for slow USB devices.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_waitusb
#----------------------------------------------------------------------------------------

#--------------------------------------xvesa---------------------------------------------
pcp_bootcode_xvesa() {
	[ x"" = x"$XVESA" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>xvesa=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="xvesa" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="XVESA"'
	echo '                 value="'$XVESA'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="xvesa">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="xvesa" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set Xvesa default screen resolution&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;xvesa=800x600x32&gt;</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_xvesa
#----------------------------------------------------------------------------------------
echo '  </div>'
#----------------------------------------------------------------------------------------

COLUMN4_1="col-1"
COLUMN4_2="col-1"
COLUMN4_3="col-2"
COLUMN4_4="col-8"
#----------------------------------------------------------------------------------------
# piCore bootcodes ( VARIABLE )
#----------------------------------------------------------------------------------------
echo '  <div class="'$BORDER'">'
pcp_heading5 "piCore bootcodes ( VARIABLE )"
#--------------------------------------Heading-------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN4_1'">'
echo '        <p></p>'
echo '      </div>'
echo '      <div class="'$COLUMN4_2'">'
echo '        <p>Bootcode</p>'
echo '      </div>'
echo '      <div class="'$COLUMN4_3'">'
echo '        <p>Save</p>'
echo '      </div>'
echo '      <div class="'$COLUMN4_4'">'
echo '        <p>Description/Help</p>'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------

#--------------------------------------base----------------------------------------------
pcp_bootcode_base() {
	if [ $ONLYBASE -eq 1 ]; then ONLYBASEyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="base" action="'$0'" method="get">'
	echo '          <input id="cb1" type="checkbox" name="ONLYBASE" value="1" '$ONLYBASEyes'>'
	echo '          <label for="cb1">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="base">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>base&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="base" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Only load base system&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Skip loading extensions, only load the base system.</p>'
	echo '          <p><b>Note:</b> Can also be used with norestore bootcode to load a base system with no configuration.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_base
#----------------------------------------------------------------------------------------

#--------------------------------------cron----------------------------------------------
pcp_bootcode_cron() {
	if [ $CRON -eq 1 ]; then CRONyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="cron" action="'$0'" method="get">'
	echo '          <input id="cb2" type="checkbox" name="CRON" value="1" '$CRONyes'>'
	echo '          <label for="cb2">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="cron">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>cron&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="cron" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Start cron daemon&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Start the cron daemon at boot.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_cron
#----------------------------------------------------------------------------------------

#--------------------------------------laptop--------------------------------------------
pcp_bootcode_laptop() {
	if [ $LAPTOP -eq 1 ]; then LAPTOPyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="laptop" action="'$0'" method="get">'
	echo '          <input id="cb3" type="checkbox" name="LAPTOP" value="1" '$LAPTOPyes'>'
	echo '          <label for="cb3">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="laptop">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>laptop&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="laptop" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Force load laptop related modules&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Force load laptop related modules.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_laptop
#----------------------------------------------------------------------------------------

#--------------------------------------noautologin---------------------------------------
pcp_bootcode_noautologin() {
	if [ $NOAUTOLOGIN -eq 1 ]; then NOAUTOLOGINyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="noautologin" action="'$0'" method="get">'
	echo '          <input id="cb4" type="checkbox" name="NOAUTOLOGIN" value="1" '$NOAUTOLOGINyes'>'
	echo '          <label for="cb4">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="noautologin">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>noautologin&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="noautologin" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>No automatic login&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Skip automatic login at boot.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_noautologin
#----------------------------------------------------------------------------------------

#--------------------------------------nodhcp--------------------------------------------
pcp_bootcode_nodhcp() {
	if [ $NODHCP -eq 1 ]; then NODHCPyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="nodhcp" action="'$0'" method="get">'
	echo '          <input id="cb5" type="checkbox" name="NODHCP" value="1" '$NODHCPyes'>'
	echo '          <label for="cb5">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="nodhcp">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>nodhcp&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="nodhcp" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>No dhcp request&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Skip the dhcp request at boot.</p>'
	echo '          <p>This is used when a static IP is set.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_nodhcp
#-----------------------------------------------------------------------------------------

#--------------------------------------noembed--------------------------------------------
pcp_bootcode_noembed() {
	if [ $NOEMBED -eq 1 ]; then NOEMBEDyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="noembed" action="'$0'" method="get">'
	echo '          <input id="cb6" type="checkbox" name="NOEMBED" value="1" '$NOEMBEDyes'>'
	echo '          <label for="cb6">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="noembed">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>noembed&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="noembed" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Use a separate tmpfs&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This is an advanced option that changes where in RAM Core is run from.</p>'
	echo '          <p><b>Default:</b> Core uses the tmpfs setup by the kernel; with this bootcode, Core will setup a new tmpfs file system, and use that instead.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_noembed
#----------------------------------------------------------------------------------------

#--------------------------------------nofstab-------------------------------------------
pcp_bootcode_nofstab() {
	if [ $NOFSTAB -eq 1 ]; then NOFSTAByes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="nofstab" action="'$0'" method="get">'
	echo '          <input id="cb7" type="checkbox" name="NOFSTAB" value="1" '$NOFSTAByes'>'
	echo '          <label for="cb7">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="nofstab">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>nofstab&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="nofstab" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set nofstab&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_nofstab
#----------------------------------------------------------------------------------------

#--------------------------------------noicons-------------------------------------------
pcp_bootcode_noicons() {
	if [ $NOICONS -eq 1 ]; then NOICONSyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="noicons" action="'$0'" method="get">'
	echo '          <input id="cb8" type="checkbox" name="NOICONS" value="1" '$NOICONSyes'>'
	echo '          <label for="cb8">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="noicons">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>noicons&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="noicons" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Do not use icons&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Do not use icons.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_noicons
#----------------------------------------------------------------------------------------

#--------------------------------------norestore-----------------------------------------
pcp_bootcode_norestore() {
	if [ $NORESTORE -eq 1 ]; then NORESTOREyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="norestore" action="'$0'" method="get">'
	echo '          <input id="cb9" type="checkbox" name="NORESTORE" value="1" '$NORESTOREyes'>'
	echo '          <label for="cb9">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="norestore">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>norestore&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="norestore" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Turn off the restoring the configuration file&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Prevent the loading of the configuration file (mydata.tgz)</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_norestore
#----------------------------------------------------------------------------------------

#--------------------------------------nortc---------------------------------------------
pcp_bootcode_nortc() {
	if [ $NORTC -eq 1 ]; then NORTCyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="nortc" action="'$0'" method="get">'
	echo '          <input id="cb10" type="checkbox" name="NORTC" value="1" '$NORTCyes'>'
	echo '          <label for="cb10">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="nortc">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>nortc&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="nortc" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set no Real Time Clock (nortc)&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>The Raspberry Pi does not have a Real Time Clock.</p>'
	echo '          <p>The time is set during each boot from a ntp server.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_nortc
#----------------------------------------------------------------------------------------

#--------------------------------------noswap--------------------------------------------
pcp_bootcode_noswap() {
	if [ $NOSWAP -eq 1 ]; then NOSWAPyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="noswap" action="'$0'" method="get">'
	echo '          <input id="cb11" type="checkbox" name="NOSWAP" value="1" '$NOSWAPyes'>'
	echo '          <label for="cb11">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="noswap">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>noswap&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="noswap" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Do not use swap partition&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p><b>Default:</b> The system will use all Linux swap partitions automatically.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_noswap
#----------------------------------------------------------------------------------------

#--------------------------------------noutc---------------------------------------------
pcp_bootcode_noutc() {
	if [ $NOUTC -eq 1 ]; then NOUTCyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="noutc" action="'$0'" method="get">'
	echo '          <input id="cb12" type="checkbox" name="NOUTC" value="1" '$NOUTCyes'>'
	echo '          <label for="cb12">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="noutc">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>noutc&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="noutc" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>BIOS is using localtime&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>BIOS is using localtime.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_noutc
#----------------------------------------------------------------------------------------

#--------------------------------------nozswap-------------------------------------------
pcp_bootcode_nozswap() {
	if [ $NOZSWAP -eq 1 ]; then NOZSWAPyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="nozswap" action="'$0'" method="get">'
	echo '          <input id="cb13" type="checkbox" name="NOZSWAP" value="1" '$NOZSWAPyes'>'
	echo '          <label for="cb13">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="nozswap">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>nozswap&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="nozswap" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Disable compressed swap in RAM&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p><b>Default:</b> Core uses a RAM compression technique allowing you to use more RAM than you actually have.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_nozswap
#----------------------------------------------------------------------------------------

#--------------------------------------pause---------------------------------------------
pcp_bootcode_pause() {
	if [ $PAUSE -eq 1 ]; then PAUSEyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="pause" action="'$0'" method="get">'
	echo '          <input id="cb14" type="checkbox" name="PAUSE" value="1" '$PAUSEyes'>'
	echo '          <label for="cb14">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="pause">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>pause&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="pause" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Wait for a keypress before completing boot&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>By waiting for an enter key press before completing the boot, this bootcode lets you view the system boot messages more easily.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_pause
#----------------------------------------------------------------------------------------

#--------------------------------------protect-------------------------------------------
pcp_bootcode_protect() {
	if [ $PROTECT -eq 1 ]; then PROTECTyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="protect" action="'$0'" method="get">'
	echo '          <input id="cb15" type="checkbox" name="PROTECT" value="1" '$PROTECTyes'>'
	echo '          <label for="cb15">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="protect">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>protect&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="protect" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Use password encrypted backup&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>For added security, use a password encrypted backup.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_protect
#----------------------------------------------------------------------------------------

#--------------------------------------safebackup----------------------------------------
pcp_bootcode_safebackup() {
	if [ $SAFEBACKUP -eq 1 ]; then SAFEBACKUPyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="safebackup" action="'$0'" method="get">'
	echo '          <input id="cb16" type="checkbox" name="SAFEBACKUP" value="1" '$SAFEBACKUPyes'>'
	echo '          <label for="cb16">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="safebackup">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>safebackup&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="safebackup" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Enable safe backup (mydatabk.tgz)&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>A copy of your previous backup is made before doing a new backup (mydatabk.tgz).</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_safebackup
#----------------------------------------------------------------------------------------

#--------------------------------------secure--------------------------------------------
pcp_bootcode_secure() {
	if [ $SECURE -eq 1 ]; then SECUREyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="secure" action="'$0'" method="get">'
	echo '          <input id="cb17" type="checkbox" name="SECURE" value="1" '$SECUREyes'>'
	echo '          <label for="cb17">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="secure">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>secure&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="secure" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set password on boot&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>If you need to set the password on boot, for example on a first run.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_secure
#----------------------------------------------------------------------------------------

#--------------------------------------showapps------------------------------------------
pcp_bootcode_showapps() {
	if [ $SHOWAPPS -eq 1 ]; then SHOWAPPSyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="showapps" action="'$0'" method="get">'
	echo '          <input id="cb18" type="checkbox" name="SHOWAPPS" value="1" '$SHOWAPPSyes'>'
	echo '          <label for="cb18">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="showapps">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>showapps&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="showapps" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Display application names when booting&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Show each extension by name when loading it.'
	echo '             It slightly delays the boot, but it’s useful to find which extension has trouble loading.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_showapps
#----------------------------------------------------------------------------------------

#--------------------------------------superuser-----------------------------------------
pcp_bootcode_superuser() {
	if [ $SUPERUSER -eq 1 ]; then SUPERUSERyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="superuser" action="'$0'" method="get">'
	echo '          <input id="cb19" type="checkbox" name="SUPERUSER" value="1" '$SUPERUSERyes'>'
	echo '          <label for="cb19">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="superuser">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>superuser&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="superuser" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Textmode as user root&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Textmode as user root.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_superuser
#----------------------------------------------------------------------------------------

#--------------------------------------syslog--------------------------------------------
pcp_bootcode_syslog() {
	if [ $SYSLOG -eq 1 ]; then SYSLOGyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="syslog" action="'$0'" method="get">'
	echo '          <input id="cb20" type="checkbox" name="SYSLOG" value="1" '$SYSLOGyes'>'
	echo '          <label for="cb20">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="syslog">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>syslog&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="syslog" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Start syslog daemon&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Start syslog daemon at boot.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_syslog
#----------------------------------------------------------------------------------------

#--------------------------------------text----------------------------------------------
pcp_bootcode_text() {
	if [ $TEXT -eq 1 ]; then TEXTyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="text" action="'$0'" method="get">'
	echo '          <input id="cb21" type="checkbox" name="TEXT" value="1" '$TEXTyes'>'
	echo '          <label for="cb21">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="text">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>text&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="text" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Boot to text mode&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>In case an X server is installed, do not boot to graphical mode.'
	echo '             If an X server is not installed, the system will always boot to text mode.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_BETA ] && pcp_bootcode_text
#----------------------------------------------------------------------------------------

#--------------------------------------xonly---------------------------------------------
pcp_bootcode_xonly() {
	if [ $XONLY -eq 1 ]; then XONLYyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="xonly" action="'$0'" method="get">'
	echo '          <input id="cb22" type="checkbox" name="XONLY" value="1" '$XONLYyes'>'
	echo '          <label for="cb22">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="xonly">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>xonly&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="xonly" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set xonly&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_xonly
#----------------------------------------------------------------------------------------

#--------------------------------------xsetup--------------------------------------------
pcp_bootcode_xsetup() {
	if [ $XSETUP -eq 1 ]; then XSETUPyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="xsetup" action="'$0'" method="get">'
	echo '          <input id="cb23" type="checkbox" name="XSETUP" value="1" '$XSETUPyes'>'
	echo '          <label for="cb23">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="xsetup">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>xsetup&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="xsetup" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set xsetup&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>TODO</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_bootcode_xsetup
#----------------------------------------------------------------------------------------
echo '  </div>'
#----------------------------------------------------------------------------------------

COLUMN4_1="col-sm-2"
COLUMN4_2="col-sm-3"
COLUMN4_3="col-sm-2"
COLUMN4_4="col-sm-5"
#----------------------------------------------------------------------------------------
# Kernel bootcodes ( VARIABLE=value )
#----------------------------------------------------------------------------------------
echo '  <div class="'$BORDER'">'
pcp_heading5 "Kernel bootcodes ( VARIABLE=value )"
#--------------------------------------Heading-------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN4_1'">'
echo '        <p>Bootcode</p>'
echo '      </div>'
echo '      <div class="'$COLUMN4_2'">'
echo '        <p>Set</p>'
echo '      </div>'
echo '      <div class="'$COLUMN4_3'">'
echo '        <p>Save</p>'
echo '      </div>'
echo '      <div class="'$COLUMN4_4'">'
echo '        <p>Description/Help</p>'
echo '      </div>'
echo '      </div>'
#----------------------------------------------------------------------------------------

#---------------------------------------console------------------------------------------
pcp_bootcode_console() {
	[ x"" = x"$CONSOLE" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>console=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="console" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="CONSOLE"'
	echo '                 value="'$CONSOLE'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="console">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="console" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set console&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;console=tty1&gt;</p>'
	echo '          <p>&lt;console=tty3&gt;</p>'
	echo '          <p>&lt;console=ttyAMA0,115200&gt;</p>'
	echo '          <p>To set multiple values, use a space to separate values ie. tty1 ttyAMA0,115200</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_console
#----------------------------------------------------------------------------------------

#--------------------------------------consoleblank--------------------------------------
pcp_bootcode_consoleblank() {
	[ x"" = x"$CONSOLEBLANK" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>consoleblank=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="consoleblank" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="CONSOLEBLANK"'
	echo '                 value="'$CONSOLEBLANK'"'
	echo '                 readonly'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="consoleblank">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="consoleblank" type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Display consoleblank&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p><b>Note:</b> Use [Tweaks] page to set.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_consoleblank
#----------------------------------------------------------------------------------------

#--------------------------------------dwc_otg.fiq_fsm_mask------------------------------
pcp_bootcode_fiq_fsm_mask() {
	[ x"" = x"$FIQ_FSM_MASK" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>dwc_otg.fiq_fsm_mask=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="fiq_fsm_mask" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="FIQ_FSM_MASK"'
	echo '                 value="'$FIQ_FSM_MASK'"'
	echo '                 readonly'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="fiq_fsm_mask">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="fiq_fsm_mask" type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Display dwc_otg.fiq_fsm_mask&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p><b>Note:</b> Use [Tweaks] page to set.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_fiq_fsm_mask
#----------------------------------------------------------------------------------------

#--------------------------------------dwc_otg.lpm_enable--------------------------------
pcp_bootcode_lpm_enable() {
	[ x"" = x"$LPM_ENABLE" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>dwc_otg.lpm_enable=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="lpm_enable" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="LPM_ENABLE"'
	echo '                 value="'$LPM_ENABLE'"'
	echo '                 readonly'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="lpm_enable">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="lpm_enable" type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Display dwc_otg.lpm_enable&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p><b>Note:</b> Use [Tweaks] page to set.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_lpm_enable
#----------------------------------------------------------------------------------------

#--------------------------------------elevator------------------------------------------
pcp_bootcode_elevator() {
	[ x"" = x"$ELEVATOR" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>elevator=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="elevator" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="ELEVATOR"'
	echo '                 value="'$ELEVATOR'"'
	echo '                 readonly'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="elevator">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="elevator" type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Display elevator&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;elevator=cfq|deadline|noop&gt;</p>'
	echo '          <p>See https://www.kernel.org/doc/Documentation/block/deadline-iosched.txt.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_elevator
#----------------------------------------------------------------------------------------

#----------------------------------------fbcon-------------------------------------------
pcp_bootcode_fbcon() {
	[ x"" = x"$FBCON" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>fbcon=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="fbcon" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="FBCON"'
	echo '                 value="'$FBCON'"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="fbcon">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="fbcon" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set fbcon&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;fbcon=map:10&gt;</p>'
	echo '          <p>&lt;fbcon=font:ProFont6x11&gt;</p>'
	echo '          <p>To set multiple values, use a space to separate values ie. map:10 font:ProFont6x11.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_fbcon
#----------------------------------------------------------------------------------------

#--------------------------------------isolcpus------------------------------------------
pcp_bootcode_isolcpus() {
	[ x"" = x"$ISOLCPUS" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>isolcpus=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="isolcpus" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="ISOLCPUS"'
	echo '                 value="'$ISOLCPUS'"'
	echo '                 readonly'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="isolcpus">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="isolcpus" type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set CPU isolation&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p><b>Note:</b> Use [Tweaks] page to set.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_isolcpus
#----------------------------------------------------------------------------------------

#--------------------------------------loglevel------------------------------------------
pcp_bootcode_loglevel() {
	[ x"" = x"$LOGLEVEL" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>loglevel=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="loglevel" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="number"'
	echo '                 name="LOGLEVEL"'
	echo '                 value="'$LOGLEVEL'"'
	echo '                 min="0"'
	echo '                 max="7"'
	echo '                 title="logelevel ( 0 - 7 )"'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="loglevel">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="loglevel" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Set the default console log level&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;loglevel=x&gt;</p>'
	echo '          <p>Specify the initial console log level:</p>'
	echo '          <ul>'
	echo '            <li>0 (KERN_EMERG) The system is unusable.</li>'
	echo '            <li>1 (KERN_ALERT) Actions that must be taken care of immediately.</li>'
	echo '            <li>2 (KERN_CRIT) Critical conditions.</li>'
	echo '            <li>3 (KERN_ERR) Noncritical error conditions.</li>'
	echo '            <li>4 (KERN_WARNING) Warning conditions that should be taken care of.</li>'
	echo '            <li>5 (KERN_NOTICE) Normal, but significant events.</li>'
	echo '            <li>6 (KERN_INFO) Informational messages that require no action.</li>'
	echo '            <li>7 (KERN_DEBUG) Kernel debugging messages, output by the kernel
                                  if the developer enabled debugging at compile time.</li>'
	echo '          </ul>'
	echo '          <p><b>Default:</b> 3</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_loglevel
#----------------------------------------------------------------------------------------

#--------------------------------------root----------------------------------------------
pcp_bootcode_root() {
	[ x"" = x"$ROOT" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>root=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="root" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="ROOT"'
	echo '                 value="'$ROOT'"'
	echo '                 readonly'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="root">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="root" type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Specify the root filesystem to boot from&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>&lt;root=device&gt;</p>'
	echo '          <p>Tell the kernel which disk device the root filesystem image is on.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_root
#----------------------------------------------------------------------------------------

#--------------------------------------smsc95xx.turbo_mode-------------------------------
pcp_bootcode_turbo_mode() {
	[ x"" = x"$TURBO_MODE" ] && INDICATOR="" || INDICATOR="border-success"
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <p>smsc95xx.turbo_mode=</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <form id="turbo_mode" action="'$0'" method="get">'
	echo '          <input class="form-control form-control-sm '$INDICATOR'"'
	echo '                 type="text"'
	echo '                 name="TURBO_MODE"'
	echo '                 value="'$TURBO_MODE'"'
	echo '                 readonly'
	echo '          >'
	echo '          <input type="hidden" name="VARIABLE" value="turbo_mode">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="root" type="submit" name="SUBMIT" value="Readonly" disabled>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Display smsc95xx.turbo_mode&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p><b>Note:</b> Use [Tweaks] page to set.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_turbo_mode
#----------------------------------------------------------------------------------------
echo '  </div>'
#----------------------------------------------------------------------------------------

COLUMN4_1="col-sm-1 text-sm-right"
COLUMN4_2="col-sm-2"
COLUMN4_3="col-sm-2"
COLUMN4_4="col-sm-7"
#----------------------------------------------------------------------------------------
# Kernel bootcodes ( VARIABLE )
#----------------------------------------------------------------------------------------
echo '  <div class="'$BORDER'">'
pcp_heading5 "Kernel bootcodes ( VARIABLE )"
#--------------------------------------Heading-------------------------------------------
echo '    <div class="row mx-1">'
echo '      <div class="'$COLUMN4_1'">'
echo '        <p></p>'
echo '      </div>'
echo '      <div class="'$COLUMN4_2'">'
echo '        <p>Bootcode</p>'
echo '      </div>'
echo '      <div class="'$COLUMN4_3'">'
echo '        <p>Save</p>'
echo '      </div>'
echo '      <div class="'$COLUMN4_4'">'
echo '        <p>Description/Help</p>'
echo '      </div>'
echo '    </div>'
#----------------------------------------------------------------------------------------

#-----------------------------------logo.nologo------------------------------------------
pcp_bootcode_nologo() {
	if [ $NOLOGO -eq 1 ]; then NOLOGOyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="nologo" action="'$0'" method="get">'
	echo '          <input id="cb" type="checkbox" name="NOLOGO" value="1" '$NOLOGOyes'>'
	echo '          <label for="cb">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="logo.nologo">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>logo.nologo&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="nologo" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Turn off RPi logo&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>This bootcode will disable the Raspberry Pi logo during booting.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_nologo
#----------------------------------------------------------------------------------------

#--------------------------------------quiet---------------------------------------------
pcp_bootcode_quiet() {
	if [ $QUIET -eq 1 ]; then QUIETyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="quiet" action="'$0'" method="get">'
	echo '          <input id="cb" type="checkbox" name="QUIET" value="1" '$QUIETyes'>'
	echo '          <label for="cb">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="quiet">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>quiet&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="quiet" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Disable all log messages&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Set the default kernel log level to KERN_WARNING (4),
                               which suppresses all messages during boot except extremely serious ones.</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_quiet
#----------------------------------------------------------------------------------------

#--------------------------------------rootwait------------------------------------------
pcp_bootcode_rootwait() {
	if [ $ROOTWAIT -eq 1 ]; then ROOTWAITyes="checked"; INDICATOR=$GREEN; else INDICATOR=$RED; fi
	pcp_incr_id
	echo '    <div class="row mx-1">'
	echo '      <div class="'$COLUMN4_1'">'
	echo '        <form id="rootwait" action="'$0'" method="get">'
	echo '          <input id="cb" type="checkbox" name="ROOTWAIT" value="1" '$ROOTWAITyes'>'
	echo '          <label for="cb">&#8239;</label>'
	echo '          <input type="hidden" name="VARIABLE" value="rootwait">'
	echo '        </form>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_2'">'
	echo '        <p>rootwait&nbsp;&nbsp;'$INDICATOR'</p>'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_3'">'
	echo '        <input class="'$BUTTON'" form="rootwait" type="submit" name="SUBMIT" value="Save">'
	echo '      </div>'
	echo '      <div class="'$COLUMN4_4'">'
	echo '        <p>Wait for root device&nbsp;&nbsp;'
	echo '          <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'
	echo '        </p>'
	echo '        <div id="dt'$ID'" class="'$COLLAPSE'">'
	echo '          <p>Wait (indefinitely) for root device to show up.'
	echo '             Useful for devices that are detected asynchronously (e.g. USB and MMC devices)</p>'
	echo '        </div>'
	echo '      </div>'
	echo '    </div>'
}
[ $MODE -ge $MODE_PLAYER ] && pcp_bootcode_rootwait
#----------------------------------------------------------------------------------------
echo '  </div>'

echo '<hr>'
#========================================================================================
# $CMDLINETXT - /mnt/mmcblk0p1/cmdline.txt
#----------------------------------------------------------------------------------------
pcp_textarea "[ INFO ] Current: $CMDLINETXT" "cat $CMDLINETXT" 6

pcp_textarea_begin "[ INFO ] Bootcodes:" 25

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

pcp_textarea_end

pcp_umount_bootpart >/dev/null 2>&1
#----------------------------------------------------------------------------------------

echo '<hr>'
#========================================================================================
# /proc/cmdline
#----------------------------------------------------------------------------------------
pcp_proc_cmdline() {
	pcp_textarea "[ INFO ] Current: /proc/cmdline" "cat /proc/cmdline" 10

	pcp_textarea_begin "[ INFO ] Bootcodes:" 25

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

	pcp_textarea_end
}
[ $MODE -ge $MODE_DEVELOPER ] && pcp_proc_cmdline
#----------------------------------------------------------------------------------------

pcp_html_end
