#!/usr/bin/env python3

import winsound
import time
import _thread
import threading
import socket
from time import sleep
from multiprocessing import Queue
import sys




ipSideA = "192.168.0.1"
portSideA = 12345           # The port used by the server


class socketConnector():
    def __init__(self):
        self.tcpip = '192.168.0.3'  # PLC IP
        self.port = 2000 # Port of the PLC
        self.bsize = 1024  # Buffer size
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
        # valid_byte.append(data)
        # self.connection.send(valid_byte)
        print(type(bytearray(data)))
        self.connection.send(bytearray(data))


def tcpListenPLC(socket, queue):
    socket.connect()
    print("connection astablished at ",socket.tcpip , socket.port)
    time.sleep(1)
    while True:

        data = socket.waitForData()
        queue.put(data)
        if data:
            string = data.decode('utf-8')
            print("recieved:", string)



def tcpSendPLC(socket, queue):
    while True:
        if(queue.empty() is False):
            data = queue.get()
            print("sendingPLC: ", data.decode('utf-8'))
            socket.sendData(data)

def tcpListen(socket, ipaddres, poort, queue):
    socket.connect((ipaddres, poort))
    print("connection astablished at ",ipaddres , poort)
    time.sleep(1)
    while True:

        data = socket.recv(1024)
        queue.put(data)
        if data:
            string = data.decode('utf-8')
            print("recieved:", data)



def tcpSend(socket, queue):
    while True:
        if(queue.empty() is False):
            data = queue.get()
            print("sending 1: ", data.decode('utf-8'))
            socket.send(data)


if __name__ == '__main__':
    qa = Queue()
    qb = Queue()
    sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sb = socketConnector()
    print("sockets made!")


    # tcpListenPLC(sb, qb)

    sideAlisten = threading.Thread(name='sidea listen thread', target=tcpListen, args=(sa, ipSideA, portSideA, qa,))
    sideAlisten.start()
    print("started ", sideAlisten.getName())

    sideBlisten = threading.Thread(name='PLC listen thread', target=tcpListenPLC, args=(sb, qb,))
    sideBlisten.start()
    print("started ", sideBlisten.getName())

    time.sleep(5)

    sideAsend = threading.Thread(name='sideA send trhead', target=tcpSend, args=(sa, qb))
    sideAsend.start()
    print("started ", sideAsend.getName())

    sideBsend = threading.Thread(name='PLC sent thread', target=tcpSendPLC, args=(sb, qa))
    sideBsend.start()
    print("started ", sideAsend.getName())

    sideAlisten.join()
    sideBlisten.join()
