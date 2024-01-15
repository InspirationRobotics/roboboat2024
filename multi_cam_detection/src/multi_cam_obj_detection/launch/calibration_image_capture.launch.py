from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
     
     config = os.path.join(get_package_share_directory('multi_cam_obj_detection'),
        'config',
        'img_capture.yaml'
        )
     
     return LaunchDescription([      
        Node(package='multi_cam_obj_detection',
             name = "cams",
             executable='cams',
             parameters = [config])
    ]) 