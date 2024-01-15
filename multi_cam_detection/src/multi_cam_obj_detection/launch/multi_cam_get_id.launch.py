from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='multi_cam_obj_detection',
             executable='cams', 
             output='screen'),
        
        Node(package='rviz2', 
             executable='rviz2', 
             output='screen'),
    ])