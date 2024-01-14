# to rotate a square using polar coordinates and then convert back to cartesian to then plot
# reference https://academo.org/demos/rotation-about-point/

import matplotlib.pyplot as plt
import numpy as np

coords = [
    [2,1],
    [2,5],
    [7,1],
    [7,5]
]
coords_inital = []

coords_final = []

rotation = 10
degree_rotated = rotation * -1
theta_to = np.deg2rad(degree_rotated)

# Rotation about 0,0
for coord in coords: 
    coords_inital.append(coord)
    x = coord[0]
    y = coord[1]
    xd = x*np.cos(theta_to) - y*np.sin(theta_to)
    yd = y*np.cos(theta_to) + x*np.sin(theta_to)
    coords_final.append([xd,yd])

print("final rotated coords cartesian: {}".format(coords_final))

# Translation to gps coords
origin = [32.91395015273022, -117.10028402024729]
lon_meter_to_degree_displacement = 1/111111
lat_meter_to_degree_displacement = 1/(111111 * np.cos(np.deg2rad(origin[0])))
coords_gps = []
for coord in coords_final: 
    lat = coord[0]*lat_meter_to_degree_displacement + origin[0]
    lon = coord[1]*lon_meter_to_degree_displacement + origin[1]
    coords_gps.append([lat,lon])

print("final gps coords: {}".format(coords_gps))

x1 = []
y1 = []
s1 = []
c1 = []

x2 = []
y2 = []
s2 = []
c2 = []

for points in coords_inital: 
    x1.append(points[0])
    y1.append(points[1])
    s1.append(20)
    c1.append(15)

for points in coords_final: 
    x2.append(points[0])
    y2.append(points[1])
    s2.append(20)
    c2.append(80)


#print(c1)
#print(c2)
#front end
fig, ax = plt.subplots()
ax.scatter(x1, y1, s=s1, c=c1, vmin=0, vmax=100)
ax.scatter(x2, y2, s=s2, c=c2, vmin=0, vmax=100)


ax.set(xlim=(-10, 10), xticks=np.arange(-10, 10),
       ylim=(-10, 10), yticks=np.arange(-10, 10))

plt.show()
