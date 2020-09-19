import bluetooth

target_name = "Joy"
target_address = None

def Connect(device):
		bd_addr = device[0]
		name = device[1]
		controlsocket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
		try:
			controlsocket.connect((bd_addr,17))
		except:
			return False
		datasocket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
		datasocket.connect((bd_addr,19))
		sendsocket = controlsocket
		CMD_SET_REPORT = 0x52
		if name == "Nintendo RVL-CNT-01-TR":
	             CMD_SET_REPORT = 0xa2
	             sendsocket = datasocket

		try:
			datasocket.settimeout(1)
		except NotImplementedError:
			print ("socket timeout not implemented with this bluetooth module")

		print ("Connected to ", bd_addr)
		start_time = datetime.now()
		#f = open('wiimote.log', 'w')
		#measurement_ended = False
		#start() #start this thread
		return True

nearby_devices = bluetooth.discover_devices(lookup_names=True)

for addr, name in nearby_devices:
	print("{} --> {}".format(addr, name))
	if target_name in name:
		device = (addr, name)
		print(device)
		break



Connect(device)


