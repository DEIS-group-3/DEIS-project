#!/usr/bin/env python
# coding: utf-8

# # Camera calibration using CHARUCO

# In[1]:


import numpy as np
import cv2, PIL, os
from cv2 import aruco
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
#get_ipython().run_line_magic('matplotlib', 'nbagg')

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
board = aruco.CharucoBoard_create(7, 5, 1, .8, aruco_dict)
#imboard = board.draw((2000, 2000))
'''
# ## 2. Camera pose estimation using CHARUCO chessboard
# 
# First, let's create the board consisting from aruco markers in our desired aruco_dict. Then we need to print it!
# 

# In[32]:


workdir = ".\calib_cam"
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
#board = aruco.CharucoBoard_create(7, 5, 1, .8, aruco_dict)
#imboard = board.draw((2000, 2000))
# cv2.imwrite(workdir + "/chessboard.tiff", imboard)
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# plt.imshow(imboard, cmap = mpl.cm.gray, interpolation = "nearest")
# ax.axis("off")
# plt.show()


# Then let's shot a video from our camera and save it on our working directory. On the video we should have the chessboard under different angles.

# In[33]:



# # define a video capture object 
vid = cv2.VideoCapture(0) 
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
videoWriter = cv2.VideoWriter("calib2.avi", fourcc, 30.0, (640,480))
 
  
while(True): 
      
     # Capture the video frame 
     # by frame 
    ret, frame = vid.read()
    if (ret != True):
        break
    
    # Display the resulting frame 
    cv2.imshow('frame', frame)
    videoWriter.write(frame)
    
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

# After the loop release the cap object 
vid.release()
videoWriter.release()
# Destroy all the windows 
cv2.destroyAllWindows() 
'''
'''
# Then let's make a bunch of pictures - screenshots from this video, and save it in separate folder.

# In[20]:


import math

videoFile = "./calib_cam/calib2.avi"
imagesFolder = "./calib_cam/"
cap = cv2.VideoCapture(videoFile)
frameRate = 10 #frame rate
while(cap.isOpened()):
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
#     print(frameId%math.floor(frameRate))
    if (frameId%math.floor(frameRate) == 0):
#         print(frameId%math.floor(frameRate))
        filename = imagesFolder + "\image_" +  str(int(frameId)) + ".png"
        cv2.imwrite(filename, frame)
cap.release()
print ("Done!")

'''
# Let's take all those photos.

# In[34]:



datadir = "calib_pics/"
images = np.array([ datadir + f for f in os.listdir(datadir) if f.endswith(".png") ])
order = np.argsort([int(p.split(".")[-2].split("_")[-1]) for p in images])
images = images[order]
images


# In[35]:


#im = PIL.Image.open(images[0])
#fig = plt.figure()
#ax = fig.add_subplot(1,1,1)
#plt.imshow(im)
#ax.axis('off')
#plt.show()


# Now, the camera calibration can be done using all the images of the chessboard. Two functions are necessary:
# 
# * The first will detect markers on all the images and.
# * The second will proceed the detected markers to estimage the camera calibration data.

# In[36]:


def read_chessboards(images):
    """
    Charuco base pose estimation.
    """
    print("POSE ESTIMATION STARTS:")
    allCorners = []
    allIds = []
    decimator = 0
    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

    for im in images:
        print("=> Processing image {0}".format(im))
        frame = cv2.imread(im)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)
        
        if len(corners)>0:
            # SUB PIXEL DETECTION
            for corner in corners:
                cv2.cornerSubPix(gray, corner, 
                                 winSize = (3,3), 
                                 zeroZone = (-1,-1), 
                                 criteria = criteria)
            res2 = cv2.aruco.interpolateCornersCharuco(corners,ids,gray,board)        
            if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
                allCorners.append(res2[1])
                allIds.append(res2[2])              
        
        decimator+=1   

    imsize = gray.shape
    return allCorners,allIds,imsize


# In[37]:


allCorners,allIds,imsize=read_chessboards(images)


# In[38]:


