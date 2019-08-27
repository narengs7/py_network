#! /usr/bin/env python3
import socket

# clinet program using python
s = socket.socket()
ip = '172.16.50.192'
port = 1632
s.connect((ip,port))
print("Successfully connected to ",ip)
print(" Data : ",s.recv(1024))
s.close()

