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
#import pandas as pd
#get_ipython().run_line_magic('matplotlib', 'nbagg')


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

