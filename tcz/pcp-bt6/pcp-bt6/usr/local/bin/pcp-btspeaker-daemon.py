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
import socket
from subprocess import Popen,PIPE
import threading, time

CONFIG_FILE = '/usr/local/etc/pcp/pcp-bt.conf'
SQUEEZE_LITE = '/usr/local/bin/squeezelite'
STREAMER_CFG = '/tmp/bt_stream_device'
LOG_FILE = '/var/log/pcp_bt.log'
DEVNULL = open(os.devnull, 'w')

squeezelite={}
bt_speakers={}
a2dp_sinks={}

def dbus_get_pcm_devices():
	# Read from the bluealsa interface, check for an A2DP PCM
	dev_object = bus.get_object('org.bluealsa', '/org/bluealsa')
	dev_iface = dbus.Interface(dev_object, dbus_interface='org.bluealsa.Manager1')
	try:
		devices = dev_iface.GetPCMs()
	except dbus.exceptions.DBusException as error:
		bt_log.debug(str(error) + "\n")
		return None
	return devices

def dbus_get_a2dp_modes( node ):
	# Check node for a2dp Mode, or modes (sink,source)
	# node arg is full dbus node: /org/bluealsa/hci0/dev_xx_xx_xx_xx_xx_xx/a2dp
	try:
		node_obj = bus.get_object('org.bluealsa', node)
		node_iface = dbus.Interface(node_obj, dbus_interface='org.freedesktop.DBus.Properties')
		res = node_iface.Get('org.bluealsa.PCM1', 'Modes')
		modes = ', '.join(res)
	except dbus.exceptions.DBusException as error:
		bt_log.info('Error getting PCM mode: %s' % str(error))
		return None
	return modes

# Some speakers only like to make sco connection, this checks for a2dp connection
def A2DP_Monitor(dev):
	wait_time = 15
	dbus_errors = 0
	a2dp_found = 0

	while a2dp_found == 0 and dbus_errors < 5:
		time.sleep(wait_time)

		device = dbus_get_pcm_devices()
		if device == None:
			dbus_errors += 1

		for obj in device:
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

def LMS_JSON_discover( ip = '<broadcast>'):
	port = 3483
	query = b'eJSON\0'
	response = b'EJSON'
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			sock.settimeout(5)
			sock.bind(('', 0))
			sock.sendto(query, (ip, port))
			while True:
				try:
					data, (ip, _) = sock.recvfrom(1024)
					if not data.startswith(response):
						continue
					length = data[5:6][0]
					port = int(data[0 - length:]) 
					return ip, port
				except socket.timeout:
					break
	except OSError as err:
		bt_log.info('   Discovery failed: %s', err)
	return None, None

# Find currently running blueasla/squeezelite sessions and build list of PID's/MACs
# Runs at startup to detect any open sessions from a dae
def get_running_squeezelite():
	pid = None
	cmd = ['/bin/ps']
	ip = Popen( cmd , stdout=PIPE, stderr=DEVNULL)
	for line in io.TextIOWrapper(ip.stdout, encoding="utf-8"):
		if 'squeezelite' in line and 'bluealsa' in line:
			parts=' '.join(line.split()).strip().split(' ')
			pid = parts[0]
			mac = parts[5].split(',')[1].split('=')[1]
			key = mac.replace(':', '_')
			squeezelite[key] = int(pid)
			bt_log.info('Found squeezelite running (%s) with device %s.' % (pid, mac))

def get_connected_devices():
	device = dbus_get_pcm_devices()
	for obj in device:
		if 'a2dp' in obj:
			modes = dbus_get_a2dp_modes( obj )
			if 'source' in modes:
				parts=obj.split('/')
				if len(parts)>=4:
					mac =":".join(parts[4].split('_')[1:])
					key = mac.replace(':', '_')
					bt_speakers[key] = mac
					bt_log.info('Found a2dp source %s connected.' % mac)

