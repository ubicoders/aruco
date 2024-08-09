import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl

def mm2pixel(mm):
    test_pixel = 603
    exp_mm = 80
    return int(mm*test_pixel/exp_mm)

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)
w, h = 1920, 1400 # good for letter size paper
board = np.ones((h, w))*255
gap = 75
mSize = mm2pixel(90) 
print(mSize)
nx = int(w / (mSize+gap))
ny = int(h / (mSize+gap))

# rSize = mm2pixel(160)
# rect = np.zeros((rSize, rSize, 3))

index = 0
index_des = 10
while index<index_des :
    for i in range(0, nx):
        for j in range(0, ny):
            img = aruco.generateImageMarker(aruco_dict, index, mSize) 
            print(img.shape)
            sIndex_x = gap*(j+1) + j*mSize
            sIndex_y = gap*(i+1) + i*mSize
            board[sIndex_x:sIndex_x+mSize, sIndex_y:sIndex_y+mSize] = img
            index += 1
    cv2.imwrite(f"./4x4/{index-1}.png", board)

#cv2.imshow('asdf', board)
#cv2.waitKey(-1)


# opencv-contrib-python  4.5.1.48
# opencv-python          4.5.1.48





