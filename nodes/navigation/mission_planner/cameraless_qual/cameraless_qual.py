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



class cameraless_qual(mission_template):
    def __init__(self, floating_objects):
        self.get_buoys(floating_objects)
        
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
        if envmap is not None:
            self.envmap = envmap

        if floating_objects is not None:
            return True
        

        return False
               
    
    def estimate_path(self, start_point):
        self.aPlanner = AStar(self.envmap)
        all_buoys, area = self.extract_from_envmap(self.envmap)
        all_buoys = np.flip(all_buoys,1)
        to_keep = []
        for i in range(np.shape(area)[0]):
            if(area[i]>5 and area[i]< 50):
                to_keep.append(i)
        all_buoys = all_buoys[to_keep,:]
        closest = all_buoys[0]
        second_closest = all_buoys[1]
        closest_distance = np.linalg.norm(closest-second_closest) 

        for i in all_buoys:
            curr_dist = np.linalg.norm(start_point-i)
            if(curr_dist <= closest_distance):
                second_closest = closest
                closest = i
                closest_distance = curr_dist
        #print(start_point, closest, second_closest)

        second_closest_distance = np.linalg.norm(start_point-second_closest)
        for i in all_buoys:
            curr_dist = np.linalg.norm(start_point-i)
            if(curr_dist < second_closest_distance and not np.array_equal(i,closest)):
                second_closest = i
                second_closest_distance = curr_dist

        gate_vector = self.unit_vector(second_closest-closest)
        start_point_vector = start_point-closest
        start_qualification = second_closest-self.unit_vector(second_closest-closest)*np.linalg.norm(second_closest-closest)/2
        # print(all_buoys)
        # print(closest, second_closest)
        # print(start_qualification)

        subspace = gate_vector
        vector_for_projection = start_point_vector

        # finding norm of the vector v
        v_norm = np.sqrt(sum(subspace**2))    
        projection_vector = (np.dot(vector_for_projection, subspace)/(v_norm**2))*subspace
        orthogonal_vector = projection_vector-vector_for_projection
        targetpos = np.array(30*orthogonal_vector/np.linalg.norm(orthogonal_vector)+start_qualification).astype(int)

        path = self.aPlanner.full_path(start_point, np.array(start_qualification).astype(int))
        path = np.concatenate((path, self.aPlanner.full_path(path[-1], targetpos)), axis = 0)
        self.aPlanner.__del__()
        return np.array(path).astype(int)

        

    def extract_from_envmap(self, envmap):
        kernel = np.ones((3, 3), np.uint8)
        newmap = np.copy(envmap)
        
        # extract connected components
        connectivity = 4
        outputs = cv2.connectedComponentsWithStats(newmap, connectivity, cv2.CV_32S)
        area = outputs[2][:,4]
        centroids = np.array(outputs[3]).astype(int)
        
        return centroids, area
    
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