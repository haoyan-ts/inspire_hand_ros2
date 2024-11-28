import sys

from inspire_hand_interfaces.msg import AngleState, ForceState

import rclpy
from rclpy.node import Node

class InspireHandSub(Node):
    def __init__(self):
        super().__init__('inspire_hand_sub')
        self.sub = self.create_subscription(AngleState, 'inspire_hand_angle_state', self.angle_state_callback, 10)
        self.sub = self.create_subscription(ForceState, 'inspire_hand_force_state', self.force_state_callback, 10)
    
    def angle_state_callback(self, msg: AngleState):
        # self.get_logger().info('Angle state: %s' % msg.angle1)
        self.get_logger().info('Angle values: %s, %s, %s, %s, %s, %s' % (msg.angle1, msg.angle2, msg.angle3, msg.angle4, msg.angle5, msg.angle6))
    
    def force_state_callback(self, msg: ForceState):
        # self.get_logger().info('Force state: %s' % msg.force1)
        self.get_logger().info('Force values: %s, %s, %s, %s, %s, %s' % (msg.force1, msg.force2, msg.force3, msg.force4, msg.force5, msg.force6))

def main():
    rclpy.init()
    inspire_hand_sub = InspireHandSub()
    rclpy.spin(inspire_hand_sub)
    rclpy.shutdown()

if __name__ == '__main__':
    main()