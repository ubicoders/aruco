
import numpy as np

with np.load("calibration.npz") as data:
    camera_matrix = data['mtx']
    dist_coeffs = data['dist']

print("Camera intrinsic matrix:")
print(camera_matrix)
print(dist_coeffs)
