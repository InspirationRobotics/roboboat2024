import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraSubscriberNode(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/wamv/sensors/cameras/front_left_camera_sensor/image_raw',
            self.image_callback,
            10)
        self.bridge = CvBridge()

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except Exception as e:
            self.get_logger().error("Error converting image: %s" % str(e))
            return

        # Display the image using OpenCV
        cv2.imshow("Front Left Camera", cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    camera_subscriber = CameraSubscriberNode()
    rclpy.spin(camera_subscriber)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
