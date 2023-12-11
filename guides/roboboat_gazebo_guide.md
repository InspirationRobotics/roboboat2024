# Running Roboboat Simulation 2023 (for 2024)

> Tested on Ubuntu 22.04
> ROS Version: Noetic

Go to this [repo](https://gitlab.com/SimLE/SeaSentinel/sese-sim-docker)
Run the following

```bash
mkdir SeSe && cd SeSe
git clone https://github.com/PX4/PX4-Autopilot.git --recursive --shallow-submodules
git clone https://gitlab.com/SimLE/SeaSentinel/sese-sim-docker simulation --recursive
# if submodules changed, try updating them
git submodule update --init --recursive --force
```

You will not be able to access `sese_asv` and that is normal (that is that team's Roboboat build file.)

```bash
cd simulation
sudo make build
```

Enter bash shell in SITL (Software In the Loop) container

```bash
sudo make shell-sitl
# or if it is running
sudo docker compose exec sitl /entrypoint.sh bash
```

## Running

### Testing sese_asv

```bash
roslaunch asv_description px4.launch record:=true
# or 
roslaunch asv_description px4.launch world:=course_a our_vehicle:=sese_asv_vision
```

This is a repo we don't have. However, once we have the description file of our boat, we can likely change it to this

### Testing roboboat_gazebo
```bash
roslaunch roboboat_gazebo px4.launch vehicle:=uuv_bluerov2_heavy
# or
roslaunch roboboat_gazebo px4.launch world:=task2-gen vehicle:=boat
```

### Get available worlds

```bash
list-world
```

### Get ROS Topics

For more commands, see [the documentation](https://wiki.ros.org/rostopic)

```bash
rostopic list
```
