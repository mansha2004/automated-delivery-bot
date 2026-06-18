#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import time


class VoiceNavBridge(Node):
    def __init__(self):
        super().__init__('voice_nav_bridge')

        self.sub = self.create_subscription(
            String,
            '/voice_command',
            self.callback,
            10
        )

        self.pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

    def callback(self, msg):   # ✅ NOW INSIDE CLASS
        command = msg.data.lower()
        twist = Twist()

        print(f"Received: {command}")

        # 🛑 STOP
        if "stop" in command:
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        # 🚀 FORWARD
        elif "forward" in command or "go" in command or "room" in command:
            twist.linear.x = 0.5
            twist.angular.z = 0.0

        # ↩ LEFT
        elif "left" in command:
            twist.linear.x = 0.2
            twist.angular.z = 0.5

        # ↪ RIGHT
        elif "right" in command:
            twist.linear.x = 0.2
            twist.angular.z = -0.5

        else:
            self.get_logger().info(f"Unknown command: {command}")
            return

        # 🚀 PUBLISH
        self.pub.publish(twist)
        self.get_logger().info(f"Executing: {command}")

        # ⏱ MOVE LONGER (VISIBLE IN RViz)
        time.sleep(2)

        # 🛑 STOP AFTER MOTION
        stop_twist = Twist()
        self.pub.publish(stop_twist)


def main():
    rclpy.init()
    node = VoiceNavBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