def startup_sync_devices():
	#Check for connected speakers matching squeezelite processes, start new squeezelite processes if needed.
	for key in bt_speakers:
		mac = key.replace('_', ':')
		if key in squeezelite:
			bt_log.info('Synced device %s to squeezelite(%d).' % (mac, squeezelite[key]))
		else:
			bt_log.info('No squeezelite process for device %s.  Starting squeezelite......' % mac)
			
			name, delay = getName(mac)
			if None==name:
				bt_log.info("Unknown device %s" % mac)
			else:
				start_squeezelite(mac, name, delay)

	#Check squeezelite processes for no speaker connected, and kill process.
	for key in squeezelite:
		if key not in bt_speakers:
			bt_log.info('Squeezelite process(%d) for device not currently connected. Killing...' % squeezelite[key])
			os.kill(squeezelite[key], 3)
			os.waitpid(squeezelite[key], 0)
			squeezelite.pop(key)


# Find the LMS IP address that squeezelite is connected to.
def find_lms( pid ):
	lmsip = None
	cmd = ['/bin/netstat', '-tuapn']
	ip = Popen( cmd , stdout=PIPE, stderr=DEVNULL)
	for line in io.TextIOWrapper(ip.stdout, encoding="utf-8"):
		if str(pid) in line and '3483' in line:
			parts=' '.join(line.split()).strip().split(' ')
			lmsip = parts[4].split(':')[0]
	if not lmsip:
		return None, None
	# Discover JSON interface port for connected LMS server
	host, port = LMS_JSON_discover( lmsip ) 
	if not host:
		return None, None
	if not port:
		port = 9000  # Assume default port.
	return host, port

# Sends a Play command to LMS via the jsonrpc interface.
def send_play_command( lmsip, port, player):
	bt_log.info("   Sending Play command for %s to LMS at %s" % (player, lmsip))
	json_req = '{"id":1,"method":"slim.request","params":[ "%s", [ "play" ]]}' % player
	cmdline = '/usr/bin/wget -T 5 -q -O- --post-data=\'%s\' --header \'Content-Type: application/json\' http://%s:%s/jsonrpc.js' % ( json_req, lmsip, port)
	bt_log.debug("   %s" % cmdline)
	t = Popen( cmdline, shell=True, stdout=DEVNULL, stderr=DEVNULL)
	t.wait(timeout=10)
	bt_log.debug ('   Play command returned %d' % t.returncode)

def start_squeezelite(mac, name, delay):
	key=mac.replace(':', '_')
	if key in squeezelite:
		return
	alsa_buffer='80:::1'
	bt_log.info("Connected %s" % name)
	bt_log.debug("   bluealsa:SRV=org.bluealsa,DEV=%s,PROFILE=a2dp,DELAY=%s,ALSA=%s" % (mac, delay, alsa_buffer))
	proc = Popen([SQUEEZE_LITE, '-o', 'bluealsa:SRV=org.bluealsa,DEV=%s,PROFILE=a2dp,DELAY=%s' % (mac, delay), '-n', name, '-m', mac, '-a', alsa_buffer, '-f', '/dev/null'], stdout=DEVNULL, stderr=DEVNULL, shell=False)
	squeezelite[key] = proc.pid
	time.sleep(5)
	i = 0
	while i < 5:
		lmsip, port = find_lms ( squeezelite[key] )
		if lmsip != '':
			bt_log.info ("   Player Connected to LMS at: %s:%s" % (lmsip, port) )
			send_play_command( lmsip, port, name)
			break
		else:
			bt_log.info ("   Squeezelite not yet connected to LMS")
			i += 1
			time.sleep(1)
	if i == 5:
		bt_log.info ("   No connection to LMS detected")

def stop_squeezelite(mac, name):
	key=mac.replace(':', '_')
	if key not in squeezelite:
		return

	bt_log.info("Disconnected %s" % name)
	os.kill(squeezelite[key], 3)
	os.waitpid(squeezelite[key], 0)
	squeezelite.pop(key)

