import socket
import signal

def SigHandler(arg1,arg2):
	print("Exiting..")
	exit(0)	

signal.signal(signal.SIGINT,SigHandler)
	
def file_write(file,data):
	print(data)
	with open(file,'a') as f:
		f.write(data)

temp_log=[
	"1000,1.txt,2000",
	"1230,2.txt,1000"
]
s2_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2_sock.bind(("",1632))
status=0
s2_sock.listen(1)
while True:
	try:
		con,addr=s2_sock.accept()
		lastSavedTime_s1=con.recv(1024)
		con.send(b"1000,1.txt,0,Naren testing writing content of file<<EOF>>1020,naren.txt,5, Naren testing writing content of file<<EOF>><<EOC>>")
		

	except ConnectionResetError:
		print("Ava Sathha")
		print("Acting as Backup")
		
	
