import gps_navigator
import sys


if (len(sys.argv) < 3):
	print("Usage: gps_test.py <lat> <lon> ..")
index = 1;
for i in range(0, len(sys.argv) // 2):
	print("Waypoint\n")
	navigator = gps_navigator.GPS_Nav()
	navigator.gps_navigator(float(sys.argv[index]), float(sys.argv[index+1]))
	index += 2


