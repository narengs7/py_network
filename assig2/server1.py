import os
import socket
import pickle
import signal 
from datetime import datetime

def SigHandler(a,vb):
	print("Exiting..")
	exit(0)	

signal.signal(signal.SIGINT,SigHandler)

ips = [
    {
        'ip':"localhost",
        'port':1632
    }
]

# def cmp_mylog_s2log(log,arr);
#     log_size = len(log)
#     return tmp_log
#     return 

def write_log(l_log):
    print("Writing:",l_log)
    with open("server.log","wb") as fp:
        pickle.dump(l_log,fp)
    with open("server.log","rb") as fp:
        print("written:",pickle.load(fp))

def write_2_file(data):
    with open(''+data[1],'a') as fp:
        print("seeking to :",data[2])
        # data[2] = int(data[2])
        # fp.seek(data[2])
        fp.write(str(data[3]))
        print("wrote ",data[3],":to ",data[1])
        
def fetch_new_files(sock,arr):
    print("[+] Server is backing data.")
    try:
        for i in arr:
            print("Tango",i,":",i.strip()== '0000,,,')
            if i.strip() and not i.strip()== '0000,,,':
                print(i)
                write_2_file(i.split(','))
                log.append(i)
    except:
        print("Exception")
    write_log(log)
    
    print("[+] Server is backup complete.")

def fetch_backed_data(log):
    # Note s2 -> server 2 details
    s2_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2_details = ips.copy().pop()
    s2_sock.connect((s2_details["ip"],s2_details["port"]))
    s2_sock.send(b"DATA_FETCHER")
    resp = s2_sock.recv(1024).decode()
    if resp == "OK":
        print(log)
        last_com = log[-1].split(',')[0]
        print("Last Log time:",last_com)
        s2_sock.send(last_com.encode())
        s2_logs_with_contents=[]
        temp = s2_sock.recv(500).decode()
        while "<<EOC>>" not in temp:
            s2_logs_with_contents.append(temp)
            temp =s2_sock.recv(500).decode()
        s2_logs_with_contents.append(temp)
        s2_logs_with_contents = "".join(s2_logs_with_contents)
        s2_logs_with_contents=s2_logs_with_contents.split("<<EOC>>")[0]
        # cmp_my_s2_log(log,arr)
        arr = s2_logs_with_contents.split("<<EOF>>")
        # print(arr)
        fetch_new_files(s2_sock,arr)
    #End of Function

def backup_data(my_arr):
    print("[+] Backing data to server2..")
    s2_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2_details = ips.copy().pop()
    print("[+] Connecting to backup server ",s2_details["ip"],":",s2_details["port"])
    s2_sock.connect((s2_details["ip"],s2_details["port"]))
    s2_sock.send(b'WRITE')
    resp = s2_sock.recv(1024).decode()

    print("Resp OK STATUS :",resp=='OK')
    if resp == 'OK':
        f_name = my_arr[1]
        print(f_name)
        s2_sock.send(f_name.encode())
        content = ""
        tmp_read = s2_sock.recv(1024).decode()
        while "<<EOC>>" not in tmp_read:
            content = content+tmp_read
            tmp_read = s2_sock.recv(1024).decode()
        print("[Info] Content in you file: ")
        print(content)
        content = my_arr[-1]
        content = content +"<<EOC>>"
        print("Sending content:",content)
        s2_sock.send(content.encode())
        if s2_sock.recv(1024) ==b'OK':
            print("[+] Succesfully Saved")
        else:
            print("[!] Failed")
    else:
        print("respone is not 'ok'")




log=[]
try:
    files = list(os.walk('server1'))
    print(files[0])
    os.chdir('server1')
    if not os.path.exists("server.log"):
        print("Log file doesn't exist")
        with open("server.log","wb") as fp:
            log.append("0000,,,")
            pickle.dump(log,fp)
	
    with open("server.log","rb") as fp:
        print('lol',log)
        log = pickle.load(fp)
except EOFError:
    print("+[!] File exist or Log file is empty")

try:
    print(log)
    fetch_backed_data(log)
except ConnectionRefusedError:
    print("Server 2 is down..")

s1_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1_sock.bind(("",1635))

print("[+] Server is online now...")
s1_sock.listen(2)
while True:
    # Client Request
    c_conn,addr = s1_sock.accept()
    request_type = c_conn.recv(1024).decode()
    if request_type == "WRITE":
        c_conn.send(b'OK')
        f_name = c_conn.recv(1024).decode()
        assert(len(f_name.strip())!=0)
        content = b""
        if os.path.exists(''+f_name):
            with open(""+f_name,"rb") as fd:
                content = fd.read()
        content=content+b"<<EOC>>"
        print("Content is :",f_name,":",content)
        c_conn.send(content)
        content =""
        length = len(content)
        tmp_read = c_conn.recv(1024).decode()
        content = content + tmp_read
        while "<<EOC>>" not in tmp_read:
            tmp_read = c_conn.recv(1024).decode()
            content = content + tmp_read
        print("Writing conent:",content)
        content = content.replace("<<EOC>>","")
        #writting to file content
        with open(""+f_name,"a") as fd:
            length = length+fd.write(content)
        
        #updaing my log
        curr_time = datetime.now()
        curr_time = curr_time.strftime("%H%M")
        arr = []
        arr.append(curr_time)
        arr.append(f_name)
        arr.append(str(length))
        arr.append(content)
        log.append(",".join(arr))
        write_log(log)

        #Starting to backing up content
        try:
            backup_data(arr)
        except ConnectionRefusedError:
            print("[!] Server 2 is down.")

        c_conn.send(b"OK")
        print("[+] Completed All Transaction")
    

# print(a)
# fp.close()