def set_sink(mac):
	if a2dp_sinks:
		bt_log.info("   a2dp sink already connected: Can only handle one device.")
		return

	key=mac.replace(':', '_')
	a2dp_sinks[key] = 'set'
	bt_log.info("   Writing device string for pcp-streamer")
	f = open(STREAMER_CFG, "w")
	f.write("OUTPUT_DEVICE=bluealsa:SRV=org.bluealsa,DEV=%s,PROFILE=a2dp\n" % mac)
	f.close()

def unset_sink(mac):
	key=mac.replace(':', '_')
	if key not in a2dp_sinks:
		return
	bt_log.info("   Removing device string for pcp-streamer")
	if os.path.exists(STREAMER_CFG):
		os.remove(STREAMER_CFG)

# Reads config file and returns device options for squeezelite.
def getName(mac):
	with open(CONFIG_FILE) as f:
		for line in f:
			parts=line.strip().split('#')
			if 3==len(parts) and mac==parts[0]:
				return parts[1], parts[2]
	return None, None

def connect_handler ( * args, **kwargs):
	bt_log.info('---- Caught Connect signal ----')
	#This signal only contains the node: /org/bluealsa/hci0/dev_xx_xx_xx_xx_xx_xx/a2dp

	parts=args[0].split('/')
	if len(parts)>=4:
		hci=parts[3]
		mac=":".join(parts[4].split('_')[1:])
		profile=parts[5]

	# Check node for a2dp Mode, we only want source
	modes = dbus_get_a2dp_modes( args[0] )
	if modes == None:
		return

	bt_log.debug("   HCI:%s" % hci)
	bt_log.info("   MAC:%s" % mac)
	bt_log.info("   PROFILE:%s" % profile)
	bt_log.info("   Modes:%s" % modes)

	if profile == 'a2dp':
		if 'source' in modes:
			name = None
			if None!=mac and None!=hci:
				name, delay = getName(mac)
			if None==name:
				bt_log.info("Unknown device %s" % mac)
			else:
				start_squeezelite(mac, name, delay)
		elif 'sink' in modes:
			set_sink(mac)
		else:
			bt_log.info("Device is unknown a2dp device")
	else:
		watch_for_a2dp(('dev_%s' % mac.replace(':', '_')))

def disconnect_handler ( * args, **kwargs):
	bt_log.info('---- Caught Disconnect signal ----')
	parts=args[0].split('/')
	if len(parts)>=4:
		hci=parts[3]
		mac=":".join(parts[4].split('_')[1:])
		profile=parts[5]
	bt_log.debug("   HCI:%s" % hci)
	bt_log.info("   MAC:%s" % mac)
	bt_log.info("   PROFILE:%s" % profile)

	if profile == 'a2dp':
		name = None
		if None!=mac and None!=hci:
			name, delay = getName(mac)
		if None!=name:
			stop_squeezelite(mac, name)
		unset_sink(mac)

if __name__ == '__main__':

	bt_log = logging.getLogger('BTINFO')
	formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M')
	handler = logging.handlers.RotatingFileHandler(LOG_FILE, mode='a', maxBytes=800000, backupCount=0)
	handler.setFormatter(formatter)
	bt_log.addHandler(handler)
	bt_log.setLevel(logging.INFO)

	bt_log.info("Starting pCP BT Speaker Daemon...")

	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	dbus.mainloop.glib.threads_init()

	bus = dbus.SystemBus()

	get_running_squeezelite()
	get_connected_devices()
	startup_sync_devices()
	
	bt_log.info('Staring connection signal handlers.')
	bus.add_signal_receiver(connect_handler, dbus_interface='org.bluealsa.Manager1', signal_name='PCMAdded')
	bus.add_signal_receiver(disconnect_handler, dbus_interface='org.bluealsa.Manager1', signal_name='PCMRemoved')

	mainloop = gobject.MainLoop()

	mainloop.run()
