#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import ResetCounter

class ResetCounterClient(Node):
    def __init__(self):
        super().__init__("reset_counter_client")
        self.client_ = self.create_client(ResetCounter, "reset_counter")

    def call_reset_counter(self, value):
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Waiting for service...")

        request = ResetCounter.Request()
        request.reset_value = value

        future = self.client_.call_async(request)
        future.add_done_callback(self.callback_reset_counter_response)

    def callback_reset_counter_response(self, future):
        try:
            response = future.result()
            self.get_logger().info("Success flag: " + str(response.success))
            self.get_logger().info("Message: " + str(response.message))
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = ResetCounterClient()
    
    # Example reset value
    node.call_reset_counter(0)

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
