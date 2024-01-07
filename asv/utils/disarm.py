from ..device.pix_standalone import ASV
from . import statusLed
import os


def disarm():
    asv = ASV()
    asv.arm(False)
    statusLed.red(False)


if __name__ == "__main__":
    disarm()
