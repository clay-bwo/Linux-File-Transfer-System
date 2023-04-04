#!/usr/bin/env python3
import os
import socket

HOST = '127.0.0.1' # The server's hostname or IP address
PORT = 65432 # The port used by the server
FILE = "" # Path of file to be transferred

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    file = open(FILE, "rb") # open file in read-binary mode
    file_size = os.path.getsize(FILE);
    
    s.send("received image.png".encode())
    s.send(str(file_size).encode())


    data = s.recv(1024)
    print('Received', repr(data))

file.close()
s.close()
