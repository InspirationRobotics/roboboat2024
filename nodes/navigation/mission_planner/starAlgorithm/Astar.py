import rclpy
from rclpy.node import Node

from asyncio import open_connection
from cgitb import small
from os import stat
from turtle import st
import numpy as np
import math
import time

from boat_interfaces.msg import *
from geometry_msgs.msg import *

import matplotlib.pyplot as plt
from starAlgorithm.starUtils import *
import cv2

class recievePathNode(Node):
    def __init__(self):
        super().__init__('recievePathNode')
        self.partial_path_sub = self.create_subscription(
            VectorArray,
            '/path_section',
            self.path_callback,
            10)
        self.partial_path = []
        self.finished_path = False

    def send_request(self, message):
        self.req.a = int(sys.argv[1])
        self.req.b = int(sys.argv[2])
        self.req.c = int(sys.argv[3])                 
        self.future = self.cli.call_async(self.req)

    def path_callback(self, message):
        self.finished_path = True
        self.partial_path = []
        for i in message.vec3list:
            self.partial_path.append(np.array([i.x, i.y]).astype(int))

class AStar():
    def __init__(self,envmap):
        kernel = np.ones((3,3))
        envmap = cv2.dilate(envmap, kernel, iterations = 1)
        self.envmap = envmap
        self.path = pqdict({})
        self.all_states = pqdict({})
        self.open_dict = pqdict({})
        self.closed_dict = pqdict({})
        self.needs_update = -1
        self.node = rclpy.create_node('minimal_publisher')
        self.occupancy_publisher = self.node.create_publisher(VectorArray, '/occupied_points', 1)
        self.end_points_publisher = self.node.create_publisher(VectorArray, '/end_points', 1)
        self.map_size_ptr = self.node.create_publisher(Vector3, '/map_size_ptr', 1)
        self.forOcupiedSpaces = VectorArray()

        self.finished_path = False
        self.last_envmap = np.zeros((np.shape(self.envmap)[0], np.shape(self.envmap)[1]))
        self.partial_path_sub = recievePathNode()
    def __del__(self):
        self.node.destroy_node()
        pass
    def updateMap(self, new_envmap):
        self.envmap = new_envmap
        kernel = np.ones((3,3))
        self.envmap = cv2.dilate(self.envmap, kernel, iterations = 1)
    
    def full_path(self, robotpos, targetpos):
        isEqual = np.array_equal(self.last_envmap,self.envmap)
        self.last_envmap = np.copy(self.envmap)
        
        for i in range(3):
            for j in range(3):
                x_delete = robotpos[0]-1+i
                y_delete = robotpos[1]-1+j
                if(x_delete> 0 and x_delete < np.shape(self.envmap)[0] and y_delete> 0 \
                and y_delete < np.shape(self.envmap)[1]):
                    if(self.envmap[robotpos[0]-1+i][robotpos[1]-1+j] == 1):
                        isEqual = False
                        self.envmap[robotpos[0]-1+i][robotpos[1]-1+j] = 0
        """
        if(not isEqual):
            self.forOcupiedSpaces = VectorArray()
            nonzero_indices = np.nonzero(self.envmap)
            self.forOcupiedSpaces.vec3list = [Vector3()]*np.shape(nonzero_indices)[1]

            for i in range(np.shape(nonzero_indices)[1]):
                tempObject = Vector3()
                tempObject.x = float(nonzero_indices[0][i])
                tempObject.y = float(nonzero_indices[1][i])
                tempObject.z = float(0)
                self.forOcupiedSpaces.vec3list[i] = tempObject
        forEndSpaces = VectorArray()
        start_pos = Vector3()
        start_pos.x = float(robotpos[0])
        start_pos.y = float(robotpos[1])
        start_pos.z = float(0)            
        end_pos = Vector3()
        end_pos.x = float(targetpos[0])
        end_pos.y = float(targetpos[1])
        end_pos.z = float(0)
        forEndSpaces.vec3list.append(start_pos)
        forEndSpaces.vec3list.append(end_pos)

        mapSize = Vector3()
        mapSize.x = float(np.shape(self.envmap)[0])
        mapSize.y= float(np.shape(self.envmap)[1])
        mapSize.z = float(0)

        self.occupancy_publisher.publish(self.forOcupiedSpaces)
        self.end_points_publisher.publish(forEndSpaces)
        self.map_size_ptr.publish(mapSize)
        
        self.finished_path = False
        self.partial_path = None
        time_to_stop = 0

        rclpy.spin_once(self.partial_path_sub, timeout_sec = 2)
        to_return = np.copy(self.partial_path_sub.partial_path)
        return to_return
        #publish here
        """
        robotpos = np.array(robotpos)
        targetpos = np.array(targetpos)
        desired_path = []
        while(robotpos[0]!=targetpos[0] or robotpos[1]!=targetpos[1]):
            robotpos = np.array(self.robotplanner(robotpos, targetpos))
            desired_path.append(robotpos)
        desired_path=np.stack(desired_path, axis=0)
        return desired_path
        
        
        
        

        

    #since the directions is reversible, going from the target to the robot
    #is the same as going from the robot to the target
    def robotplanner(self, robotpos, targetpos):
        self.needs_update = self.needs_update+1
        endpose = (robotpos[0], robotpos[1])

        #initializes the subspaces to zero
        self.open_dict = pqdict({})
        self.close_dict = pqdict({})

        #creates the start node
        dict0 = targetpos[0]
        dict1 = targetpos[1]
        self.open_dict[(dict0, dict1)] = stateObject(targetpos,robotpos)
        
        #while the target node is not closed
        while endpose not in self.close_dict:
            #take the smallest f value out of the open node
            smallest = self.open_dict.popitem()
            self.close_dict[smallest[0]] = smallest[1]
            smallest_array = np.array((smallest[0]))

            #for all children of the current node
            theChildren = all_children(self.envmap, smallest_array)
            for i in range(len(theChildren)):
                aKey = tuple(theChildren[i])

                #if the node is not in the open or closed direcory, put it in the open directory
                if(aKey not in self.close_dict and aKey not in self.open_dict):
                    self.open_dict[aKey] = stateObject(aKey, robotpos, self.close_dict[smallest[0]])
                #if the node is in the open directory update the values
                elif(aKey in self.open_dict):
                    if self.open_dict[aKey].g > smallest[1].g+1:
                        self.open_dict[aKey].updateG(smallest[1].g+1)
                        self.open_dict[aKey].previousPosition = smallest[1]
            """
            print("hello world")
            #for all children of the current node
            theChildren = ocupied_children(self.envmap, smallest_array)
            for i in range(len(theChildren)):
                aKey = tuple(theChildren[i])

                #if the node is not in the open or closed direcory, put it in the open directory
                print(aKey)
                if(aKey not in self.close_dict and aKey not in self.open_dict):
                    self.open_dict[aKey] = stateObject(aKey, robotpos, self.close_dict[smallest[0]])
                    self.open_dict[aKey].updateG(self.close_dict[smallest[0]].g+10000)
                #if the node is in the open directory update the values
                elif(aKey in self.open_dict):
                    if self.open_dict[aKey].g > smallest[1].g+10000:
                        self.open_dict[aKey].updateG(smallest[1].g+10000)
                        self.open_dict[aKey].previousPosition = smallest[1]
            """
            
        #return the value of the most optimal path
        return self.close_dict[endpose].previousPosition.position

