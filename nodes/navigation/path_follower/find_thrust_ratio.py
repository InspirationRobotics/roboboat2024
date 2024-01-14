from t500 import t500_setpwm
from torqueedo import torqueedo_setpwr
import rclpy
from rclpy.node import Node
from transform import * 

from std_msgs.msg import String


class FindThrustRatio(Node):
    
    def __init__(self):
        super().__init__('find_thrust_ratio')
        self.gps_s = self.create_subscription(
            PoseInfo,
            '/wamv/gps/global_pose',
            self.gps_cb,
            10)
        self.gps_s  # prevent unused variable warning

        self.gps_hdg = self.create_subscription(
            PoseInfo,
            '/wamv/gps/global_pose',
            self.gps_cb,
            10)
        self.gps_hdg  # prevent unused variable warning

        # lat, lon, hdg, time
        self.p_prev = []
        self.p = []
        
    def gps_cb(self, msg):
        self.p_prev = p
        self.p = [msg.p.x, msg.p.y, msg.p.z, msg.ts]

    def gps_hdg(self, msg):
        self.hdg = msg.data

    def gps_d(p, p_prev):
        dt = p[3] - p_prev[3]
        if p_prev != [] and p != []:
            return [(p[0] - p_prev[0]) / dt, (p[1] - p_prev[1]) / dt, (p[2] - p_prev[2]) / dt]

        return []

    def v_angle_strafe():
        return normalize_angle(angle_between_points([0, 0], self.gps_d()) - (self.gps_hdg - (PI / 2)))

        
def main(args=None):
    rclpy.init(args=args)

    ftr = FindThrustRatio()


    tr = 1
    while rclpy.ok() and (ftr.v_angle_strafe() > (PI / 16) or ftr.v_angle_strafe() < 0):
        if (ftr.v_angle() > 0):
            tr -= 0.1
        if (ftr.v_angle() < 0):
            tr += 0.1

        torqueedo_setpwr(tr, -tr)
        t500_setpwm(1900, 1300)
        rclpy.spin_once(ftr)

    print("thrust ratio:")
    print(tr)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
