import numpy as np
import cv2.aruco as aruco
import cv2, time

def rotation_matrix_to_euler_angles(R):
    """
    Converts a rotation matrix to Euler angles (in radians).
    """
    sy = np.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(R[2, 1], R[2, 2])
        y = np.arctan2(-R[2, 0], sy)
        z = np.arctan2(R[1, 0], R[0, 0])
    else:
        x = np.arctan2(-R[1, 2], R[1, 1])
        y = np.arctan2(-R[2, 0], sy)
        z = 0
    return np.array([x, y, z])

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# Load camera calibration parameters from the saved file
with np.load("cam_calibrator/calibration.npz") as data:
    camera_matrix = data['mtx']
    dist_coeffs = data['dist']

marker_size = 0.09

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)
img = None
while(True):
    s = time.time()
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
    print(time.time() - s)
    print(ids)
    print(corners)
    #img = aruco.drawDetectedMarkers(frame, corners)

    if ids is not None:
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, dist_coeffs)
        

        for i in range(len(ids)):
            R, _ = cv2.Rodrigues(rvecs[i])
            # Draw axis for the ArUco marker
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], 0.1)
            
            # Calculate distance to the marker
            distance = np.linalg.norm(tvecs[i])
            print(f"Distance to marker {ids[i]}: {distance:.2f} meters")
            print(f"Rotation vector: {rvecs[i]}")
            euler_angles = rotation_matrix_to_euler_angles(R)
            print(f"Euler angles: {np.degrees(euler_angles)}")

        
            # Draw the detected markers and their axes
            img = aruco.drawDetectedMarkers(frame, corners, ids)
    else:
        img = frame

    # Display the resulting frame
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()