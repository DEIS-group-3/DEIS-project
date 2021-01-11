#taking video, detect aruco and create a new video with aruco
import time
#from tkinter import*
#import keyboard
from cv2 import aruco
import PIL
#import pandas as pd
import cv2
import numpy as np
import logging
import os

#import time
import cv2 as cv
from easytello import tello
#import tello
import math

MAP_SIZE_COEFF = 0.21088#0.20083075 #0.23285 ##0.514
MF = 1/3.49 # 
MF = MAP_SIZE_COEFF
flag12 = False

aruco_dict_6x6 = aruco.Dictionary_get(aruco.DICT_6X6_100)
aruco_dict_7x7 = aruco.Dictionary_get(aruco.DICT_7X7_100)
__SCREEN_WIDTH = 1280
__SCREEN_HEIGHT = 960

NB_MARKERS = 3
our_id=20#4#12
s_id=1
d_id=94

#drone x1 and y1 (drone's which is fixed)
Xa, Ya = 644.69, 314.85 #dummy value in GPS server coordinate
Xa, Ya = 95, 418 #dummy value in pixel coordinate

#source x1 and y1 (drone's which is fixed)
Xb, Yb = 644.69, 314.85 #dummy value in GPS server coordinate
Xb, Yb = 95, 418 #dummy value in pixel coordinate

#Destination x1 aand y1 (hospital which is fixed)
Xc, Yc = 808.86, 1029.23 #dummy value in GPS server coordinate
Xc, Yc = 555, 420 #dummy value in pixel coordinate

def detectMarkers(frame):
    a=[]
    a_our=[]

    logging.debug('detecting ArUco...')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
    parameters =  aruco.DetectorParameters_create()

    # if (aruco_len == 6):
        # corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict_6x6, parameters=parameters)
    # elif (aruco_len == 7):
        # corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict_7x7, parameters=parameters)

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict_6x6, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)
    
    if ids is not None:
        for i in range(len(ids)):
            c = corners[i][0]
            a_new=[ids[i], c[:, 0].mean(), c[:, 1].mean()]
            #print(a_new.shape)
            a.append(a_new)
            if ids[i]==s_id:
                 a_our.append([c[:, 0].mean(), c[:, 1].mean()])
            if ids[i]==our_id:
                 a_our.append([c[:, 0].mean(), c[:, 1].mean()])
            if ids[i]==d_id:
                 a_our.append([c[:, 0].mean(), c[:, 1].mean()])
            #print(a.shape)
            #cv2.drawMarker(frame, (c[:, 0].mean(), c[:, 1].mean()), (0,255,255), markerType=cv2.MARKER_STAR, markerSize=5, thickness=2, line_type=cv2.LINE_AA)  
    #print(a)       
    return frame, a, a_our


def save_coordinates(an_array, txt_file):
   a_file = open(txt_file, "w")
   for row in an_array:
        np.savetxt(a_file, row)

   a_file.close()

def test_video(video_file=0):
    our_a = []
    print(video_file)
    cap = cv2.VideoCapture(video_file)    
#    cap.set(3, __SCREEN_WIDTH)
#    cap.set(4, __SCREEN_HEIGHT)
    d=[]
    if video_file==0 or video_file=='http://192.168.1.2//axis-cgi/mjpg/video.cgi':
       fps=20
    
    else: 
       fps=1 #keep the same rate as initial video
    if video_file=='http://192.168.1.2//axis-cgi/mjpg/video.cgi':
       fps=20
       video_file="overhead_camera"

    # skip first second of video.
    for i in range(3):
        ret, frame = cap.read()
        print(ret)
    coordinates=[]
    our_coordinates=[]
    video_type = cv2.VideoWriter_fourcc(*'XVID')
    video_overlay = cv2.VideoWriter("%s_overlay.avi" % (video_file), video_type, fps, (__SCREEN_WIDTH, __SCREEN_HEIGHT))
    try:
        j = 0
        while cap.isOpened():
            _, frame = cap.read()
            #frame=cv2.resize(frame,( __SCREEN_WIDTH,__SCREEN_HEIGHT))

            print('frame %s' % j )
            combo_image, a, our_a = detectMarkers(frame)
            print(a)
            
            if not len(a) ==0:
                coordinates.append(a)

            if not len(our_a)==0:
                our_coordinates.append(our_a)

            combo_image=cv2.resize(combo_image,( __SCREEN_WIDTH,__SCREEN_HEIGHT))
            
