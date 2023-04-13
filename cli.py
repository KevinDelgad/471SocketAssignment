import sys
from socket import *

server_name = sys.argv[1]
server_port = int(sys.argv[2])

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

while True:
    command = input("ftp> ")
    if not command:
        continue