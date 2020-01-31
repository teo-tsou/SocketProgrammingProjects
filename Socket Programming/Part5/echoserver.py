import socket
import struct
import sys

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

#After the regular socket is created and bound to a port,
#  it can be added to the multicast group by using setsockopt() to change the IP_ADD_MEMBERSHIP option.
#  The option value is the 8-byte packed
#  representation of the multicast group address followed by the network interface on which the server should listen for the traffic,
#  identified by its IP address. 
# In this case, the receiver listens on all interfaces using INADDR_ANY.

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)

mreq = struct.pack('4sL', group, socket.INADDR_ANY)
mreq = struct.pack('4s4s', group, socket.inet_aton('192.168.1.5')) #must put interface here
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    try:
        print('waiting to receive',sys.stderr)
        data, address = sock.recvfrom(1024)
        print( f'received { len(data) } bytes from {address}', sys.stderr)
        print( f'received {data.decode()}  from {address}', sys.stderr)

        print(f'sending acknowledgement to {address}',sys.stderr)
        sock.sendto('ack'.encode(), address)
    except KeyboardInterrupt:
        break
