import cv2
import numpy as np
import winsound
import time
import _thread
import threading
import socket
import random
from time import sleep
from multiprocessing import Queue
random.seed(time.time())
# -*- coding: utf-8 -*-
"""
@name moduleV2
@author: Bart de Langen
@description: This program is used to detect the way the Rexnord modules are placed. It uses a HD webcam to make an
picture of the bays, then it creates cropped version from it using the coordinates in the dock array variabel.
It then does its image vision magic and sends a dock nummer (for example 2), followed by the side the modulehole is one where 1 equals life
and 2 equals right. so a module that is right placed in bay 1 would be the value "12"

"""

debug = False
#white = 255, black = 0

# 9,2           38, 2




# 9.58          38.58
#
# dock = [[90, 131,             #coordinates of the docks
#          91, 128],
#         [91, 134,
#          210, 247],
#         [89, 134,
#          332, 377],
#         [86, 132,
#          453, 498]
#         ]

dock = [
        [86, 132,
         453, 498],
        [89, 134,
         332, 377],
        [91, 134,
         210, 247],
        [90, 131,             #coordinates of the docks
         91, 128]
        ]

global selectedDock
selectedDock = random.randint(0, len(dock)-1) #select een random begin dock
print(selectedDock)

host = "192.168.0.1"
port = 12345

alpha = 1.4
beta = 20
thresh = 128

def takeImage():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    time.sleep(1)
    return frame

def brightness(image):
    new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return new_image


def loadImage(image):   #loads initial image
    cv2Img = cv2.imread(image)
    return cv2Img


def toGreyscale(image):    #converts image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def cropImage(image, dockNumber):      # crops image acording to dock number
    crop_img = image[dock[dockNumber][0]:dock[dockNumber][1], dock[dockNumber][2]:dock[dockNumber][3]]
    return crop_img


def toBW(image):       # makes grayscale image black and white
    black_image = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return black_image


def erodeImg(image):
    kernel = np.ones((5,5),np.uint8)
    erode = cv2.erode(image,kernel,iterations = 1)
    return erode


def findContours(image, drawImage):
    ret,thresh = cv2.threshold(image,127,255,0)
    im2, contours, hierarchy = cv2.findContours(cv2.bitwise_not(thresh), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, )
    return drawContours(contours, drawImage)


def drawSelectedArea(image, area):
    for dock in area:
        print(dock)
        contour = [np.array([[dock[1], dock[3]], [dock[0], dock[2]]], dtype=np.int32)]
        for cnt in contour:
            cv2.drawContours(image, [cnt], 0, (255, 0, 128), 2)

def drawContours(drawImage):

    backtorgb = cv2.cvtColor(drawImage,cv2.COLOR_GRAY2RGB) #convert an image to color so we can draw a colored countour


    contours34 = [np.array([[len(drawImage)/2-1, 0], [len(drawImage)/2-1, len(drawImage)-1]], dtype=np.int32)] #draws square
    for cnt in contours34:
        cv2.drawContours(backtorgb,[cnt],0,(255,0,0),2)
    return backtorgb


def calculateSide(image):
    # calculate white pixels in left side
    whiteCounterLeft = 0
    for y in range(0, len(image), 1): # loop through x axis
        for x in range(0, int((len(image[0]))/2), 1): #loop through y axis
            if(image[y][x] == 255):
                whiteCounterLeft += 1
    print("left:", whiteCounterLeft)


    # calculate white pixels on right side
    whiteCounterRight = 0
    for y in range(0, len(image), 1): # loop through x axis
        # print(int((len(image[0]))/2))
        # print(len(image)-1)
        for x in range(int((len(image[0]))/2), len(image[0])-1, 1): #loop through y axis
            if (image[y][x] == 255):
                whiteCounterRight += 1
    print("right:", whiteCounterRight)

    if(whiteCounterLeft+ whiteCounterRight > 900):
        print("empty")
        return 3
    elif(whiteCounterLeft > whiteCounterRight):
        return str(selectedDock+1) + str(2)
    elif(whiteCounterRight > whiteCounterLeft):
            return str(selectedDock+1)+ str(1)
    else:
        print("error!")
        return 3



def main():
    global selectedDock
    emptyDock = True
    while emptyDock:
        selectedDock = selectedDock + 1
        if(selectedDock >= len(dock)):
            selectedDock = 0
        print("selected dock is", selectedDock+1)

        unmodifiedImage = takeImage()
        # unmodifiedImage = cv2.flip(unmodifiedImage, 0 )
        # drawSelectedArea(unmodifiedImage, dock)
        cv2.imshow("unmod image", unmodifiedImage)

        # unmodifiedImage = loadImage("loadingDock2.png")
        #
        bright_image = brightness(unmodifiedImage)
        cv2.imshow('bright', bright_image)

        croppedImage = cropImage(bright_image, selectedDock)
        cv2.imshow('cropped', croppedImage)



        grey_image = toGreyscale(croppedImage)
        cv2.imshow('greyImage', grey_image)

        bwImage = toBW(grey_image)
        cv2.imshow('black and white', bwImage)

        erodedImage = erodeImg(bwImage)
        cv2.imshow('black and white', erodedImage)


        contour_image = drawContours(erodedImage)
        cv2.imshow('contour', contour_image)


        # print(len(erodedImage))

        # conTour, smallest, biggest = findContours(erodedImage, erodedImage)
        # cv2.imshow('greyqwdwqImage', conTour)

        result = calculateSide(erodedImage)
        if(result != 3):
            emptyDock = False
        print(result)

        cv2.waitKey(1)  # Waits forever for user to press any key if 0
    return result
    # cv2.destroyAllWindows()  # Closes displayed windows



if __name__ == "__main__":
    if (debug):
        while 1:
            print("result main", main())
            time.sleep(5)
    else:
        while 1:
            try:
                sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sa.connect((host, port))
                # print(sa)
                print("connection astablished to ",host , port)
            except Exception as e:
                print(e)
                print("failed to make connection. Sleep briefly & try again")
                time.sleep(5)
                continue
            print("entering loop")
            while True:

                data = sa.recv(1024)
                if data:
                    data = data.decode('utf-8')
                    print("recieved:", data)
                if data == "63":
                    # cv2.destroyAllWindows()  # Closes displayed windows
                    result = str(main())
                    print("sending: ", result)
                    sa.send(result.encode())
    # while 1:
    #     print(main())
    #     time.sleep(5)

    # main()

