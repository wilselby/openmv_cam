#!/usr/bin/env python2.7

# Python libraries
import sys, serial, struct, time, os

# Import OpenCV
import cv2
import numpy as np


port = '/dev/openmvcam'
serial_port = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
         xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=None, dsrdtr=True)

# Check for calibration data
cal_path = './calibration/output/calib.npz'
calibration = 0
if os.path.isfile(cal_path):
    cal = np.load(cal_path)
    K = cal['camera_matrix']
    D = cal['dist_coefs']
    calibration = 1

while True:
    # Read data from the serial buffer
    serial_port.write("snap")
    serial_port.flush()
    size = struct.unpack('<L', serial_port.read(4))[0]
    buf = serial_port.read(size)

    # Use numpy to construct an array from the bytes
    x = np.fromstring(buf, dtype='uint8')

    # Decode the array into an image
    img = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)

    # Undistort the image if calibration exists
    if calibration:
        DIM = img.shape[1::-1]
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
        img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    cv2.imshow("Stream:", img)
    key = cv2.waitKey(20)
    #print(key)

    if key == 27:
        #seial_port.close()
        cv2.destroyWindow("Stream:")  
	break      

         
