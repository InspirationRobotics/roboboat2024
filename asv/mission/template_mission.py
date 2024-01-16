"""
Template file to create a mission class
"""

# import what you need from within the package

import json

import rclpy
from std_msgs.msg import String

from ..device import cvHandler
from ..motion import robot_control


class TemplateMission:
    cv_files = ["template_cv"]

    def __init__(self, **config):
        """
        Init of the class,
        sets up everything needed for run()

        Parameters
        ----------
        config: dict
            Contains config of the sub

        Returns
        -------
        None
        """
        self.config = config
        self.data: dict = {}  # dict to store the data from the cv handlers
        self.next_data: dict = {}  # dict to store the data from the cv handlers
        self.received: bool = False

        self.robot_control = robot_control.RobotControl()
        self.cv_handler = cvHandler.CVHandler(**self.config)

        # init the cv handlers
        # dummys are used to input a video file instead of the camera
        dummys = self.config.get("cv_dummy", [None] * len(self.cv_files))
        for file_name, dummy in zip(self.cv_files, dummys):
            self.cv_handler.start_cv(file_name, self.callback, dummy=dummy)

        node.get_logger().info("[INFO] Template mission init")

    def callback(self, msg) -> None:
        """Callback for the `cv_handler` output, you can have multiple callback for multiple `cv_handler`"""
        file_name = msg._connection_header["topic"].split("/")[-1]
        data = json.loads(msg.data)
        self.next_data[file_name] = data
        self.received = True

        node.get_logger().info(f"[DEBUG] Received data from {file_name}")

    def run(self):
        """
        Should be all the code required to run the CV.

        Could be a loop, grabbing frames using ROS, etc.

        Parameters
        ----------
        parameter1: description

        Returns
        -------
        description of what this function returns
        """

        while rclpy.ok():
            if not self.received:
                continue

            for key in self.next_data.keys():
                if key in self.data.keys():
                    self.data[key].update(self.next_data[key])
                else:
                    self.data[key] = self.next_data[key]
            self.received = False
            self.next_data = {}

            # TODO: do something with the data

            # here is an example of how to set a target
            self.cv_handler.set_target("template_cv", "albedo")

            break  # TODO: remove this line when making your mission

        node.get_logger().info("[INFO] Template mission run")

    def cleanup(self):
        """
        All the code required after `run()`

        Could be cleaning up, saving data, closing files, etc.
        """
        for file_name in self.cv_files:
            self.cv_handler.stop_cv(file_name)

        # idle the robot
        self.robot_control.movement()
        node.get_logger().info("[INFO] Template mission terminate")


if __name__ == "__main__":
    """
    Testing purposes only
    ----------
    If you run this file directly, the following code will be executed

    Run "python -m asv.cv.template_cv"
    """

    import time
    from asv.utils import deviceHelper

    rclpy.init()
    node = rclpy.create_node("template_mission")

    config = deviceHelper.variables
    config.update(
        {
            # # this dummy video file will be used instead of the camera if uncommented
            # "cv_dummy": ["/somepath/thisisavideo.mp4"],
        }
    )

    # Create a mission object with arguments
    mission = TemplateMission(**config)

    # Run the mission
    mission.run()
    time.sleep(2)
    mission.cleanup()
