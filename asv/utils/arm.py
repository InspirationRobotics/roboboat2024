from ..device.pix_standalone import ASV
from . import statusLed
import os


def arm():
    asv = ASV()
    asv.arm(True)
    statusLed.red(True)


if __name__ == "__main__":
    arm()
