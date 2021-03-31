# Simple Web Server
# This web server listens for requests from clients and responses with the requested file.

# import socket module
from socket import *

# import datatime module to add the date and time to the header of the response
import datetime

# import sys module to exit the program
import sys

# Establish a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Port Number of the web server
serverPort = 8080

# Bind the socket to server IP address and port number
serverSocket.bind(("", serverPort))

# Listen for incoming connections from clients
serverSocket.listen(1)

# Listen for connections
while True:
    print('The web server is wainting for connections...')

    # Accept connection from the client
    connectionSocket, addr = serverSocket.accept()

    # Fetch the client request
    try:
        # parse the request
        message = connectionSocket.recv(1024).decode()
        if len(message) > 0:
           
            # get the name of the request file
            filename = message.split()[1]

            # open the requested file
            f = open(filename[1:])
            
            # read the requested file
            outputdata = f.read()

            # Create  the HTTP header
            
            # get the current date and time
            now  = datetime.datetime.now()
            
            # create the status line of the response
            statusLine = "HTTP/1.1 200 OK\r\n"
            
            # create the header of the response
            headerInfo = {"Date":now.strftime("%Y-%m-%d%H:%M:%S"),
                           "Content-Type":"text/html",
                           "Charset=": "uuiltf-8",
                           "Content-Length": len(outputdata),
                           "Keep-Alive": "timeout=%d,Max%d"%(10,100),
                           "Connection": "Keep-Alive:"}
            headerLines = "\r\n".join("%s:%s"%(item, headerInfo[item]) for item in headerInfo)
            HTTPResponse = statusLine + headerLines + "\r\n\r\n"

            # Send the HTTP response header line to the clinet
            connectionSocket.send(HTTPResponse.encode())

            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())

            # Terminate the connection
            connectionSocket.close()



    except IOError:
        # Send HTTP response error message for file not found if the file does not exists in the server
        connectionSocket.send("HTTP/1.1 404  File Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404  File Not Found</h1></body></html>\r\n".encode())
        
        # Terminate the connection
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Terminate the program

