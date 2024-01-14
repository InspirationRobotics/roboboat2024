from cmath import sqrt
from floating_objects import Object_Colors, Object_Types, Floating_Object
import numpy as np

# helper funciton, defines metric to sort list of objects by
def DistFunc(dict):
    return dict['dist']

class Grid: 
    def __init__(self, origin, heading, length, width, cell_size):
        self.origin = origin # lat, long of the bottom left corner of the course
        self.heading = np.deg2rad(heading) # heading of the course (provided in 0,360) north is 0, converting it to rad
        self.length = length # length of course (meters)
        self.width = width # width of course (meters)
        self.cell_size = cell_size # (meters)
        self.objects = []
        self.counter = 0
        self.mat = [[-1]*width for _ in range(length)]

    # to increment the id when objects are added into the mapper
    def add_object(self, obj):
        lon, lat = self.grid_to_gps(obj.location[0], obj.location[1])
        geolocation = [lon, lat]
        obj.set_id(self.counter)
        obj.set_geolocation(geolocation)
        #self.mat[obj.location[0]][obj.location[1]] = self.counter
        self.objects.append(obj)
        self.counter += 1

    # ouputs list of objects from closet to furtherest from the boat, second output distance of objects from each object to the boat
    def sort_by_dist(self, x, y, obj_list):
        hypotonuse = []

        for obj in obj_list:
            dist = np.sqrt(np.square(obj.location[0]-x) + np.square(obj.location[1]-y))
            hypotonuse.append({'obj': obj, 'dist': dist})
        hypotonuse.sort(key=DistFunc)

        sorted_list = []
        dist_list = []
        for i in hypotonuse:
            sorted_list.append(i['obj'])
            dist_list.append(i['dist'])
        return sorted_list, dist_list

    # to cut down the master list to desired outputs (all objects of a specific type, ex only bouys)
    def find_object(self, type, x, y):
        list_desired = []
        for i in self.objects:
            if type == i.type:
                list_desired.append(i)
        list_output, dist_list = self.sort_by_dist(x,y,list_desired)
        return list_output, dist_list
            
    def rotateToGpsNorth(self, x, y):
        xd = x*np.cos(self.heading * -1) - y*np.sin(self.heading * -1)
        yd = y*np.cos(self.heading * -1) + x*np.sin(self.heading * -1)
        return xd, yd

    def rotateToGridNorth(self, x, y):
        xd = x*np.cos(self.heading) - y*np.sin(self.heading)
        yd = y*np.cos(self.heading) + x*np.sin(self.heading)
        return xd, yd

    #funciton to translate grid x, y to gps lat lon
    #https://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters
    def grid_to_gps(self, x, y):
        xr , yr = self.rotateToGpsNorth(x, y)
        lat_meter_to_degree_displacement = 1/111320
        lon_meter_to_degree_displacement = 360/(40075000 * np.cos(np.deg2rad(self.origin[0])))
        lat = yr * lat_meter_to_degree_displacement + self.origin[0] # note lat maps to y
        lon = xr * lon_meter_to_degree_displacement + self.origin[1] # note lon maps to x
        return lon, lat

    #funciton to translate gps lat lon to grid x , y
    def gps_to_grid(self, lat, lon):
        lat_meter_to_degree_displacement = 1/111320
        lon_meter_to_degree_displacement = 360/(40075000 * np.cos(np.deg2rad(self.origin[0])))
        y = (lat - self.origin[0]) / lat_meter_to_degree_displacement # note y maps to lat
        x = (lon - self.origin[1]) / lon_meter_to_degree_displacement # note x maps to lon
        xr , yr = self.rotateToGridNorth(x, y)
        xri = int(xr + (0.5 if xr > 0 else -0.5))
        yri = int(yr + (0.5 if yr > 0 else -0.5))
        return xri, yri

    # specify based off x,y on grid if object is in the cell or not 
    def cell_status(self, x, y):
        # NULL assume cell is empty
        object_found = None
        for i in self.objects: 
            if i.location[0] == x and i.location[1] == y:
                object_found = i
                break
        return object_found

    # to create the boundary of the competition field based off origin lat long, and 
    # length, width will be in meters
    def grid_creation(self, origin_x, origin_y, theta, length, width):
        new_theta = 90 - theta
        new_theta_rad = np.deg2rad(new_theta)
        base_tri = length*np.sin(new_theta_rad)
        height_tri = width*np.cos(new_theta_rad)
        coord1 = [origin_x+base_tri, origin_y+height_tri] #bottom left of the square
        coord2 = []
        coord4 = [origin_x+height_tri, origin_y-base_tri] #bottom right of the square

    # helper function to ouput the varaible values
    @property
    def OuputList(self):
        return self.origin, self.heading, self.length, self.width, self.cell_size, self.objects