#             cv2.imwrite("%s_%03d_%03d.png" % (video_file, i, lane_follower.curr_steering_angle), frame)           
#            cv2.imwrite(combo_image)
#            cv2.imwrite("%s_overlay_%03d.png" % (video_file, i), combo_image)
            video_overlay.write(combo_image)

            cv2.imshow("Frame with ArUco", combo_image)
            j += 1

            if not len(our_a)==NB_MARKERS:
                 our_a = []
				 
            else:
               break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        video_overlay.release()
        cv2.destroyAllWindows()

        #print("Writing coordinates to the file..")
        #print(coordinates)
        #save_coordinates(coordinates, "coordinates.txt")
        #save_coordinates(our_coordinates, "our_coordinates.txt")
    return our_a

def test_photo(file): #for testing photo  
#     retval  =   cv2.haveImageReader (file)
    if os.path.isfile(file):
    #ignore if no such file is present.
         frame = cv2.imread(file) 
         combo_image = detectMarkers(frame)
         cv2.imshow('final', combo_image)
         
         cv2.waitKey(0)
         cv2.destroyAllWindows()
    else:
         print("File not found")
         print("Finishing..")
        
#     if not retval:
# #         break      
#          print("File not found")
#          print("Finishing..")
#          return 0
#     else:
#         return frame

def head_photo(): #for testing photo  

    frame = cv2.imread('http://192.168.1.2//axis-cgi/mjpg/video.cgi') 
    combo_image = detectMarkers(frame)
    cv2.imshow('final', combo_image)
         
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def getdroneposition(t_drone_id):
    #get pixel position of its marker
    xx, yy = Xa, Ya #getsourceposition(t_drone_id) #TEST
    return xx, yy

def getsourceposition(t_source_id):
    #get pixel position of its marker
    xx, yy = Xb, Yb #TEST
    return xx, yy

def getdestposition(t_dest_id):
    #get pixel position of its marker
    xx, yy = Xc, Yc #TEST
    return xx, yy


#from the pixel cordinates of gps image to cm convert and then calulate the distance 
def calculateL2Distance(xp,yp,xq,yq):
    x =(xq-xp)
    y =(yq-yp)
    dist_px = math.hypot(x, y)
    dist_cm = dist_px * MF
    return dist_cm
    
def calculateL1Distance(xp,yp,xq,yq):
    x =(xq-xp) * MF
    y =(yq-yp) * MF

    return x, y
    
#my_drone = tello.Tello()
#print("Battery: ", my_drone.get_battery())
def mainNew():
    flag12 = False
    distance = 0
    while(flag12 != True):
        xa, ya = getdroneposition(our_id)
        xs, ys = getsourceposition(s_id) #
        xd, yd = getdestposition(d_id)
        distance1 = calculateL2Distance(xa,ya,xs,ys)
        distance2 = calculateL2Distance(xs,ys,xd,yd)
        flag12 = True
        #if(distance1 > 15 and distance2 > 15):
            #flag12 = True
    print(distance1)
    print(distance2)
    #GO
    my_drone.takeoff()
    #my_drone.up(20);
    print("TAKEOFF.")
    #my_drone.forward(int(distance))
    #my_drone.go(int(distance),0,0,30)
    dist21 = calculateL1Distance(xa,ya,xs,ys)
    dist32 = calculateL1Distance(xs,ys,xd,yd)
    my_drone.go(int(dist21[0]),int(dist21[1]),0,50)
    my_drone.go(int(dist32[0]),int(dist32[1]),0,50)
    print("MOTION.")
    my_drone.land()
    print("LAND.")

if __name__ == '__main__':
#    logging.basicConfig(level=logging.INFO)
    wrk_dir=os.path.abspath(os.getcwd())
    print(wrk_dir)
    #test_video(wrk_dir + "\Video\head_cam_3.avi")
    #test_photo(wrk_dir+'\pictures\image_40.png') 
#    test_video()
    our_coord = test_video('http://192.168.1.2//axis-cgi/mjpg/video.cgi')
    print(our_coord)
    Xa, Ya = our_coord[0][0], our_coord[0][1] #actual value in pixel coordinate
    print(Xa)
    print(Ya)
    Xb, Yb = our_coord[1][0], our_coord[1][1] #actual value in pixel coordinate
    print(Xb)
    print(Yb)
    Xc, Yc = our_coord[2][0], our_coord[2][1] #actual value in pixel coordinate
    print(Xc)
    print(Yc)
    #TEST
    #while(True):
     #   continue
    my_drone = tello.Tello()
    print("Tello Battery: ", my_drone.get_battery())
    mainNew()
 
