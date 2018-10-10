import threading
from multiprocessing import Queue
from time import sleep



import time, threading


def berekenSnelheid(l):
    global interuptCounter, snelheid
    l.acquire()
    snelheid = (2 * 3.14) * (1 / interuptCounter) * 0.05
    l.release()
    time.sleep(1)

if __name__ == '__main__':
    l = threading.Lock()

    snelheidThread = threading.Thread(name='snelheid berekning thread', target=berekenSnelheid,args=(l,) )
    snelheidThread.start()
    print("started ", snelheidThread.getName())

    snelheidThread.join()

    l.acquire()