#testing functionality of the classes within "floating_objects"

from floating_objects import Object_Colors, Object_Types, Floating_Object
from read_csv import read_input, format_data
from navigation import mapper_points
from grid import Grid
import matplotlib.pyplot as plt
import numpy as np
from gmaputil import CustomGoogleMapPlotter
#import rospya
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String
from angle import *
from std_msgs.msg import Float64
from obj_msg.msg import MapInfo
from obj_msg.msg import Obj
from geometry_msgs.msg import Point


import json

class mapper(Node):
    def __init__(self):
        super().__init__('mapper')

        # fixed
        self.map_origin = []
        self.map_orientation = []
        self.map_density = []
        self.map_w = []
        self.map_h = []

        # state info
        self.gps_pose = []
        self.gps_hdg = []
    
        self.lon_sub = self.create_subscription(
            Float64,
            '/wamv/gps/lon',
            self.lon_cb,
            10)
        self.lon_sub

        self.lat_sub = self.create_subscription(
            Float64,
            '/wamv/gps/lat',
            self.lat_cb,
            10)
        self.lat_sub

        self.hdg_sub = self.create_subscription(
            Float64,
            '/wamv/gps/hdg',
            self.hdg_cb,
            10)
        self.hdg_sub

        self.obj_pub = self.create_publisher(String, '/wamv/mapper/grid', 10)
        self.info_pub = self.create_publisher(MapInfo, '/wamv/map/info', 10)
        self.pose_pub = self.create_publisher(Point, '/wamv/map/pose', 10)
        self.hdg_pub = self.create_publisher(Float64, '/wamv/map/hdg', 10)

        timer_period = 3
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        self.pub_map_hdg()
        self.pub_map_pose()
        self.pub_map_info()
        # self.point_publisher_.publish(aPoint)
        # self.map_publisher_.publish(aMap)


    def lat_cb(self, msg):
        if self.gps_pose == []:
            self.gps_pose = [0, 0]
            
        self.gps_pose[1] = msg.data

    def lon_cb(self, msg):
        if self.gps_pose == []: 
            self.gps_pose = [0, 0]
            
        self.gps_pose[0] = msg.data

    def hdg_cb(self, msg):
        self.gps_hdg = msg.data

    def initialize_map(self, origin, orientation, density, w, h):
        self.map_origin = origin
        self.map_orientation = orientation
        self.density = 1.0
        self.map_w = w
        self.map_h = h

    def calculate_map_coords(self):
        m_per_ll = 111000

        m = [0, 0]
        m[0] = (self.gps_pose[0] - self.map_origin[0]) * m_per_ll
        m[1] = (self.gps_pose[1] - self.map_origin[1]) * m_per_ll
        
        m = rotate(m, [0, 0], PI / 2 - self.map_orientation)
        
        return m
        
    def calculate_map_hdg(self):
        return normalize_angle(self.gps_hdg - self.map_orientation)
        
    def pub_map_info(self):
        m = MapInfo()

        m.origin_lat = self.map_origin[1]
        m.origin_lon = self.map_origin[0]
        m.hdg = self.gps_hdg
        m.density = self.density
        m.w = self.map_w
        m.h = self.map_h
        print(m)
        self.info_pub.publish(m)

    def pub_map_pose(self):
        map_p = self.calculate_map_coords()

        p = Point()
        p.x = map_p[0]
        p.y = map_p[1]
        print(p)
        self.pose_pub.publish(p)

    def pub_map_hdg(self):
        msg = Float64()
        msg.data = self.calculate_map_hdg()
        print(msg)
        self.hdg_pub.publish(msg)

        
    def run(self):
        #intializing objects to be added into the grid
        item_1 = Floating_Object(Object_Colors.RED,[5,5],Object_Types.BOUY)
        item_2 = Floating_Object(Object_Colors.RED,[5,10],Object_Types.BOUY)
        item_3 = Floating_Object(Object_Colors.GREEN,[15,5],Object_Types.BOUY)
        item_4 = Floating_Object(Object_Colors.GREEN,[15,10],Object_Types.BOUY)

        # adding objects into the grid class
        #print(item_1)
        self.initialize_map([32.914057, -117.100150], 0.0, 1.0, 100, 100)
        Grid_1 = Grid([32.914057, -117.100150], 10, 20, 20, 1)
        Grid_1.add_object(item_1)
        Grid_1.add_object(item_2)
        Grid_1.add_object(item_3)
        Grid_1.add_object(item_4)
        print(Grid_1.OuputList)

        boat_x = 9
        boat_y = 9

        # output from the grid class
        sorted_list, dist_list = Grid_1.find_object(Object_Types.BOUY,boat_x,boat_y)
        #print(sorted_list)
        #for i in sorted_list:
        #    print(i.id)
        final_list = []
        # front view of printing out the output from the grid class
        for i in range(0,len(sorted_list)):
            print("id {}, coord {}, dist: {}, color: {}".format(sorted_list[i].id,sorted_list[i].location, dist_list[i], sorted_list[i].color))
            final_list.append(sorted_list[i].get_json())
        final_json = String()
        final_json.data = str( "{\"objects\": " + json.dumps(final_list) + "}" )
        print("the json: {}, type: {}".format(final_json, type(final_json)))
        #pub.publish(final_json)


        # for the front end google maps integration
        plot_x = []
        plot_y = []
        plot_color = []
        plot_size = []
        gps_lat = []
        gps_lon = []
        test_x = []
        test_y = []
        values = []
        for i in sorted_list:
            plot_x.append(i.location[0])
            plot_y.append(i.location[1])
            plot_color.append(i.color.value)
            plot_size.append(80)
            lat, lon = Grid_1.grid_to_gps(i.location[0], i.location[1])
            gps_lat.append(lat)
            gps_lon.append(lon)
            x,y = Grid_1.gps_to_grid(lat, lon)
            test_x.append(x)
            test_y.append(y)
            values.append(i.id)

        print(plot_x)
        print(plot_y)
        print(gps_lat)
        print(gps_lon)
        print(test_x)
        print(test_y)
        print(Grid_1.mat)

        #initial_zoom = 25
        #gmap = CustomGoogleMapPlotter(gps_lat[0], gps_lon[0], initial_zoom,
        #                    map_type='satellite')
        #gmap.color_scatter(gps_lat, gps_lon, values, colormap='coolwarm', size=1)

        #gmap.draw("objmap.html")

        # start of the matplot lib front end 
        #print(plot_color)
        #fig, ax = plt.subplots()

        # plotting the boat
        #ax.scatter(boat_x, boat_y, s=80, c=80, marker=5, vmin=0, vmax=100)

        # plotting the bouys
        #ax.scatter(plot_x, plot_y, s=plot_size, c=plot_color, vmin=0, vmax=100)

        # plotting tick marks and the axis labels
        #ax.set(xlim=(0, 20), xticks=np.arange(1, 20),
        #    ylim=(0, 20), yticks=np.arange(1, 20))

        #plt.show()
def main(args=None):
    rclpy.init()
    map = mapper()
    map.run()
    map.gps_pose = [2,3]
    map.gps_hdg = 0.0
    print(map.gps_pose, map.gps_hdg)
    while rclpy.ok():
        if (map.gps_pose != [] and map.gps_hdg != []):
            print("hello darling")
            map.pub_map_info()
            map.pub_map_pose()
            map.pub_map_hdg()
        print("my old friend")
        rclpy.spin_once(map)
    print(rclpy)

if __name__ == '__main__':
    main()
