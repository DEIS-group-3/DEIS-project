##!/usr/bin/env python3
import serial
import time
#import argparse

class ActionPerformer(object):

    def perform(self,action_id, times):
        #  ser = serial.Serial('/dev/ttyUSB3', 9600, timeout=1)
        #  ser.flush()
         action_string=self.recognize(action_id)
         for i in range(times):
            # ser.write(action_string.encode('utf-8'))
            # line = ser.readline().decode('utf-8').rstrip()
            # print(line)
            print(i+1, action_string)
            # time.sleep(1)
            # if ser.in_waiting > 0:
            #    line = ser.readline().decode('utf-8').rstrip()
            #    print("--------received data-------")
            #    print(line)
         return
    def recognize(self,action_id):
          method_name='action_'+str(action_id)
          method=getattr(self,method_name,lambda :'Invalid')
          return method()
  
    def action_f(self):
                   return 'forward'
    def action_b(self):
                   return 'backward'
    def action_r(self):
                   return 'right'  
    def action_l(self):
                   return 'left'
    def action_s(self):
                   return 'stop'

def main():

     print("Starting..")  
     q=ActionPerformer()
     q.perform("s",10)

if __name__ == '__main__':
     main()
