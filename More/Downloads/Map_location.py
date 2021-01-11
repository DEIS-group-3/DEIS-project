##!/usr/bin/env python3

import re
import numpy as np
from numpy import linalg as LA

our_robot_id=4
M=[0.004115136893506476, 0.00785102775779539, -127.16666666666578, -89.33333333333456, -89.99999999999997, 194.0000000000115]
C=[387.82644564107, 582.5283366723754, 29574.49999999979, 36858.83333333383, 77632.99999999997, -201755.00000001208]
Int=Int=[[307,487.75],[952.75,490.5]]

class LocationMap(object):
    
    def test_isleft(self,i,X):#y=m*x+c. Check if the dot X lines to the left or right of this lane
    #using scalar product
        a=M[i-1]
        b=C[i-1]
        x=X[0]
        y=X[1]
    #first point on the line (arbitrary)
        x1=0
        y1=a*x1+b
    #s econd point on the line (arbitrary)
        x2=100
        y2=a*x2+b
    #first vector
        f1=np.array((x2-x1,y2-y1))
    #first vector
        f2=np.array((x2-x,y2-y))
#     print(np.cross(f1,f2))
        z=np.cross(f1,f2)
        if z>0:
            return 1
        elif z<0:
            return -1
        return 0

    def if_between(self,i1,i2,X): #if the point between two lines: a1x+b1 and a2x+b2
       
        z=self.test_isleft(i1,X)*self.test_isleft(i2,X)
        if (z==-1):
            return 1
        elif z==1:
            return -1
        return 0 #if on the line

    def if_in_intersec(self,i,X): #if the point inside rectangles of intersection 0 or 1 (i)
        if i == 0:
            i1=2
            i2=3
        elif i == 1:
            i1=4
            i2=5
        z1=self.if_between(i1,i2,X)
        z2=self.if_between(i3,i4,X)
        if z1==1 and z2==1:
            return 1
        elif z1*z2==0:
            return 0
        return -1 #outside intersection
    
    def dist_to_line(self,i,X):
        a=M[i-1]
        b=C[i-1]
        x1=0
        x2=100
        y1=a*0+b
        y2=a*100+b  
    
        f1=np.array((x2-x1,y2-y1,0)) #vector on the line
        f2=np.array((x2-X[0],y2-X[1],0))
#         print(f1)
#     f2=np.array(X1-X)
#         print(f2)
        z=np.cross(f1,f2)
#         print(z)
        d=LA.norm(z)/LA.norm(f1)
        return abs(d)
    
    def eucl_dist(self,a,b):#distance between points a and b
        return LA.norm(a-b)

#     def dist_to_int(self,n,x,y):#n - number of intersections; eps_x - extra space in x-directions
#         i1=Int[n-1]
#         d=eucl_dist([x,y],i1)
#         return d


    def where(self,X): #if the point inside rectangles of intersection 0 or 1 (i)
        p12=self.if_between(1,2,X)
        p34=self.if_between(3,4,X)
        p56=self.if_between(5,6,X)
        l1=self.test_isleft(1,X)
        l4=self.test_isleft(4,X)
 #       print('l4',l4)
        l6=self.test_isleft(6,X)
  #      print('l6',l6)
        if p12>=0:
            s=121 #center part
            if p34>=0:
                s=1#first intersection
            elif p56>=0:
                s=2#second intersection
            elif l4>=0:
                s=120
            elif l6<=0:
                s=122           
        elif p34>=0:
            if l1>=0:
                s=340
            else: s=341
        elif p56>=0:
            if l1>=0:
                s=560
            else: s=561
        else: s=-1
        return s #outside intersection

    def closest_line(self,X): #if the point inside rectangles of intersection 0 or 1 (i)
        p=self.where(X)
        if p==-1:
                 return None
        if p==340 or p==560:
            d=self.dist_to_line(1,X)
        elif p==341 or p==561:
            d=self.dist_to_line(2,X)
        elif p==120:
            d=self.dist_to_line(3,X)
        elif p==122:
            d=self.dist_to_line(5,X)
        elif p==121:
            d=min(self.dist_to_line(4,X),self.dist_to_line(5,X))
        elif p==1:
             d=0
 #           d=min(self.dist_to_line(1,X),self.dist_to_line(2,X),self.dist_to_line(3,X),self.dist_to_line(4,X))
        elif p==2:
             d=0
           # d=min(self.dist_to_line(1,X),self.dist_to_line(2,X),self.dist_to_line(5,X),self.dist_to_line(6,X))
        return d #outside intersection    
    
def main():

     print("Starting..")  
     q=LocationMap()
     #t=q.splitter_actions('k, 4')
     #print(t[1])
     #s=['-1 -1 -1 -1 -1;-1 -1 -1 -1 -1;550.89396418456 1111.49193236916 1.53974843013584 2 0.554857314971339;442.023307909461 1114.00050625987 2.18427907071948 3 0.566817960934568;-1 -1 -1 -1 -1;-1 -1 -1 -1 -1;-1 -1 -1 -1 -1;299.524247756989 95.9661582671803 -1.55186518441895 7 0.517454436231951;-1 -1 -1 -1 -1;-1 -1 -1 -1 -1']
     #print(q.splitter_robot(s))
     #print(q.if_between(1,2,Int[0]))
     print(q.test_isleft(3,[0, 0]))
   #  print(q.where([467.699780167377, 1145.21172493475]))
   #  print(q.where([450.518773703457, 749.237423949244]))
     print(q.where([463.995342947696, 162.979641111362]))
     print(q.where([464.403410400053, 162.804744915978]))
     #data: '[463.995342947696, 162.979641111362] 120 73.02035888863787'

#data: '[463.347637969258, 162.638452783139] 122 689.8964650636681'

     #print(q.closest_line(Int[1]))

if __name__ == '__main__':
     main()
