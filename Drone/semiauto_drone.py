
def Semiauto1():
    my_drone.takeoff()
    my_drone.forward(30)
    my_drone.forward(30)
    my_drone.up(30)
    my_drone.right(30)
    my_drone.right(30)
    my_drone.cw(15)
    my_drone.flip(15)
    my_drone.land()
    
def Semiauto2():
    my_drone.takeoff()
    my_drone.forward(30)
    my_drone.forward(30)
    my_drone.up(30)
    my_drone.left(30)
    my_drone.left(30)
    my_drone.cw(15)
    my_drone.flip(15)
    my_drone.land()
    
def Semiauto3():
    my_drone.takeoff()
    my_drone.forward(30)
    my_drone.flip(15)
    my_drone.back(30)
    my_drone.flip(15)
    my_drone.cw(15)
    my_drone.ccw(15) 
    my_drone.land()
    
Semiauto1();
#Semiauto2();
#Semiauto3();