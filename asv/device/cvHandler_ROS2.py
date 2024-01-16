"""
CV Handler
Author: Maxime Ellerbach
"""
import ctypes
import json
import os
import threading
import time
import traceback

import cv2
import rclpy
from rclpy.node import Node
import cv_bridge as CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String


class CVHandler(Node):
    def __init__(self, **config):
        super().__init__("cv_handler_node")
        self.config = config
        self.active_cv_scripts = {}
        self.subs = {}

    def start_cv(self, file_name, callback, dummy_camera=None):
        if file_name in self.active_cv_scripts:
            self.get_logger().error("Cannot start a script that is already running")
            return

        try:
            module = __import__(f"asv.cv.{file_name}", fromlist=["CV"])
        except Exception as e:
            self.get_logger().error("Error while importing CV module from file name")
            self.get_logger().error(str(e))
            return

        cv_class = getattr(module, "CV", None)
        if cv_class is None:
            self.get_logger().error(
                "No CV class found in file, check the file name and file content"
            )
            return

        if dummy_camera:
            self.active_cv_scripts[file_name] = _DummyScriptHandler(
                file_name, cv_class(**self.config), dummy_camera
            )
        else:
            self.active_cv_scripts[file_name] = _ScriptHandler(
                self, file_name, cv_class(**self.config)
            )
        self.subs[file_name] = self.create_subscription(
            String, f"asv/cv_handler/{file_name}", callback, 10
        )

    def stop_cv(self, file_name):
        if file_name not in self.active_cv_scripts:
            self.get_logger().error("Cannot stop a script that is not running")
            return

        self.active_cv_scripts[file_name].stop()
        del self.active_cv_scripts[file_name]

        self.subs[file_name].destroy()
        del self.subs[file_name]

    def switch_oakd_model(self, file_name, model_name):
        if file_name not in self.active_cv_scripts:
            self.get_logger().error(
                "Cannot change model of a script that is not running"
            )
            return

        if not self.active_cv_scripts[file_name].is_oakd:
            self.get_logger().error(
                "Cannot change model of a script that is not running on an OAK-D camera"
            )
            return

        if not isinstance(model_name, str):
            self.get_logger().error("Model name must be a string")
            return

        self.active_cv_scripts[file_name].pub_oakd_model.publish(model_name)
        self.get_logger().info(f"Model published {model_name}")

    def set_target(self, file_name, target):
        if file_name not in self.active_cv_scripts:
            self.get_logger().error(
                "Cannot change target of a script that is not running"
            )
            return

        self.active_cv_scripts[file_name].target = target


