import numpy as np
import cv2.aruco as aruco
import cv2, time


aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
arucoParameters = aruco.DetectorParameters_create()

cap = cv2.VideoCapture('aruco.mp4')

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
while(True):
    s = time.time()
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=arucoParameters)
    print(time.time() - s)
    img = aruco.drawDetectedMarkers(frame, corners)
    # Display the resulting frame
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()