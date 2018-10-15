import cv2
import numpy as np

#white = 255, black = 0

# 9,2           38, 2




# 9.58          38.58

dock = [[129 , 191,
         208, 258],
        [128, 188,
         326, 375]]



image = cv2.imread('loadingDock2.png')
startPosition = cv2.imread('initial.png')
cv2.imshow('sffr', image)

# End of Code

def toGreyscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image



crop_img = image[dock[0][0]:dock[0][1], dock[0][2]:dock[0][3]]
cv2.imshow('gray_image', crop_img)

grey_image=toGreyscale(crop_img)

thresh = 120
black_image = cv2.threshold(grey_image, thresh, 255, cv2.THRESH_BINARY)[1]
cv2.imshow('black image', black_image)



kernel = np.ones((5,5),np.uint8)
erode = cv2.erode(black_image,kernel,iterations = 1)
cv2.imshow('erode', erode)


ret,thresh = cv2.threshold(erode,127,255,0)
im2, contours, hierarchy = cv2.findContours(cv2.bitwise_not(thresh), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, )
# print(contours[0])
print(contours[0][0][0][0]) #contours[countour][element][keep 0][key])

# calculates the smallest [0][0] and the biggest [100][100] value to make a square
biggest = [0, 0]
smallest = [10000, 10000]
for cnt in contours:
    for x in range(len(cnt)):
        # print(cnt[x][0])
        if(cnt[x][0][0] > biggest[0] and cnt[x][0][1] > biggest[1]):
            biggest = [cnt[x][0][0], cnt[x][0][1]]
            print("new biggest:", biggest)
        if(cnt[x][0][0] < smallest[0] and cnt[x][0][1] < smallest[1]):
            smallest = [cnt[x][0][0], cnt[x][0][1]]
            print("new smallest:", smallest)
    print("endResult:", " smallest:", smallest, " biggest:", biggest, [smallest[0], biggest[1]])
    # print(smallest[1])


backtorgb = cv2.cvtColor(black_image,cv2.COLOR_GRAY2RGB) #convert an image to color so we can draw a colored countour

cnt = contours[0]
M = cv2.moments(cnt)
# cv2.drawContours(backtorgb, contours, -1, (0,255,0), 3)


contours34 = [np.array([smallest, [smallest[0], biggest[1]], biggest, [biggest[0], smallest[1]]], dtype=np.int32)] #draws square
for cnt in contours34:
    print("new")
    print(type(cnt))
    cv2.drawContours(backtorgb,[cnt],0,(255,0,0),2)
cv2.imshow('final?', backtorgb)
print(len(backtorgb))

print(black_image[0][0])

rightSide= [[50 for x in range(int(biggest[0]/2)+1)] for y in range(biggest[1]+1)]
# leftSide = [[50 for x in range(500)] for y in range(500)]
leftSide= [[50 for x in range(int(biggest[0]/2)+1)] for y in range(biggest[1]+1)]
print("lenghte leftside:", len(leftSide[0]))

print(type(biggest))
print("biggest1:", biggest[1], int(biggest[0]/2))
# fill leftSide list
whiteCounterLeft = 0
for y in range(smallest[1], biggest[1], 1): # loop through x axis
    for x in range(smallest[0], int(biggest[0]/2), 1): #loop through y axis
        if(black_image[y][x] == 255):
            whiteCounterLeft += 1
print("left:", whiteCounterLeft)

#
# fill rightSide list
whiteCounterRight = 0
for y in range(smallest[1], biggest[1], 1): # loop through x axis
    # print("y", y)
    for x in range(int(biggest[0]/2),biggest[0] , 1): #loop through y axis
        if (black_image[y][x] == 255):
            whiteCounterRight += 1
print("left:", whiteCounterRight)


cv2.waitKey(0)  # Waits forever for user to press any key
cv2.destroyAllWindows()  # Closes displayed windows