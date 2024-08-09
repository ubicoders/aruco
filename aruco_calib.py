import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
from aruco_utils import *


aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_1000)
w, h = 1920, 1400
board = np.ones((h, w))*255
gap = 5
mSize = test_pixel
nx = 1
ny = 1

index = 0
for i in range(0, nx):
    for j in range(0, ny):
        img = aruco.drawMarker(aruco_dict, index, mSize)
        sIndex_x = gap*(j+1) + j*mSize
        sIndex_y = gap*(i+1) + i*mSize
        board[sIndex_x:sIndex_x+mSize, sIndex_y:sIndex_y+mSize] = img
        index += 1

cv2.imwrite('./calibration.png', board)




