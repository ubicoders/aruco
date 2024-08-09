import cv2
import numpy as np

# Define the dimensions of the checkerboard (number of internal corners)
CHECKERBOARD = (6, 9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Create arrays to store object points and image points from all images.
objpoints = []  # 3d points in real world space
imgpoints = []  # 2d points in image plane.

# Prepare the object points based on the checkerboard dimensions
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= 19 # 19 mm square size

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Find the checkerboard corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        # If corners are found, add object points, image points (after refining them)
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        frame = cv2.drawChessboardCorners(frame, CHECKERBOARD, corners2, ret)
        print("Checkerboard detected and corners refined.")
        index += 1
        print(f"Frame {index} captured.")
    else:
        print("Checkerboard not detected in this frame.")
    
    cv2.imshow('Calibration', frame)
    cv2.waitKey(1000)
    
    # Break the loop with the 'q' key
    if index >= 20:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if len(objpoints) < 10:
    print("Error: Not enough valid frames captured for calibration. Please capture more frames.")
else:
    print("Calibrating camera...")
    # Calibration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # Output the camera intrinsic matrix
    print("Camera intrinsic matrix:")
    print(mtx)
    print(dist)

    # Optional: save the intrinsic matrix and distortion coefficients
    np.savez("calibration.npz", mtx=mtx, dist=dist)

    print("Calibration completed and results saved.")

