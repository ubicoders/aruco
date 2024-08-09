import cv2
import numpy as np
w, h = 1920, 1400
board = np.zeros((h, w, 3))
boarder = 5
c = np.ones((h-boarder*2, w-boarder*2, 3))
board[boarder:h-boarder, boarder:w-boarder] = c
cv2.imshow('asdf', board)
cv2.waitKey(-1)

