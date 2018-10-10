import cv2
import numpy as np

img = cv2.imread('wierdblop.png')

gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


ret,thresh = cv2.threshold(gray_image,127,255,0)


cv2.imshow('sffefefr', thresh)

im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnt = contours[0]
M = cv2.moments(cnt)
# cv2.drawContours(img, contours, 1, (0,255,0), 3)

epsilon = 0.1*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)

cv2.drawContours(img,[approx],-1,(0,255,0),3)

print(M)
cv2.imshow('sffr', img)
cv2.waitKey(0)  # Waits forever for user to press any key
cv2.destroyAllWindows()  # Closes displayed windows