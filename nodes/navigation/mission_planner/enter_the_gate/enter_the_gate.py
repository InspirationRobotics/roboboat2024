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

class enter_the_gate(mission_template):
    def __init__(self, floating_objects):
        self.floating_green = self.retrieve_color(floating_objects,Object_Colors.GREEN)
        self.floating_red = self.retrieve_color(floating_objects,Object_Colors.RED)
        self.floating_white = self.retrieve_color(floating_objects,Object_Colors.WHITE)
    
    def __str__(self):
        rep = "avoid the wall"
        return rep

    def ready_for_mission(self, floating_objects = None, envmap = None):
        found_line = False
        if floating_objects is not None:
            self.floating_black = None
            self.beacon_for_gate = None
            self.floating_white = self.retrieve_color(floating_objects,Object_Colors.WHITE)
            self.floating_green = self.retrieve_color(floating_objects,Object_Colors.GREEN)
            self.floating_red = self.retrieve_color(floating_objects,Object_Colors.RED)
            for i in floating_objects:
                if(i.color == Object_Colors.BLACK):
                    self.floating_black = i
                if(i.type == Object_Types.BEACON):
                    self.beacon_for_gate = i
            if(self.floating_black is not None and self.beacon_for_gate is not None):
                found_line = self.find_line()

            
        if envmap is not None:
            self.envmap = envmap
        if(found_line):
            return True
        return False

    def estimate_path(self, start_point):
        self.aPlanner = AStar(self.envmap)
        print("entering the map")
        to_right_side = self.avoid_wall(start_point)
        
        try:
            if(np.size(to_right_side) == 2):
                second_start = to_right_side
            else:
                second_start = to_right_side[-1]
        except:
            second_start = to_right_side[-1]
        to_cross_the_gates = self.cross_the_gates(second_start)
        finished_rotation = self.go_around(to_cross_the_gates[-1])
        back_to_gates = self.back_in_gates(finished_rotation[-1])

        try:
            full_path = np.concatenate((to_right_side,to_cross_the_gates,finished_rotation,back_to_gates), axis = 0)
        except:
            full_path = np.concatenate((to_cross_the_gates,finished_rotation,back_to_gates), axis = 0)
        self.aPlanner.__del__()
        return full_path

    def back_in_gates(self, start_point):
        return self.aPlanner.full_path(start_point, self.beacon_for_gate.location)

    def go_around(self, start_point):
        vector = np.array(self.floating_black.location-start_point)
        unit_vector = vector/np.sqrt(sum(vector**2))
        min_distane = 5
        min_vector = unit_vector*min_distane

        target_array = []
        rotation = self.rotation_matrix(-np.pi/2)
        min_vector = np.matmul(rotation,min_vector)
        target_array.append(np.array(-min_vector+self.floating_black.location).astype(int))
        min_vector = np.matmul(rotation,min_vector)
        target_array.append(np.array(-min_vector+self.floating_black.location).astype(int))
        min_vector = np.matmul(rotation,min_vector)
        target_array.append(np.array(-min_vector+self.floating_black.location).astype(int))
        rotate_path = np.array([start_point])
        for i in target_array:
            rotate_path = np.concatenate((rotate_path , self.aPlanner.full_path(start_point, i)), axis = 0)
            start_point = i

        return rotate_path

    def avoid_wall(self, start_point):

        # check if we are in the correct side of the gates
        subspace = self.floating_green.location-self.floating_red.location
        vector_for_projection_black = self.floating_black.location-self.floating_red.location

        v_norm = np.sqrt(sum(subspace**2))    
        projection_vector = (np.dot(vector_for_projection_black, subspace)/(v_norm**2))*subspace
        orthogonal_vector_black = projection_vector-vector_for_projection_black

        vector_for_projection_white = start_point-self.floating_red.location
        projection_vector = (np.dot(vector_for_projection_white, subspace)/(v_norm**2))*subspace
        orthogonal_vector_white = projection_vector-vector_for_projection_white

        angle_diff = self.angle_between(orthogonal_vector_white, orthogonal_vector_black)

        if(angle_diff == np.pi):
            return start_point

        # if we are not in the correct side of the gates go to the other side before traveling throught the gates
        og_map = np.array(self.envmap)
        x = bresenham2D(self.floating_green.location[0], self.floating_green.location[1], \
        self.floating_red.location[0], self.floating_red.location[1])

        for j in range(np.shape(x)[1]):
            self.envmap[int(x[0,j])][int(x[1,j])] = 1
        
        subspace = self.floating_green.location-self.floating_red.location
        vector_for_projection = self.floating_black.location-self.floating_red.location

        # finding norm of the vector v
        v_norm = np.sqrt(sum(subspace**2))    
        projection_vector = (np.dot(vector_for_projection, subspace)/(v_norm**2))*subspace
        orthogonal_vector = projection_vector-vector_for_projection
        targetpos = np.array(orthogonal_vector+orthogonal_vector/np.sqrt(sum(orthogonal_vector))+self.floating_black.location).astype(int)

        self.aPlanner.updateMap(self.envmap)
        path = self.aPlanner.full_path(start_point, targetpos)
        self.aPlanner.updateMap(og_map)
        self.envmap = og_map

        return path

    def cross_the_gates(self, start_point):
        
        all_buoys = [self.floating_white[0], self.floating_white[1], self.floating_green, self.floating_red]

        closest = all_buoys[0]
        second_closest = all_buoys[1]
        closest_distance = np.linalg.norm(self.beacon_for_gate.location-closest.location) 

        for i in all_buoys:
            curr_dist = np.linalg.norm(self.beacon_for_gate.location-i.location)
            if(curr_dist <= closest_distance):
                second_closest = closest
                closest = i
                closest_distance = curr_dist

        second_closest_distance = np.linalg.norm(self.beacon_for_gate.location-second_closest.location)
        for i in all_buoys:
            curr_dist = np.linalg.norm(self.beacon_for_gate.location-i.location)
            if(curr_dist < second_closest_distance and i is not closest):
                second_closest = i
                second_closest_distance = curr_dist

        closest_buoys = [closest, second_closest]
        closest_vectors = np.array([second_closest.location - closest.location, closest.location - second_closest.location])
        closest_vectors = closest_vectors * 20

        x = bresenham2D(closest_buoys[0].location[0], closest_buoys[0].location[1], \
        closest_buoys[0].location[0]-closest_vectors[0][0], closest_buoys[0].location[0]-closest_vectors[0][1])
        sizes = np.shape(self.envmap)
        for j in range(np.shape(x)[1]):
            if(x[0,j]>0 and x[1,j]>0 and x[0,j]<sizes[0] and x[1,j]<sizes[1]):
                self.envmap[int(x[0,j])][int(x[1,j])] = 1        
        

        x = bresenham2D(closest_buoys[1].location[0], closest_buoys[1].location[1], \
        closest_buoys[1].location[0]-closest_vectors[1][0], closest_buoys[1].location[0]-closest_vectors[1][1])
        sizes = np.shape(self.envmap)

        for j in range(np.shape(x)[1]):
            if(x[0,j]>0 and x[1,j]>0 and x[0,j]<sizes[0] and x[1,j]<sizes[1]):
                self.envmap[int(x[0,j])][int(x[1,j])] = 1  
        
        self.aPlanner.updateMap(self.envmap)
        # add extra space for crossing the buoys

        targetpos = np.array(closest_buoys[0].location - (closest_buoys[0].location-closest_buoys[1].location)/2).astype(int)
        path = self.aPlanner.full_path(start_point, targetpos)

        return path
    
    def find_line(self):
        # go thoruhg thw white buoys untill we find a good one or we don't
        while(len(self.floating_white)>1):
            #find the closest white buoy
            minimum_white = self.floating_white[1]
            min_dist = np.linalg.norm(self.floating_white[1].location-self.floating_white[0].location)
            for j in range(1,len(self.floating_white)):
                loc_min = np.linalg.norm(self.floating_white[j].location-self.floating_white[0].location)
                if loc_min < min_dist:
                    min_dist = loc_min
                    minimum_white = self.floating_white[j]

            #find the closest red_buoy
            minimum_red = self.floating_red[0]
            min_dist_r = np.linalg.norm(self.floating_red[0].location-self.floating_white[0].location)
            for j in range(1,len(self.floating_red)):
                loc_min = np.linalg.norm(self.floating_red[j].location-self.floating_white[0].location)
                if loc_min < min_dist_r:
                    min_dist_r = loc_min
                    minimum_red = self.floating_red[j]

            #find the closest green_buoy
            minimum_green = self.floating_green[0]
            min_dist_g = np.linalg.norm(self.floating_green[0].location-self.floating_white[0].location)
            for j in range(1,len(self.floating_green)):
                loc_min = np.linalg.norm(self.floating_green[j].location-self.floating_white[0].location)
                if loc_min < min_dist_g:
                    min_dist_g = loc_min
                    minimum_green = self.floating_green[j]
            
            #deside if the red or the green buoy are the closest
            if(min_dist_g < min_dist_r):
                closest_colored_buoy = minimum_green
                closest_color = "green"
            else:
                closest_colored_buoy = minimum_red
                closest_color = "red"
            
            color_angle = self.angle_between(closest_colored_buoy.location-self.floating_white[0].location, minimum_white.location-self.floating_white[0].location)
            succesfull = False
            if(abs(color_angle-np.pi) < .1):
                succesfull = True

            if(closest_color == "red"):
                other_color = self.floating_green
            else:
                other_color = self.floating_red

            #get the other closest color
            other_closest = other_color[0]
            min_dist_other = np.linalg.norm(other_color[0].location-minimum_white.location)
            for i in range(1,len(other_color)):
                loc_min = np.linalg.norm(other_color[j].location-minimum_white.location)
                if loc_min < min_dist_other:
                    min_dist_other = loc_min
                    other_closest = other_color[j]

            if(succesfull):
                color_angle = self.angle_between(other_closest.location-self.floating_white[0].location, minimum_white.location-self.floating_white[0].location)
                if(color_angle > .1):
                    succesfull = False

            if(succesfull):
                self.floating_white = [self.floating_white[0], minimum_white]
                if(closest_colored_buoy.color == Object_Colors.RED):
                    self.floating_red = closest_colored_buoy
                    self.floating_green = other_closest
                else:
                    self.floating_red = other_closest
                    self.floating_green = closest_colored_buoy
                return True 
            else:
                #remove if whe are not in a good angle
                self.floating_white.remove(self.floating_white[0])
                
                #guarantee that we are not removing a byoy for a far away angle         
                for i in range(len(self.floating_white)):
                    if(self.floating_white[i] == minimum_white and min_dist < 15):
                        self.floating_white.remove(self.floating_white[i])
                        break

        return False
        
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
    
    def rotation_matrix(self, theta):
        R = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])
        return R