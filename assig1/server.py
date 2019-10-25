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
	fileName = "1"+fileName.split('/')[-1]
	print(fileName)
	with open(fileName,'w+') as fd:
		while True:
			print("INSIDE TRUE")
			bi = c.recv(1024)
			print("lol b",bi)
			if bi== b'<<EOF>>':
				break
			fd.write(bi.decode('utf-8'))
	
	with open(fileName,'r') as fd:
		for line in fd:
			c.sendall(bytes(line,'utf-8'))
	c.sendall(b"\n")
	time.sleep(0.5)
	c.sendall(bytes(time.ctime(os.path.getmtime(fileName))+"\n",'utf-8'))
	c.close()