#!/bin/bash

source /opt/ros/galactic/setup.bash
source ~/livox_projection/install/setup.bash

sudo chmod 777 /dev/ttyACM0
# start perception
start cam
start sub
start lidar_driver
start projection
start gps

#wamv

#python3 ~/inspiration_robotx2022/nodes/navigation/nmea_reader.py &
#python3 ~/inspiration_robotx2022/nodes/navigation/differential.py &
#python3 ~/inspiration_robotx2022/nodes/navigation/torqeedo_client.py &
#python3 ~/inspiration_robotx2022/nodes/navigation/t500_client.py &

#start ros bags
#ros2 bag record /annotated_image /cam184430104161721200/image /distances /livox/imu /livox/lidar /livox/stamped /parameter_events /right_camera/image /right_set/bbox /rosout /wamv/sensors/gps/hdg /wamv/sensors/gps/lat /wamv/sensors/gps/lon /wamv/torqeedo/motor_cmd
