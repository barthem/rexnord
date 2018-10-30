#!/usr/bin/env python3

import winsound
import time
import _thread
import threading
import socket
from time import sleep
from multiprocessing import Queue
import sys
import struct




ipSideA = "192.168.0.1"
portSideA = 9000           # The port used by the server
buffersize = 1024

def stripByte(input):
    input = str(input)
    translation_table = dict.fromkeys(map(ord, '\\x0'), None)
    input = input.translate(translation_table)

    return bytes(input)

class socketConnector():
    def __init__(self):
        self.tcpip = '192.168.0.3'  # PLC IP
        self.port = 9000 # Port of the PLC
        self.bsize = buffersize  # Buffer size
        self.connection = 0

    def connect(self):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.tcpip, self.port))
        except:
            print("Connection failed")
            sys.exit()

    def waitForData(self):
        data = self.connection.recv(self.bsize)

        while not data:
            data = self.connection.recv(self.bsize)

        return data

    def sendData(self, data):
        # valid_byte = bytearray()
        data = int(data)
        print("tipen byte is: ", type(data))
        # valid_byte.append(data
        sent_data = struct.pack(">h", data)
        # print(ord(data))
        self.connection.send(sent_data)
        # print(type(bytearray(data)))
        # self.connection.send(bytearray(data))


def tcpListenPLC(socket, queue):
    while 1:
        # try:
        socket.connect()
        print("connection astablished at ",socket.tcpip , socket.port)
        time.sleep(1)
        while True:
            data = socket.waitForData()
            # string = str(data.decode('utf-8'))
            # string = stripByte(string)
            # string = string.encode()
            stripped = int(struct.unpack(">h", data[0:2])[0])
            queue.put(stripped)
            if data:
                # string = data.decode('utf-8')
                print("recieved PLC:", data, "  sending it as: ", stripped)
        # except:
        #     print("failed to make connection with plc. Sleep briefly & try again")
        #     time.sleep(5)
        #     continue




def tcpSendPLC(socket, queue):
    while True:
        if(queue.empty() is False):
            data = queue.get()
            print("sending to PLC: ", data)
            socket.sendData(data)

def tcpListen(socket, ipaddres, poort, queue):
    while 1:
        # try:
        socket.connect((ipaddres, poort))
        print("connection astablished at ",ipaddres , poort)
        time.sleep(1)
        while True:

            data = socket.recv(buffersize)
            # string = str(data.decode('utf-8'))
            # string = stripByte(string)
            # string = string.encode()
            # stripped = int(struct.unpack(">h", data[0:2])[0])
            queue.put(data)
            if data:
                # string = data.decode('utf-8')
                print("RA recieved:", data, " sending it as ", data)
        # except:
        #     print("failed to make connection with RA. Sleep briefly & try again")
        #     time.sleep(5)
        #     continue



def tcpSend(socket, queue):
    while True:
        if(queue.empty() is False):
            data = queue.get()
            print("sending RA: ", data, " data type: ", type(data))
            if(data == 1):
                string = "1"
                socket.send(string.encode())
            elif(data == 2):
                string = "2"
                socket.send(string.encode())

            # valid_byte = bytearray()
            # valid_byte.append(data)
            # socket.send(valid_byte)


if __name__ == '__main__':
    qa = Queue()
    qb = Queue()
    sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sb = socketConnector()
    print("sockets made!")


    # tcpListenPLC(sb, qb)

    sideAlisten = threading.Thread(name='kawasaki listen thread', target=tcpListen, args=(sa, ipSideA, portSideA, qa,))
    sideAlisten.start()
    print("started ", sideAlisten.getName())

    sideBlisten = threading.Thread(name='PLC listen thread', target=tcpListenPLC, args=(sb, qb,))
    sideBlisten.start()
    print("started ", sideBlisten.getName())

    time.sleep(5)

    sideAsend = threading.Thread(name='kawasaki send trhead', target=tcpSend, args=(sa, qb))
    sideAsend.start()
    print("started ", sideAsend.getName())

    sideBsend = threading.Thread(name='PLC sent thread', target=tcpSendPLC, args=(sb, qa))
    sideBsend.start()
    print("started ", sideBsend.getName())

    sideAlisten.join()
    sideBlisten.join()

    # while 1:
    #     sb.sendData(123)
    #     print("sending data: ")
    #     time.sleep(5)


    # while 1:
    #     try:
    #         sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         sa.connect((host, port))
    #         # print(sa)
    #         print("connection astablished to ",host , port)
    #     except:
    #         print("failed to make connection. Sleep briefly & try again")
    #         time.sleep(5)
    #         continue