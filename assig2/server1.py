import socket
import pickle
import signal 

def SigHandler():
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

def write_2_file(data):
    with open('server1/'+data[1],'a') as fp:
        print("seeking to :",data[2])
        # data[2] = int(data[2])
        # fp.seek(data[2])
        fp.write(str(data[3]))
        print("wrote ",data[3],":to ",data[1])
        
    

def fetch_new_files(sock,arr):
    print("[+] Server is backing data.")
    try:
        for i in arr:
            if i.strip():
                print(i)
                write_2_file(i.split(','))
                log.append(i)
    except:
        print("Exception")
    
    print("[+] Server is backup complete.")

    

def fetch_backed_data(log):
    # Note s2 -> server 2 details
    s2_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2_details = ips.pop()
    s2_sock.connect((s2_details["ip"],s2_details["port"]))
    last_com = log[-1].split(',')[0]
    s2_sock.send(bytes(last_com,"utf-8"))
    s2_logs_with_contents=[]
    temp = s2_sock.recv(500).decode('utf-8')
    while "<<EOC>>" not in temp:
        s2_logs_with_contents.append(temp)
        temp =s2_sock.recv(500).decode('utf-8')
    s2_logs_with_contents.append(temp)
    s2_logs_with_contents = "".join(s2_logs_with_contents)
    s2_logs_with_contents=s2_logs_with_contents.split("<<EOC>>")[0]
    # cmp_my_s2_log(log,arr)
    arr = s2_logs_with_contents.split("<<EOF>>")
    # print(arr)
    fetch_new_files(s2_sock,arr)
    #End of Function


log=["0000,,,"]
try:
    with open("server1/server.log","rb") as fp:
        log = pickle.load(fp)
        print(log)
except EOFError:
    print("+[!] File exist or Log file is empty")


fetch_backed_data(log)

with open("server1/server.log","wb") as fp:
    pickle.dump(log,fp)


s1_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1_sock.bind(("",1635))

print("[+] Server is online now...")
s1_sock.listen(1)
while True:
    c_conn,addr = s1_sock.connect()
    

# print(a)
# fp.close()