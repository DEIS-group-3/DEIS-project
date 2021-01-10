#access overhead camera, watch it in real time and make a record that can be used afterwards
import numpy as np
import cv2, PIL, os
from cv2 import aruco


vid = cv2.VideoCapture('http://192.168.1.2//axis-cgi/mjpg/video.cgi')
w = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
h = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

w1=1280
h1=960
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')


videoWriter = cv2.VideoWriter("head_cam_record.avi", fourcc, 20.0,(w1,h1))
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
