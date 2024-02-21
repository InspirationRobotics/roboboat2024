**Overall RoboBoat accomplishments**
We attempted 4 tasks in competition and completed 3, all using GPS navigation and surveying.
We did not attempt to use perception for our missions as would be required for many of the other missions.
We also had code for actuating the water pump for the Duck Wash mission, but did not implement it in time for attempting the task in competition.

**How the code works**
Each file run for each mission uses ROS to transfer data from our differential GPS. It uses this GPS data to calculate heading.
Then, based on angle and radius thresholds for each waypoint, the mission files send commands to serial_server.py,
which sends serial messages to an Arduino with simple forwards/backwards on/off controls for the thrusters.
We settled on threshold angles of 8-10 degrees for Barco Polo. For Nav Channel and Speed Challenge,
minimum distances were .00003 degrees (~9.5 ft) for reaching a waypoint. For Docking, minimum distance was .000015 deg.
We were attempting .000012 degrees and .00001 degrees for Path, but had a hardware issue with one of the ESCs that prevented
us verifying whether that was the correct threshold.

**What we did not attempt**
- PID control for motion
- perception and computer vision
- mission planning for the boat to do several missions in one code


**We directly called files for each mission as follows:**
1. *Nav Channel*: gate_delay_thr_10.py
2. *Follow the Path*: gate_delay_thr_10.py (attempted but not successful; need to test with all motors intact)
3. *Docking*: dock_back_one_wp_amit.py (need to verify dock_back_two_wp_simple.py works as this is easier to integrate with other missions) *verify*
4. *Speed Challenge*: gate_delay_thr_10.py

**These files were also used across all missions:**
- serial_server.py (inside mission_planner --> enter_the_gates_roboboat)
- motor_mix.ino (inside mission_planner --> enter_the_gates_roboboat)
- Motor_mix_new(1).ino (a faster version of motor_mix.ino with higher PWM values; inside mission_planner --> enter_the_gates_roboboat)
- lat_lon_collection.py (for surveying)

**These files were also used for bench tests**
 - terminal_key_pub.py (for testing motor_mix.ino; found in mission_planner --> enter_the_gates_roboboat)
