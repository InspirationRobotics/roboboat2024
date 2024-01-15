from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
      
      config = os.path.join(get_package_share_directory('multi_cam_obj_detection'),
      'config',
      'cam.yaml'
      )
      
      return LaunchDescription([
      Node(package='multi_cam_obj_detection',
             name = "cams",
             executable='cams', 
             output='screen',
             parameters = [config],
             remappings = [('/cam1844301011FF0A1300/image', 'right_camera/image'),
                     #       ('/cam184430104161721200/image', 'left_camera/image')
                           ]),
    ]) 
