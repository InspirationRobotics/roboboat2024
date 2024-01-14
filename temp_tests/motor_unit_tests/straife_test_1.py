import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64
from std_msgs.msg import Int16
import time
import math

# note 1250 lower bound, 1750 upper bound, do not know what is forward and backward

# hardcodied the publishing
class testTorquedo(Node):
    def __init__(self):
        super().__init__('test_torquedo')
        self.mc_t500 = self.create_publisher(String, '/wamv/t500/motor_cmd', 10)
        self.mc_torqeedo = self.create_publisher(String, '/wamv/torqeedo/motor_cmd', 10)
        self.heading = self.create_subscription(Float64, "/wamv/sensors/gps/hdg", self.heading_callback, 10)
        print("init done")

    def initilize_t500(self, seconds):
        time.sleep(seconds)
        pwrL = 1500 # default pwn signal to initialize the t500 thrusters to receieve commands
        pwrR = 1500 # default pwn signal to initialize the t500 thrusters to receieve commands
        pub_str = String()
        pub_str.data = '{"lp":' + str(pwrL) +  ', "rp":' + str(pwrR) +  '}'
        self.mc_t500.publish(pub_str)
        print("initialziation done")
        time.sleep(seconds)

    def heading_callback(self, data):
        self.heading = data.data # assume degress

    # -1 = left, 1 = right 
    # default is strafing right
    def strafe(self, direction, pwr_t500, pwr_torqeedo, seconds):
        #manuvers
        pwrL_t500 = 1500 + (pwr_t500 * direction) # default is motor moving forward
        pwrR_t500 = 1500 + (pwr_t500 * direction) * -1 # default is motor moving backward
        pub_str_t500 = String()
        pub_str_t500.data = '{"lp":' + str(pwrL_t500) +  ', "rp":' + str(pwrR_t500) +  '}'

        pwrL_torqeedo = 0 + (pwr_torqeedo * direction) * -1 # default is motor moving backward
        pwrR_torqeedo = 0 + (pwr_torqeedo * direction) # default is motor moving forward
        posL_torqeedo = -1000 # angle all the way to the left
        posR_torqeedo = 1000 # angle all the way to the right
        pub_str_torqeedo = String()
        pub_str_torqeedo.data = '{"lp":' + str(pwrL_torqeedo) +  ', "rp":' + str(pwrR_torqeedo) + ', "la":' + str(posL_torqeedo) +', "ra":'+str(posR_torqeedo)+ '}'
        msg = String()
        msg.data = pub_str_torqeedo


        print(pub_str_torqeedo)
        print(pub_str_t500)
        self.mc_torqeedo.publish(pub_str_torqeedo)
        self.mc_t500.publish(pub_str_t500)
        print("pwr t500: {}, pwr torqeedo: {}".format(pwr_t500, pwr_torqeedo))
        time.sleep(seconds)
        self.stop()

    def stop(self):
        msg = String()
        msg.data = '{"lp":1500, "rp": 1500"}'
        self.mc_t500.publish(msg)
        print("Motor stopped")

    # 1 is cw, -1 is ccw
    def tank_turning(self, direction, pwr_t500, pwr_torqeedo, seconds):
        #manuvers
        pwrL_t500 = 1500 + (pwr_t500 * direction) # default is motor moving forward
        pwrR_t500 = 1500 + (pwr_t500 * direction) * -1 # default is motor moving backward
        pub_str_t500 = '{"lp":' + str(pwrL_t500) +  ', "rp":' + str(pwrR_t500) +  '}'

        pwrL_torqeedo = 0 + (pwr_torqeedo * direction)  # default is motor moving foward
        pwrR_torqeedo = 0 + (pwr_torqeedo * direction) * -1 # default is motor moving backward
        posL_torqeedo = -1000 # angle all the way to the left
        posR_torqeedo = 1000 # angle all the way to the right
        pub_str_torqeedo = '{"lp":' + str(pwrL_torqeedo) +  ', "rp":' + str(pwrR_torqeedo) + ', "la":' + str(posL_torqeedo) +', "ra":'+str(posR_torqeedo)+ '}'
        msg = String()
        msg.data = pub_str_torqeedo

        mc_torqeedo.mc_pub.publish(msg)
        mc_t500.publish(pub_str_t500)
        print("pwr t500: {}, pwr torqeedo: {}".format(pwr_t500, pwr_torqeedo))
        time.sleep(seconds)

    def cmd(self):
        # calibration_ratio = 0.5
        # torqeedo_power = 1000
        # scaling_factor = 0.25 #because t500 is 0,250 torqeedo is 0,1000
        # t500_power = torqeedo_power * scaling_factor * calibration_ratio

        time = 10 # seconds
        calibration_ratio = 2
        tolerance_degree = 10
        direction = 1 # 1 is right -1 is left
        # Make boat go right
        while self.heading:
            init_heading = self.heading
            print(f"Current heading: {init_heading}")
            torqeedo_power = 200
            t500_power = torqeedo_power * 0.25 * calibration_ratio
            print(f'Current calibration ratio: {calibration_ratio}')

            start_time = time.time()
            self.strafe(direction, t500_power, torqeedo_power, time) # strafe right for 10 seconds
            print(f"T500 power: {t500_power}")
            print(f"torqeedo power: {torqeedo_power}")
            
            angle_diff = init_heading - self.heading
            if (math.abs(angle_diff) > tolerance_degree):
                print(f"Rotated by {angle_diff}. Starting another round of calibration.")
                if (angle_diff == math.abs(angle_diff)): # positive
                    # if positive, then t500 is too strong.
                    calibration_ratio -= 0.1 * direction
                    print(f"Lowering t500 power. Setting ratio to {calibration_ratio}")
                else:
                    # if negative, then t500 is too weak.
                    calibration_ratio += 0.1 * direction
                    print(f"Increasing t500 power. Setting ratio to {calibration_ratio}")
            else:
                print(f"Calibration done. Calibration ratio: {calibration_ratio}")
                break

        # self.initilize_t500(3)

        # # strafe right, 150 pwm t500, 100 pwm torqeedo, 3 seconds
        # self.strafe(1, 150, 200, 3)

        # # stop the thrusters
        # #self.strafe(0, 150, 100, 3)

        # # strafe left, 150 pwm t500, 100 pwm torqeedo, 3 seconds
        # #self.strafe(-1, 150, 100, 3)

        # # stop the thrusters
        # self.strafe(0, 150, 100, 3)
    def test_unit(self):
        self.strafe(1, 10, 0, 1)

def main(args=None):
    rclpy.init(args=args)
    mc = testTorquedo()
    mc.test_unit()
    #mc.cmd()
if __name__ == '__main__':
    main()
