import cv2
import depthai as dai
import contextlib

import os
from sensor_msgs.msg import Image
from std_msgs.msg import Int16
from cv_bridge import CvBridge
from rclpy.parameter import Parameter
import rclpy
from rclpy.node import Node


class CamImageNode(Node):

    def __init__(self):
        super().__init__("cam_image_node")
        self.device_info = dai.Device.getAllAvailableDevices()
        self.q_rgb_list = []
        self.num_devices = len(self.device_info)
        self.cam_publishers = []
        self.bridge = CvBridge()
        self.device_publisher = self.create_publisher(Int16, "device/info", 10)
        self.mxids = []
        
        self.get_logger().info("Initializing camera capture node")
        self.declare_parameter("img_width", 600)
        self.declare_parameter("img_height", 300)
        self.declare_parameter("save_path", "./")
        
        self.img_width = self.get_parameter("img_width").get_parameter_value().integer_value
        self.img_height = self.get_parameter("img_height").get_parameter_value().integer_value
        self.save_path = self.get_parameter("save_path").get_parameter_value().string_value
        
        
        self.get_logger().info("img_width: " + str(self.img_width) +  " img_height: " + str(self.img_height))

    def getPipeline(self, preview_res = (1448, 568)):
        # Start defining a pipeline
        pipeline = dai.Pipeline()

        # Define a source - color camera
        cam_rgb = pipeline.create(dai.node.ColorCamera)
        # For the demo, just set a larger RGB preview size for OAK-D
        cam_rgb.setPreviewSize(preview_res[0], preview_res[1]) # FIX ME, need to match what ever pipeline we are using
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)

        # Create output
        xout_rgb = pipeline.create(dai.node.XLinkOut)
        xout_rgb.setStreamName("rgb")
        cam_rgb.preview.link(xout_rgb.input)

        return pipeline


    def camera_initialization(self, path = "./"):

        # https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack
        with contextlib.ExitStack() as stack:
            device_infos = dai.Device.getAllAvailableDevices()
            if len(device_infos) == 0:
                self.get_logger.info("No device found, exiting")
                exit()
            else:
                print("Found", len(device_infos), "devices")

            for device_info in device_infos:
                openvino_version = dai.OpenVINO.Version.VERSION_2021_4
                usb2_mode = False
                device = stack.enter_context(dai.Device(openvino_version, device_info, usb2_mode))

                # Note: currently on POE, DeviceInfo.getMxId() and Device.getMxId() are different!
                print("=== Connected to " + device_info.getMxId())
                mxid = device.getMxId()
                self.mxids.append(mxid)
                self.cam_publishers.append(self.create_publisher(Image, "cam" + mxid + "/image", 10))
                print("   >>> MXID:", mxid)

                # Get a customized pipeline based on identified device type
                pipeline = self.getPipeline(preview_res=(self.img_width, self.img_height))
                print("   >>> Loading pipeline at resolution ", self.img_width, "x", self.img_height)
                device.startPipeline(pipeline)

                # Output queue will be used to get the rgb frames from the output defined above
                q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
                stream_name = "rgb-" + mxid + "-" + "OAK-D"
                self.q_rgb_list.append((q_rgb, stream_name))

                self.image_display_opencv(path)
            
                            
                            
    
    def image_display_opencv(self, path): # debug
        img_cnt = 0
        print("Starting image display, press 'q' to quit, press 's' to save, make sure change to absolute path")
        input("Press Enter to continue...")
        while True:
            for q_rgb, stream_name in self.q_rgb_list:
                in_rgb = q_rgb.tryGet()
                if in_rgb is not None:
                    cv2.imshow(stream_name, in_rgb.getCvFrame())
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('s'):
                        cv2.imwrite(os.path.join(path, str(img_cnt) + '.bmp'), in_rgb.getCvFrame())
                        print("Saved image: ", img_cnt)
                        img_cnt += 1
                    elif key == ord('q'):
                        exit("user quit")


def main():
    rclpy.init()
    cam_node = CamImageNode()
    cam_node.camera_initialization()


if __name__ == "main":
    main()