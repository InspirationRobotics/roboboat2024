import rclpy
from rclpy.node import Node

from obj_msg.msg import Obj
from obj_msg.msg import Objlst
from time import sleep

gatelst = []

class MissionPlanner(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Objlst,
            '/gate',
            self.gate_callback,
            10)
        self.subscription  # prevent unused variable warning

    def gate_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def gate_action():
        
def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    while (rclpy.ok()):
        rclpy.spin_once(minimal_subscriber)
        sleep(1)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
