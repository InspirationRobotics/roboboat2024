import lsb_release

if lsb_release.get_distro_information()["RELEASE"] == "18.04":
    import ctypes

    libgcc_s = ctypes.CDLL("libgcc_s.so.1")

import platform
import signal
import threading
import time
from statistics import mean
from struct import pack, unpack

import geographic_msgs.msg
import geometry_msgs.msg
import mavros_msgs.msg
import mavros_msgs.srv
import numpy as np
import rclpy
import sensor_msgs.msg
import std_msgs.msg
from simple_pid import PID

from ..utils import statusLed, deviceHelper
from ..utils.rospyHandler import RosHandler
from ..utils.topicService import TopicService

MODE_MANUAL = "MANUAL"
MODE_STABILIZE = "STABILIZE"
MODE_ALTHOLD = "ALT_HOLD"
MODE_LOITER = "LOITER"
MODE_AUTO = "AUTO"
MODE_GUIDED = "GUIDED"

config = deviceHelper.variables


class ASV(RosHandler):
    def __init__(self):
        super().__init__('asv')

        self.config = config

        super().__init__()
        self.do_publish_thrusters = True
        self.do_get_sensors = True
        self.armed = False
        self.guided = False
        self.mode = ""

        # depth hold
        self.channels = [1500] * 18
        self.thrustTime = time.time()  # timeout for no new thruster
        self.depth = None
        self.do_hold_depth = False
        self.depth_pwm = 0
        self.depth_calib = 0
        self.depth_pid_params = config.get("depth_pid_params", [0.5, 0.1, 0.1])
        self.depth_pid_offset = config.get("depth_pid_offset", 1500)
        self.depth_pid = PID(*self.depth_pid_params, setpoint=0.5)
        self.depth_pid.output_limits = (-self.depth_pid_params[0], self.depth_pid_params[0])

        # init topics
        self.TOPIC_STATE = TopicService("/mavros/state", mavros_msgs.msg.State)
        self.SERVICE_ARM = TopicService("/mavros/cmd/arming", mavros_msgs.srv.CommandBool)
        self.SERVICE_SET_MODE = TopicService("/mavros/set_mode", mavros_msgs.srv.SetMode)
        self.SERVICE_SET_PARAM = TopicService("/mavros/param/set", mavros_msgs.srv.ParamSet)
        self.SERVICE_GET_PARAM = TopicService("/mavros/param/get", mavros_msgs.srv.ParamGet)

        # movement
        # only works in auto/guided mode
        self.TOPIC_SET_VELOCITY = TopicService("/mavros/setpoint_velocity/cmd_vel_unstamped", geometry_msgs.msg.Twist)
        self.TOPIC_SET_RC_OVR = TopicService("/mavros/rc/override", mavros_msgs.msg.OverrideRCIn)

        # sensory
        self.TOPIC_GET_IMU_DATA = TopicService("/mavros/imu/data", sensor_msgs.msg.Imu)
        self.TOPIC_GET_CMP_HDG = TopicService("/mavros/global_position/compass_hdg", std_msgs.msg.Float64)
        self.TOPIC_GET_RC = TopicService("/mavros/rc/in", mavros_msgs.msg.RCIn)
        self.TOPIC_GET_MAVBARO = TopicService("/mavlink/from", mavros_msgs.msg.Mavlink)
        # https://discuss.bluerobotics.com/t/ros-support-for-bluerov2/1550/24
        self.TOPIC_GET_BATTERY = TopicService("/mavros/battery", sensor_msgs.msg.BatteryState)

        # custom topics
        self.asv_COMPASS = TopicService("/asv/devices/compass", std_msgs.msg.Float64)
        self.asv_IMU = TopicService("/asv/devices/imu", sensor_msgs.msg.Imu)
        # self.asv_BARO = TopicService("/asv/devices/baro", std_msgs.msg.Float32MultiArray)
        self.asv_GET_THRUSTERS = TopicService("/asv/devices/thrusters", mavros_msgs.msg.OverrideRCIn)
        self.asv_GET_DEPTH = TopicService("/asv/devices/setDepth", std_msgs.msg.Float64)
        self.asv_GET_REL_DEPTH = TopicService("/asv/devices/setRelativeDepth", std_msgs.msg.Float64)
        self.asv_GET_ARM = TopicService("/asv/status/arm", std_msgs.msg.Bool)
        self.asv_GET_MODE = TopicService("/asv/status/mode", std_msgs.msg.String)

    def arm(self, status: bool):
        if status:
            statusLed.red(True)
        else:
            statusLed.red(False)
        data = mavros_msgs.srv.CommandBoolRequest()
        data.value = status
        self.SERVICE_ARM.set_data(data)
        result = self.service_caller(self.SERVICE_ARM, timeout=30)
        return result.success, result.result

    def get_param(self, param: str):
        data = mavros_msgs.srv.ParamGetRequest()
        data.param_id = param
        self.SERVICE_GET_PARAM.set_data(data)
        result = self.service_caller(self.SERVICE_GET_PARAM, timeout=30)
        return result.success, result.value.integer, result.value.real

    def set_param(self, param: str, value_integer: int, value_real: float):
        data = mavros_msgs.srv.ParamSetRequest()
        data.param_id = param
        data.value.integer = value_integer
        data.value.real = value_real
        self.SERVICE_SET_PARAM.set_data(data)
        result = self.service_caller(self.SERVICE_SET_PARAM, timeout=30)
        return result.success, result.value.integer, result.value.real

    def change_mode(self, mode: str):
        # ALT_HOLD = stabilize + depth hold
        if mode == MODE_ALTHOLD:
            self.do_hold_depth = True
            mode = MODE_STABILIZE
        data = mavros_msgs.srv.SetModeRequest()
        data.custom_mode = mode
        self.SERVICE_SET_MODE.set_data(data)
        result = self.service_caller(self.SERVICE_SET_MODE, timeout=30)
        return result.mode_sent

    def calibrate_depth(self, sample_time=3):
        print("\n[depth_calib] Starting Depth Calibration...")
        samples = []

        # wait for depth data
        while self.depth == None:
            pass

        prevDepth = self.depth
        start_time = time.time()

        # get depth data for sample_time seconds
        # then take the mean of the data
        while time.time() - start_time < sample_time:
            if self.depth == prevDepth:
                continue

            samples.append(self.depth)
            prevDepth = self.depth

        self.depth_calib = mean(samples)
        print(f"[depth_calib] Finished. Surface is: {self.depth_calib}")

    def depth_hold(self, depth):
        try:
            if depth < -9 or depth > 100:
                return
            self.depth_pwm = int(self.depth_pid(depth) * -1 + self.depth_pid_offset)
            print(f"[depth_hold] depth: {depth:.4f} depthMotorPower: {self.depth_pwm} Target: {self.depth_pid.setpoint}")
            # assume motor range is 1200-1800 so +-300
        except Exception as e:
            print("DepthHold error")
            print(e)

    # dont have baro for roboboat
    # def get_baro(self, baro):
    #     try:
    #         if baro.msgid == 143:
    #             p = pack("QQ", *baro.payload64)
    #             time_boot_ms, press_abs, press_diff, temperature = unpack("Iffhxx", p)  # pressure is in mBar

    #             # calculate depth
    #             press_diff = round(press_diff, 2)
    #             press_abs = round(press_abs, 2)
    #             self.depth = (press_abs / (997.0474 * 9.80665 * 0.01)) - self.depth_calib

    #             # publish baro data
    #             baro_data = std_msgs.msg.Float32MultiArray()
    #             baro_data.data = [self.depth, press_diff]
    #             self.asv_BARO.set_data(baro_data)
    #             self.topic_publisher(topic=self.asv_BARO)

    #             # hold depth
    #             if self.do_hold_depth and self.armed:
    #                 self.depth_hold(self.depth)
    #     except Exception as e:
    #         print("Baro Failed")
    #         print(e)

    def set_depth(self, depth):
        if depth.data < 0:
            return
        self.depth_pid.setpoint = depth.data

    def set_rel_depth(self, relative_depth):
        new_depth = self.depth_pid.setpoint + relative_depth.data
        if new_depth < 0:
            return
        self.depth_pid.setpoint = new_depth

    def batteryIndicator(self, msg):
        if self.config.get("battery_indicator", False):
            self.voltage = msg.voltage
            if self.voltage < 13.5:
                statusLed.flashRed()

    def thrusterCallback(self, msg):
        self.thrustTime = time.time()
        self.channels = list(msg.channels)
        #print(self.channels)

    def enable_topics_for_read(self):
        self.topic_subscriber(self.TOPIC_STATE, self.update_parameters_from_topic)
        self.topic_subscriber(self.TOPIC_GET_IMU_DATA)
        self.topic_subscriber(self.TOPIC_GET_CMP_HDG)
        self.topic_subscriber(self.TOPIC_GET_RC)
        self.topic_subscriber(self.asv_GET_THRUSTERS, self.thrusterCallback)
        self.topic_subscriber(self.asv_GET_ARM)
        self.topic_subscriber(self.asv_GET_MODE)
        self.topic_subscriber(self.TOPIC_GET_MAVBARO, self.get_baro)
        self.topic_subscriber(self.asv_GET_DEPTH, self.set_depth)
        self.topic_subscriber(self.asv_GET_REL_DEPTH, self.set_rel_depth)
        self.topic_subscriber(self.TOPIC_GET_BATTERY, self.batteryIndicator)

    def start_threads(self):
        # start sensor and thruster thread
        sensor_thread = threading.Thread(target=self.get_sensors, daemon=True)
        thruster_thread = threading.Thread(target=self.publish_thrusters, daemon=True)
        sensor_thread.start()
        thruster_thread.start()

    def publish_sensors(self):
        try:
            if self.imu != None:
                imu_data = self.imu
                self.asv_IMU.set_data(imu_data)
                self.topic_publisher(topic=self.asv_IMU)
            if self.hdg != None:
                comp_data = self.hdg
                self.asv_COMPASS.set_data(comp_data)
                self.topic_publisher(topic=self.asv_COMPASS)
        except Exception as e:
            print("publish sensors failed")
            print(e)

    def publish_thrusters(self):
        while rclpy.ok() and self.do_publish_thrusters:
            if self.connected:
                try:
                    channels = self.channels
                    if time.time() - self.thrustTime > 1:
                        channels = [1500] * 18
                    if self.do_hold_depth:
                        channels[2] = self.depth_pwm
                    thruster_data = mavros_msgs.msg.OverrideRCIn()
                    thruster_data.channels = channels
                    # print(f"[THRUSTER_SEND]: {thruster_data.channels}")
                    self.TOPIC_SET_RC_OVR.set_data(thruster_data)
                    self.topic_publisher(topic=self.TOPIC_SET_RC_OVR)
                except Exception as e:
                    print("Thrusters publish failed")
                    print(e)
            time.sleep(0.1)

    def get_sensors(self):
        while rclpy.ok() and self.do_get_sensors:
            if self.connected:
                try:
                    self.hdg = self.TOPIC_GET_CMP_HDG.get_data_last()
                    self.imu = self.TOPIC_GET_IMU_DATA.get_data_last()
                    armRequest = self.asv_GET_ARM.get_data()
                    modeRequest = self.asv_GET_MODE.get_data()
                    if armRequest != None:
                        self.armRequest = armRequest.data
                        while asv.armed != self.armRequest:
                            self.arm(self.armRequest)
                            time.sleep(2)
                    if modeRequest != None:
                        self.modeRequest = modeRequest.data
                        while self.mode != self.modeRequest:
                            self.change_mode(self.modeRequest)
                            time.sleep(0.5)
                    self.publish_sensors()
                except Exception as e:
                    print("sensor failed")
                    print(e)
                time.sleep(0.1)

    def update_parameters_from_topic(self, data):
        if self.connected:
            try:
                self.armed = data.armed
                if not self.armed:
                    self.depth_pid.reset()
                self.mode = data.mode
                self.guided = data.guided
            except Exception as e:
                print("state failed")
                print(e)


def main():
    try:
        # wait for connection
        while not asv.connected:
            print("Waiting to connect...")
            time.sleep(0.5)
        print("Connected!")

        # calibrate depth
        asv.change_mode(MODE_ALTHOLD)
        asv.calibrate_depth()
        time.sleep(2)
        # arming
        # while not asv.armed:
        #     print("Attempting to arm...")
        #     asv.arm(True)
        #     time.sleep(3)
        # print("Armed!")
        print("\nNow beginning loops...")
        asv.start_threads()

    except KeyboardInterrupt:
        # stopping sub on keyboard interrupt
        asv.arm(False)


def onExit(signum, frame):
    try:
        print("\nDisarming and exiting...")
        asv.arm(False)
        rclpy.shutdown("Rospy Exited")
        time.sleep(1)
        while rclpy.ok():
            pass
        print("\n\nCleanly Exited")
        exit(1)
    except:
        pass


signal.signal(signal.SIGINT, onExit)

if __name__ == "__main__":
    asv = ASV()
    asv.enable_topics_for_read()
    mainTh = threading.Thread(target=main, daemon=True)
    mainTh.start()
    asv.connect("pix_standalone", rate=20)  # change rate to 10 if issues arrive
