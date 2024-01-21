"""
Perception
1. have a camera ID buoys
2. have it keep track of size of said buoys
3. have it move s.t. the buoys grow in pixel size and go out until invisible
4. repeat

GPS (simpler)
1. ID starting point
2. go 100 ft due north
   - make sure you are facing North
   - set error threshold
"""
#author: Lindsay Wright
import sys
sys.path.append('../')
import numpy as np
import math
import time
from serial_server import * #adding control functions
#from randomAStar import randomAStar
from pqdict import pqdict
#from starAlgorithm.Astar import *
#from Dstarworks import *
#from starAlgorithm.starUtils import *
#from prequalification.connect_buoys import *
### not using A* or traveling salesman algorithms
#from floating_objects import Object_Colors, Object_Types, Floating_Object
### not using color perception
from itertools import combinations
from mission_template import *
import time


class enter_the_gates_blind(mission_template):
    def __init__(self, floating_objects):
        pass
        #self.get_buoys(floating_objects)
    """
    from serial_server.py:

    		super().__init__('serial_server')
		#Default Value declarations of ros2 params:
		self.declare_parameters(
		namespace='',
		parameters=[
			('device', '/dev/ttyACM0'), #device we are transmitting to & receiving messages from
		    ('servo_keyboard_input', 'servo_keyboard_input'),
		    ('move_forward_cmd', 'w'),
		    ('turn_backward_cmd', 'x'),
		    ('stop_cmd', 's')		
			]
		)
		self.servo_topic_name = self.get_param_str('servo_keyboard_input')
		self.device_name = self.get_param_str('device')
		self.move_forward_cmd = self.get_param_str('move_forward_cmd')
		self.move_backward_cmd = self.get_param_str('move_backward_cmd')
		self.stop_cmd = self.get_param_str('stop_cmd')
		self.ser = serial.Serial(self.device_name,
                           9600, #Note: Baud Rate must be the same in the arduino program, otherwise signal is not received!
                           timeout=.1)
                           """
    def __str__():
        rep = "avoid the wall"
        return rep    

    def ready_for_mission(self, floating_objects = None, envmap = None):
        if envmap is not None:
            self.envmap = envmap

        if floating_objects is not None and len(floating_objects) > 0:
            return True
        

        return False
               
    
    def estimate_path(self, start_point):
        desired_heading=0; #due North
        if current_heading-desired_heading>5 & current_heading-desired_heading<180: #degrees
            self.turn_left
        elif current_heading-desired_heading<355 & current_heading-desired_heading>180:
            

        desired_long=; #need to write code to get this from the gps
        if current_long-desired_long>

