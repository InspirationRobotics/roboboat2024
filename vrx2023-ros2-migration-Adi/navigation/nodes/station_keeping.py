import gps_navigator
import sys

if (len(sys.argv) < 4):
	print("Usage: station_keeping.py <lat> <lon> ..")

navigator = gps_navigator.GPS_Nav()
navigator.gps_navigator(float(sys.argv[1]), float(sys.argv[2]), True, float(sys.argv[3]))

