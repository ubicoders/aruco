import numpy as np
import cv2.aruco as aruco
import cv2, time

img = cv2.imread('aruco0.jpg')
img = cv2.resize(img, (1920, 1080))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
arucoParameters = aruco.DetectorParameters_create()

s = time.time()
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=arucoParameters)
e = time.time()-s

img = aruco.drawDetectedMarkers(img, corners)

# cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
cv2.imshow('Display', img)
cv2.waitKey(-1)

print(e)

print(corners)
print(ids)
print(rejectedImgPoints)