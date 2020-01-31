import socket
import threading
import os
import sys

def GetFile(name,sock):
    filename = sock.recv(1024)
    filename = filename.decode("utf-8")
    if(os.path.isfile(filename)): #checks if the given path is a file
        size = os.stat(filename)
        size =size.st_size
        print(f'The size is {size}', sys.stderr)
        sock.send(bytes("ok" + str(size),"utf-8"))
        useresp = sock.recv(1024)
        useresp = useresp.decode("utf-8")
        if(useresp[:3] == 'yes'):
            with open(filename, 'rb') as fd:
                filebytes = fd.read(1024)
                numfbytes = len(filebytes)
                total = sock.send(filebytes)
                while(filebytes != ""):
                    filebytes = fd.read(1024)
                    numfbytes = numfbytes + len(filebytes)
                    temp = sock.send(filebytes)
                    total = total + temp
                if(total == numfbytes):
                    print("file succesfully transfered")
                else:
                    print("Error tranfering file")
    else:
        print('Theres no such file')
    sock.close()

def main():
    host = "192.168.1.9"
    port = 5000 
    s = socket.socket()   #Auto TCP
    s.bind((host,port))
    s.listen(5)         

    print("NFS Server Started")
    while True:
        client , addr = s.accept()
        print(f"Client: {str(addr)} connected")
        t =threading.Thread(target = GetFile, args = ("thread-worker",client))
        t.start()
    s.close()    

if __name__ == "__main__":
    main()


                    