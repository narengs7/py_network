#!/usr/bin/env python3
import socket
import signal

def SigHandler(arg1,arg2):
	print("Stopped server..")
	exit(0)	

signal.signal(signal.SIGINT,SigHandler)

sock = socket.socket()
sock.bind(('',1632))
sock.listen(1)
print("Server Starting....")
while True:
    c, addr = sock.accept()
    str_obj = c.recv(1024).decode('utf-8')
    print(str_obj[::-1])
    c.send(str_obj[::-1].encode('utf-8'))
    c.close()
