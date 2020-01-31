import socket
import select
import errno
import sys

HEADER_LENGTH = 10
serverPort = 12000
IP = "127.0.0.1"

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((IP,serverPort)) 

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
clientSocket.setblocking(False)



def user_msg(clientSocket):
    user = input('select your user name:')
    msg = bytes(f'{len(user):<{HEADER_LENGTH}}{user}', "utf-8") 
    clientSocket.send(msg)
    return(user)

def data_msg(clientSocket,user):
    msg = input(f'{user}:')
    if(msg):
        msg = bytes(f'{len(msg):<{HEADER_LENGTH}}{msg}' , "utf-8") 
        clientSocket.send(msg)

user = user_msg(clientSocket)
while(1):
    data_msg(clientSocket,user)
    try:
        username_header = clientSocket.recv(HEADER_LENGTH) 

        if(not len(username_header)):
                print('Connection closed by the server')
                sys.exit()
        
        username_length = int(username_header.decode('utf-8'))
        username = clientSocket.recv(username_length).decode('utf-8') #It starts 'reading' from the last time we stop .
        message_header = clientSocket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode("utf-8"))
        message = clientSocket.recv(message_length).decode('utf-8')
        print(f'{username}: {message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        # We just did not receive anything
        continue
    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()  
    data_msg(clientSocket,user)
    
    
