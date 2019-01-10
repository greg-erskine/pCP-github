#!/bin/sh

# Version: 4.2.0 2019-01-11

PNAME="Shairport-sync"
DESC="Shairport-sync player"
[ -f /mnt/mmcblk0p2/tce/shairport-sync ] && DAEMON=/mnt/mmcblk0p2/tce/shairport-sync || DAEMON=/usr/local/sbin/shairport-sync

# Not used.
# ON_START="echo power 0 | nc 192.168.1.101 9090"
# ON_STOP="echo power 1 | nc 192.168.1.101 9090"
# -B "$ON_START" -E "$ON_STOP"

# Read from config file
. /usr/local/etc/pcp/pcp.cfg

if [ x"$SHAIRPORT_CONTROL" = x"" ]; then
	SHAIRPORT_CONTROL=''
else
	SHAIRPORT_CONTROL='-c '"$SHAIRPORT_CONTROL"''
fi

case "$1" in
	start)
		echo "Starting $DESC: $PNAME..."
		start-stop-daemon --start --quiet --exec $DAEMON \
						  -- -a "$NAME" -o alsa -S soxr -d -D -R \
						  --metadata-pipename=/tmp/shairport-sync-metadata --get-coverart \
						  -- -d $SHAIRPORT_OUT $SHAIRPORT_CONTROL
	;;
	stop)
		echo "Stopping $DESC: $PNAME..."
		start-stop-daemon --stop --quiet --exec $DAEMON
	;;
	restart)
		echo "Restarting $DESC..."
		$0 stop
		sleep 1
		$0 start
	;;
	status)
		# Check if shairport-sync daemon is running
		PID=$(ps -ef | grep $DAEMON | grep -v grep | awk '{ print $1 }')
		if [ 0$PID -gt 0 ]; then
			echo "$PNAME is running."
			exit 0
		else
			echo "$PNAME not running."
			exit 1
		fi
	;;
	*)
		echo
		echo -e "Usage: $0 [start|stop|restart|status]"
		echo
		exit 1
	;;
esac

exit 0
