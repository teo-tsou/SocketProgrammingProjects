import socket
import struct
import sys

message = f'very important data'
multicast_group = ('224.3.29.71', 10000)

#Create of a udp socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(10)


#The socket also needs to be configured 
# with a time-to-live value (TTL) for the messages.
# The TTL controls how many networks will receive the packet. 
# Set the TTL with the IP_MULTICAST_TTL option and setsockopt().
#  The default, 1, means that the packets are not forwarded by the router beyond the current network segment.
#  The value can range up to 255,
#  and should be packed into a single byte.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:
    print(f'sending {message}')
    sent = sock.sendto(message.encode(),multicast_group)

    #Look for responses from all recipients
    while(1):
         print('waiting to receive',sys.stderr)
         try:
             data,server = sock.recvfrom(16)
             data = data.decode("utf-8")
         except socket.timeout:
             print('timed out, no more responses',sys.stderr) 
         
         else:
             print( f'received {data} from {server}', sys.stderr)

finally:
    print("closing socket")
    sock.close()