class _ScriptHandler:
    def __init__(self, cv_handler, file_name, cv_object):
        self.cv_handler = cv_handler
        self.cv_object = cv_object
        self.file_name = file_name
        self.camera_topic = getattr(self.cv_object, "camera", None)

        if self.camera_topic is None:
            self.get_logger().warning(
                "No camera topic specified, using default front camera"
            )
            self.camera_topic = "/asv/camera/videoUSBRaw0"

        self.br = CvBridge()

        self.sub_cv = self.cv_handler.create_subscription(
            Image, self.camera_topic, self.callback_cam, 10
        )
        self.pub_viz = self.cv_handler.create_publisher(
            Image, self.camera_topic.replace("Raw", "Output"), 10
        )
        self.pub_out = self.cv_handler.create_publisher(
            String, f"asv/cv_handler/{file_name}", 10
        )
        self.pub_cam_select = self.cv_handler.create_publisher(
            String, "/asv/camsVersatile/cameraSelect", 10
        )

        if "OAKd" in self.camera_topic:
            self.is_oakd = True
            pub_oakd_model_topic = self.camera_topic.replace("Raw", "Model")
            pub_oakd_data_topic = self.camera_topic.replace("Raw", "Data")
            self.pub_oakd_model = self.cv_handler.create_publisher(
                String, pub_oakd_model_topic, 10
            )
            self.sub_oakd_data = self.cv_handler.create_subscription(
                String, pub_oakd_data_topic, self.callback_oakd_data, 10
            )
        else:
            self.is_oakd = False
            self.pub_oakd_model = None
            self.sub_oakd_data = None

        time.sleep(1.5)
        self.initCameraStream()

        self.target = "main"
        self.oakd_data = None
        self.next_frame = None
        self.running = False
        self.closed = False
        self.last_received = time.time()
        self.last_processed = self.last_received

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def callback_cam(self, msg):
        try:
            self.next_frame = self.br.imgmsg_to_cv2(msg)
            self.last_received = time.time()
        except Exception as e:
            self.get_logger().error("Error while converting image to cv2")
            self.get_logger().error(str(e))

    def callback_oakd_data(self, msg):
        try:
            dataList = []
            data = json.loads(msg.data)
            for detections in data.values():
                dataList.append(Detection(detections))
            self.oakd_data = dataList
        except Exception as e:
            self.get_logger().error("Error while converting oakd data to json")
            self.get_logger().error(str(e))
            return

    def initCameraStream(self):
        topic = self.camera_topic
        toSend = {}
        if not self.is_oakd:
            self.camID = int(topic[-1])
        else:
            if "Forward" in topic:
                self.camID = 10
            elif "Bottom" in topic:
                self.camID = 20
            elif "Poe" in topic:
                self.camID = 30
            model = getattr(self.cv_object, "model", None)
            if model is None:
                self.get_logger().info("No oakD model specified, defaulting to raw")
                model = "raw"
            toSend["model"] = model
        toSend["camera_ID"] = self.camID
        toSend["mode"] = "start"
        data = json.dumps(toSend)
        self.pub_cam_select.publish(data)

    def killCameraStream(self, killAll=False):
        if killAll:
            data = json.dumps({"kill": True})
        else:
            toSend = {"camera_id": self.camID, "mode": "stop"}
            data = json.dumps(toSend)
        self.pub_cam_select.publish(data)

    def run(self):
        self.running = True

        while self.running:
            if self.next_frame is None:
                continue
            if self.last_received == self.last:
                continue
            self.last_processed = self.last_received

            # Run the CV
            frame = self.next_frame
            try:
                ret = self.cv_object.run(frame, self.target, self.oakd_data)
            except Exception as e:
                self.cv_handler.get_logger().error(
                    f"Error while running CV {self.file_name}: {e}"
                )
                continue

            if isinstance(ret, tuple) and len(ret) == 2:
                result, viz_img = ret
            elif isinstance(ret, dict):
                result = ret
                viz_img = None
            else:
                self.cv_handler.get_logger().error("CV returned invalid type")
                continue

            # Publish the result
            self.pub_out.publish(json.dumps(result))

            if viz_img is not None:
                self.pub_viz.publish(self.br.cv2_to_imgmsg(viz_img))

    def stop(self):
        self.running = False
        self.thread.join()
        # self.killCameraStream()  # Commented out temporarily so we can continue watching stream post-mission
        self.sub_cv.destroy_subscription()
        self.pub_viz.destroy_publisher()
        self.pub_out.destroy_publisher()
        self.pub_cam_select.destroy_publisher()
        self.closed = True


class _DummyScriptHandler:
    def __init__(self, file_name, cv, dummy):
        self.file_name = file_name
        self.cv = cv

        self.camera_topic = getattr(self.cv, "camera", None)
        if self.camera_topic is None:
            print("[WARN] No camera topic specified, using default front camera")
            self.camera_topic = "/asv/camera/videoUSBRaw0"

        self.is_oakd = False
        self.target = "main"
        self.oakd_data = None
        self.running = False
        self.closed = False

        self.dummy_video = dummy
        self.cap = cv2.VideoCapture(self.dummy_video)
        if not self.cap.isOpened():
            print("[ERROR] [cvHandler] Error while opening dummy video")
            return

        self.thread = threading.Thread(target=self.run)

        self.pub_viz = self.cv.create_publisher(
            Image, self.camera_topic.replace("Raw", "Output"), 10
        )
        self.pub_out = self.cv.create_publisher(
            String, f"asv/cv_handler/{file_name}", 10
        )

    def run(self):
        self.running = True

        while self.running:
            ret, frame = self.cap.read()

            if not ret:
                self.cap = cv2.VideoCapture(self.dummy_video)
                continue

            try:
                ret = self.cv.run(frame, self.target, self.oakd_data)
            except Exception as e:
                traceback.print_exception()
                print(f"[ERROR] [cvHandler] Error while running CV {self.file_name}")
                continue

            if isinstance(ret, tuple) and len(ret) == 2:
                result, viz_img = ret
            elif isinstance(ret, dict):
                result = ret
                viz_img = None
            else:
                print("[ERROR] [cvHandler] CV returned invalid type")
                continue

            self.pub_out.publish(json.dumps(result))

            if viz_img is not None:
                self.pub_viz.publish(self.br.cv2_to_imgmsg(viz_img))

    def stop(self):
        self.running = False
        self.thread.join()

        self.pub_viz.destroy_publisher()
        self.pub_out.destroy_publisher()
        self.closed = True


class Detection:
    def __init__(self, data):
        self.label = data[0]
        self.confidence = data[1]
        self.xmin = data[2]
        self.xmax = data[3]
        self.ymin = data[4]
        self.ymax = data[5]


if __name__ == "__main__":

    def dummy_callback(msg):
        print(f"[INFO] received: {msg.data}")

    rclpy.init()
    cv = CVHandler()
    cv.start_cv("template_cv", dummy_callback)
    rclpy.spin(cv)
    rclpy.shutdown()
