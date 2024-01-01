"""
Description
---
Interface for the CV class used for each mission

"""

# import what you need from within the package

import time

import cv2
import numpy as np
import shapely


class CV:
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
        self.current_sub = self.config.get("sub", "onyx")
        if self.current_sub == "onyx":
            self.camera = "/auv/camera/videoOAKdRawBottom"
            self.model = "bins3"

        self.viz_frame = None
        self.error_buffer = []

        print("[INFO] Bin CV init")

    def run(self, frame, target, oakd_data):
        """
        Should be all the code required to run the CV.

        Could be a loop, grabbing frames using ROS, etc.

        Parameters
        ----------
        frame: the frame from the camera
        target: could be any type of information, for example the thing to look for
        oakd_data: only applies for Oak-D cameras, this is the list of detections
        """
        return {"lateral": 0, "forward": 0, "end": False}, frame


if __name__ == "__main__":
    """
    Testing purposes only
    ----------
    If you run this file directly, the following code will be executed

    Run "python -m auv.cv.template_cv"
    """

    # Create a CV object with arguments
    cv = CV()

    # here you can for example initialize your camera, etc
    cap = cv2.VideoCapture("../../testing_data/")

    while True:
        # grab a frame
        ret, frame = cap.read()
        if not ret:
            break

        # run the cv
        result = cv.run(frame, "some_info", None)

        # do something with the result
        print(f"[INFO] {result}")

        # debug the frame
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
