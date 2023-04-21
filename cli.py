import sys
from socket import socket, AF_INET, SOCK_STREAM
import subprocess

if len(sys.argv) < 3:
    server_name = 'localhost'
    server_port = 1234
else:
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

print("ftp> ")
acceptableRequests = ['get', 'put', 'ls', 'quit']

while(True):
    
    splitCommand = input().split()
    command = splitCommand[0]

    if(command == 'get'):
        print("get success")
    if(command == 'put'):
        print("put succes")
    if(command == 'ls'):
        print("ls success")
    if(command == 'quit'):
        print("quit success")
    
    
#input = ('get', 'put', 'ls', 'quit')
#if(command in acceptableRequests):
#    print("Valid Request")
#else:
#    print("Request not found")
