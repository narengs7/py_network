#!/usr/bin/env python3
import socket
import signal 

ips = [
    {
        'ip':"localhost",
        'port':1632
    },
    {
        'ip':"localhost",
        'port':1635
    }
]

# def signal_handler(signum,frame):
#     print("exitttt")
#     exit(0)

# signal.signal(signal.SIGINT,signal_handler)

s=socket.socket()

a = ips.pop()
print(a)
ip = a['ip']
port = a["port"]
content=''
Status = 0
while True:
    try:
        s.connect((ip,port))
        s.send(bytes(str(Status),'utf-8'))
        if(s.recv(1024) != b'OK'):
            print("You have already written!!!!")
            break

        s.send(b"sample_2.txt")
        if not content:
            content=input("Enter the contents for the file : ")
        s.send(bytes(content,'utf-8'))

        Status=s.recv(1024)
        Status=int(Status.decode('utf-8'))
        if Status == 1:
            print("Server 1 has completed its task")
            data=s.recv(1024)
            print(data.decode('utf-8'))
        print("close")
        s.close()
        break

    except ConnectionResetError:
       print("Server is closed")
       Status=0
        # change ip to next ip
        s.close()
        if(len(ips)>0):
            a = ips.pop()
            ip = a['ip']
            port = a['port']
            s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        else:
            break
    finally:
        print("Finally Block")
print("I dying my self!!!")

