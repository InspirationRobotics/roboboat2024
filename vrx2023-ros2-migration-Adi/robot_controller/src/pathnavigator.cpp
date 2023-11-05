#include "pathnavigator.h"

#include "std_msgs/Float32.h"

#include <math.h>

void init_path_navigator(Path_Navigator* navigator, ros::NodeHandle node_handle) {
    navigator->fl_publisher = node_handle.advertise<std_msgs::Float32>("/wamv/thrusters/left_front_thrust_cmd", 32);
    navigator->fr_publisher = node_handle.advertise<std_msgs::Float32>("/wamv/thrusters/right_front_thrust_cmd", 32);
    navigator->bl_publisher = node_handle.advertise<std_msgs::Float32>("/wamv/thrusters/left_rear_thrust_cmd", 32);
    navigator->br_publisher = node_handle.advertise<std_msgs::Float32>("/wamv/thrusters/right_rear_thrust_cmd", 32);
}

void write_motor_values(Path_Navigator* navigator, Motor_Values values) {
    std_msgs::Float32 msg;

    msg.data = values.fl;
    navigator->fl_publisher.publish(msg);

    msg.data = values.fr;
    navigator->fr_publisher.publish(msg);
    
    msg.data = values.bl;
    navigator->bl_publisher.publish(msg);
    
    msg.data = values.br;
    navigator->br_publisher.publish(msg);
}

void write_motion_vector(Path_Navigator* navigator, float motion_x, float motion_y, float rotation) {
    Motor_Values mv;

    float motion_length = abs(motion_x) + abs(motion_y);

    if (motion_length == 0) {motion_length = 1;}

    float mx = motion_x / motion_length;
    float my = motion_y / motion_length;

    float total = abs(mx) + abs(my) + abs(rotation);

    mx /= total;
    my /= total;
    rotation /= total;

    mv.fl = ( mx + my) + rotation;
    mv.fr = (-mx + my) - rotation;
    mv.bl = (-mx + my) + rotation;
    mv.br = ( mx + my) - rotation;

    printf("fl: %f, fr: %f, bl: %f, br: %f\n", mv.fl, mv.fr, mv.bl, mv.br);

    write_motor_values(navigator, mv);
}