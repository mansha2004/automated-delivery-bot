#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped

import yaml
import os
import math

class VoiceNavBridge(Node):

    def __init__(self):
        super().__init__('voice_nav_bridge')

        self.navigator = BasicNavigator()

        config_file = os.path.expanduser(
            "~/automated-delivery-bot/src/my_bot/config/locations.yaml"
        )

        with open(config_file, "r") as file:
            self.locations = yaml.safe_load(file)

        self.get_logger().info(
            f"Loaded {len(self.locations)} locations"
        )

        self.sub = self.create_subscription(
            String,
            '/voice_command',
            self.callback,
            10
        )

        self.get_logger().info("Voice Nav Bridge Ready")

    def go_to(self, x, y,yaw):

        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.header.stamp = self.get_clock().now().to_msg()

        goal.pose.position.x = x
        goal.pose.position.y = y

        import math

        goal.pose.orientation.z = math.sin(yaw / 2.0)
        goal.pose.orientation.w = math.cos(yaw / 2.0)
        self.get_logger().info(
            f"Navigating to ({x}, {y})"
        )

        self.navigator.goToPose(goal)

    def callback(self, msg):

        command = msg.data.strip().lower()

        self.get_logger().info(
            f"Received: {command}"
        )

        if command in self.locations:

            location = self.locations[command]

            x = float(location["x"])
            y = float(location["y"])
            yaw=float(location["yaw"])

            self.go_to(x, y,yaw)

        else:
            self.get_logger().warn(
                f"Unknown location: {command}"
            )
def main(args=None):

    rclpy.init(args=args)

    node = VoiceNavBridge()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
