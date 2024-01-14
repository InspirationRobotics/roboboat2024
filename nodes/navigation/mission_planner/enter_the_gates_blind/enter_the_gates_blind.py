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



class enter_the_gates_blind(mission_template):
    def __init__(self, floating_objects):
        pass
        #self.get_buoys(floating_objects)
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

        if floating_objects is not None and len(floating_objects) > 0:
            return True
        

        return False
               
    
    def estimate_path(self, start_point):
        self.aPlanner = AStar(self.envmap)
        all_buoys, area = self.extract_from_envmap(self.envmap)
        all_buoys = np.flip(all_buoys,1)
        to_keep = []
        for i in range(np.shape(area)[0]):
            if(area[i]>4 and area[i]< 100):
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

        black_buoy = self.guess_black_buoy(start_point, closest, second_closest, all_buoys)
        to_enter_gate = self.aPlanner.full_path(start_point, start_qualification)
        to_surround_buoy = self.surround_buoy(to_enter_gate[-1], black_buoy)
        to_exit_gate = self.aPlanner.full_path(to_surround_buoy[-1], start_qualification)
        self.aPlanner.__del__()
        return np.concatenate((to_enter_gate, to_surround_buoy, to_exit_gate), axis = 0)


    def surround_buoy(self, start_point, black_buoy):
        vector = np.array(black_buoy-start_point)
        unit_vector = vector/np.sqrt(sum(vector**2))
        min_distane = 5
        min_vector = unit_vector*min_distane

        target_array = []
        rotation = self.rotation_matrix(-np.pi/2)
        min_vector = np.matmul(rotation,min_vector)
        target_array.append(np.array(-min_vector+black_buoy).astype(int))
        min_vector = np.matmul(rotation,min_vector)
        target_array.append(np.array(-min_vector+black_buoy).astype(int))
        min_vector = np.matmul(rotation,min_vector)
        target_array.append(np.array(-min_vector+black_buoy).astype(int))
        rotate_path = np.array([start_point])
        for i in target_array:
            rotate_path = np.concatenate((rotate_path , self.aPlanner.full_path(start_point, i)), axis = 0)
            start_point = i

        return rotate_path

    def guess_black_buoy(self, start_point, buoy_one, buoy_two, all_buoys):
        buoys_in_correct_side = self.filter_correct_side(start_point, buoy_one, buoy_two, all_buoys)
        closest_buoy = buoys_in_correct_side[0]
        closest_distance = np.linalg.norm(start_point-closest_buoy)
        for i in buoys_in_correct_side:
            tempDistance = np.linalg.norm(start_point-i)
            if closest_distance > tempDistance:
                closest_distance = tempDistance
                closest_buoy = i
        return i



    def filter_correct_side(self, start_point, buoy_one, buoy_two, all_buoys):
        gate_vector = self.unit_vector(buoy_one-buoy_two)
        start_to_orth = start_point-self.orthogonal_projection(gate_vector, start_point-buoy_two)
        not_near_line = []
        for i in all_buoys:
            tempVect = i-buoy_two
            tempProjection = tempVect-self.orthogonal_projection(gate_vector, tempVect)
            if np.linalg.norm(tempProjection) > 6 and \
            self.angle_between(tempProjection, start_to_orth) > np.pi/2:
                not_near_line.append(i)
        
        return not_near_line
    
    def objects_in_line(self, buoy_one, buoy_two, all_buoys):
        gate_vector = self.unit_vector(buoy_one-buoy_two)
        near_line = []
        for i in all_buoys:
            if np.linalg.norm(i-self.orthogonal_projection(gate_vector, i)) <= 6:
                near_line.append(i)
        
        return near_line
        
    def orthogonal_projection(self, subspace, vector):
        normed = subspace/(np.linalg.norm(subspace)**2)
        return np.dot(vector, normed)*subspace

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
    
    def rotation_matrix(self, theta):
        R = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])
        return R