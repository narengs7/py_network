#! /usr/bin/env python3
import socket
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
	c.sendall(b'Welcome Aboard')
	c.close()

