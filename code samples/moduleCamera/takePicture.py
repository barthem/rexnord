import numpy as np
import cv2


# for i in range(50, -1, -1):
#     print("trying numbero: " , i)
#     cap = cv2.VideoCapture(i)
#     if cap.isOpened() is True:
#         print("found camera at: ", i, cap)
#         ret, frame = cap.read()
#         print(ret, frame)
#
cap = cv2.VideoCapture(50)
while cap.isOpened() is False:
    pass
print(cap)
#
while True:
# Capture frame-by-frame
    ret, frame = cap.read()
    print(ret, frame)
# do what you want with frame
#  and then save to file
cv2.imwrite('test.png', frame)

# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()