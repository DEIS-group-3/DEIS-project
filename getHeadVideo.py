import numpy as np
import cv2, PIL, os
from cv2 import aruco
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import pandas as pd

# define a video capture object
axisip='192.168.1.2'
axisuser='root'
axispass='r3dM1lk'

vid = cv2.VideoCapture('http://192.168.1.2//axis-cgi/mjpg/video.cgi')
#vid = cv2.VideoCapture(0)
w = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
h = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(w, h)
w1=1280
h1=960
#w1=w
#h1=h
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

#videoWriter = cv2.VideoWriter("head_cam.avi", fourcc, 30.0,(w,h))
videoWriter = cv2.VideoWriter("head_cam_nnnnn.avi", fourcc, 20.0,(w1,h1))
while(vid.isOpened()):
  while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    if (ret != True):
        break
    frame=cv2.resize(frame,(w1,h1))
    # Display the resulting frame
    cv2.imshow('frame', frame)
    videoWriter.write(frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# # After the loop release the cap object
  vid.release()
  videoWriter.release()
# # Destroy all the windows
  cv2.destroyAllWindows()
else: 
    print("Alert ! Camera disconnected") 