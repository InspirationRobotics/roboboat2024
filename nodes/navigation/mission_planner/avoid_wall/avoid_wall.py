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
from floating_objects import Object_Colors, Object_Types, Floating_Object
from itertools import combinations
from mission_template import *

class avoid_wall(mission_template):
    def __init__(self, floating_objects):
        self.floating_objects = self.retrieve_color(floating_objects,Object_Colors.PURPLE)
        self.aPlanner = AStar(np.zeros((10,10)))
    
    def __str__(self):
        rep = "avoid the wall"
        return rep

    def ready_for_mission(self, floating_objects = None, envmap = None):
        if floating_objects is not None:
            #check for walls
            self.floating_objects = self.retrieve_color(floating_objects,Object_Colors.PURPLE)
        if envmap is not None:
            self.envmap = envmap
            self.aPlanner = AStar(envmap)
        if(len(self.floating_objects) == 2):
            return True
        return False
    
    def estimate_path(self, start_point):
        #line drawing algorithm
        x = bresenham2D(self.floating_objects[0].location[0], self.floating_objects[0].location[1], \
        self.floating_objects[1].location[0], self.floating_objects[1].location[1])

        for j in range(np.shape(x)[1]):
            self.envmap[int(x[0,j])][int(x[1,j])] = 1
        
        subspace = self.floating_objects[0].location-self.floating_objects[1].location
        vector_for_projection = start_point-self.floating_objects[1].location

        # finding norm of the vector v
        v_norm = np.sqrt(sum(subspace**2))    
        projection_vector = (np.dot(vector_for_projection, subspace)/(v_norm**2))*subspace
        orthogonal_vector = projection_vector-vector_for_projection
        targetpos = np.array(orthogonal_vector+orthogonal_vector/np.sqrt(sum(orthogonal_vector))+start_point).astype(int)
        
        self.aPlanner.updateMap(self.envmap)
        path = self.aPlanner.full_path(start_point, targetpos)

        return path

    def update_floating_objects(self, floating_objects):
        self.floating_objects = self.retrieve_color(floating_objects,Object_Colors.PURPLE)
    
    def update_map(self, envmap):
        self.envmap = envmap
    
    def retrieve_color(self, floating_objects, color):
        color_list = []
        for i in floating_objects:
            if i.color == color:
                color_list.append(i)
        return color_list

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