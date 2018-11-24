#!/usr/bin/env python2.7

# Python libraries
import sys, serial, struct, time

# Import OpenCV
import cv2
import numpy as np


port = '/dev/openmvcam'
serial_port = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
         xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=None, dsrdtr=True)

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

    cv2.imshow("Stream:", img)
    key = cv2.waitKey(20)
    print(key)

    if key == 27:
        #seial_port.close()
        cv2.destroyWindow("Stream:")  
	break      

         
