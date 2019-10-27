
import os
import socket
import signal
import pickle
from datetime import datetime

def SigHandler(arg1,arg2):
	print("Exiting..")
	exit(0)	

signal.signal(signal.SIGINT,SigHandler)
	
def write_log(l_log):
    with open("server2/server.log","wb+") as fp:
        pickle.dump(l_log,fp)

def file_write(file,data):
	with open(file,'a') as f:
		f.write(data)

def get_content(last_com_time):
	content = []
	for each_log in log:
		log_time = int(each_log.split(",")[0])
		if (last_com_time<log_time):
			content.append(each_log)
	
	content = "<<EOF>>".join(content)
	content = content +"<<EOC>>"
	return content

log=["0000,,,"]
try:
	with open("server2/server.log","rb") as fp:
		log = pickle.load(fp)
except EOFError:
	print("+[!] File exist or Log file is empty")

s2_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2_sock.bind(("",1632))
status=0
s2_sock.listen(1)
while True:
	try:
		c_conn,addr=s2_sock.accept()
		req_type = c_conn.recv(1024).decode("utf-8")
		if req_type == "DATA_FETCHER":
			# -- Server1 Request backed data ----
			c_conn.send(b'OK')
			lastSavedTime_s1=c_conn.recv(1024).decode('utf-8')
			print("Last Server Time:",lastSavedTime_s1)
			content = get_content(int(lastSavedTime_s1))
			c_conn.send(content.encode())
		elif req_type == "WRITE":
			# -- Client Writes data directly to server
			c_conn.send(b'OK')
			f_name = c_conn.recv(1024).decode('utf-8')
			content = b""
			if os.path.exists('server2/'+f_name):
				with open("server2/"+f_name,"rb") as fd:
					content = fd.read()
					content = content+"<<EOC>>"
			c_conn.send(content)
			content =""
			length = len(content)
			tmp_read = c_conn.recv(1024)
			while "<<EOC>>" not in tmp_read:
				content = content + tmp_read
				tmp_read = c_conn.recv(1024).decode('utf-8')
			content = content.replace("<<EOC>>","")
			
			#writting to file content
			with open("server2/"+f_name,"a") as fd:
				length = length+fd.write(content)
			
			#updaing my log
			curr_time = datetime.now()
			curr_time = curr_time.strftime("%H%M")
			arr = []
			arr.append(curr_time)
			arr.append(f_name)
			arr.append(str(length))
			log.append(",".join(arr))
			write_log(log)
			
		else:
			c_conn.send(b'NO')
	except ConnectionResetError:
		print("Ava Sathha")
		print("Acting as Backup")
		
	
