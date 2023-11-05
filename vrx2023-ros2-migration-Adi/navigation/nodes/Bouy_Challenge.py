import matplotlib.pyplot as plt
import numpy as np

class bouy:
    def __init__(self, centerx, centery, heading, waypoints):
        self.centerx = centerx
        self.centery = centery
        self.heading = heading
        self.waypoints = waypoints
    
    def angle_from_center(self, radius):
        slices = (2 * np.pi)/self.waypoints
        self.waypoints_list = []
        for i in range(0,self.waypoints + 1):
            self.waypoints_list.append((slices*i))
        return self.waypoints_list
    
    def changing_angle(self,radius):
        self.waypoints_list = self.angle_from_center(radius)
        self.waypoints_90 = []
        self.waypoints_90 = list(self.waypoints_list)
        for i in range(0,self.waypoints + 1):
            self.waypoints_90[i] = self.waypoints_list[i] + 90
        return self.waypoints_90
    
    def translation(self,radius):
        angles = self.changing_angle(radius)
        self.coordinates_listx = []
        self.coordinates_listy = []
        self.coordinates_listx = list(self.waypoints_list)
        self.coordinates_listy = list(self.waypoints_list)
        for i in range(0,self.waypoints + 1):
            self.coordinates_listx[i] = radius * np.cos(angles[i])
            self.coordinates_listy[i] = radius * np.sin(angles[i])
        plt.plot(self.coordinates_listx, self.coordinates_listy)
        plt.show()
        



T1 = bouy(0,0,1,100)    
T1.translation(2)