import sys

from inspire_hand_interfaces.srv import SetAngle, SetSpeed, SetForce
from inspire_hand_interfaces.msg import AngleState, ForceState

import rclpy
from rclpy.node import Node

class InspireHandClientAsync(Node):
    def __init__(self):
        super().__init__('inspire_hand_client_async')
        self.cli_set_angle = self.create_client(SetAngle, 'inspire_hand_set_angle_srv')
        self.cli_set_speed = self.create_client(SetSpeed, 'inspire_hand_set_speed_srv')
        self.cli_set_force = self.create_client(SetForce, 'inspire_hand_set_force_srv')
        
        while not self.cli_set_angle.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')