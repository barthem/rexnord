import cv2
import numpy as np

#white = 255, black = 0

# 9,2           38, 2




# 9.58          38.58

dock = [[129 , 191,             #coordinates of the docks
         208, 258],
        [128, 188,
         326, 375]]

host = "192.168.0.1"
port = 12345



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
    thresh = 120
    black_image = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
    return black_image


def erodeImg(image):
    kernel = np.ones((5,5),np.uint8)
    erode = cv2.erode(image,kernel,iterations = 1)
    return erode


def findContours(image, drawImage):
    ret,thresh = cv2.threshold(image,127,255,0)
    im2, contours, hierarchy = cv2.findContours(cv2.bitwise_not(thresh), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, )
    return drawContours(contours, drawImage)


def drawContours(contours, drawImage):
    # calculates the smallest [0][0] and the biggest [100][100] value to make a square
    biggest = [0, 0]
    smallest = [10000, 10000]
    for cnt in contours:
        for x in range(len(cnt)):
            if(cnt[x][0][0] > biggest[0] and cnt[x][0][1] > biggest[1]):
                biggest = [cnt[x][0][0], cnt[x][0][1]]
            if(cnt[x][0][0] < smallest[0] and cnt[x][0][1] < smallest[1]):
                smallest = [cnt[x][0][0], cnt[x][0][1]]
    backtorgb = cv2.cvtColor(drawImage,cv2.COLOR_GRAY2RGB) #convert an image to color so we can draw a colored countour

    cnt = contours[0]

    contours34 = [np.array([smallest, [smallest[0], biggest[1]], biggest, [biggest[0], smallest[1]]], dtype=np.int32)] #draws square
    for cnt in contours34:
        cv2.drawContours(backtorgb,[cnt],0,(255,0,0),2)
    return backtorgb, smallest, biggest




def calculateSide(image, smallest, biggest):
    # calculate white pixels in left side
    whiteCounterLeft = 0
    for y in range(smallest[1], biggest[1], 1): # loop through x axis

        for x in range(smallest[0], int(biggest[0]/2), 1): #loop through y axis
            if(image[y][x] == 255):
                whiteCounterLeft += 1
    print("left:", whiteCounterLeft)


    # calculate white pixels on left side
    whiteCounterRight = 0
    for y in range(smallest[1], biggest[1], 1): # loop through x axis
        for x in range(int(biggest[0]/2),biggest[0] , 1): #loop through y axis
            if (image[y][x] == 255):
                whiteCounterRight += 1
    print("left:", whiteCounterRight)

    if(whiteCounterLeft > whiteCounterRight):
        return 1
    elif(whiteCounterRight > whiteCounterLeft):
            return 2
    else:
        print("error!")
        return -1



def main():
    unmodifiedImage = loadImage("loadingDock2.png")

    croppedImage = cropImage(unmodifiedImage, 1)

    grey_image = toGreyscale(croppedImage)
    cv2.imshow('greyImage', grey_image)

    bwImage = toBW(grey_image)

    erodedImage = erodeImg(bwImage)

    conTour, smallest, biggest = findContours(erodedImage, erodedImage)
    cv2.imshow('greyqwdwqImage', conTour)

    result = calculateSide(erodedImage, smallest, biggest)
    print(result)

    cv2.waitKey(0)  # Waits forever for user to press any key
    cv2.destroyAllWindows()  # Closes displayed windows

    return result

if __name__ == "__main__":
    main()
    pass
