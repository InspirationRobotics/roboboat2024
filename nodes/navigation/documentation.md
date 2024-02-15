**Overall RoboBoat accomplishments**
We attempted 4 tasks in competition and completed 3, all using GPS navigation and surveying.
We did not attempt to use perception for our missions as would be required for many of the other missions.
We also had code for actuating the water pump for the Duck Wash mission, but did not implement it in time for attempting the task in competition.

**How the code works**
Each file run for each mission uses ROS to transfer data from our differential GPS. It uses this GPS data to calculate heading.
Then, based on angle and radius thresholds for each waypoint, the mission files send commands to serial_server.py,
which sends serial messages to an Arduino with simple forwards/backwards on/off controls for the thrusters.

**What we did not attempt**
- PID control for motion
- perception and computer vision
- mission planning for the boat to do several missions in one code


**We used files for each mission as follows:**
1. *Nav Channel*: gate_delay_thr_10.py
2. *Follow the Path*: gate_delay_thr_10.py (attempted but not successful; need to test with all motors intact)
3. *Docking*: 
4. *Speed Challenge*: gate_delay_thr_10.py

**These files were also used across all missions:**
- serial_server.py (inside mission_planner --> enter_the_gates_roboboat)
- motor_mix.ino (inside mission_planner --> enter_the_gates_roboboat)
-

**These files were also used for bench tests**
 - terminal_key_pub.py (for testing motor_mix.ino; found in mission_planner --> enter_the_gates_roboboat)
