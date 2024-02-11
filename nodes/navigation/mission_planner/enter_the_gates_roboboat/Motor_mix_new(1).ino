#include <Servo.h>

byte servoPin_1 = 3;
byte servoPin_2 = 5;
byte servoPin_3 = 6;
byte servoPin_4 = 9;

Servo servo1; // Define a servo object
Servo servo2;
Servo servo3;
Servo servo4;

int motor_forward = 1550;
int motor_backward = 1450;
int motor_stop = 1500;


const char move_forward = 'w';
const char move_backward = 'x';
const char stop_ = 's';
const char turn_left = 'a';
const char turn_right = 'd';

void setup() {
  // Initialize Serial Communication
  Serial.begin(115200);

  // Attach the servo to the specified pin
  servo1.attach(servoPin_1);
  servo2.attach(servoPin_2);
  servo3.attach(servoPin_3);
  servo4.attach(servoPin_4);
  servo1.writeMicroseconds(1500);
  servo2.writeMicroseconds(1500);
  servo3.writeMicroseconds(1500);
  servo4.writeMicroseconds(1500);
  delay(1000);

}

void runCommand(char command) {
  if (command == turn_left) {
    //Serial.println("Move Forward");
    // Adjust the servo position to move straight (center position)
    servo1.write(motor_forward);
    servo2.write(motor_forward);
    servo3.write(motor_forward);
    servo4.write(motor_backward);
    
  } else if (command == turn_right) {
    //Serial.println("Move Backward");
    // Adjust the servo position to move back
    servo1.write(motor_backward);
    servo2.write(motor_backward);
    servo3.write(motor_backward);
    servo4.write(motor_forward);

  } else if (command == move_forward) {
    //Serial.println("Turn Right");
    // Adjust the servo position to turn left
    servo1.write(1600);
    servo2.write(1600);
    servo3.write(1400);
    servo4.write(1600);

  } else if (command == move_backward) {
    //Serial.println("Turn Left");
    // Adjust the servo position to turn right
    servo1.write(1400);
    servo2.write(1400);
    servo3.write(1600);
    servo4.write(1400);
    
  } else if (command == stop_){
    Serial.println("Stop");
    // Adjust the servo position to stop
    servo1.write(motor_stop);
    servo2.write(motor_stop);
    servo3.write(motor_stop);
    servo4.write(motor_stop);
  }
}

void loop() {
  // Check for serial commands and execute corresponding actions
  if (Serial.available()) {
    char command = Serial.read();
    runCommand(command);
  }
}
