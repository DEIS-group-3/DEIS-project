#!/usr/bin/env python3
#Simulation of GPS server - publishing data to the topic /actions. Currently, it has the structure as String: action_id, robot_id
import numpy as np
from datetime import datetime
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from .Map_location import LocationMap
from .Action_message_convert import MessageTransformer

MsgConvert = MessageTransformer()
dest_x, dest_y = 1059.5, 611.25

def path_planning(our_x, our_y, dest_x, dest_y, w, d):
    # write the path planning code here
    lspeed, rspeed = 200, 200
    if w in [120, 121, 122, 340, 341, 560, 561]:
    #if approaching intersection, then decrease the speed and if approaching the end, then increase the speed. Range: [25, 340] 
    	lspeed, rspeed = 128, 128 # straight
    elif w in [1, 2]:
    	lspeed, rspeed = 229, -229 # turn right
    return 'g', lspeed, rspeed
    
class ActionPublisher(Node):
    def __init__(self):
        super().__init__("ActionPublisher")
        self.robot_name_ = "PC"
        
        self.subscriber_=self.create_subscription(String, "/aruco_gps_3", self.gps_received, 10)#robot_news is the name of the topic; 10 is buffer, max numner of msg that will be kept if they not delivered in time       
        self.get_logger().info("Position_listener node has been created")#+ str(self.counter_)


        self.publisher_ = self.create_publisher(String, '/action', 10)
        #self.timer_ = self.create_timer(1, self.publisher_code) # OPTIONAL
        self.get_logger().info("Local PC Node has been started!!!!!!!!!")
        
        # Create subscriber(s)    
        # The callback function is called as soon as a message is received.
        # The maximum number of queued messages is 10.
        self.subscription_a = self.create_subscription(
      	String,
      '/feedback',
        self.subscriber_code,
      	10)
        self.subscription_a  # prevent unused variable warning
        
    def gps_received(self, msg):
        """Callback function. This function gets called as soon as the position of the object is received."""
        print("gps_received >> ")
        print("msg.data=", msg.data)
        our_coord = MsgConvert.splitter_coords(msg.data)

        l=LocationMap()

        our_coord=[(float) (our_coord[0]), (float)(our_coord[1])]
        #our_coord.reshape(1,2)
        print("our_coord=", our_coord)
        
        w=l.where(our_coord)
        print("wher am I?", w)
        d=l.closest_line(our_coord)  #distance to the closest line
        print("distance to the closest line:", d)
        our_x, our_y = our_coord[0], our_coord[1]
        action_id, l_speed, r_speed = path_planning(our_x, our_y, dest_x, dest_y, w, d)
        self.publisher_code(action_id, l_speed, r_speed)


    def publisher_code(self, action_id, l_speed, r_speed):
        print("publisher_code")
        msg = String()
        robot_id=4 # TEST
        
        dt_string = String();
        dt_string = datetime.now().strftime("%d/%m/%Y-%H:%M:%S.%f")
        
        msg.data = dt_string+","+action_id+","+"-1"+","+"-1"+","+str(robot_id)+","+str(l_speed)+","+str(r_speed)
        self.publisher_.publish(msg)
        
    def subscriber_code(self, msg):
        print("Received Feedback : ", msg.data)

def main(args=None):
    rclpy.init(args=args)
    node = ActionPublisher()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