def calibrate_camera(allCorners,allIds,imsize):   
    """
    Calibrates the camera using the dected corners.
    """
    print("CAMERA CALIBRATION")
    
    cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
                                 [    0., 1000., imsize[1]/2.],
                                 [    0.,    0.,           1.]])

    distCoeffsInit = np.zeros((5,1))
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO) 
    #flags = (cv2.CALIB_RATIONAL_MODEL) 
    (ret, camera_matrix, distortion_coefficients0, 
     rotation_vectors, translation_vectors,
     stdDeviationsIntrinsics, stdDeviationsExtrinsics, 
     perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
                      charucoCorners=allCorners,
                      charucoIds=allIds,
                      board=board,
                      imageSize=imsize,
                      cameraMatrix=cameraMatrixInit,
                      distCoeffs=distCoeffsInit,
                      flags=flags,
                      criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

    return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors


# In[39]:


#get_ipython().run_line_magic('time', 'ret, mtx, dist, rvecs, tvecs = calibrate_camera(allCorners,allIds,imsize)')

ret, mtx, dist, rvecs, tvecs = calibrate_camera(allCorners,allIds,imsize)

# In[40]:


#ret


# In[41]:


#mtx


# In[42]:


#dist


# Save all coefficients to the file.

# In[43]:


def saveCoefficients(mtx, dist, path):
    """ Save the camera matrix and the distortion coefficients to given path/file. """
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write("mtx", mtx)
    cv_file.write("dist", dist)
    # note you *release* you don't close() a FileStorage object
    cv_file.release()
    
def loadCoefficients(path):
    """ Loads camera matrix and distortion coefficients. """
    # FILE_STORAGE_READ
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode("camera_matrix").mat()
    dist_matrix = cv_file.getNode("dist_coeff").mat()

    # Debug: print the values
    # print("camera_matrix : ", camera_matrix.tolist())
    # print("dist_matrix : ", dist_matrix.tolist())

    cv_file.release()
    return [camera_matrix, dist_matrix]

saveCoefficients(mtx, dist, "calibrationCoefficients_picam.yaml")
mtx1, dist1 = loadCoefficients("calibrationCoefficients_picam.yaml")


# In[44]:


mtx1


# In[45]:


dist1


# ### Check calibration results
# I do not know how it works and what results should we receive:)

# In[52]:


I=50 # select image id
plt.figure()
frame = cv2.imread(images[I])
img_undist = cv2.undistort(frame,mtx,dist,None)
plt.subplot(1,2,1)
plt.imshow(frame)
plt.title("Raw image")
plt.axis("off")
plt.subplot(1,2,2)
plt.imshow(img_undist)
plt.title("Corrected image")
plt.axis("off")
plt.show()


# ## 3 . Use of camera calibration to estimate 3D translation and rotation of each marker on a scene

# In[53]:



frame = cv2.imread(images[I])
plt.figure()
plt.imshow(frame, interpolation = "nearest")
plt.show()


# ## Post processing

# In[54]:



gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters =  aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, 
                                                      parameters=parameters)
# SUB PIXEL DETECTION
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
for corner in corners:
    cv2.cornerSubPix(gray, corner, winSize = (3,3), zeroZone = (-1,-1), criteria = criteria)
    
frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)


# 
# 
# ## Results

# In[55]:


plt.figure()
plt.imshow(frame_markers, interpolation = "nearest")
plt.show()


# ### Add local axis on each marker

# In[ ]:





# In[56]:


size_of_marker =  0.0322 # 0.0285 # side lenght of the marker in meter
rvecs,tvecs,_objPoints = aruco.estimatePoseSingleMarkers(corners, size_of_marker , mtx, dist)#here we use our calibration results!


# In[ ]:





# In[ ]:





# In[58]:


length_of_axis = 0.1
imaxis = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

for i in range(len(tvecs)):
    imaxis = aruco.drawAxis(imaxis, mtx, dist, rvecs[i], tvecs[i], length_of_axis)


# In[59]:


plt.figure()
plt.imshow(imaxis)
plt.grid()
plt.show()


# In[60]:


data = pd.DataFrame(data = tvecs.reshape(len(tvecs),3), columns = ["tx", "ty", "tz"], 
                    index = ids.flatten())
data.index.name = "marker"
data.sort_index(inplace= True)
data


# In[33]:


datar = pd.DataFrame(data = tvecs.reshape(len(rvecs),3), columns = ["rx", "ry", "rz"], 
                    index = ids.flatten())
datar.index.name = "marker"
datar.sort_index(inplace= True)
np.degrees(datar)


# In[34]:


v = data.loc[3:6].values
((v[1:] - v[:-1])**2).sum(axis = 1)**.5


# In[35]:


cv2.Rodrigues(rvecs[0], np.zeros((3,3)))


# In[36]:


fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
ax = fig.add_subplot(1,2,1)
ax.set_aspect("equal")
plt.plot(data.tx, data.ty, "or-")
plt.grid()
ax = fig.add_subplot(1,2,2)
plt.imshow(imaxis, origin = "upper")
plt.plot(np.array(corners)[:, 0, 0,0], np.array(corners)[:, 0, 0,1], "or")
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


