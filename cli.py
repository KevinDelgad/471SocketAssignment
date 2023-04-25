import sys
from socket import socket, AF_INET, SOCK_STREAM
import subprocess

if len(sys.argv) < 3:
    server_name = 'localhost'
    server_port = 1234
else:
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])

connectionSocket = socket(AF_INET, SOCK_STREAM)
connectionSocket.connect((server_name, server_port))

acceptableRequests = ['get', 'put', 'ls', 'quit']

while(True):
    command = input("ftp> ").strip()
    connectionSocket.send(command.encode())
    splitCommand = command.split()
    command = splitCommand[0]

    if command == 'get':
        targetFile = splitCommand[1]
        fileData = connectionSocket.recv(1024).decode()
        
        with open(targetFile, "w") as fileObj:
            fileObj.write(fileData)

        print(f"{targetFile} ({len(fileData)}) bytes)")

    if command == 'put':
        fileData = 0
        fileObj = open(targetFile, "r")

        fileData = fileObj.read()
        dataSize = str(len(fileData))

        while(len(dataSize) < 10):
            dataSize = '0' + dataSize

        fileData = dataSize + " | File Content: " + fileData

        numSent = 0

        while(numSent < len(fileData)):
            numSent += connectionSocket.send(fileData[numSent:].encode())

        fileObj.close() 


        print("Successful Put Request")

    if command == 'ls':

        fileData = connectionSocket.recv(1024).decode()

        print("Successful ls Request")
    if command == 'quit':
            connectionSocket.close()
            break
    
    
    

