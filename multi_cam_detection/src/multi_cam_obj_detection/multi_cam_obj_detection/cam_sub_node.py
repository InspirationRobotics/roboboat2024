import cv2
import depthai as dai
import message_filters
import os
import torch
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import (Header)
from rclpy.parameter import Parameter
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from vision_msgs.msg import (
    Detection2D,
    Detection2DArray,
    BoundingBox2D,
    ObjectHypothesisWithPose,
    ObjectHypothesis
)
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MultiCamSubscriber(Node):
        def __init__(self):
            super().__init__("cam_subs")
            print("torch version is", torch.__version__)
            # _cam = Node("cam_subs")
            
            self.get_logger().info(f"{bcolors.OKGREEN}Initializing MultiCamSubscriber{bcolors.ENDC}")
            
            # Declare parameters
            self.declare_parameter("model_path", "~/multi_cam_detection/src/multi_cam_obj_detection/multi_cam_obj_detection/yolov5s.pt")
            self.declare_parameter("queue_size", 1)
            self.declare_parameter("slop", 0.1)
            self.declare_parameter("cam_topics", ["None"])
            self.declare_parameter("bbox_topics", ["None"])
            self.declare_parameter("mode_iou", 0.5)
            self.declare_parameter("model_conf", 0.5)
            self.declare_parameter("hub_cfg", "")
            
            
            # Get parameters
            model_path = self.get_parameter('model_path').get_parameter_value().string_value
            self.iou = self.get_parameter('mode_iou').get_parameter_value().double_value
            self.conf = self.get_parameter('model_conf').get_parameter_value().double_value
            self.sync_queue = self.get_parameter('queue_size').get_parameter_value().integer_value
            self.sync_slop = self.get_parameter('slop').get_parameter_value().double_value
            self.topics = self.get_parameter('cam_topics').get_parameter_value().string_array_value
            self.bbox_topic = self.get_parameter('bbox_topics').get_parameter_value().string_array_value
            self.hub_cfg = self.get_parameter('hub_cfg').get_parameter_value().string_value
            
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            
            self.get_logger().info(f"{bcolors.OKGREEN}Loading model {model_path} with conf {str(self.conf)}, iou {str(self.iou)} {bcolors.ENDC}")
            
            self.model = torch.hub.load(self.hub_cfg, 'custom', path=model_path, source='local', verbose=False, force_reload=True).to(self.device)
            self.model.iou = self.iou
            self.model.conf = self.conf

            self.get_logger().info(f"{bcolors.OKCYAN}Subscribing to Topics: {bcolors.ENDC}" + str(self.topics))
             
            self.camera_subs = []
            self.bbox_pub = []
            self.bridge = CvBridge()
            
            self.annotated_publisher = self.create_publisher(Image, "annotated_image", 10)
            
            for topic in self.topics:
                self.camera_subs.append(message_filters.Subscriber(self, Image, topic))
                
            for topic in self.bbox_topic:
                self.bbox_pub.append(self.create_publisher(Detection2DArray, topic, 10))
            
            ts = message_filters.ApproximateTimeSynchronizer(self.camera_subs, self.sync_queue, self.sync_slop)
            ts.registerCallback(self.on_images_recieve)
            
            self.get_logger().info(f"{bcolors.OKGREEN}MultiCamSubscriber Initialized{bcolors.ENDC}")          
        
        def on_images_recieve(self, *args):
            images = [self.bridge.imgmsg_to_cv2(msg, "bgr8") for msg in args] # RGB, ndarray
            # dim = (640, 640)
            # images = [cv2.resize(image, dim, interpolation=cv2.INTER_AREA) for image in images]
            # self.get_logger().info()
            bboxs, scores, classes = self.process_images(images)
            self.publish_2d_boxes_array(bboxs, scores, classes)
           
            
            
        def process_images(self, images):
            for i in range(len(images)):
                images[i] = cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB)
            
            outputs = self.model(images).tolist()
            
            result_boxs = [[] for _ in range(len(outputs))]
            scores = [[] for _ in range(len(outputs))]
            classes = [[] for _ in range(len(outputs))]

            imgs = [o.render() for o in outputs]
            
            for i in range(len(imgs)):
                for img in imgs[i]:
                    # img = img.cpu().numpy()
                    # img = img.transpose((1, 2, 0))
                    # img = img * 255
                    # img = img.astype(np.uint8)
                    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    self.annotated_publisher.publish(self.bridge.cv2_to_imgmsg(img, "rgb8"))
                    
                   
            
            # for i in range(len(imgs)):
            #     self.annotated_publisher.publish(self.bridge.cv2_to_imgmsg(imgs[i], "bgr8"))
                
            
            for output in outputs:
                for i, det in enumerate(output.pred):
                    for *box, conf, cls in det:
                        cls = int(cls.cpu().detach().numpy()) 
                        conf = round(float(conf.cpu().detach().numpy()), 2)
                        minx, miny, maxx, maxy = [
                            int(t.cpu().detach().numpy()) for t in box]
                        result_boxs[i].append([minx, miny, maxx, maxy])
                        scores[i].append(conf)
                        classes[i].append(self.model.names[cls])
            
            return result_boxs, scores, classes

        
        def publish_2d_boxes_array(self, boxes, scores, classes):
            for i, (b, s, c) in enumerate(zip(boxes, scores, classes)):
                header = Header()
                header.stamp = self.get_clock().now().to_msg()
                detection_2d_array_msg = Detection2DArray(header=header)
                for box, score, cls in zip(b, s, c):
                    detection_2d_msg = Detection2D(header=header)
                    minx, miny, maxx, maxy = box
                    detection_2d_msg.bbox = BoundingBox2D(
                    center=Pose2D(
                    x=float((maxx + minx) / 2), y=float((maxy + miny) / 2), theta=0.0
                    ),
                    size_x=float(maxx - minx),
                    size_y=float(maxy - miny),
                    )
                    obs = ObjectHypothesisWithPose()
                    obs.hypothesis = ObjectHypothesis(class_id=cls, score=float(score))
                    detection_2d_msg.results.append(obs)
                    detection_2d_array_msg.detections.append(detection_2d_msg)
                self.bbox_pub[i].publish(detection_2d_array_msg)
            


def main():
    rclpy.init()
 
    cam_sub = MultiCamSubscriber()

    rclpy.spin(cam_sub)

if __name__ == "__main__":
    main()