import cv2
import numpy as np


dock = [[281, 357,
         214, 279],
        [271, 360,
        331, 400]]

thresh = 10

image = cv2.imread('loadingDock.png')
startPosition = cv2.imread('initial.png')
cv2.imshow('sffr', image)

# End of Code

def toGreyscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image



crop_img = image[dock[1][0]:dock[1][1], dock[1][2]:dock[1][3]]
cv2.imshow('gray_image', crop_img)

grey_image=toGreyscale(crop_img)

thresh = 120
black_image = cv2.threshold(grey_image, thresh, 255, cv2.THRESH_BINARY)[1]
cv2.imshow('black iamge', black_image)



kernel = np.ones((5,5),np.uint8)
erode = cv2.dilate(black_image,kernel,iterations = 2)
cv2.imshow('erode', erode)


ret,thresh = cv2.threshold(erode,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, )

print(contours)

backtorgb = cv2.cvtColor(erode,cv2.COLOR_GRAY2RGB)

cnt = contours[0]
M = cv2.moments(cnt)
cv2.drawContours(backtorgb, contours, -1, (0,255,0), 3)


# epsilon = 0.1*cv2.arcLength(cnt,True)
# approx = cv2.approxPolyDP(cnt,epsilon,True)
#
# cv2.drawContours(backtorgb,[approx],-1,(0,255,0),3)


print(M)

cv2.imshow('final', backtorgb)



# kernel = np.ones((5,5),np.uint8)
# erode = cv2.dilate(crop_img,kernel,iterations = 2)



# cv2.imshow('color_image', image)
# cv2.imshow('erode', erode)
# cv2.imshow('gray_image', crop_img)

# image = np.ones((5,5),np.uint8)
# erode = cv2.dilate(crop_img,kernel,iterations = 2)

# im = cv2.imread('loadingDock.png')
# imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
# ret,thresh = cv2.threshold(imgray,127,255,0)
#
# im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
# cv2.drawContours(im2, contours, -1, (0, 255, 0), 3)
# cv2.imshow('countour', im2)


cv2.waitKey(0)  # Waits forever for user to press any key
cv2.destroyAllWindows()  # Closes displayed windows