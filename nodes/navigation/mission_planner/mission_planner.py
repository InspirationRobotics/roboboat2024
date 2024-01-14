import sys
sys.path.append('../../../mapper_reference/')

from grid import Grid
from follow_path.follow_the_path import *
from avoid_wall.avoid_wall import *
from prequalification.prequalification import *
from enter_the_gate.enter_the_gate import *
from wildlife.wildlife import *
from floating_objects import Object_Colors, Object_Types, Floating_Object
from testing_objects import *
from cameraless_qual.cameraless_qual import *
from dock_the_boat.dock_the_boat import *
from enter_the_gates_blind.enter_the_gates_blind import *
from itertools import chain
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Point, Pose
from obj_msg.msg import MapInfo

from gmaputil import CustomGoogleMapPlotter
import skimage.measure

import cv2

PATH_PLANNER_DEFINITION = .5
SLAM_DEFINITION = .05
class mission_planner(Node):
    def __init__(self, floating_objects, envmap):
        super().__init__('mission_planner')

        self.missions_to_do = []
        self.missions_ready = []
        self.missions_done = []
        self.map_info = []
        self.in_mission = None
        for i in floating_objects:
            i.location = np.array(i.location*SLAM_DEFINITION/PATH_PLANNER_DEFINITION).astype(int)
        self.floating_objects = floating_objects
        #self.round_objects(floating_objects)
        #self.missions_to_do.append(follow_the_path(floating_objects))
        #self.missions_to_do.append(avoid_wall(floating_objects))
        #self.missions_to_do.append(prequalification(floating_objects))
        #self.missions_to_do.append(wildlife(floating_objects))
        #self.missions_to_do.append(wildlife(floating_objects))
        #self.missions_to_do.append(enter_the_gate(floating_objects))
        self.missions_to_do.append(dock_the_boat(floating_objects))
        #self.missions_to_do.append(enter_the_gates_blind(floating_objects))
        #self.missions_to_do.append(cameraless_qual(floating_objects))

    def check_mission_readiness(self, floating_objects, envmap):
        floating_copy = []
        if envmap is None:
            return
        for i in floating_objects:
            floating_copy.append(Floating_Object(i.color,np.array(i.location),i.type))
            floating_copy[-1].location = np.array(floating_copy[-1].location*SLAM_DEFINITION/PATH_PLANNER_DEFINITION).astype(int)

        if(self.in_mission is not None):
            return

        missions_found = 0
        simplified_map = self.normalize_map(envmap, PATH_PLANNER_DEFINITION, SLAM_DEFINITION)
        #self.round_objects(floating_objects)
   
        self.current_map = np.array(simplified_map)
            
        for i in range(len(self.missions_to_do)):
            if envmap is not None:
                isReady = self.missions_to_do[i-missions_found].ready_for_mission(floating_copy,np.copy(np.array(simplified_map).astype('uint8')))
            else:
                isReady = self.missions_to_do[i-missions_found].ready_for_mission(floating_copy,np.copy(np.array(simplified_map).astype('uint8')))
            if(isReady):
                self.missions_ready.append(self.missions_to_do[i-missions_found])
                self.missions_to_do.remove(self.missions_to_do[i-missions_found])
                missions_found = missions_found+1
        
    def do_a_mission(self, start_point):
        start_point = np.array(start_point*SLAM_DEFINITION/PATH_PLANNER_DEFINITION).astype(int)
        if(self.in_mission is not None):
            simplified_map = self.normalize_map(envmap, PATH_PLANNER_DEFINITION, SLAM_DEFINITION)
            envmap = np.copy(simplified_map)
             
            #when mission is done, get throug finish point
            if(self.in_mission.check_done(start_point)):
                self.missions_done.append(self.missions_ready[0])
                self.missions_ready.remove(self.missions_ready[0])   
                return None  
            return None 
            return self.in_mission.update_path(start_location, floating_object.copy(), simplified_map) 
                  
        # need to be more involved, but as a first iteration looks goodsimplified_map
        elif(len(self.missions_ready)>0):
            #print("doing the " + str(self.missions_ready[0]) + "mission")
            #self.missions_ready[0].ready_for_mission(floating_object.copy(),simplified_map)
            #self.mission
            #self.in_mission = self.missions_ready[0]
            #try:
            thePath = self.missions_ready[0].estimate_path(start_point)
            print(thePath)
            print()
            for i in thePath:
                self.missions_ready[0].envmap[i[0]][i[1]] = 1
            plt.imshow(self.missions_ready[0].envmap)
            plt.show()
            #except:
            #    thePath = None
            thePath = np.array(thePath*PATH_PLANNER_DEFINITION/SLAM_DEFINITION).astype(int)
            self.missions_done.append(self.missions_ready[0])
            self.missions_ready.remove(self.missions_ready[0])
            #self.show_path(thePath)

            return thePath
        return None

    def go_to_wp(self, wp_idx):
        # called self.thePath and self.waypoint_idx, self.grid2gps in main

        # TODO: Update dynamic
        # TODO: change target when map updates.
        # TODO: Jesus
        if (self.waypoint_idx < len(self.thePath)):
            p = self.thePath[wp_idx]
            x, y = p
            print(f"Procedding to point {x}, {y}")
            lon, lat = self.grid2gps(x, y)
            msg = Point()
            msg.x = lon
            msg.y = lat
            # TODO: add passthrough = True 
            # TODO: Rishi
            self.target_pub.publish(msg)
        else:
            print("mission complete")

    def normalize_map(self, envmap, desired_def, curr_def):
        desired_ratio = int(desired_def/curr_def)
        one_color = np.array([*range(0,envmap.height*envmap.width*3,3)])
        first_array = np.array(envmap.data)[one_color]
        first_array = np.reshape(first_array, (-1,envmap.width))
        first_array = np.array(1*(first_array>0)).astype('uint8')
        plt.imshow(first_array)
        plt.show()

        kernel = np.ones((2,2))
        first_array = cv2.dilate(first_array, kernel, iterations = 1)
        first_array = cv2.erode(first_array, kernel, iterations = 1)

        kernel = np.ones((3,3))
        first_array = cv2.erode(first_array, kernel, iterations = 1)
        first_array = cv2.dilate(first_array, kernel, iterations = 1)
        simplified_map = skimage.measure.block_reduce(first_array, (desired_ratio,desired_ratio), np.max)
        plt.imshow(simplified_map)
        plt.show()
        return simplified_map

    def extract_from_envmap(self, envmap):
        kernel = np.ones((3, 3), np.uint8)
        newmap = np.copy(envmap)
        
        # filter out noise
        #newmap = cv2.erode(newmap, kernel, iterations=10)
        #newmap = cv2.dilate(newmap, kernel, iterations=10)
        
        # extract connected components
        connectivity = 4
        outputs = cv2.connectedComponentsWithStats(newmap, connectivity, cv2.CV_32S)
        centroids = outputs[2]
        
        return centroids

    def check_new_ojbects(self, floating_objects):
        for i in floating_objects:
            pass
        pass