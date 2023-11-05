cmake_minimum_required(VERSION 3.0.2)
project(navigation)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  sensor_msgs
  geometry_msgs
)

catkin_package()



