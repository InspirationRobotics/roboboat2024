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
from follow_path.connect_buoys import *
from floating_objects import Object_Colors, Object_Types, Floating_Object
from itertools import combinations
from mission_template import *
import time



class follow_the_path(mission_template):
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

        self.floating_white = self.retrieve_color(floating_objects, Object_Colors.WHITE)
        
        self.filter_unecessary()

    def ready_for_mission(self, floating_objects = None, envmap = None):
        if floating_objects is not None:
            self.get_buoys(floating_objects)
        if envmap is not None:
            self.envmap = envmap
            self.aPlanner.updateMap(envmap) 
        # think about a way to filter out entrance and exit gates
        # maybe using other angles

        # given a certain number of buoys determine whether we are ready to take on the challenge
        if(len(self.floating_white) == 4 and len(self.floating_green) >= 2 and len(self.floating_red) >= 2):
            return True
        
        return False
               
    
    def estimate_path(self, start_point):
        self.ends = self.find_start()
        
        self.organize_objects(self.ends, self.floating_red)
        self.organize_objects(self.ends, self.floating_green)
        
        # for i in self.floating_green:
        #     self.envmap[i.location[0]][i.location[1]] = 1
        # for i in self.floating_red:
        #     self.envmap[i.location[0]][i.location[1]]= 1
        # for i in self.floating_red:
        #     self.envmap[i.location[0]][i.location[1]] = 1
        # plt.imshow(self.envmap)
        # plt.show()
        envmap = connect_the_buoys(self.envmap, self.floating_red)
        envmap = connect_the_buoys(self.envmap, self.floating_green)
        # plt.imshow(envmap)
        # plt.show()
        self.aPlanner = AStar(self.envmap)

        total_path = []

        first = np.argmin([np.linalg.norm(start_point-self.floating_green[0].location), np.linalg.norm(start_point-self.floating_green[-1].location)])
        first = first *-1
        print(first)
        entering_grid = self.enter_the_grid( start_point, first)
        travesing_path = self.to_end_of_grid( entering_grid[-1], first)
        get_out = self.get_out( travesing_path[-1], first)
        get_through = np.concatenate((entering_grid,travesing_path),axis=0)
        full_path = np.concatenate((get_through,get_out),axis=0)
        # for i in full_path:
        #     envmap[i[0]][i[1]] = 1
        # plt.imshow(envmap)
        # plt.show()
        return full_path
    
    def enter_the_grid(self, start_point, first):
        if(first == 0):
            arr_val = 1
        else:
            arr_val = -2
        midpoint = np.array((self.floating_green[arr_val].location-self.floating_red[arr_val].location)/2).astype(int)
        midpoint = self.floating_green[arr_val].location-midpoint
        return self.aPlanner.full_path(start_point,midpoint)
    
    def to_end_of_grid(self, start_point, first):
        envmap_temp = np.array(self.envmap)

        x = bresenham2D(self.floating_green[0].location[0], self.floating_green[0].location[1],\
        self.floating_red[0].location[0],self.floating_red[0].location[1])
            
        for j in range(np.shape(x)[1]):
            envmap_temp[int(x[0,j])][int(x[1,j])] = 1

        x = bresenham2D(self.floating_green[-1].location[0], self.floating_green[-1].location[1],\
        self.floating_red[-1].location[0],self.floating_red[-1].location[1])
            
        for j in range(np.shape(x)[1]):
            envmap_temp[int(x[0,j])][int(x[1,j])] = 1

        self.aPlanner.updateMap(envmap_temp)

        if(first == 0):
            arr_val = -2
        else:
            arr_val = 1

        end_point = np.array((self.floating_green[arr_val].location-self.floating_red[arr_val].location)/2).astype(int)
        end_point = self.floating_green[arr_val].location-end_point
        calc_path = self.aPlanner.full_path(start_point,end_point)
        self.aPlanner.updateMap(self.envmap)

        return calc_path

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


    

    def organize_objects(self, ends, floating_buoys):
        color = floating_buoys[0].color
        added_start = False
        for end_pair in ends:
            for an_end in end_pair:
                if an_end[1].color == color:
                    floating_buoys.remove(an_end[1])
                    if not added_start:
                        floating_buoys.insert(0,an_end[1])
                        floating_buoys.insert(0,an_end[0])
                        added_start = True
                    else:
                        floating_buoys.append(an_end[1])
                        floating_buoys.append(an_end[0])
                      

    def find_start(self):
        #find the minimum distance of each white buoy to all others
        i = 0

        min_red = []
        min_green = []
        min_red_dist = np.zeros((len(self.floating_white),1))+inf
        min_green_dist = np.zeros((len(self.floating_white),1))+inf
        for white in self.floating_white:
            min_red.append(self.floating_red[0])
            min_green.append(self.floating_green[0])
            for green in self.floating_green:
                dist = np.linalg.norm(white.location-green.location)
                if(dist < min_green_dist[i]):
                    min_green_dist[i] = dist
                    min_green[i] = green

            for red in self.floating_red:
                dist = np.linalg.norm(white.location-red.location)
                if(dist < min_red_dist[i]):
                    min_red_dist[i] = dist     
                    min_red[i] = red       
            i = i+1
        
        aPermutation = list(combinations(self.floating_white,2))
        closest_white_dist = np.zeros(len(self.floating_white))+inf
        closest_white = [None] * len(self.floating_white)
        for i in aPermutation:
            dist = np.linalg.norm(i[0].location-i[1].location)
            for single_buoy in range(len(self.floating_white)):
                if i[0] == self.floating_white[single_buoy]:
                    if(dist<closest_white_dist[single_buoy]):
                        closest_white_dist[single_buoy] = dist
                        closest_white[single_buoy] = i[1]

            for single_buoy in range(len(self.floating_white)):
                if i[1] == self.floating_white[single_buoy]:
                    if(dist<closest_white_dist[single_buoy]):
                        closest_white_dist[single_buoy] = dist
                        closest_white[single_buoy] = i[0]
        
        white_pairs = []
        for i in range(len(self.floating_white)):
            for j in range(i,len(self.floating_white)):
                if self.floating_white[j] == closest_white[i] and self.floating_white[i] == closest_white[j]:
                    white_pairs.append((self.floating_white[j],self.floating_white[i]))

        tail_ends = []
        for i in range(len(white_pairs)):
            for j in range(len(self.floating_white)):
                if(self.floating_white[j] == white_pairs[i][0]):
                    green = min_green[j]
                    red = min_red[j]
                    break

            vector_one = np.zeros((2,2))
            vector_one[0,:] = white_pairs[i][0].location - green.location
            vector_one[1,:] = white_pairs[i][1].location - red.location
            vector_two = np.zeros((2,2))
            vector_two[0,:] = white_pairs[i][0].location - red.location
            vector_two[1,:] = white_pairs[i][1].location - green.location

            angle_one = self.angle_between(np.array(vector_one[0,:]), np.array(vector_one[1,:]))
            angle_two = self.angle_between(np.array(vector_two[0,:]), np.array(vector_two[1,:]))
            
            best_pair = np.argmin([angle_one,angle_two])

            if(best_pair == 0):
                tail_ends.append(((white_pairs[i][0], green), (white_pairs[i][1], red)))
            else:
                tail_ends.append(((white_pairs[i][0], red), (white_pairs[i][1], green)))
        return tail_ends

        # for i in range(np.shape(min_green_dist)[0]):
        #     print(self.floating_white[i].location, min_red[i].location, min_green[i].location)


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
    
    def filter_unecessary(self):
        # go thoruhg thw white buoys untill we find a good one or we don't
        temp_white = self.floating_white.copy()
        while(len(temp_white)>1):
            #find the closest white buoy
            minimum_white = temp_white[1]
            min_dist_w = np.linalg.norm(temp_white[1].location-temp_white[0].location)
            for j in range(1,len(temp_white)):
                loc_min = np.linalg.norm(temp_white[j].location-temp_white[0].location)
                if loc_min < min_dist_w:
                    min_dist_w = loc_min
                    minimum_white = temp_white[j]

            #find the closest red_buoy
            minimum_red = self.floating_red[0]
            min_dist_r = np.linalg.norm(self.floating_red[0].location-temp_white[0].location)
            for j in range(1,len(self.floating_red)):
                loc_min = np.linalg.norm(self.floating_red[j].location-temp_white[0].location)
                if loc_min < min_dist_r:
                    min_dist_r = loc_min
                    minimum_red = self.floating_red[j]

            #find the closest green_buoy
            minimum_green = self.floating_green[0]
            min_dist_g = np.linalg.norm(self.floating_green[0].location-temp_white[0].location)
            for j in range(1,len(self.floating_green)):
                loc_min = np.linalg.norm(self.floating_green[j].location-temp_white[0].location)
                if loc_min < min_dist_g:
                    min_dist_g = loc_min
                    minimum_green = self.floating_green[j]
            
            #deside if the red or the green buoy are the closest
            if(min_dist_g < min_dist_r):
                closest_colored_buoy = minimum_green
                closest_color = "green"
                min_dist_closest_color = min_dist_g
                to_delete = self.floating_green
            else:
                closest_colored_buoy = minimum_red
                closest_color = "red"
                min_dist_closest_color = min_dist_r
                to_delete = self.floating_red

            color_angle = self.angle_between(closest_colored_buoy.location-temp_white[0].location, minimum_white.location-temp_white[0].location)

            throw_away = False
            if(abs(color_angle-np.pi) < .1 or min_dist_w > 20):
                throw_away = True
            
            if(throw_away and min_dist_closest_color <= 20):
                to_delete.remove(closest_colored_buoy)

            if(throw_away and min_dist_w > 20):
                self.floating_white.remove(temp_white[0])
            elif(throw_away):
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

                if(min_dist_other < 20):
                    other_color.remove(other_closest)
                
                self.floating_white.remove(minimum_white)
                temp_white.remove(minimum_white)
                self.floating_white.remove(temp_white[0])
            if(not throw_away and min_dist_w < 20):
                temp_white.remove(minimum_white)
            temp_white.remove(temp_white[0])
