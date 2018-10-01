#!/usr/bin/env python3

import socket

HOST = '192.168.0.3'  # The server's hostname or IP address
PORT = 9000        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'1')
    data = s.recv(1024)
    s.close()

print('Received', repr(data))