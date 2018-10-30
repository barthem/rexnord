#!/usr/bin/env python3

import socket
import time


HOST = '192.168.0.1'  # The server's hostname or IP address
PORT = 9500        # The port used by the server

# try:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("setting up connection")
s.connect((HOST, PORT))
# for i in range(0,100):
while True :
    data = str(input("data to input?"))
    # data = "123"
    # print(i)
    if data == "quit":
        print("closing connection")
        # s.close()
        break
    print("sending message:", data.encode())
    s.send(data.encode())
    # print(s.recv(1024))
    # time.sleep(5)
s.send("quit".encode())
s.close()


# while(True):
#     data = input("input?")
#     s.send(data)
#
# except Exception as inst:
#     print(inst)
#     s.close()