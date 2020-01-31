import socket
import select

HEADER_LENGTH = 10
serverPort = 8000
IP = "192.168.1.8"

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #In order to reuse adressess


#Bind, so server informs operating system that it's going to use given IP and port
# For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
server_socket.bind(("", serverPort))



# This makes server listen to new connections
server_socket.listen() 

# List of sockets for select.select()
sockets_list = [server_socket]


# List of connected clients - socket as a key, user header and name as data
clients = {}



# Handles message receiving
def receive_message(client_socket):
    try:
         # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        if (not len(message_header)): #If a client closes a connection gracefully, then a socket.close() will be issued and there will be no header.
            return False

        message_length = int(message_header.decode("utf-8")) #Python understands that we need the number so by it self ignores the spaces that header has and give us only the number . In other languages strip() would do the job.
        return {"header": message_header , "data":client_socket.recv(message_length)} #After we recv only the header then we receive the data message 

    # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
    except:
        return False  

while(1):
    # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
    
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list) #Actually from the socket_list we take only the sockets that have received data. Actually the os inform us.
    
    for notified_socket in read_sockets:
        
          # If notified socket is a server socket - new connection, accept it
        if(notified_socket == server_socket): #If the server has data to read, that means that we have some new user trying to multicast his message. So we have to save his name in to the clients dict.
          
          
            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept() 
           
            # Client should send his name right away, receive it
            user = receive_message(client_socket)
            
            # If False - client disconnected before he sent his name
            if(user == False):
                continue
             # Add accepted socket to select.select() list
            sockets_list.append(client_socket)

            # Also save username and username header
            clients[client_socket] = user
            print(f"Acceptted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")  

        # Else existing socket is sending a message
        else:
            message = receive_message(notified_socket)
             # If False, client disconnected, cleanup
            if(message == False):
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")

                #Remove from list fro socket.socket
                sockets_list.remove(notified_socket)
                #Remove from our list of users
                del clients[notified_socket]

                continue

            user = clients[notified_socket] 
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}') #Print out the username and his message

             # Iterate over connected clients and broadcast message

            for client_socket in clients:
                   # But don't sent it to sender
                    if client_socket != notified_socket:
                       client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

             # It's not really necessary to have this, but will handle some socket exceptions just in case
            for notified_socket in exception_sockets:

                # Remove from list for socket.socket()
                 sockets_list.remove(notified_socket)

                # Remove from our list of users
                 del clients[notified_socket]            