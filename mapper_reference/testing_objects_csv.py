#testing functionality of the classes within "floating_objects"

from floating_objects import Object_Colors, Object_Types, Floating_Object
from read_csv import read_input, format_data
from navigation import mapper_points
from grid import Grid
import matplotlib.pyplot as plt
import numpy as np
from gmaputil import CustomGoogleMapPlotter

#print(Object_Colors.GREEN)
#print(Object_Types.BOUY)

#intilizing the bottom left coordinate of the grid, the heading from vertical, width, height, cell size
Grid_1 = Grid([32.91424737414133, -117.10087410624423], 0, 100, 100, 1)

data = read_input("input2.csv")
items = format_data(data, Grid_1)
print(len(items))

# adding objects into the grid class
for item in items:
    Grid_1.add_object(item)
   
print(Grid_1.OuputList)

boat_x = 9
boat_y = 9

# output from the grid class
sorted_list, dist_list = Grid_1.find_object(Object_Types.BOUY,boat_x,boat_y)
final_list = []
# front view of printing out the output from the grid class
for i in range(0,len(sorted_list)):
    print("id {}, coord {}, dist: {}, color: {}".format(sorted_list[i].id,sorted_list[i].location, dist_list[i], sorted_list[i].color))
    final_list.append(sorted_list[i].get_json())

final_json = str({ 'objects' : final_list})
print("the json: {}, type: {}".format(final_json, type(final_json)))

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

initial_zoom = 25
gmap = CustomGoogleMapPlotter(gps_lat[0], gps_lon[0], initial_zoom,
				      map_type='satellite')
gmap.color_scatter(gps_lat, gps_lon, values, colormap='coolwarm', size=1)

gmap.draw("objmap.html")

# start of the matplot lib front end 
print(plot_color)
fig, ax = plt.subplots()

# plotting the boat
ax.scatter(boat_x, boat_y, s=80, c=80, marker=5, vmin=0, vmax=100)

# plotting the bouys
ax.scatter(plot_x, plot_y, s=plot_size, c=plot_color, vmin=0, vmax=100)

# plotting tick marks and the axis labels
ax.set(xlim=(0, 100), xticks=np.arange(1, 1000, 20),
       ylim=(0, 100), yticks=np.arange(1, 1000, 20))

plt.show()
