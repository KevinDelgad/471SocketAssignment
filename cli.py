import sys
from socket import socket, AF_INET, SOCK_STREAM
import subprocess

if len(sys.argv) < 3:
    server_name = 'localhost'
    server_port = 1234
else:
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])

bufferSize = 1024
connectionSocket = socket(AF_INET, SOCK_STREAM)
connectionSocket.connect((server_name, server_port))

acceptableRequests = ['get', 'put', 'ls', 'quit']

while(True):
    command = input("ftp> ").strip()

    tempSocket = socket(AF_INET, SOCK_STREAM)
    tempSocket.bind(('', 0))
    tempSocket.listen(1)
    
    metaData = str(tempSocket.getsockname()[1]) + " " + command


    connectionSocket.send(metaData.encode())

    tempSendSocket, addr = tempSocket.accept()


    splitCommand = command.split()
    command = splitCommand[0]
    if command == 'get':
        targetFile = splitCommand[1]
        fileData = tempSendSocket.recv(1024).decode()
        
        with open(targetFile, "w") as fileObj:
            fileObj.write(fileData)

        print(f"{targetFile} ({len(fileData)}) bytes)")

    if command == 'put':
        fileData = 0
        targetFile = splitCommand[1]
        fileObj = open(targetFile, "r")

        fileData = fileObj.read()
        dataSize = str(len(fileData))

        while(len(dataSize) < 10):
            dataSize = '0' + dataSize

        fileData = dataSize + " | File Content: " + fileData

        numSent = 0

        while(numSent < len(fileData)):
            numSent += tempSendSocket.send(fileData[numSent:].encode())

        fileObj.close() 


        print("Successful Put Request")

    if command == 'ls':
        listedData = b''
        while True:
            data = tempSendSocket.recv(bufferSize)
            if b'\0' in data:
                data = data.replace(b'\0', b'')
                listedData += data
                break
            elif not data:
                break
            else:
                listedData += data

        print(listedData.decode())
 
    if command == 'quit':
            connectionSocket.sendall(b'quit')
            connectionSocket.close()
            sys.exit(0)
            break
    
    
    tempSocket.close()
    tempSendSocket.close()