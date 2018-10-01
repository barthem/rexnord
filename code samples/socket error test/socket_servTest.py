import socket

HOST = '192.168.0.25'  # Standard loopback interface address (localhost)
PORT = 9000        # Port to listen on (non-privileged ports are > 1023)

try:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        counter = 0
        conn, addr = s.accept()
        print("connection made!")

        while(True):
            data = conn.recv(1024)
            if not data:
                break
            string = data.decode('utf-8')
            print(string)

            # if(counter != int(data)):
            #     print("errrrrorrrrrr")
            #     break
            # else:
            #     counter += 1
    s.close()


except Exception as inst:
    s.close()
