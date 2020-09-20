import socket
# Port des Servers



cmd_mplayer = 'mplayer -fps 25 -cache 512 -'
mprocess = subprocess.Popen(cmd_mplayer, shell=True, stdin=subprocess.PIPE)
PORT = x
# Lesepuffergröße
BUFFER_SIZE = 1400
# Unterstützte Addresstypen (IPv4, IPv6, lokale Addressen)
address_families = (socket.AF_INET, socket.AF_INET6, socket.AF_UNIX)
# Unterstützte Sockettypen (TCP, UDP, Raw (ohne Typ))
socket_types = (socket.SOCK_STREAM, socket.SOCK_DGRAM, socket.SOCK_RAW)
# Passenden Address- und Sockettyp wählen
address_family = address_families[0]
socket_type = socket_types[0]
# Maximale Anzahl der Verbindungen in der Warteschlange
backlog = 1
# Erstellen eines Socket (TCP und UDP)
sock = socket.socket(address_family, socket_type)
sock.bind(('', PORT))
# Lausche am Socket auf eingehende Verbindungen (Nur TCP)
sock.listen(backlog)
clientsocket, address = sock.accept()
# Daten (der Größe BUFFER_SIZE) aus dem Socket holen und ausgeben:
while True:
	# TCP:
	data = clientsocket.recv(BUFFER_SIZE)
	print(data)
	# UDP:
	data, address = sock.recvfrom(BUFFER_SIZE)
	print(data)

	mprocess.stdin.write(data)