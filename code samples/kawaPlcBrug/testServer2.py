import socket
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 13338        # Port to listen on (non-privileged ports are > 1023)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    counter = 0
    conn, addr = s.accept()
    print("connection made!")

    while(True):
        conn.send(b"side B rulez")
        print("sended hello2!")
        data = conn.recv(1024)
        # if not data:
        #     break
        string = data.decode('utf-8')
        print("recieved:", string)
        time.sleep(2)

s.close()

