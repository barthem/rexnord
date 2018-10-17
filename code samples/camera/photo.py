import getpass
import telnetlib
from ftplib import FTP
import cv2
import time


HOST = "192.168.0.58"
port = 10001
user = 'admin'
password = ''
debug = True



def takePhoto():
    tn = telnetlib.Telnet(host=HOST, port=port)
    if(debug):
        tn.set_debuglevel(1)
    tn.read_until(b'User: ')
    tn.write(b"admin\r\n")  # the user name is admin
    tn.read_until(b'Password: ')
    tn.write(b"\r\n")  # there is no password - just return - now logged in
    tn.read_until(b'User Logged In')
    tn.write(b"SE8\r\n")  # Take picture and save it as image.jpg
    tn.close()

def downloadPhoto():
    ftp = FTP(HOST)
    if(debug):
        ftp.set_debuglevel(level=1)

    ftp.login(user)
    ftp.retrbinary('RETR image.jpg', open('image.jpg', 'wb').write)

    ftp.close()


while(True):
    # Capture frame-by-frame
    takePhoto()
    downloadPhoto()
    image = cv2.imread('image.jpg')
    cv2.imshow('sffr', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # time.sleep(0.1)

