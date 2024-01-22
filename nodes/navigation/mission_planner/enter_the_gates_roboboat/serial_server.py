# Serial server node
import rclpy
from rclpy.node import Node
import serial

# Handle Twist messages, linear and angular velocity
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class NavigationServer(Node):
	def __init__(self):
		super().__init__('navigation_server')
		#Default Value declarations of ros2 params:
		self.declare_parameters(
		namespace='',
		parameters=[
			('device', '/dev/ttyACM0'), #device we are transmitting to & receiving messages from
		    	('navigation_input', 'navigation_input'),
		    	('move_forward_cmd', 'w'),
		    	('move_backward_cmd', 'x'),
			('turn_left_cmd', 'a'),
            		('turn_right_cmd', 'd'),
		    	('stop_cmd', 's')		
			]
		)
		self.servo_topic_name = self.get_param_str('navigation_input')
		self.device_name = self.get_param_str('device')
		self.move_forward_cmd = self.get_param_str('move_forward_cmd')
		self.move_backward_cmd = self.get_param_str('move_backward_cmd')
		self.stop_cmd = self.get_param_str('stop_cmd')
        	self.turn_left_cmd = self.get_param_str('turn_left_cmd')
        	self.turn_right_cmd = self.get_param_str('turn_right_cmd')
		self.ser = serial.Serial(self.device_name,
                           9600, #Note: Baud Rate must be the same in the arduino program, otherwise signal is not received!
                           timeout=.1)

		self.subscriber = self.create_subscription(String, 
                                              self.servo_topic_name, 
                                              self.serial_listener_callback, 
                                              10)
		self.subscriber # prevent unused variable warning
		self.ser.reset_input_buffer()
	def get_param_float(self, name):
		try:
			return float(self.get_parameter(name).get_parameter_value().double_value)
		except:
			pass
	def get_param_str(self, name):
		try:
			return self.get_parameter(name).get_parameter_value().string_value
		except:
			pass
	def send_cmd(self, cmd):
		print("Sending: " + cmd)
		self.ser.write(bytes(cmd,'utf-8'))
	def receive_cmd(self):
		try:
			line = self.ser.readline().decode('utf-8').rstrip()
			print("Received: " + line)
			return line
		except Exception as e:
			print(f"Error receiving command: {e}")
			return None

    	def serial_listener_callback(self, msg):
		#
		# For some reason, arduino sends back null byte (0b'' or Oxff) back after the first call to ser.write
		# If the statement in "try" executes when this happens, it causes this error which crashes the program:
		# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
		# To prevent this, I added the try-except blocks to prevent the program from crashing
		# If a null byte is sent, "except" is called which prevents the program from crashing
		"""Move Forward"""
		if msg.data == self.move_forward_cmd:
			self.send_cmd(self.move_forward_cmd)
			self.receive_cmd()
		"""Move Backward"""
		elif msg.data == self.move_backward_cmd:
			self.send_cmd(self.move_backward_cmd)
			self.receive_cmd()
		"""Stop"""
		elif msg.data == self.stop_cmd:
			self.send_cmd(self.stop_cmd)
			self.receive_cmd()
        	"""Turn Left"""
        	elif msg.data == self.stop_cmd:
			self.send_cmd(self.turn_left_cmd)
			self.receive_cmd()
        	"""Turn Right"""
        	elif msg.data == self.stop_cmd:
			self.send_cmd(self.turn_right_cmd)
			self.receive_cmd()



def main(args=None):
	rclpy.init(args=args)
	navigation_server = NavigationServer()
	rclpy.spin(navigation_server)

if __name__ == '__main__':
	main()
