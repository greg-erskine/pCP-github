#!/bin/sh

# Version: 3.50 2017-11-21
#	Setting binary location in pCP web interface, Need to follow symlink for DEAMON. PH.

# Version: 3.03 2016-11-14 RI
#	Override DAEMON if a squeezelite binary installed in /mnt/mmcblk0p2/tce/.

# Version: 3.02 2016-09-20 RI
#	Fixed -i option only when Jivelite and LIRC enabled.

# Version: 0.07 2016-03-29 PH
#	Fixed $VISUALISER and $IR_LIRC.
#	Changed log location to ${LOGDIR}.

# Version: 0.06 2016-03-14 GE
#	Updated -e option.
#	Updated -U option.
#	Updated -V option.
#	Added -G option.
#	Added -S option.
#	Removed LOGFILE.
#	Updated -G option. PH.
#	Updated $VISUALISER and $IR_LIRC.

# Version: 0.05 2015-09-20 GE
#	Added -e option.
#	Added -U option (not working).
#	Added -V option.

# Version: 0.04 2015-03-13 SBP
#	Fixed VISUALISER -v option.

# Version: 0.03 2015-02-08 SBP
#	Changed how we check the status of squeezelite.

# Version: 0.03 2015-01-22 SBP
#	Added CLOSEOUT.

# Version: 0.02 2014-10-07 GE
#	Force now always kills squeezelite daemon.
#	Added support for spaces in player name. (I don't understand why it works!)
#	Trimmed sleep times down to 1 second in Restart and Force.

# Version: 0.01 2014-06-27 GE
#	Original.

TCEMNT="/mnt/$(readlink /etc/sysconfig/tcedir | cut -d '/' -f3)"
PNAME=Squeezelite
DESC="Squeezelite player"
# Set DAEMON to the actual binary
[ -f $TCEMNT/tce/squeezelite ] && DAEMON=`readlink $TCEMNT/tce/squeezelite` || DAEMON=/usr/local/bin/squeezelite
# Legacy check, incase this is the binary instead of symlink.
[ "$DAEMON" = "" ] && DAEMON=$TCEMNT/tce/squeezelite
PIDFILE=/var/run/squeezelite.pid
LOGDIR=/var/log

# Read from config file
. /usr/local/sbin/config.cfg

# Check if variable is present then add the correct option in front
[ x"" != x"$NAME" ]         && NAME="$NAME"							# <--- Moved "-n" to allow for spaces
[ x"" != x"$OUTPUT" ]       && OUTPUT="-o $OUTPUT"
[ x"" != x"$ALSA_PARAMS" ]  && ALSA_PARAMS="-a "$ALSA_PARAMS""
[ x"" != x"$BUFFER_SIZE" ]  && BUFFER_SIZE="-b $BUFFER_SIZE"
[ x"" != x"$_CODEC" ]       && _CODEC="-c $_CODEC"
[ x"" != x"$XCODEC" ]       && XCODEC="-e $XCODEC"
[ x"" != x"$PRIORITY" ]     && PRIORITY="-p $PRIORITY"
[ x"" != x"$MAX_RATE" ]     && MAX_RATE="-r $MAX_RATE"
[ x"" != x"$UPSAMPLE" ]     && UPSAMPLE="-R $UPSAMPLE"
[ x"" != x"$MAC_ADDRESS" ]  && MAC_ADDRESS="-m $MAC_ADDRESS"
[ x"" != x"$SERVER_IP" ]    && SERVER_IP="-s $SERVER_IP"
[ x"" != x"$LOGLEVEL" ]     && LOGLEVEL="-d $LOGLEVEL -f ${LOGDIR}/pcp_squeezelite.log"
[ x"" != x"$DSDOUT" ]       && DSDOUT="-D $DSDOUT"
[ "$VISUALISER" = "yes" ]     && VIS="-v"
[ x"" != x"$CLOSEOUT" ]     && CLOSEOUT="-C $CLOSEOUT"
[ x"" != x"$UNMUTE" ]       && UNMUTE="-U $UNMUTE"
[ x"" != x"$ALSAVOLUME" ]   && ALSAVOLUME="-V $ALSAVOLUME"
[ "$IR_LIRC" = "yes" ] && [ "$JIVELITE" != "yes" ] && LIRC="-i $IR_CONFIG"
[ x"" != x"$POWER_GPIO" ]   && POWER_GPIO="-G $POWER_GPIO:$POWER_OUTPUT"
[ x"" != x"$POWER_SCRIPT" ] && POWER_SCRIPT="-S $POWER_SCRIPT"
[ x"" != x"$OTHER" ]        && OTHER="$OTHER"

case "$1" in
	start)
		if [ -f $PIDFILE ]; then
			echo "$PNAME already running."
			exit 1
		fi
		echo "Starting $DESC: $PNAME..."
		start-stop-daemon --start --quiet -b -m -p $PIDFILE --exec $DAEMON -- -n "$NAME" $OUTPUT $ALSA_PARAMS $BUFFER_SIZE $_CODEC $XCODEC $PRIORITY $MAX_RATE $UPSAMPLE $MAC_ADDRESS $SERVER_IP $LOGLEVEL $DSDOUT $VIS $CLOSEOUT $UNMUTE $ALSAVOLUME $LIRC $POWER_GPIO $POWER_SCRIPT $OTHER
		;;
	stop)
		if [ ! -f $PIDFILE ]; then
			echo "$PNAME is not running."
			exit 1
		fi
		echo "Stopping $DESC: $PNAME..."
		start-stop-daemon --stop --quiet -p $PIDFILE
		sudo rm -f $PIDFILE
		;;
	restart)
		echo "Restarting $DESC..."
		$0 stop
		sleep 1
		$0 start
		;;
	force)
		# Force should only be used for testing purposes.
		echo "Forcing a restart of $PNAME..."
		if [ -f $PIDFILE ]; then
			sudo kill `cat $PIDFILE`
			sudo rm -f $PIDFILE
		fi
		sudo ps | grep squeezelite | grep -v grep | awk '{print $1}' | xargs kill -9
		sleep 1
		$0 start
		;;
	status)
		# Check if our squeezelite daemon is running.
		if [ -f $PIDFILE ]; then
			PID=`cat $PIDFILE`

			PIDS=`pgrep $DAEMON | awk '{printf "%s ", $1}'`

			for GOTPID in $PIDS; do
				if [ x"$GOTPID" = x"$PID" ]; then
					echo "$PNAME is running. PID=$PID"
					exit 0
				fi
			done
		fi

		echo "$PNAME not running."
		exit 1

		;;
	*)
		echo
		echo -e "Usage: $0 [start|stop|restart|force|status]"
		echo
		exit 1
		;;
esac

exit 0
