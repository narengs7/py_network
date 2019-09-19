#! /usr/bin/env python3
import socket
import sys
import time

#read file
fileName = sys.argv[1]
# clinet program using python
s = socket.socket()
ip = '192.168.43.149'
port = 1632
s.connect((ip,port))
print("Successfully connected to ",ip)
with open(fileName,'r') as fd:
	s.sendall(bytes(fileName,'utf-8'))
	time.sleep(0.5)
	for line in fd:
		s.send(bytes(line,'utf-8'))

time.sleep(0.5)	
s.sendall(b' ')
val = s.recv(1024)
while True:
	print(val)
	val = s.recv(1024)
	if val==b'\n':
		break
	

print("Done Reading file")
print("Last Modified time",s.recv(1024))
s.close()

