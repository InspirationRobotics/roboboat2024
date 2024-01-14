import sys
sys.path.append('../')
import numpy as np
import math
import time
#from randomAStar import randomAStar
from pqdict import pqdict
from starAlgorithm.Astar import *
#from Dstarworks import *
from starAlgorithm.starUtils import *
from prequalification.connect_buoys import *
from floating_objects import Object_Colors, Object_Types, Floating_Object
from itertools import combinations
from mission_template import *
import time



class prequalification(mission_template):
    def __init__(self, floating_objects):
        self.get_buoys(floating_objects)
        self.aPlanner = AStar(np.zeros((10,10)))
        
    def __str__():
        rep = "avoid the wall"
        return rep    
    def get_buoys(self, floating_objects):
        # separate red floating objects
        floating_red = self.retrieve_color(floating_objects, Object_Colors.RED)
        self.floating_red = floating_red

        #separate green floating objects
        floating_green = self.retrieve_color(floating_objects, Object_Colors.GREEN)
        self.floating_green = floating_green

    def ready_for_mission(self, floating_objects = None, envmap = None):
        if floating_objects is not None:
            self.get_buoys(floating_objects)
        if envmap is not None:
            self.envmap = envmap
            self.aPlanner = AStar(envmap) 
        # think about a way to filter out entrance and exit gates
        # maybe using other angles

        # given a certain number of buoys determine whether we are ready to take on the challenge
        if(len(self.floating_green) == 2 and len(self.floating_red) == 2):
            return True
        
        return False
               
    
    def estimate_path(self, start_point):
        envmap = connect_the_buoys(self.envmap, self.floating_red)
        envmap = connect_the_buoys(self.envmap, self.floating_green)

        self.aPlanner = AStar(self.envmap)

        total_path = []

        first = np.argmin([np.linalg.norm(start_point-self.floating_green[0].location), np.linalg.norm(start_point-self.floating_green[-1].location)])
        first = first *-1

        entering_grid = self.enter_the_grid( start_point, first)
        get_out = self.get_out( entering_grid[-1], first)

        full_path = np.concatenate((entering_grid,get_out),axis=0)
        return full_path
    
    def enter_the_grid(self, start_point, first):
        if(first == 0):
            arr_val = 0
        else:
            arr_val = -1
        midpoint = np.array((self.floating_green[arr_val].location-self.floating_red[arr_val].location)/2).astype(int)
        midpoint = self.floating_green[arr_val].location-midpoint
        return self.aPlanner.full_path(start_point,midpoint)

    def get_out(self, start_point, first):
        if(first == 0):
            arr_val = -1
        else:
            arr_val = 0
        midpoint = np.array((self.floating_green[arr_val].location-self.floating_red[arr_val].location)/2).astype(int)
        direction = np.array(self.floating_green[arr_val*3+1].location-self.floating_green[arr_val].location).astype(int)
        direction = np.array(direction/np.linalg.norm(direction)).astype(int)
        endpoint = self.floating_green[arr_val].location-midpoint-direction

        return self.aPlanner.full_path(start_point,endpoint)
                      

    #geek for geeks code
    def unit_vector(self,vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    def angle_between(self,v1, v2):
        """ Returns the angle in radians between vectors 'v1' and 'v2'::

                >>> angle_between((1, 0, 0), (0, 1, 0))
                1.5707963267948966
                >>> angle_between((1, 0, 0), (1, 0, 0))
                0.0
                >>> angle_between((1, 0, 0), (-1, 0, 0))
                3.141592653589793
        """
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def robotplanner(self, robotpos, targetpos):
        #is there a way to precalculate the possible path locations?
        theOptimal = self.aPlanner.robotplanner(np.array(robotpos), np.array(targetpos))
        return np.array(theOptimal)

    def update_floating_objects(self, floating_objects):
        floating_red = self.retrieve_color(floating_objects, Object_Colors.RED)
        self.aPlanner.envmap = connect_the_buoys(self.unedited_map, floating_red)
        self.floating_red = floating_red

        #separate green floating objects
        floating_green = self.retrieve_color(floating_objects, Object_Colors.GREEN)
        self.aPlanner.envmap = connect_the_buoys(self.aPlanner.envmap, floating_green)
        self.floating_green = floating_green

        self.aPlanner.updateMap()
        return self
    
    def update_map(self, envmap):
        self.aPlanner.envmap = connect_the_buoys(envmap, self.floating_red)
        self.aPlanner.envmap = connect_the_buoys(self.aPlanner.envmap, self.floating_green)

        self.aPlanner.updateMap()
        return self      

    def retrieve_color(self,floating_objects, color):
        color_list = []
        for i in floating_objects:
            if i.color == color:
                color_list.append(i)
        return color_list