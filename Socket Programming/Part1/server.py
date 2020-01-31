import time
from socket import *

HEADERSIZE = 10
serverPort = 12000


serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((gethostname(),serverPort)) #Waiting for someone 'knocking the door'
serverSocket.listen(5) #Queue of 5 .That means that server gets 5 tcp requests in waiting.

while(1):
    clientSocket, address = serverSocket.accept() #Actually here there's a new socket (clientSocket created by accept method and that is for the well-known 3type handshake).After the connection, client and server can now send eachother    print(f"Connection from {address} has been established!")
    msg = "Welcome to the server!"
    msg = f'{len(msg):<{HEADERSIZE}}' + msg  #left allignment

    clientSocket.send(bytes(msg, "utf-8")) #encoding utf-8 bytes

    while(1):
        time.sleep(3)
        msg = f"The time is {time.time()}"
        msg = f'{len(msg):<{HEADERSIZE}}' + msg  #left allignment
        clientSocket.send(bytes(msg, "utf-8")) #encoding utf-8 bytes





# Old version- Actually in this version we didn't care about the size of msgs

# serverPort = 12000
# serverSocket = socket(AF_INET,SOCK_STREAM)
# serverSocket.bind((gethostname(),serverPort)) #Waiting for someone 'knocking the door'
# serverSocket.listen(5) #Queue of 5 .That means that server gets 5 tcp requests in waiting.

# while(1):
#     clientSocket, address = serverSocket.accept() #Actually here there's a new socket (clientSocket created by accept method and that is for the well-known 3type handshake).After the connection, client and server can now send eachother
#     print(f"Connection from {address} has been established!")
#     clientSocket.send(bytes('Welcome to the server', "utf-8")) #encoding utf-8 bytes
#     clientSocket.close() #Here we are closing the socket with the client.Although the socket-server is still open
