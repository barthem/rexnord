#!/usr/bin/env python3

import socket
from time import sleep


HOST = '145.52.172.196'  # The server's hostname or IP address
PORT = 13337        # The port used by the server

try:
    for x in range(0, 1000000):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("setting up connection")
        s.connect((HOST, PORT))
        data = str(x)
        s.send(data.encode())
        print("closing connection")
        s.close()
        sleep(0.01)



# while(True):
#     data = input("input?")
#     s.send(data)

except Exception as inst:
    print(inst)
    s.close()