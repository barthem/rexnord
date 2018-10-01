import socket
import time

HOST = '192.168.0.3'  # The server's hostname or IP address
InternalHost = '127.0.0.1'
PORT = 9000        # The port used by the server
internalPort = 6969

internal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
internal.connect((InternalHost, internalPort))
print("connection made!")
while True:
    data = internal.recv(1024)
    string = data.decode('utf-8')
    print(string)
    internal.send(b"hello back")
    time.sleep(1)


internal.close()
