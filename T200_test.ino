#include <Servo.h>

byte servoPin = 9;
Servo servo; // Define a servo object

const char move_forward = 'w';
const char move_backward = 'x';
const char stop_ = 's';

void setup() {
  // Initialize Serial Communication
  Serial.begin(9600);

  // Attach the servo to the specified pin
  servo.attach(servoPin);
  servo.writeMicroseconds(1500);
  delay(7000);

}

void runCommand(char command) {
  if (command == move_forward) {
    Serial.println("Move Forward");
    // Adjust the servo position to move straight (center position)
    int signal = 1520;
    servo.write(signal);
  } else if (command == move_backward) {
    Serial.println("Move Backward");
    // Adjust the servo position to turn right
    int signal = 1470;
    servo.write(signal);
  } else if (command == stop_) {
    Serial.println("Stop");
    // Adjust the servo position to stop
    int signal = 1500;
    servo.write(signal);
  }
}

void loop() {
  // Check for serial commands and execute corresponding actions
  if (Serial.available()) {
    char command = Serial.read();
    runCommand(command);
  }
}
