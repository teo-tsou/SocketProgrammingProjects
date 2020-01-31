import time
from socket import *
import pickle

HEADERSIZE = 10
serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((gethostname(),serverPort)) #Waiting for someone 'knocking the door'
serverSocket.listen(5) #Queue of 5 .That means that server gets 5 tcp requests in waiting.

while(1):
    clientSocket, address = serverSocket.accept() #Actually here there's a new socket (clientSocket created by accept method and that is for the well-known 3type handshake).After the connection, client and server can now send eachother    print(f"Connection from {address} has been established!")

    #Pickle is very useful way to send objects via sockets
    d = {1: "Hey", 2: "There"}
    msg = pickle.dumps(d) #CONVERT an object to a string

    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg   #left allignment.Actually putting a header and encode with utf-8 bytes

    clientSocket.send(msg) 
