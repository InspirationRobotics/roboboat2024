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
def for_closest_animal(e):
    return e['distances']
class wildlife(mission_template):
    def __init__(self, floating_objects):
        count_animals = self.retrieve_animals(floating_objects)
        
        self.animal_dictionaries = [
            {"animal_type": Object_Types.WILDLIFE_PLATYPUS, "rotation_scheme": 1},
            {"animal_type": Object_Types.WILDLIFE_CROCODILE, "rotation_scheme": 2},
            {"animal_type": Object_Types.WILDLIFE_TURTLE, "rotation_scheme": -1}
            ]
    
    def __str__(self):
        rep = "wildlife"
        return rep

    def ready_for_mission(self, floating_objects = None, envmap = None):
        found_line = False
        if floating_objects is not None:
            count_animals = self.retrieve_animals(floating_objects)

        if envmap is not None:
            self.envmap = envmap
            #self.aPlanner.updateMap(envmap)

        if(count_animals == 3):
            return True

        return False

    def estimate_path(self, start_point):
        self.aPlanner = AStar(self.envmap)
        to_rotate_animals = self.rotate_animals(start_point)
        self.aPlanner.__del__()
        return to_rotate_animals



    def rotate_animals(self, start_point):
        for i in self.animal_dictionaries:
            i["distances"] = np.linalg.norm(start_point-i["animal_object"].location)

        self.animal_dictionaries.sort(key=for_closest_animal) 
        rotate_path = np.array([start_point])
        for animal in self.animal_dictionaries:
            diff_vector = np.array(start_point-animal['animal_object'].location)
            unit_vector = diff_vector/np.sqrt(sum(diff_vector**2))
            vector_for_angle = unit_vector*5

            direction = animal['rotation_scheme']/abs(animal['rotation_scheme'])
            rotation = self.rotation_matrix(direction*(-np.pi/2))
            for j in range(5*abs(animal['rotation_scheme'])):
                vector_for_angle = np.matmul(rotation, vector_for_angle)
                target_vector = np.array(-vector_for_angle+animal['animal_object'].location).astype(int)
                partial_path = self.aPlanner.full_path(start_point, target_vector)
                rotate_path = np.concatenate((rotate_path , partial_path), axis = 0)
                start_point = rotate_path[-1]

        return rotate_path.astype(int)
        



        
    
    def update_map(self, envmap):
        self.envmap = envmap
    
    def retrieve_animals(self, floating_objects):
        count_animals = 0
        for i in floating_objects:
            for j in self.animal_dictionaries:
                if i.type == j["animal_type"]:
                    j["animal_object"] = i
                    count_animals = count_animals+1
        return count_animals

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