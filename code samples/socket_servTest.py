import socket

HOST = '145.52.172.196'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while(True):
        conn, addr = s.accept()
        data = conn.recv(1024)
        print(data)
s.close()
