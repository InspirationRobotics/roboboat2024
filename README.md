# roboboat2024

## Notes for Migrating from ROS1 to ROS2 and Migrating from Robosub to Roboboat

- Sensors: click [here](./sensors.md) to see the sensors we need to keep and not keep

- Never do `ROS2` x `conda` : `ROS2` does not work with `conda` ([source 👀](https://docs.ros.org/en/rolling/How-To-Guides/Installation-Troubleshooting.html#anaconda-python-conflict)! run `conda deactivate` in your terminal before running anything. Make sure there's no `(base)` sign in your terminal

- Read the [Migration Guide from ROS2 Official Documentation](https://docs.ros.org/en/rolling/How-To-Guides/Migrating-from-ROS1/Migrating-Python-Packages.html)
    - There are things that will not be covered in this guide, e.g. what exceptions to throw for service (since ROS2 doesn't have the ones ROS1 uses), in these cases, consult the following sources (in this order)
        1. Official Documentation. e.g., see what exception type is used in its tutorial for service 
        2. GitHub Repo Issues Page for ROS packages, such as [`rclpy`](https://github.com/ros2/rclpy/issues)
        3. ConstuctSim (Reach out on Discord if you don't have access)
        4. StackOverflow (with a pinch of salt)
        5. ChatGPT (with a pinch of salt)

## Set up

This codebase is developed and tested on `python=3.8.10`.

- Clone this repository
- Download [`test_data/`](https://photos.app.goo.gl/y2SMzxv5S6S4NbCj6) and move it to `test_data/`


### Repo Structure

The following repo structure is from [robosub_2023](https://github.com/InspirationRobotics/robosub_2023).

`cv/`, `test_data`, `tests/` are currently implemented in this development branch. 

**Repo Structure is subject to change.**

```bash
roboboat2024
├── asv
│   ├── device
│   │   ├── # everything related to the sensors
│   │   ├── # each device should have its own file/folder
│   ├── localization 
│   │   ├── # TODO
│   ├── mission 
│   │   ├── # Mission classes
│   │   ├── # see asv/mission/template_mission.py for an example
│   ├── motion
│   │   ├── # Actuators code
│   │   ├── # each actuator should have its own file/folder
│   ├── cv
│   │   ├── # All CV classes and functions
│   │   ├── # see asv/cv/template_cv.py for an example
│   ├── utils
│   │   ├── # utility functions
├── scripts
│   ├── # bash scripts
├── mission
│   ├── # Mission files (calling mission classes)
├── tests
│   ├── # Unit tests (pytest)
├── config.json # where all the config values used in mission files are stored
├── setup.py # setup file for pip install
├── .gitignore
├── README.md
```

### Running

#### Tests

This will run all the tests in the tests folder using `pytest`.
Any file that has the name `test_*.py` will be run.

```bash
pytest
```

#### CV

The idea behind the CV classes is that they are run in a separate thread and they publish their results to a ROS topic.
You can run individually CV classes for debugging purpose (if they have a `if __name__ == "__main__"` block) by running:

```bash
python3 -m asv.cv.<cv_name>
```

## Contributing

### Unit Tests

We use pytest for unit tests. Please write unit tests for your code and make sure that they pass before pushing your code.
This is to make sure that we don't break anything when we add new features.
Tests are mainly there to make sure that there is no syntax error and that the code runs without crashing, not necessarily to make sure that the code is doing what it is supposed to do (although it is a plus).

### Code Style

It is always pleasant to read code that is well formatted and well commented.
Ideally we would want to format our code using black, so try to run regularly on your code:

```bash
black .
```

If you have trouble running this command, you can use the following command instead:

```bash
python3 -m black .
```


## Roboboat 2024 Result

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


**We used files for each mission as follows:**
1. *Nav Channel*: gate_delay_thr_10.py
2. *Follow the Path*: gate_delay_thr_10.py (attempted but not successful; need to test with all motors intact)
3. *Docking*: 
4. *Speed Challenge*: gate_delay_thr_10.py

**These files were also used across all missions:**
- serial_server.py (inside mission_planner --> enter_the_gates_roboboat)
- motor_mix.ino (inside mission_planner --> enter_the_gates_roboboat)
- Motor_mix_new(1).ino (a faster version of motor_mix.ino with higher PWM values; inside mission_planner --> enter_the_gates_roboboat)
- lat_lon_collection.py (for surveying)

**These files were also used for bench tests**
 - terminal_key_pub.py (for testing motor_mix.ino; found in mission_planner --> enter_the_gates_roboboat)
