import rclpy # Import the ROS client library for Python
from rclpy.node import Node # Enables the use of rclpy's Node class
from std_msgs.msg import Int64 
from std_msgs.msg import String
import numpy as np # NumPy Python library
from .ActionPerform import ActionPerformer
from .Action_message_convert import MessageTransformer
 
class ActionSubscriber(Node):
  
  def __init__(self):
    # Initiate the Node class's constructor and give it a name
    super().__init__('GPS_actions_perform')
     
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
    self.publish_to_feedback = self.create_publisher(Int64, '/feedback', 10)
    self.performaction=ActionPerformer()
   
  def action_received(self, msg):
    """
    Callback function.
    This function gets called as soon as the position of the object is received."""
    object_string = msg.data
#if it concerns our robot. Our robot_id=4, -2 means all robots
    m=MessageTransformer()
    INFO=m.splitter_actions(msg.data)
    
    action_id=INFO[0]
    target_robot_id=INFO[1]
   # print(action_id)
    #print(target_robot_id)

    if  (target_robot_id==str(4)) or (target_robot_id==str(-2)):
       
        self.performaction.perform(action_id,1)
        self.publish_feedback(1)

           
    
  #publish feedback to GPS   
  def publish_feedback(self,my_info):

    msg = Int64() # Create a message of this type 
    msg.data = my_info # Store the object's position
    self.publish_to_feedback.publish(msg) # Publish the position to the topic 
       
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


