import socket
import sys

welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = int(sys.argv[1])

welcomeSocket.bind(('', port))
welcomeSocket.listen(1)

print("Server is ready to recieve!")

while(True):
    connectionSocket, addr = welcomeSocket.accept()
    print("Connection Recieved!")
    connectionSocket.close()
    break