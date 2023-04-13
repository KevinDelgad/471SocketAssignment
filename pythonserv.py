import socket
import sys

welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = int(sys.argv[1])

welcomeSocket.bind(('', port))
welcomeSocket.listen(1)

print("Server is ready to recieve!")

data = "test Data"
acceptableRequests = ['get', 'put', 'ls', 'quit']

while(True):
    connectionSocket, addr = welcomeSocket.accept()
    print("Connection Recieved!")
    usersInput = connectionSocket.recv(1024).decode()
    
    splitCommand = usersInput.split()

    command = splitCommand[0]
    targetFile = splitCommand[1]

    if(command in acceptableRequests):
        print("Valid Request")
    else:
        print("Request not found")

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

    connectionSocket.close()
    break