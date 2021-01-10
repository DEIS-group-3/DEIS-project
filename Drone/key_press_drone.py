#!/usr/bin/env python
# coding: utf-8

import time
import cv2 as cv
from easytello import tello
from tkinter import*
import keyboard

my_drone = tello.Tello()

while True:
    if keyboard.is_pressed('a'):
        my_drone.takeoff()
        #time.sleep(3)
    elif keyboard.is_pressed('f'):
        my_drone.forward(30)
        #time.sleep(3)
    elif keyboard.is_pressed('b'):
        my_drone.back(30)
        #time.sleep(3)
    elif keyboard.is_pressed('u'): #up
        my_drone.up(30)
        #time.sleep(3)
    elif keyboard.is_pressed('d'): #Down
        my_drone.down(30)
        #time.sleep(3)
    elif keyboard.is_pressed('l'): #left
        my_drone.left(30)
        #time.sleep(3)
    elif keyboard.is_pressed('r'): #right
        my_drone.right(30)
        #time.sleep(3)
    elif keyboard.is_pressed('z'): #land
        my_drone.land()
    elif keyboard.is_pressed('c'): #clockwise rotataion
        my_drone.cw(15)
    elif keyboard.is_pressed('o'): #counter clockwise rotataion
        my_drone.ccw(15)
    elif keyboard.is_pressed('i'): #counter clockwise rotataion
        my_drone.flip(15)

        