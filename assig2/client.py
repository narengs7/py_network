#!/usr/bin/env python3
import socket
import signal 

ips = [
    # {
    #     'ip':"localhost",
    #     'port':1632
    # },
    {
        'ip':"localhost",
        'port':1635
    }
]

# def signal_handler(signum,frame):
#     print("exitttt")
#     exit(0)

# signal.signal(signal.SIGINT,signal_handler)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

a = ips.pop()
print(a)
ip = a['ip']
port = a["port"]
content=''
Status = 0
while True:
    try:
        s.connect((ip,port))
        s.send(b'WRITE')
        print("Connected ",ip,"to ",port)
        resp = s.recv(1024).decode()

        print("Resp OK STATUS :",resp=='OK')
        if resp == 'OK':
            f_name = input("Enter File name : ")
            print(f_name)
            s.send(f_name.encode())
            content = ""
            tmp_read = s.recv(1024).decode()
            while "<<EOC>>" not in tmp_read:
                content = content+tmp_read
                tmp_read = s.recv(1024).decode()
            print("[Info] Content in you file: ")
            print(content)
            content = input("Enter content : \n")
            content = content +"<<EOC>>"
            print("Sending content:",content)
            s.send(content.encode())
            if s.recv(1024) ==b'OK':
                print("[+] Succesfully Saved")
            else:
                print("[!] Failed")
        else:
            print("respone is not 'ok'")
        break
    except ConnectionResetError:
        print("Server is closed")
        Status=0
        # change ip to next ip
        s.close()
        print(len(ips))
        if(len(ips)>0):
            a = ips.pop()
            ip = a['ip']
            port = a['port']
            print("Trying to send to :",ip,":",port)
            s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            print("No More IPS")
            break
    except OSError:
        break

    finally:
        print("Finally Block")
print("I dying my self!!!")

