import time
# from easytello import tello
from tkinter import*
import keyboard
from cv2 import aruco
import PIL
import pandas as pd
import cv2 as cv
import numpy as np
import serial
if __name__ == '__main__':
    ser = serial.Serial("COM6", 9600, timeout=1)#"/dev/ttyUSB1"
    ser.flush()

cap = cv.VideoCapture(0);
x=[21]

while(True):
    ret, frame = cap.read()
    # Check if frame is not empty
    if not ret:
        continue

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)

    if ids is not None:
        print("ids type", type(ids))
        print("ids ==", ids)
        print("ids 0", ids[0])
        for i in range(len(ids)):
            c = corners[i][0]
            cv.drawMarker(frame, (c[:, 0].mean(), c[:, 1].mean()), (0,255,255), markerType=cv.MARKER_STAR, markerSize=5, thickness=2, line_type=cv.LINE_AA) 

    
    cv.imshow("frame",frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    if ids is None:
        count = 0
        continue
    elif x in ids:
        count+=1
        print("Marker id=21 detected!")
        if count > 0:
            ser.write(b"s,s,s,\n")
            tx_line = ser.readline().decode('ascii').rstrip()
            print("-----------transmitted data---------")
            print(tx_line)
            if ser.in_waiting > 0:
                rx_line = ser.readline().decode('utf-8').rstrip()
                print("--------received data-------")
                print(rx_line)
        else:
            continue
    else:
        count = 0
        print("Marker id=21 NOT detected!")

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()