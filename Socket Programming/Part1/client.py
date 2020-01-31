from socket import *

HEADERSIZE = 10
serverPort = 12000

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((gethostname(),serverPort)) #gethostname() in order to use the same machine

full_msg = "" #our buffer
new_msg = True

while(1):
    msg = clientSocket.recv(16)
    if(new_msg):
        print(f"New message length: {msg[:HEADERSIZE].decode('utf-8')}")
        msglen = int(msg[:HEADERSIZE].decode("utf-8"))

        new_msg = False

    full_msg = full_msg + msg.decode("utf-8")

    if(len(full_msg) - HEADERSIZE == msglen): #Checking if we received all the data
        print("Full message received")
        print(full_msg[HEADERSIZE:]) #Extracting all the data
        new_msg = True
        full_msg = ""


#Old version- Actually in this version we didn't care about the size of msgs
# clientSocket = socket(AF_INET,SOCK_STREAM)
# clientSocket.connect((gethostname(),serverPort)) #gethostname() in order to use the same machine

# full_msg = '' #our buffer
# while(1):
#     msg = clientSocket.recv(8)
#     if(len(msg) <= 0):
#         break
#     full_msg = full_msg + msg.decode("utf-8")
   
# print(full_msg) #decoding 
# clientSocket.close() #Here we are closing the socket session with server.

