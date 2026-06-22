#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped


class VoiceNavBridge(Node):

    def __init__(self):
        super().__init__('voice_nav_bridge')

        self.navigator = BasicNavigator()

        self.locations = {
            "medical_station": (0.0, 0.0),
            "room_301": (1.5, 1.0),
        }

        self.sub = self.create_subscription(
            String,
            '/voice_command',
            self.callback,
            10
        )

        self.get_logger().info("Voice Nav Bridge Ready")

    def go_to(self, x, y):

        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.header.stamp = self.get_clock().now().to_msg()

        goal.pose.position.x = x
        goal.pose.position.y = y
        goal.pose.orientation.w = 1.0

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

            x, y = self.locations[command]

            self.go_to(x, y)

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
