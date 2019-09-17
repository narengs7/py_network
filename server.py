#! /usr/bin/env python3
import socket
import os
import time
import sys
import signal
import time

def sig_handler(signum,frame):
	print("Stopping application")
	exit(0)

signal.signal(signal.SIGINT,sig_handler)

soc = socket.socket()
soc.bind(('',1632))
#help(soc.listen)
soc.listen(1)
while(True):
	c,addr = soc.accept()
	print("Person Connected: ",c,addr)
	# Receiving file from client
	fileName = c.recv(1024).decode('utf-8')
	print(fileName)
	fileName = fileName.split('/')[-1]
	with open(fileName,'w+') as fd:
		c.sendall(bytes(time.ctime(os.path.getmtime(fileName)),'utf-8'))
		while True:
			b = c.recv(1024)
			print("lol b",b)
			if not b:
				break
			fd.write(b.decode('utf-8'))	
		
	c.close()

