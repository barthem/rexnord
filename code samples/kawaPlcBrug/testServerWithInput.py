import socket
import time

HOST = '192.168.0.25'  # Standard loopback interface address (localhost)
PORT = 9000        # Port to listen on (non-privileged ports are > 1023)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    counter = 0
    conn, addr = s.accept()
    print("connection made!")

    while(True):
        data = str(input("data to input?"))
        conn.send(data.encode())
        print("sending:", data)
        data = conn.recv(1024)
        print(data)
        # if not data:
        #     break
        string = data.decode('utf-8')
        print("recieved:", string)

s.close()

