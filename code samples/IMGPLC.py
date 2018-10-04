# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 09:23:17 2018

@author: Jeremy Tiebosch
"""
# All imports
import cv2
import numpy as np
import telnetlib as tl
import math
import socket
import struct
import sys

# --------- Classes ---------- #
class socketConnector():
    def __init__(self):
        self.tcpip = '192.168.0.3' # PLC IP
        self.port = 2000 # Port of the PLC
        self.bsize = 1024 # Buffer size
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
        valid_byte = bytearray()
        valid_byte.append(data)
        self.connection.send(valid_byte)

class imageManipulation():
    def __init__(self):
        self.img = None
        self.minInlierDist = 2.0
        
    def rescale(self, frame):
        r = 768.0 / frame[1]
        dim = (768, int(frame.shape[0] * r))
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        return frame
        
    def getFrame(self):
        #send TELNET command to capture image
        #print()
        #tn.write(b"SE8r\n")
        
        #wait until TELNET reply has been received
        #tn.read_until("1")
        
        #retrieve image
        self.img = cv2.imread('4.BMP')
        
        
    def grayScale(self, frame):
        grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return grayframe
        
    def invert(self, frame):
        frame = cv2.bitwise_not(frame)
        return frame
        
    def blurFrame(self, frame):
        blurframe = cv2.blur(frame, (5,5))
        return blurframe
        
    def edgeFrame(self, frame):
        edgeframe = cv2.Canny(frame, 100, 200)
        return edgeframe
        
    def dilateFrame(self, frame):
        dilateframe= cv2.dilate(frame, None, iterations=1)
        dilateframe = cv2.erode(dilateframe, None, iterations=2)
        return dilateframe
        
    def threshFrame(self, frame):
        threshframe = cv2.adaptiveThreshold(frame, 255, 1,1,11,2)
        return threshframe
    
    def blackWhite(self, frame):
        bw = cv2.threshold(frame, 127,255,cv2.THRESH_BINARY)[1]
        return bw
        
    def detectCircles(self, frame):
        circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT,1,60,param1=100,param2=30,minRadius=50,maxRadius=140)
        bwframe = self.blackWhite(frame)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                radius = i[2]
                print(math.pow(radius, 2) * math.pi)
                carea = math.pow(radius, 2) * math.pi
                
                if carea > 8000 :                    
                    missing = 0
                    counter = 0
                    maxInlierDist = radius/25
                    
                    if(maxInlierDist<self.minInlierDist): 
                        maxInlierDist = self.minInlierDist
                    for t in np.arange(0.0, 2*math.pi, 0.1) :
                        counter += 1
                        cX = radius * math.cos(t) + i[0]
                        cY = radius * math.sin(t) + i[1]
                        cX = int(cX)
                        cY = int(cY)
                        try:
                            px= frame[cX,cY]
                            #print(px)
                            cv2.circle(frame, (cX,cY), 10, (255,0,0), 2 )
                            if(px <= 10):
                                missing += 1
                        except:
                            missing += 1
                        
                        
                else :
                    print("Pin too small")
                percentage = 100 - ((missing/counter)*100)
                print("Percentage of circle : ", 100 - (missing/counter*100), "%")
                if percentage < 90:
                    print("Defect pin")
                    return 0
                else:
                    print("Valid pin")
                    return 1
                # draw the outer circle
                cv2.circle(frame,(i[0],i[1]),i[2],(255,0,0),2)
                # draw the center of the circle
                #cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)                
                
        else :
            print("No pinhead found")
            return 0
                
    def contours(self, frame):
        im2, contours, hierarchy = cv2.findContours(frame,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            [x,y,w,h] = cv2.boundingRect(cnt)
            if h > 40 and w > 20:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,0),2)
                pin = self.img[y:y+h, x:x+w]
                
        return pin

# ----------- End of classes ---------- #

# ------------   Code  ---------------- #

sc = socketConnector()
sc.connect()
im = imageManipulation()

while True:       
    sc.waitForData()
    
    host = "192.168.0.20"
    port = "10000"
    user = "admin"
    
    #tn = tl.Telnet(host, port)
    #tn.write(user +  b"/r/n")
    #tn.write(b"/r/n")
    

    
    im.getFrame()
    frame = im.grayScale(im.img)
    cv2.imwrite('pinhead1.png', frame)
    frame = im.threshFrame(frame)
    frame = im.contours(frame)
    cv2.imwrite('pinhead2.png', frame)
    #frame = im.detectCircles(frame)
    
    frame = im.grayScale(frame)
    #frame = im.threshFrame(frame)
    valid = im.detectCircles(frame)
    cv2.imwrite('pinhead3.png', frame)
    
    sc.sendData(valid)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    