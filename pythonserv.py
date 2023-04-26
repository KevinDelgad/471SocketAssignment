import socket
import sys
import subprocess

def recvAll(sock, numBytes):
	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		print(recvBuff)
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff = recvBuff + tmpBuff.decode()
	
	return recvBuff

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

    if(command == 'get'):
        targetFile = splitCommand[1]
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

    if(command == 'put'):
        # The buffer to all data received from the
        # the client.
        recvFileData = ""
        
        # The temporary buffer to store the received
        # data.
        recvBuff = ""
        
        # The size of the incoming file
        fileSize = 0	
        
        # The buffer containing the file size
        fileSizeBuff = ""
        
        # Receive the first 10 bytes indicating the
        # size of the file
        fileSizeBuff = recvAll(connectionSocket, 10) 
        # Get the file size
        fileSize = int(fileSizeBuff)
        # Get the file data
        recvFileData = recvAll(connectionSocket, fileSize)
        print(recvFileData)

    if command == "ls":
        listedData = subprocess.getstatusoutput('ls')[1]

        listedDataSize = len(listedData)
        listedDataNumSent = 0

        while listedDataNumSent < listedDataSize:
            listedDataNumSent += connectionSocket.send(listedData[listedDataNumSent:].encode())

        # Had to add sending null byte after transmitting all the listed data to let client know it ended
        connectionSocket.send(b'\0')


    if(command in acceptableRequests):
        connectionSocket.send(("Sucessful Command").encode())
    else:
        connectionSocket.send(("Unsucessful Command").encode())

    if(command == "quit"):
        connectionSocket.close()
        break

