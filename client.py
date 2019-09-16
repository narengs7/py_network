#! /usr/bin/env python3
import socket

# clinet program using python
s = socket.socket()
ip = '192.168.43.149'
port = 1633
s.connect((ip,port))
print("Successfully connected to ",ip)
with open('sum_client.py','r') as fd:
	str = fd.read()
	s.sendall(b'sum_client.py')
	print("Sent filename")
	s.sendall(bytes(str,'utf-8'))
	
print(s.recv(1024))
s.close()

