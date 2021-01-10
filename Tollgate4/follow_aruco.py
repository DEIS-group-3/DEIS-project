import time
# from easytello import tello
from tkinter import*
import keyboard
from cv2 import aruco
import PIL
import pandas as pd
import cv2 as cv
import numpy as np

id2find=24

def getMarkerAngles(cap):
# Readimageframefromcamera
    ret, frame = cap.read()
# Undistorttheframe
#     if not ret:
#           continue
    return 0
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)
    rvecs,tvecs,_objPoints = aruco.estimatePoseSingleMarkers(corners, size_of_marker , cameraMatrix, cameraDistortion)
# GetanglesbetweencameraandmarkerwithID=2
    if ids is not None and id2find in ids:
        idx_r ,idx_c =np.where(ids==id2find)
        tvec=tvec[idx_r ,:]
        rvec=rvec[idx_r ,:]
# drawrectanglearoundmarkerwithID=2
#         corners=np.asarray(corners)
        corners=corners[idx_r,:]
        corners=np.reshape(corners,[4,2])
        cv.drawMarker(frame, (c[:, 0].mean(), c[:, 1].mean()), (0,255,255), markerType=cv.MARKER_STAR, markerSize=5, thickness=2, line_type=cv.LINE_AA) 
        imaxis = aruco.drawAxis(frame_markers, cameraMatrix, cameraDistortion, rvecs[i], tvecs[i], length_of_axis)
# frame_markers
# imgWithAruco=arc.drawRec(imgWithAruco,corners)
        EulerAngles=aruco.angleFromAruco(rvec,tvec,ids)
    else:
        EulerAngles=None
    if EulerAngles is not None:
        psi=EulerAngles[0] * 180/math.pi # yaw
        theta=EulerAngles[1] * 180/math.pi # pitch
        phi=EulerAngles[2] * 180/math.pi # roll
       # Correntforrotation
        psi=angCor(psi)
        EulerAngles=np.array([psi,theta,phi])
        EulerAngles_rot=arc.rotate(EulerAngles)
        alpha=EulerAngles_rot[0,0] # yaw
        return (alpha,imgWithAruco,tvec)
    else:
        return (None,imgWithAruco,None)


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


length_of_axis = 0.1
size_of_marker =  0.0322 # side lenght of the marker in meter
mtx, dist = loadCoefficients("calibrationCoefficients.yaml")
cameraMatrix=mtx
cameraDistortion=dist

# frame = cv2.imread("aruco_photo.jpg")
cap = cv.VideoCapture(0);
# plt.figure()
# plt.imshow(frame)
# plt.show()


while(True):
# %%time
    ret, frame = cap.read()
        # Check if frame is not empty
    if not ret:
        continue
        
#     print(ret)
#     cv.imshow("frame",frame)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)

##    rvecs,tvecs,_objPoints = aruco.estimatePoseSingleMarkers(corners, size_of_marker , cameraMatrix, cameraDistortion)
#     cv.imshow("frame",frame)
##    print(tvecs)
#     try:
##    tvec=np.asarray(tvecs).tolist()
##    print(tvecs)
#     tvec=np.reshape(tvec,[1,3])
##    print(tvec)
#     dist_x =tvecs[0,0]
#     dist_y =tvecs[0,1]
#     dist_z =tvecs[0,2]
        
#     dist=sqrt(dist_x^2+dist_y^2+dist_z^2)
#     except ValueError:
#         print ( "err")

# # plt.figure()
# # plt.imshow(frame_markers)
#     if type(ids)!=NoneType:
    if ids is not None:
#         print(type(ids))
        for i in range(len(ids)):
            c = corners[i][0]
#             print(([c[:, 0]]))
#             print(c.size)
#             print((c[:, 0].mean()))
            cv.drawMarker(frame, (c[:, 0].mean(), c[:, 1].mean()), (0,255,255), markerType=cv.MARKER_STAR, markerSize=5, thickness=2, line_type=cv.LINE_AA) 
##            imaxis = aruco.drawAxis(frame_markers, cameraMatrix, cameraDistortion, rvecs[i], tvecs[i], length_of_axis)
            
# frame_markers
# plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "o", label = "id={0}".format(ids[i]))
# #     plt.legend()
# #     plt.show()
    
    cv.imshow("frame",frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()





# def dist_bwn_uco(data):
#     l = data.shape[0]//2
#     corners = data[["c1", "c2", "c3", "c4"]].values.reshape(l, 2,4)
#     c1 = corners[:, :, 0]
#     c2 = corners[:, :, 1]
#     c3 = corners[:, :, 2]
#     c4 = corners[:, :, 3]
#     e1 = c2-c1
#     e2 = c3-c2
#     e3 = c4-c3
#     e4 = c1-c4
#     a = -.5 * (np.cross(-e1, e2, axis = 1) + np.cross(-e3, e4, axis = 1))
#     return a

#size of borders of 1 uco
# def size_uco(data):
#     l = data.shape[0]//2
#     corners = data[["c1", "c2", "c3", "c4"]].values.reshape(l, 2,4)
#     c1 = corners[:, :, 0]
#     c2 = corners[:, :, 1]
#     c3 = corners[:, :, 2]
#     c4 = corners[:, :, 3]
#     e1 = c2-c1
#     e2 = c3-c2
#     e3 = c4-c3
#     e4 = c1-c4
#     a = -.5 * (np.cross(-e1, e2, axis = 1) + np.cross(-e3, e4, axis = 1))
#     return a

# corners2 = np.array([c[0] for c in corners])

# data = pd.DataFrame({"x": corners2[:,:,0].flatten(), "y": corners2[:,:,1].flatten()},
#                    index = pd.MultiIndex.from_product(
#                            [ids.flatten(), ["c{0}".format(i )for i in np.arange(4)+1]],
#                        names = ["marker", ""] ))

# data = data.unstack().swaplevel(0, 1, axis = 1).stack()
# data["m1"] = data[["c1", "c2"]].mean(axis = 1)
# data["m2"] = data[["c2", "c3"]].mean(axis = 1)
# data["m3"] = data[["c3", "c4"]].mean(axis = 1)
# data["m4"] = data[["c4", "c1"]].mean(axis = 1)
# data["o"] = data[["m1", "m2", "m3", "m4"]].mean(axis = 1)
# data

mtx

dist



