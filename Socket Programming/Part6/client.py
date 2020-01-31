import socket
import sys

def main():
    ip = "192.168.1.2"
    port = 5000

    s = socket.socket()
    s.connect((ip,port))

    filename = input("Filename: ")

    if(filename != 'q'):
        s.send(bytes(filename ,"utf-8"))
        data = s.recv(1024)
        data = data.decode()
        data = str(data)
        if(data[:2] == "ok"):
            size = data[2:]
            print(f'The size is {size}', sys.stderr)
            size = int(size)
            
            ##size = int(size)
            print(f"{filename} exists with size: {size} . Do you want to proceed? (yes/no)?")
            choice = input("Filename: ")
            if(choice == 'yes' or choice == 'YES'):
                s.send(bytes('yes', "utf-8"))
                fd = open("new_"+filename, 'wb')
                data = s.recv(1024)
                total = len(data)
                fd.write(data)
                while(total < size):
                    data = s.recv(1024)
                    total = total + len(data)
                    fd.write(data)
                    stat = (total /(size))*100
                    stat = round(stat,2)
                    print(f"Downloading: {stat} %")
            print('Download Complete')
        else:
             print("File does not exists")
    else:
        print('Goodbye!\n')         
    s.close()

if __name__ == "__main__":
    main()