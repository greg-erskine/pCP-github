#!/usr/local/bin/python3.6 -u

# pCP - Bluetooth speaker monitor
#   Connect multiple bluetooth speakers and start squeezelite instance for connected device

# Original concept from https://github.com/oweitman/squeezelite-bluetooth
# 

from __future__ import absolute_import, print_function, unicode_literals

# Using Pure GObject from https://pypi.org/project/pgi/, its alot leaner than full GObject
from pgi.repository import GObject as gobject

import dbus
import dbus.mainloop.glib
import os, sys, io, signal, logging, logging.handlers
from subprocess import Popen,PIPE
import threading, time

CONFIG_FILE = '/usr/local/etc/pcp/pcp-bt.conf'
SQUEEZE_LITE = '/usr/local/bin/squeezelite'
LOG_FILE = '/var/log/pcp_bt.log'
DEVNULL = open(os.devnull, 'w')

players={}

# Some speakers only like to make sco connection, this checks for a2dp connection
def A2DP_Monitor(dev):
	wait_time = 15
	dbus_errors = 0
	a2dp_found = 0
	dev_object = bus.get_object('org.bluealsa', '/org/bluealsa')
	dev_iface = dbus.Interface(dev_object, dbus_interface='org.bluealsa.Manager1')

	while a2dp_found == 0 and dbus_errors < 5:
		time.sleep(wait_time)
		# Read from the bluealsa interface, check for an A2DP PCM
		try:
			res = dev_iface.GetPCMs(name='PCMs', direction='out')
		except dbus.exceptions.DBusException as error:
			bt_log.debug(str(error) + "\n")
			dbus_errors += 1

		for obj in res:
			if dev in obj:
				if 'a2dp' in obj:
					bt_log.info('   Device: %s, connected with a2dp' % dev )
					a2dp_found = 1
					return
		#   Issue a bluetooth connect command seems to give the device a kick.
		bt_log.info('   Device: %s, not connected with a2dp' % dev )
		dev_conn_object = bus.get_object('org.bluez', '/org/bluez/hci0/%s' % dev)
		dev_conn_iface = dbus.Interface(dev_conn_object, dbus_interface='org.bluez.Device1')
		try:
			res = dev_conn_iface.Connect()
		except dbus.exceptions.DBusException as error:
			bt_log.debug(str(error) + "\n")
			dbus_errors += 1
	# Only gets here if there is no a2dp connection
	bt_log.info('   Device: %s, error connecting a2dp' % dev )

def watch_for_a2dp( dev ):
	# Create a thread for each device connection, thread dies when a2dp is connected.
	device = '%s' % dev
	Monitor = threading.Thread(target=A2DP_Monitor, args=(device,))
	Monitor.start()

# Find the LMS IP address that squeezelite is connected to.
#   ToDo: probe LMS to find the Web interface port.
def find_lms( pid ):
	cmd = ['/bin/netstat', '-tuapn']
	ip = Popen( cmd , stdout=PIPE, stderr=DEVNULL)
	for line in io.TextIOWrapper(ip.stdout, encoding="utf-8"): 
		if str(pid) in line and '3483' in line:
			parts=' '.join(line.split()).strip().split(' ')
			lmsip = parts[4].split(':')[0]
	return lmsip

# Sends a Play command to LMS via the jsonrpc interface.
def send_play_command( lmsip, player):
	bt_log.info("   Sending Play command for %s to LMS at %s" % (player, lmsip))
	json_req = '{"id":1,"method":"slim.request","params":[ "%s", [ "play" ]]}' % player
	cmdline = '/usr/bin/wget -T 5 -q -O- --post-data=\'%s\' --header \'Content-Type: application/json\' http://%s:9000/jsonrpc.js' % ( json_req, lmsip)
	bt_log.debug("   %s" % cmdline)
	t = Popen( cmdline, shell=True, stdout=DEVNULL, stderr=DEVNULL)
	t.wait(timeout=10)
	bt_log.debug ('   Play command returned %d' % t.returncode)

