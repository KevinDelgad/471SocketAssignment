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

    client_socket.send(command.encode())

    command_parts = command.split()

    if command_parts[0].lower() == "get":
        response = client_socket.recv(1024).decode()
        if response == "SUCCESS":
            file_size = int(client_socket.recv(1024).decode())
            file_name = command_parts[1]

            with open(file_name, 'wb') as f:
                bytes_received = 0
                while bytes_received != file_size:
                    data = client_socket.recv(min(1024, file_size - bytes_received))
                    bytes_received += len(data)
                    f.write(data)

            print(f"{file_name} downloaded ({bytes_received} bytes)")
        else:
            print("File not found on server")

    elif command_parts[0].lower() == "put":
        file_name = command_parts[1]
        if os.path.isfile(file_name):
            file_size = os.stat(file_name).st_size
            client_socket.recv(1024)  # Receive ACK from server
            client_socket.send(str(file_size).encode())

            with open(file_name, 'rb') as f:
                bytes_sent = 0
                while bytes_sent != file_size:
                    data = f.read(1024)
