VRX Code

As Ashiria left the code, we currently have capabilities for Wayfinding and Station Keeping. 
There are also skeleton files for buoys, a control node, GPS, IMU, straight travel, waypoint generation and navigation and tasks.

I added in the custom .yaml files for our real-life configuration; these may need to be copied to a folder outside of the repo.

We will want to use these resources to get the remaining capabilities:
* Landmark Localization/Characterization
* Acoustic perception
* Wildlife Encounter/Avoid
* Follow the Path
* Acoustic tracking
* Scan, Dock & Deliver

Some good coding practices:
* Clone the repo to your directory using git (automatically installed in Linux)
* create your own branch to avoid merge conflicts when everyone commits
* git add . leads to a commit with all your changes, while git add <filename> leads to a commit with modifications just to that one file
* When we want to combine changes, someone can merge branches

Control Toolbox found at this link:
https://github.com/ros-controls/control_toolbox

**Create python package in ROS2 humble**

cd vrx_ws/src

ros2 pkg create navigation --build-type ament_python --dependencies rclpy

cd ..

colcon build

**Updates as of November 4, 2023:**
We have waypoint navigation capabilities, and can identify colors with cameras.
We can render LiDAR data in a way that humans can understand it, but haven't translated it to depth perception capabilities as of yet.
* The branch that has the most recent code is ros2-migration---Adi
* Branches in ROS (deprecated) are as follows: main, modifications_to_main
* Branches in ROS2 are as follows: ros2-migration, ros2-migration---Adi
* Documentation will be organized in the Team Inspiration Google Drive
