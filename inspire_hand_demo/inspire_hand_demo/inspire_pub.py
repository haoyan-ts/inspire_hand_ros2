import sys

from inspire_hand_interfaces.msg import AngleState, ForceState
from .inspire_api import InspireHandAPI

import rclpy
from rclpy.node import Node

class InspireHandPub(Node):
    def __init__(self):
        super().__init__('inspire_hand_pub')
        self.angle_pub = self.create_publisher(AngleState, 'inspire_hand_angle_state', 10)
        self.force_pub = self.create_publisher(ForceState, 'inspire_hand_force_state', 10)

        self.hand = InspireHandAPI('/dev/ttyUSB0', 115200, 1)
        self.timer = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        angle_state = AngleState()
        force_state = ForceState()

        angle = self.hand.read6(1, 'angleAct')
        force = self.hand.read6(1, 'forceAct')
        
        if len(angle) == 6:
            angle_state.angle1 = angle[0]
            angle_state.angle2 = angle[1]
            angle_state.angle3 = angle[2]
            angle_state.angle4 = angle[3]
            angle_state.angle5 = angle[4]
            angle_state.angle6 = angle[5]

            self.angle_pub.publish(angle_state)

        if len(force) == 6:
            force_state.force1 = force[0]
            force_state.force2 = force[1]
            force_state.force3 = force[2]
            force_state.force4 = force[3]
            force_state.force5 = force[4]
            force_state.force6 = force[5]

            self.force_pub.publish(force_state)

def main():
    rclpy.init()
    inspire_hand_pub = InspireHandPub()
    rclpy.spin(inspire_hand_pub)
    rclpy.shutdown()

if __name__ == '__main__':
    main()