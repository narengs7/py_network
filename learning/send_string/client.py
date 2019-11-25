#!/usr/bin/env python3
import socket



#Fireing request
def fire_request(request):
    request = request+1
    sock = socket.socket()
    sock.connect(('localhost',1632))
    str_obj = input("Enter the string: ")
    sock.send(str_obj.encode('utf-8'))
    if request == 1: # refire to same server again
        fire_request(request)
    
    print(sock.recv(1025).decode('utf-8'))
    sock.close()

fire_request(0)
