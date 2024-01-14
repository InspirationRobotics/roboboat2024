import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int16
import time

# note 1250 lower bound, 1750 upper bound, do not know what is forward and backward

# hardcodied the publishing
class testTorquedo(Node):
    def __init__(self):
        super().__init__('test_torquedo')
        self.mc_pub = self.create_publisher(String, '/wamv/torqeedo/motor_cmd',10)
        print("init done")


def main(args=None):
        rclpy.init(args=args)
        mc = testTorquedo()
        time.sleep(3)
        pwrL = 100
        pwrR = 100
        posR = 500
        posL = 500

        pub_str = '{"lp":' + str(pwrL) +  ', "rp":' + str(pwrR) + ', "la":' + str(posL) +', "ra":'+str(posR)+ '}'
        msg = String()
        msg.data = pub_str
        mc.mc_pub.publish(msg)
        print("step1 done")
        time.sleep(3)

#manuvers
        pwrL = 0
        pwrR = 0
        posR = 0
        posL = 0
        pub_str = '{"lp":' + str(pwrL) +  ', "rp":' + str(pwrR) + ', "la":' + str(posL) +', "ra":'+str(posR)+ '}'
        msg = String()
        msg.data = pub_str
        mc.mc_pub.publish(msg)
        print("step2 done")

if __name__ == '__main__':
    main()
