#include <Servo.h>

byte servoPin_1 = 9;
byte servoPin_2 = 10;
byte servoPin_3 = 11;
byte servoPin_4 = 12;

Servo servo1; // Define a servo object
Servo servo2;
Servo servo3;
Servo servo4;

int motor_forward = 1530;
int motor_backward = 1470;
int motor_stop = 1500;


const char move_forward = 'w';
const char move_backward = 'x';
const char stop_ = 's';
const char turn_left = 'a';
const char turn_right = 'd';

void setup() {
  // Initialize Serial Communication
  Serial.begin(9600);

  // Attach the servo to the specified pin
  servo1.attach(servoPin_1);
  servo2.attach(servoPin_2);
  servo3.attach(servoPin_3);
  servo4.attach(servoPin_4);
  servo1.writeMicroseconds(1500);
  servo2.writeMicroseconds(1500);
  servo3.writeMicroseconds(1500);
  servo4.writeMicroseconds(1500);
  delay(7000);

}

void runCommand(char command) {
  if (command == move_forward) {
    Serial.println("Move Forward");
    // Adjust the servo position to move straight (center position)
    // int signal = 1520;
    servo1.write(motor_forward);
    servo2.write(motor_forward);
    servo3.write(motor_backward);
    servo4.write(motor_backward);
    
  } else if (command == move_backward) {
    Serial.println("Move Backward");
    // Adjust the servo position to move back
    servo1.write(motor_backward);
    servo2.write(motor_backward);
    servo3.write(motor_forward);
    servo4.write(motor_forward);

  } else if (command == turn_left) {
    Serial.println("Turn Left");
    // Adjust the servo position to turn left
    servo1.write(motor_forward);
    servo2.write(motor_forward);
    servo3.write(motor_backward);
    servo4.write(motor_forward);

  } else if (command == turn_right) {
    Serial.println("Turn Left");
    // Adjust the servo position to turn right
    servo1.write(motor_backward);
    servo2.write(motor_backward);
    servo3.write(motor_forward);
    servo4.write(motor_backward);
    
  } else {
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
