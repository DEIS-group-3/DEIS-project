import serial
import time
#import argparse
import rclpy # Import the ROS client library for Python
from rclpy.node import Node # Enables the use of rclpy's Node class
from std_msgs.msg import Int64 
from std_msgs.msg import String
import numpy as np # NumPy Python library
#from .ActionPerform import ActionPerformer
from .Action_message_convert import MessageTransformer
 
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) 
ser.flush()
MsgConvert = MessageTransformer()

class ActionSubscriber(Node):
  
  def __init__(self):
    # Initiate the Node class's constructor and give it a name
    super().__init__('ActionSubscriber')
     
    # Create subscriber(s)    
    # The callback function is called as soon as a message is received.
    # The maximum number of queued messages is 10.
    self.subscription_a = self.create_subscription(
      String,
      '/action',
      self.action_received,
      10)
    self.subscription_a  # prevent unused variable warning
    
    # Create publisher(s)   
    self.feedback_publisher = self.create_publisher(String, '/feedback', 10)
    #self.timer_ = self.create_timer(1, self.publish_feedback)
    self.get_logger().info("Robot Board Node has been started")
  
  #publish feedback to GPS   
  def publish_feedback(self,my_info):
    print("publish_feedback>>")
    msg = String() # Create a message of this type 
    msg.data = my_info # Store the object's status
    self.feedback_publisher.publish(msg) # Publish the position to the topic 
   
  def action_received(self, msg):
    """
    Callback function.
    This function gets called as soon as the position of the object is received."""
    print("action_received>>")

#if it concerns our robot. Our robot_id=4, -2 means all robots
#    m=MessageTransformer()
    print('msg.data:', msg.data)
    INFO=MsgConvert.splitter_actions(msg.data)
    action_id=INFO[0]
    target_robot_id=INFO[1]
    print('action_id=',action_id)
    print('target_robot=',target_robot_id)
      
    object_string = MsgConvert.identify_actions() + "\n"
    print('String=',object_string)

    if  (target_robot_id==str(4)) or (target_robot_id==str(-2)):
        #Transmit message to lower board
        ser.write(object_string.encode('utf-8'))
        #print(object_string.encode('utf-8'))
        #line = ser.readline().decode('utf-8').rstrip()
        print("--------transmitted data-------")
        #print(line)
        #ser.flush()
        #time.sleep(1)
        #while True:
        if ser.in_waiting > 0:
            #line = ser.readline().decode('utf-8').rstrip()
            print("--------received data-------")
            #print(line)
            #ser.flush()
            if(line == "SUCCESSS"):
                #publish feedback
                self.publish_feedback("SUCCESS:Acknowledgement")
            elif(line == "FAIL"):
                #publish feedback
                self.publish_feedback("FAIL:NAK")
            else:
                #DEMO publish feedback
                self.publish_feedback("FEEDBACK")
        else:
            print("ser.in_waiting=", ser.in_waiting)
        
        self.publish_feedback("TEST2")
      
def main(args=None):
 
  # Initialize the rclpy library
    rclpy.init(args=args)
 
  # Create the node
    node  = ActionSubscriber()
    rclpy.spin(node)
    node.destroy_node()
 
  # Shutdown the ROS client library for Python
    rclpy.shutdown()
 
if __name__ == '__main__':
  main()


