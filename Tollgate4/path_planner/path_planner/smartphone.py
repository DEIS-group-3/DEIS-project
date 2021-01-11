
import rclpy #ros2 library for python
from rclpy.node import Node
from datetime import datetime
from std_msgs.msg import String


class SmartPhone(Node):

    def __init__(self):
       super().__init__("positions_listener")#name of the node
       
       self.sunscriber_=self.create_subscription(String, "/robotPositions", self.callback_robot_news, 10)#robot_news is the name of the topic; 10 is buffer, max numner of msg that will be kept if they not delivered in time
       
       self.get_logger().info("Position_listener node has been created")#+ str(self.counter_)
       
    def callback_robot_news(self,msg):
       dt_string = String();
       dt_string = datetime.now().strftime("%d/%m/%Y-%H:%M:%S.%f")
       self.get_logger().info(msg.data+ str(dt_string))   
    
       
       
    
def main(args=None):
    rclpy.init(args=args) #needs to be in every ros2 file. Initialize ros2 communication
    node=SmartPhone()
    rclpy.spin(node)
    rclpy.shutdown()#turn off ros2 communication
    
if __name__=="__main__":
     main()
