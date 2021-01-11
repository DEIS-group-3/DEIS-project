#!/usr/bin/env python
# coding: utf-8

# In[37]:


##!/usr/bin/env python3

import re
import numpy as np
from numpy import linalg as LA

our_robot_id=4
#y=m*x+c
M=[0.004115136893506476, 0.00785102775779539, -127.16666666666578, -89.33333333333456, -89.99999999999997, 194.0000000000115]
C=[387.82644564107, 582.5283366723754, 29574.49999999979, 36858.83333333383, 77632.99999999997, -201755.00000001208]
Int=[[307,487.75],[952.75,490.5]]#center of intersections
inter_corners = [[ 229.50769933,  388.77090124],
                 [ 408.23873428,  389.50640392],
                 [ 858.24046419,  391.35822264],
                 [1041.99543505,  392.1143995 ],
                 [ 227.96997535,  584.31813528],
                 [ 406.04235612,  585.71618648],
                 [ 856.04167618,  589.24914363],
                 [1043.01916036,  590.71710905]]


class LocationMap(object):

    
    def belongs(self,i,X): #check if point belongs to the line
       eps=0.00001;
       a=M[i-1]
       b=C[i-1]
#        print(abs(X[1]-a*X[0]-b))
       if abs(X[1]-a*X[0]-b)<eps:
          return True
       else:
          return False
    
    def test_isleft(self,i,X):#y=m*x+c. Check if the dot X lines to the left or right of this lane
    #using scalar product
        a=M[i-1]
        b=C[i-1]
        xc=X[0]
        yc=X[1]
        h=0;
        xa=[0,100]
        ya=[b,100*a+b]
        for j in range (0, len(inter_corners)):
            ##print(inter_corners[i])
            if (self.belongs(i,inter_corners[j])):
                ##print(j)
                xa[h]=inter_corners[j][0]
                ya[h]=inter_corners[j][1]
                h=h+1;
            if h==2:
                break
#         print(h)
        try:
           x1=xa[0]
           y1=ya[0] 
           x2=xa[1]
           y2=ya[1]
        except:
           pass
    #first vector
        f1=np.array((x2-x1,y2-y1))
    #first vector
        f2=np.array((x2-xc,y2-yc))
#     print(np.cross(f1,f2))
        z=np.cross(f1,f2)
        if z<0:
            return 1
        elif z>0:
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
        h=0;
        xa=[0,100]
        ya=[b,100*a+b]
        for j in range (0, len(inter_corners)):
            ##print(inter_corners[i])
            if (self.belongs(i,inter_corners[j])):
                print(i)
                xa[h]=inter_corners[j][0]
                ya[h]=inter_corners[j][1]
                h=h+1;
            if h==2:
                break
        try:
           x1=xa[0]
           y1=ya[0] 
           x2=xa[1]
           y2=ya[1]
        except:
           pass 
    
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

    def plot_gr(self,X):
        #Final map
        x = np.linspace(0, 1300, 1000)
        plt.plot(x, m1*x + c1, 'r', label='L1')
        plt.plot(x, m2*x + c2, 'k', label='L2')
        plt.plot(x, m3*x + c3, 'b', label='L3')
        plt.plot(x, m4*x + c4, 'g', label='L4')
        plt.plot(x, m5*x + c5, 'y', label='L5')
        plt.plot(x, m6*x + c6, 'm', label='L6')
        plt.plot(X[0], X[1], 'x', label='Dot')

        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        plt.axis([0, 1300, 1200, 0])
        plt.grid()
        plt.show()

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
#      print(q.test_isleft(3,[0, 0]))
     #t=q.splitter_actions('k, 4')
     #print(t[1])
     #s=['-1 -1 -1 -1 -1;-1 -1 -1 -1 -1;550.89396418456 1111.49193236916 1.53974843013584 2 0.554857314971339;442.023307909461 1114.00050625987 2.18427907071948 3 0.566817960934568;-1 -1 -1 -1 -1;-1 -1 -1 -1 -1;-1 -1 -1 -1 -1;299.524247756989 95.9661582671803 -1.55186518441895 7 0.517454436231951;-1 -1 -1 -1 -1;-1 -1 -1 -1 -1']
     #print(q.splitter_robot(s))
#      print(q.if_between(5,6,Int[0]))
#      print(q.if_in_intersec(1,Int[0]))
      
   #  print(q.where([467.699780167377, 1145.21172493475]))
   #  print(q.where([450.518773703457, 749.237423949244]))
     P=[500, 500]
     print(q.where(Int[1]))
#      q.plot_gr(P)
#      P=[464.403410400053, 162.804744915978]
#      print(q.where([464.403410400053, 162.804744915978]))
#      print(q.where(P))
#      q.plot_gr(P)
     #data: '[463.995342947696, 162.979641111362] 120 73.02035888863787'

#data: '[463.347637969258, 162.638452783139] 122 689.8964650636681'

     #print(q.closest_line(Int[1]))
    

if __name__ == '__main__':
     main()


# In[ ]:





# In[ ]:




