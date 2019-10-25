import socket
import signal
import pickle

def SigHandler(arg1,arg2):
	print("Exiting..")
	exit(0)	

signal.signal(signal.SIGINT,SigHandler)
	
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
		con,addr=s2_sock.accept()
		lastSavedTime_s1=con.recv(1024).decode('utf-8')
		print("Last Server Time:",lastSavedTime_s1)
		content = get_content(int(lastSavedTime_s1))
		con.send(bytes(content,"utf-8"))

	except ConnectionResetError:
		print("Ava Sathha")
		print("Acting as Backup")
		
	
