import cv2
import numpy as np
import winsound
import time
import _thread
import threading
import socket
from time import sleep
from multiprocessing import Queue

#white = 255, black = 0

# 9,2           38, 2




# 9.58          38.58

dock = [[122 , 180,             #coordinates of the docks
         206, 252],
        [134, 182,
         329, 378]]
global selectedDock
selectedDock = len(dock)

host = "192.168.0.1"
port = 12345

alpha = 1.4
beta = 20
thresh = 128

# global selectedDock


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

def drawContours2(contours, drawImage):

    backtorgb = cv2.cvtColor(drawImage,cv2.COLOR_GRAY2RGB) #convert an image to color so we can draw a colored countour

    cnt = contours[0]

    contours34 = [np.array([smallest, [smallest[0], biggest[1]], biggest, [biggest[0], smallest[1]]], dtype=np.int32)] #draws square
    for cnt in contours34:
        cv2.drawContours(backtorgb,[cnt],0,(255,0,0),2)
    return backtorgb, smallest, biggest

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

    if(whiteCounterLeft+ whiteCounterRight > 1600):
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
    selectedDock = selectedDock + 1
    if(selectedDock >= len(dock)):
        selectedDock = 0
    print("selected dock is", selectedDock)

    unmodifiedImage = takeImage()
    # unmodifiedImage = cv2.flip(unmodifiedImage, 0 )
    drawSelectedArea(unmodifiedImage, dock)
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


    print(len(erodedImage))

    # conTour, smallest, biggest = findContours(erodedImage, erodedImage)
    # cv2.imshow('greyqwdwqImage', conTour)

    result = calculateSide(erodedImage)
    print(result)

    cv2.waitKey(5)  # Waits forever for user to press any key if 0
    return result
    # cv2.destroyAllWindows()  # Closes displayed windows



if __name__ == "__main__":
    while 1:
        try:
            sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sa.connect((host, port))
            # print(sa)
            print("connection astablished to ",host , port)
        except:
            print("failed to make connection. Sleep briefly & try again")
            time.sleep(5)
            continue

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
    #     # time.sleep(1)

    # main()

