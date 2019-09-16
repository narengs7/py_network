#! /usr/bin/env python3
import socket
import sys

#read file
fileName = sys.argv[1]
# clinet program using python
s = socket.socket()
ip = '192.168.43.149'
port = 1632
s.connect((ip,port))
print("Successfully connected to ",ip)
with open(fileName,'r') as fd:
	str = fd.read()
	s.sendall(bytes(fileName,'utf-8'))
	print("Last Modified time",s.recv(1024))
	s.sendall(bytes(str,'utf-8'))
	
s.close()

