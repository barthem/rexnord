import socket
import time

HOST = '192.168.0.3'  # The server's hostname or IP address
loopback = '127.0.0.1'
PORT = 9000        # The port used by the server
internalPort = 6969


internal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
internal.bind((loopback, internalPort))
internal.listen(1)
conn, addr = internal.accept()
print("connection made!")
while True:
    conn.send(b'hello')
    data = conn.recv(1024)
    string = data.decode('utf-8')
    print(string)
    time.sleep(1)



internal.close()
