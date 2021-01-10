#!/usr/bin/env python3
#Simulation of GPS server - publishing data to the topic /actions. Currently, it has the structure as String: action_id, robot_id
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class GPSPublisher(Node):
    def __init__(self):
        super().__init__("GPS_actions")

        self.robot_name_ = "GPS"
        self.publisher_ = self.create_publisher(String, '/action', 10)
        self.timer_ = self.create_timer(1, self.publish_actions)
        self.get_logger().info("Local GPS Server has been started")

    def publish_actions(self):
        msg = String()
        robot_id=4
        msg.data = "s"+","+str(robot_id)
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = GPSPublisher()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

