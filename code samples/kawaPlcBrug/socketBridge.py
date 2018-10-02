#!/usr/bin/env python3

import winsound
import time
import _thread
import threading
import socket
from time import sleep
from multiprocessing import Queue




ipSideA = "192.168.0.1"
ipSideB = "192.168.0.3"
portSideA = 12345           # The port used by the server
portSideB = 9000           # port used by the other side of bridge

def tcpClient(ipaddres, poort, inputQue, outputQue):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    s.connect((ipaddres, poort))
    data = s.reciev(1024)
    outputQue.put(data)


def tcpListen(socket, ipaddres, poort, queue):
    socket.connect((ipaddres, poort))
    print("connection astablished at ",ipaddres , poort)
    time.sleep(3)
    while True:

        data = socket.recv(1024)
        queue.put(data)
        if data:
            string = data.decode('utf-8')
            print("recieved:", string)



def tcpSend(socket, queue):
    while True:
        if(queue.empty() is False):
            data = queue.get()
            print("sending: ", data.decode('utf-8'))
            socket.send(data)


if __name__ == '__main__':
    qa = Queue()
    qb = Queue()
    sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("sockets made!")


    sideAlisten = threading.Thread(name='sidea listen thread', target=tcpListen, args=(sa, ipSideA, portSideA, qa,))
    sideAlisten.start()
    print("started ", sideAlisten.getName())

    sideBlisten = threading.Thread(name='side B listen thread', target=tcpListen, args=(sb, ipSideB, portSideB, qb,))
    sideBlisten.start()
    print("started ", sideBlisten.getName())

    time.sleep(5)

    sideAsend = threading.Thread(name='sideA send trhead', target=tcpSend, args=(sb, qa))
    sideAsend.start()
    print("started ", sideAsend.getName())

    sideBsend = threading.Thread(name='sideB send trhead', target=tcpSend, args=(sa, qb))
    sideBsend.start()
    print("started ", sideAsend.getName())

    sideAlisten.join()
    sideBlisten.join()
