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

# Then let's make a bunch of pictures - screenshots from this video, and save it in separate folder.

# In[20]:


import math

videoFile = "calib2.avi"
imagesFolder = "calib_pics/"
cap = cv2.VideoCapture(videoFile)
frameRate = 20 #frame rate
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

