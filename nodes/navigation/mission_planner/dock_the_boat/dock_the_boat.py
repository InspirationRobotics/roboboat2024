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
from skimage.morphology import skeletonize
import collections
import time

DISTANCE = 10

class dock_the_boat(mission_template):
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
        thePath = []
        # plt.imshow(self.envmap)
        # plt.show()
        #kernel = np.ones((2, 2), np.uint8)
        #self.envmap = cv2.dilate(self.envmap, kernel, iterations = 2)
        #self.envmap = cv2.erode(self.envmap, kernel, iterations = 2)        
        centroids, area, labeled = self.extract_from_envmap(self.envmap)
        plt.imshow(self.envmap)
        plt.show()
        to_keep = []
        for i in range(np.shape(centroids)[0]):
            if(area[i] > 100 and area[i] < 1000):
                to_keep.append((centroids[i], i))
        closest = to_keep[0]
        closest_distance = np.linalg.norm(closest[0]-start_point)
        for i in to_keep:
            temp_distance = np.linalg.norm(closest[0]-start_point)
            if(temp_distance < closest_distance):
                closest = i
                closest_distance = temp_distance

        # plt.imshow(self.envmap)
        # plt.show()
        filtered_map = np.array((labeled == closest[1])*1).astype('uint8')

        # plt.imshow(filtered_map)
        # plt.show()
        kernel = np.ones((3, 3), np.uint8)
        filtered_map = cv2.dilate(filtered_map, kernel, iterations = 1)
        filtered_map = cv2.erode(filtered_map, kernel, iterations = 1)
        skeleton_map = skeletonize(filtered_map, method='lee')
        edges = self.prunning_until(skeleton_map, 4)

        average = np.sum(edges, axis = 0)/np.shape(edges)[0]
        sortid = np.argsort(np.linalg.norm(edges-average))
        edges[np.arange(edges.shape[0])[:,None], sortid]

        closest = edges[0]
        second_closest = edges[1]
        endpoint = second_closest-self.unit_vector(second_closest-closest)*np.linalg.norm(second_closest-closest)/2
        intersection = self.orthogonal_projection(second_closest-closest, start_point-closest)

        direction_vector = start_point - closest-intersection
        direction_vector_unit = self.unit_vector(direction_vector)

        start_goal = np.around(closest-intersection-direction_vector_unit*DISTANCE*5)
        midpoint = np.around(endpoint-direction_vector_unit*DISTANCE*5)
        self.aPlanner = AStar(np.copy(cv2.erode(self.envmap, kernel, iterations = 2)))
        start_track = self.aPlanner.full_path(np.array(start_point).astype(int), np.array(start_goal).astype(int))
        mid_track = self.aPlanner.full_path(np.array(start_goal).astype(int), np.array(midpoint).astype(int))

        end_track = self.aPlanner.full_path(np.array(midpoint).astype(int), np.array(np.around(endpoint)).astype(int))

        thePath = np.concatenate((start_track, mid_track, end_track), axis = 0)
        self.aPlanner.__del__()
        return thePath


    def orthongonal_projection(self, subspace, vector):
        normed = subspace/np.linalg.norm(subspace)
        return np.dot(vector, normed)*subspace

    
    def prunning_until(self, skeleton_map, num_of_edges):
        skeleton_map = np.pad(skeleton_map, 1, mode='constant')*1
        # plt.imshow(skeleton_map)
        # plt.show()
        prunning_kernels = np.array([[1, 2, 4],[8, 16, 32], [64,128,256]])
        possible_sum_values = np.array([17, 20, 80, 272, 89, 88, 24, 25, 23, 22, 18, 19, 308, 304, 48, 52, 464, 400, 144, 208])
        nonzero_elements = np.transpose(np.nonzero(skeleton_map))

        to_prune = []
        for i in nonzero_elements:
            total_sum = np.sum(np.multiply(skeleton_map[i[0]-1:i[0]+2,i[1]-1:i[1]+2], prunning_kernels), axis = None)
            if(np.any(total_sum == possible_sum_values)):
                to_prune.append(i)

        for i in to_prune:
            skeleton_map[i[0]][i[1]] = 0
        skeleton_count = np.count_nonzero(skeleton_map)
        while(len(to_prune) > num_of_edges and skeleton_count != 0):
            to_prune = []
            for i in nonzero_elements:
                total_sum = np.sum(np.multiply(skeleton_map[i[0]-1:i[0]+2, i[1]-1:i[1]+2], prunning_kernels), axis = None)
                if(np.any(total_sum == possible_sum_values)):
                    to_prune.append(i)
            for i in to_prune:
                skeleton_map[i[0]][i[1]] = 0
            skeleton_count = np.count_nonzero(skeleton_map)
        to_prune = np.array(to_prune)
        return to_prune-1



    def geodesic_dilation(self, point, envmap):
        kernel = np.ones((3, 3), np.uint8)
        final_map = np.zeros((np.shape(envmap)[0], np.shape(envmap)[1])).astype('uint8')
        previous_count = np.count_nonzero(final_map)
        final_map[point[0]][point[1]] = 1
        current_count= np.count_nonzero(final_map)

        while(previous_count != current_count):
            # check for python copying issue
            previous_count = current_count
            final_map = cv2.dilate(final_map, kernel, iterations = 1)
            # plt.imshow(final_map)
            # plt.show()
            final_map = final_map & envmap
            # plt.imshow(final_map)
            # plt.show()
            current_count = np.count_nonzero(final_map)
        return final_map






    def extract_from_envmap(self, envmap):
        kernel = np.ones((3, 3), np.uint8)
        newmap = np.copy(envmap)
        
        # extract connected components
        connectivity = 8
        outputs = cv2.connectedComponentsWithStats(newmap, connectivity, cv2.CV_16U)
        area = outputs[2][:,4]
        labeled = outputs[1]
        centroids = np.array(outputs[3]).astype(int)
        
        return centroids, area, labeled

    #geek for geeks code
    def unit_vector(self,vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)
    def orthogonal_projection(self, subspace, vector):
        normed = subspace/(np.linalg.norm(subspace)**2)
        return np.dot(vector, normed)*subspace