#pragma once


#include "ros/ros.h"

struct Path_Navigator {
    ros::Publisher fl_publisher;
    ros::Publisher fr_publisher;
    ros::Publisher bl_publisher;
    ros::Publisher br_publisher;
};

struct Motor_Values {
    float fl; //front-left = left-front
    float fr; //front-right = right-front
    float bl; //back-left = left-rear lol
    float br; //back-right = right-rear
};

void init_path_navigator(Path_Navigator* navigator, ros::NodeHandle node_handle);
void write_motor_values(Path_Navigator* navigator, Motor_Values values);

void write_motion_vector(Path_Navigator* navigator, float motion_x, float motion_y, float rotation);