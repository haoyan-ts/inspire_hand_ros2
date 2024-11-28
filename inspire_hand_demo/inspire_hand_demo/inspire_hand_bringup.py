import rclpy
from rclpy.node import Node

from inspire_hand_interfaces.srv import SetAngle, SetSpeed, SetForce
from inspire_api import InspireHandAPI
from inspire_hand_interfaces.msg import AngleState, ForceState

from rclpy.qos import qos_profile_services_default

class InspireHandSrv(Node):
    def __init__(self):
        super().__init__('inspire_hand_srv')
        self.set_angle_srv = self.create_service(SetAngle, 'inspire_hand_set_angle_srv', self.set_angle_srv_callback)
        self.set_speed_srv = self.create_service(SetSpeed, 'inspire_hand_set_speed_srv', self.set_speed_srv_callback)
        self.set_force_srv = self.create_service(SetForce, 'inspire_hand_set_force_srv', self.set_force_srv_callback)

        self.pub = self.create_publisher(AngleState, 'inspire_hand_angle_state', qos_profile_services_default)

        self.hand = InspireHandAPI('/dev/ttyUSB0', 115200)
    
    def set_angle_srv_callback(self, request, response):
        self.get_logger().info('Incoming request')
        response.success = True
        return response
    
    def set_speed_srv_callback(self, request, response):
        self.get_logger().info('Incoming request')
        response.success = True
        return response
    
    def set_force_srv_callback(self, request, response):
        self.get_logger().info('Incoming request')
        response.success = True
        return response
    
def main():
    rclpy.init()
    inspire_hand_srv = InspireHandSrv()
    rclpy.spin(inspire_hand_srv)
    rclpy.shutdown()

if __name__ == '__main__':
    # main()
    pass