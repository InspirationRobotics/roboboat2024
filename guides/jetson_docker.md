# Roboboat Jetson Xavier NX Docker Guide
### Running the docker

```bash
sudo docker run --runtime nvidia -it --rm --network=host roboboat_humble:l4t-r35.4.1
```

View installed packages:

```bash
# need to be inside the docker
apt list
```


Source `ros2` everytime before you're using it.

```bash
source /opt/ros/humble/install/setup.bash
```


### Using the Arduino Control Code (for now for development)

On the first terminal

```bash
docker run --runtime nvidia -it --rm --privileged --network=host roboboat_humble:arduino_control
cd ~
git clone git@github.com:chenyenru/ros2_serial_interface.git
cd ros2_serial_interface
colcon build
. install/setup.bash 
ros2 run ros2_serial_interface serial_server
```

On the second terminal
```bash
docker container ls # to see the running cros2 run ros2_serial_interface serial_serverontainers.
# find the ID of container you just ran
docker exec -it CONTAINERID /bin/bash
cd /
bash ros_entrypoint.sh
cd ~/ros2_serial_interface
. install/setup.bash
ros2 run ros2_serial_interface terminal_key_pub
# then, press "w", "a", or "d" to change the servo direction
```

On the Arduino Mega, make sure you have [this file](https://github.com/chenyenru/ros2_serial_interface/blob/main/ArduinoSketches/sketch_ATMega2560/sketch_MEGA_servo.ino) uploaded

**In the Arduino file:** 

Change the setup to add more servos:

```C
void setup() {
  ...
  // Add more Servo objects if you need more servos   
  Servo servo1; // Define a servo object  
  ...
  // Attach the servo to the specified pin
  servo1.attach(9);
}
```

Customize the following section to specify servos' behaviors:

``` C
void runCommand(char command) {
  if (command == move_straight) {
    Serial.println("Move Straight");
    // Adjust the servo position to move straight (center position)
    servo1.write(90);
  } else if (command == turn_right) {
    Serial.println("Turn Right");
    // Adjust the servo position to turn right
    servo1.write(135);
  } else if (command == turn_left) {
    Serial.println("Turn Left");
    // Adjust the servo position to turn left
    servo1.write(45);
  }
}
```