def start_squeezelite(hci, dev, name, delay, alsa_buffer, usemac):
	key=dev.replace(':', '_')
	if key in players:
		return

	sqlt_log.info("Connected %s" % name)
	if usemac=='on':
		sqlt_log.debug("   bluealsa:SRV=org.bluealsa,DEV=%s,PROFILE=a2dp,DELAY=%s,ALSA=%s, Using BT Mac" % (dev, delay, alsa_buffer))
		players[key] = Popen([SQUEEZE_LITE, '-o', 'bluealsa:SRV=org.bluealsa,DEV=%s,PROFILE=a2dp,DELAY=%s' % (dev, delay), '-n', name, '-m', dev, '-a', alsa_buffer, '-f', '/dev/null'], stdout=DEVNULL, stderr=DEVNULL, shell=False)
	else:
		sqlt_log.debug("   bluealsa:SRV=org.bluealsa,DEV=%s,PROFILE=a2dp,DELAY=%s,ALSA=%s, Using Machine MAC" % (dev, delay, alsa_buffer))
		players[key] = Popen([SQUEEZE_LITE, '-o', 'bluealsa:SRV=org.bluealsa,DEV=%s,PROFILE=a2dp,DELAY=%s' % (dev, delay), '-n', name, '-a', alsa_buffer, '-f', '/dev/null'], stdout=DEVNULL, stderr=DEVNULL, shell=False)
	time.sleep(1)
	i = 0
	while i < 5:
		LMS_IP = find_lms ( players[key].pid )
		if LMS_IP != '':
			sqlt_log.info ("   Player Connected to LMS at: %s" % LMS_IP)
			send_play_command( LMS_IP, name)
			break
		else:
			sqlt_log.info ("   Squeezelite not yet connected to LMS")
			i += 1
			time.sleep(1)
	if i == 5:
		sqlt_log.info ("   No connection to LMS detected")

def stop_squeezelite(dev, name):
	key=dev.replace(':', '_')
	if key not in players:
		return

	bt_log.info("Disconnected %s" % name)
	players[key].kill()
	os.waitpid(players[key].pid, 0)
	players.pop(key)

# Reads config file and returns device options for squeezelite.
def getName(dev):
	with open(CONFIG_FILE) as f:
		for line in f:
			parts=line.strip().split('#')
			if 5==len(parts) and dev==parts[0]:
				return parts[1], parts[2], parts[3], parts[4]
	return None

def connect_handler ( * args, **kwargs):
	bt_log.info('---- Caught Connect signal ----')

	parts=args[0].split('/')
	if len(parts)>=4:
		hci=parts[3]
		dev=":".join(parts[4].split('_')[1:])
		profile=parts[5]
	bt_log.debug("   HCI:%s" % hci)
	bt_log.info("   DEV:%s" % dev)
	bt_log.info("   PROFILE:%s" % profile)

	if profile == 'a2dp':
		name = None
		if None!=dev and None!=hci:
			name, delay, alsabuf, usemac = getName(dev)
		if None==name:
			bt_log.info("Unknown device %s" % dev)
		else:
			start_squeezelite(hci, dev, name, delay, alsabuf, usemac)
	else:
		watch_for_a2dp(('dev_%s' % dev.replace(':', '_')))

def disconnect_handler ( * args, **kwargs):
	bt_log.info('---- Caught Disconnect signal ----')
	parts=args[0].split('/')
	if len(parts)>=4:
		hci=parts[3]
		dev=":".join(parts[4].split('_')[1:])
		profile=parts[5]
	bt_log.debug("   HCI:%s" %hci)
	bt_log.info("   DEV:%s" %dev)
	bt_log.info("   PROFILE:%s" % profile)

	if profile == 'a2dp':
		name = None
		if None!=dev and None!=hci:
			name, delay,buf,usemac = getName(dev)
		if None==name:
			bt_log.info("Unknown device %s" % dev) 
		else:
			stop_squeezelite(dev, name)

if __name__ == '__main__':

	bt_log = logging.getLogger('BTINFO')
	sqlt_log = logging.getLogger('SLINFO')
	formatter = logging.Formatter(fmt='%(asctime)s %(name)-6s: %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M')
	handler = logging.handlers.RotatingFileHandler(LOG_FILE, mode='a', maxBytes=800000, backupCount=0)
	handler.setFormatter(formatter)
	bt_log.addHandler(handler)
	sqlt_log.addHandler(handler)
	bt_log.setLevel(logging.INFO)
	sqlt_log.setLevel(logging.INFO)

	bt_log.info("Starting pCP BT Speaker Daemon...")

	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	dbus.mainloop.glib.threads_init()

	bus = dbus.SystemBus()

	bus.add_signal_receiver(connect_handler, dbus_interface='org.bluealsa.Manager1', signal_name='PCMAdded')
	bus.add_signal_receiver(disconnect_handler, dbus_interface='org.bluealsa.Manager1', signal_name='PCMRemoved')

	mainloop = gobject.MainLoop()

	mainloop.run()

