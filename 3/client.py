import socket
# IP und Port des Servers
import subprocess

cmd_raspivid = 'raspivid -t 0 -fps 20 -w 1280 -h 720 -b 2000000 -o -'
rasprocess = subprocess.Popen(cmd_raspivid,shell=True,stdout=subprocess.PIPE)
# mplayer starten



IP = '172.168.x.x'
PORT = x
# Passenden Address- und Sockettyp wählen
address_family = address_families[0]
socket_type = socket_types[0]
# Erstellen eines Sockets (TCP und UDP)
sock = socket.socket(address_family, socket_type)
# Verbinden zu einem Server-Socket (Nur TCP)
sock.connect((IP,PORT))
# Sende immer wieder "Hello" an den Server
while True:
	message = rasprocess.stdout.read(BUFFER_SIZE)


	# TCP
	sock.send(message)
	# UDP
	sock.sendto(message, (IP, PORT))