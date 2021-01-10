#!/usr/bin/env python
# coding: utf-8

# In[6]:


import time
# from tkinter import*
import keyboard
from cv2 import aruco
import PIL
import pandas as pd
import cv2 as cv
import numpy as np
import math


id2find=[10]
length_of_axis = 0.1
size_of_marker =  0.027 # side lenght of the marker in meter



def getMarkerDistance(frame):

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
#     frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)
    rvecs,tvecs,_objPoints = aruco.estimatePoseSingleMarkers(corners, size_of_marker, cameraMatrix, cameraDistortion)
# GetanglesbetweencameraandmarkerwithID=2
    if ids is not None and id2find in ids:
        for i in range(len(ids)):
           if ids[i] in id2find:
               c = corners[i][0]
#         idx_r ,idx_c =np.where(ids==id2find)
#            print(idx_r)
               tvec=tvecs[i ,:]
               print(tvec)
               print(tvecs)
               rvec=rvecs[i ,:]

#         corners=np.asarray(corners)
#         corners=corners[idx_r,:]
#         corners=np.reshape(corners,[4,2])
               cv.drawMarker(frame, (c[:, 0].mean(), c[:, 1].mean()), (0,255,255), markerType=cv.MARKER_STAR, markerSize=5, thickness=2, line_type=cv.LINE_AA) 
               imaxis = aruco.drawAxis(frame, cameraMatrix, cameraDistortion, rvec, tvec, length_of_axis)
               cv.putText(frame, "%.1f cm -- %.0f deg, %.0f deg, %.0f deg" % ((tvec[0][2] * 100), (rvec[0][0] / math.pi * 180),(rvec[0][1] / math.pi * 180),(rvec[0][2] / math.pi * 180)), (20, 20), cv.FONT_HERSHEY_SIMPLEX, 1.0, (12, 12, 12))
            
    return frame        
        
        # frame_markers
# imgWithAruco=arc.drawRec(imgWithAruco,corners)
#         EulerAngles=aruco.angleFromAruco(rvec,tvec,ids)
#     else:
#          EulerAngles=None
#     if EulerAngles is not None:
#         psi=EulerAngles[0] * 180/math.pi # yaw
#         theta=EulerAngles[1] * 180/math.pi # pitch
#         phi=EulerAngles[2] * 180/math.pi # roll
#        # Correntforrotation
#         psi=angCor(psi)
#         EulerAngles=np.array([psi,theta,phi])
#         EulerAngles_rot=arc.rotate(EulerAngles)
#         alpha=EulerAngles_rot[0,0] # yaw
#         return (alpha,imgWithAruco,tvec)
#     else:
#         return (None,imgWithAruco,None)


def loadCoefficients(path):
    """ Loads camera matrix and distortion coefficients. """
    # FILE_STORAGE_READ
    cv_file = cv.FileStorage(path, cv.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode("camera_matrix").mat()
    dist_matrix = cv_file.getNode("dist_coeff").mat()

    # Debug: print the values
    # print("camera_matrix : ", camera_matrix.tolist())
    # print("dist_matrix : ", dist_matrix.tolist())
    cv_file.release()
    return [camera_matrix, dist_matrix]





mtx, dist = loadCoefficients("calibrationCoefficients_plex.yaml")
cameraMatrix=mtx
cameraDistortion=dist
print("cameraMatrix",cameraMatrix)
print("cameraDistortion",cameraDistortion)
# frame = cv2.imread("aruco_photo.jpg")
cap = cv.VideoCapture(1);
# plt.figure()
# plt.imshow(frame)
# plt.show()


while(True):
# %%time
    ret, frame = cap.read()
        # Check if frame is not empty
    if not ret:
        continue
    getMarkerDistance(frame)   

#     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
#     parameters =  aruco.DetectorParameters_create()
#     corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
#     frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)
#     rvecs,tvecs,_objPoints = aruco.estimatePoseSingleMarkers(corners, size_of_marker , cameraMatrix, cameraDistortion)

#     print(tvecs)

#     tvec=np.asarray(tvecs).tolist()
#     print(tvecs)
#     print(tvec)
#     dist_x =tvecs[0,0]
#     dist_y =tvecs[0,1]
#     dist_z =tvecs[0,2]
        
#     dist=sqrt(dist_x^2+dist_y^2+dist_z^2)
#     except ValueError:
#         print ( "err")

# # # plt.figure()
# # # plt.imshow(frame_markers)
# #     if type(ids)!=NoneType:
#     if ids is not None:
# #         print(type(ids))
#         for i in range(len(ids)):
#             c = corners[i][0]
# #             print(([c[:, 0]]))
# #             print(c.size)
# #             print((c[:, 0].mean()))
#             cv.drawMarker(frame, (c[:, 0].mean(), c[:, 1].mean()), (0,255,255), markerType=cv.MARKER_STAR, markerSize=5, thickness=2, line_type=cv.LINE_AA) 
#             imaxis = aruco.drawAxis(frame_markers, cameraMatrix, cameraDistortion, rvecs[i], tvecs[i], length_of_axis)
            
    
    cv.imshow("frame",frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()


# In[5]:


mtx


# In[3]:


dist


# In[ ]:




