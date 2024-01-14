#!/bin/bash

python3 ~/inspiration_robotx2022/nodes/navigation/current_pos.py &
python3 ~/inspiration_robotx2022/nodes/navigation/mission_planner.py &
python3 ~/inspiration_robotx2022/nodes/navigation/kinematics.py &
python3 ~/inspiration_robotx2022/nodes/navigation/linear.py &
python3 ~/inspiration_robotx2022/nodes/navigation/yaw.py &
python3 ~/inspiration_robotx2022/nodes/navigation/straife.py &
