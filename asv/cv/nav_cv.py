"""
Description
---
Interface for the CV class used for each mission

Adapted from Team Inspiration Robosub 2023 path_cv.py

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

    def find_red_and_green(self, frame):
        """
        Highlight red and green part of the frame

        Parameters
        ----------
        frame
            the frame from the camera
        """

        ## convert to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask_green = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))
        mask_red1 = cv2.inRange(hsv, (0, 70, 50), (10, 255, 255))
        mask_red2 = cv2.inRange(hsv, (170, 70, 50), (180, 255, 255))
        mask_orange = cv2.inRange(hsv, (10, 100, 20), (25, 255, 255))
        mask_yellow = cv2.inRange(hsv, (21, 39, 64), (40, 255, 255))

        ## slice the red and orange
        imask_red1 = mask_red1 > 0
        imask_red2 = mask_red2 > 0
        imask_orange = mask_orange > 0
        imask_yellow = mask_yellow > 0
        red = np.zeros_like(img, np.uint8)
        red[imask_red1] = img[imask_red1]
        red[imask_red2] = img[imask_red2]
        red[imask_orange] = img[imask_orange]
        red[imask_yellow] = img[imask_yellow]

        ## slice the green
        imask_green = mask_green > 0
        green = np.zeros_like(img, np.uint8)
        green[imask_green] = img[imask_green]

        red_and_green_result = cv2.addWeighted(red, 1, green, 1, 0)

        return red_and_green_result

    # def overlay(image, mask, color, alpha, resize=None):
    #     """Combines image and its segmentation mask into a single image.
    #     https://www.kaggle.com/code/purplejester/showing-samples-with-segmentation-mask-overlay

    #     Parameters
    #     ----------
    #     image: Training image. np.ndarray,
    #     mask: Segmentation mask. np.ndarray,
    #     color: Color for segmentation mask rendering.  tuple[int, int, int] = (255, 0, 0)
    #     alpha: Segmentation mask's transparency. float = 0.5,
    #     resize: If provided, both image and its mask are resized before blending them together.
    #     tuple[int, int] = (1024, 1024))

    #     Returns
    #     -------
    #     image_combined: The combined image. np.ndarray

    #     """
    #     color = color[::-1]
    #     colored_mask = np.expand_dims(mask, 0).repeat(3, axis=0)
    #     colored_mask = np.moveaxis(colored_mask, 0, -1)
    #     masked = np.ma.MaskedArray(image, mask=colored_mask, fill_value=color)
    #     image_overlay = masked.filled()

    #     if resize is not None:
    #         image = cv2.resize(image.transpose(1, 2, 0), resize)
    #         image_overlay = cv2.resize(image_overlay.transpose(1, 2, 0), resize)

    #     image_combined = cv2.addWeighted(image, 1 - alpha, image_overlay, alpha, 0)

    #     return image_combined

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

    # read in image
    img = cv2.imread("./test_data/red-green-buoys.png")
    cv2.imshow("My Image", img)

    # image shows until you press any key
    cv2.waitKey(0)
    result = cv.find_red_and_green(img)

    cv2.imshow("image", result)
    cv2.waitKey(0)

    # image_with_masks = cv.overlay(result, img, color=np.array([0,255,0]), alpha=0.3)
    # cv2.imshow('image', image_with_masks)
    # cv2.waitKey(0)

    # while True:
    #     # grab a frame
    #     ret, frame = cap.read()
    #     if not ret:
    #         break

    #     # run the cv
    #     result = cv.run(frame, "some_info", None)

    #     # do something with the result
    #     print(f"[INFO] {result}")

    #     # debug the frame
    #     cv2.imshow("frame", frame)
    #     if cv2.waitKey(1) & 0xFF == ord("q"):
    #         break
