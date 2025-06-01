#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import ResetCounter
from example_interfaces.msg import Int64


class WordCounter(Node):
    def __init__(self, node_name, *, context = None, cli_args = None, namespace = None, use_global_arguments = True, enable_rosout = True, start_parameter_services = True, parameter_overrides = None, allow_undeclared_parameters = False, automatically_declare_parameters_from_overrides = False, enable_logger_service = False):
        super().__init__(node_name, context=context, cli_args=cli_args, namespace=namespace, use_global_arguments=use_global_arguments, enable_rosout=enable_rosout, start_parameter_services=start_parameter_services, parameter_overrides=parameter_overrides, allow_undeclared_parameters=allow_undeclared_parameters, automatically_declare_parameters_from_overrides=automatically_declare_parameters_from_overrides, enable_logger_service=enable_logger_service)
        self.Subscriber_ = self.create_subscription(Int64, "number", self.callback_number, 10)
        self.Server_ = self.create_service(ResetCounter, "counter_service", self.service_callback)
        self.counter_ = 0

        self.get_logger().info("the service Node code has been started")

    def callback_number(self, msg : Int64):
        self.counter_ += msg.data
        self.get_logger().info(f"the current value is {self.counter_}")


    def service_callback(self, request: ResetCounter.Request, response: ResetCounter.Response):
        if request.reset_value > self.counter_:
            self.get_logger().info("the resset value is greater than the counter value")
            response.success =  False
        elif request.reset_value == self.counter_:
            self.get_logger().info("the request value is same as the value given by the user")
            response.success = False
            response.message = "Failed"
        elif request.reset_value < self.counter_:
            self.get_logger().info("the reset value opted is correct and the funtion can be run")
            self.counter_ = request.reset_value
            self.get_logger().info("the value has been reseted")
            response.success = True
            response.message = "Pass"
        return response
def main(args = None):
    rclpy.init(args=args)
    node = WordCounter("Node_name_ResetCounter")
    rclpy.spin(node)
    rclpy.shutdown()


        

if __name__ == "__main__":
    main()
