import socket
import sys
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Int32MultiArray
import serial

rospy.init_node('hb_client', anonymous=True)
rate = rospy.Rate(10) # 10hz
server_addr = "192.168.0.169"
server_port = 8000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
print("Do Ctrl+c to exit the program !!")

def mc_callback(data):
    mc_data = '{"Motor Control":'+str(data.data)+'}'
    s.sendto(mc_data.encode('utf-8'), (server_addr, server_port))
    print(mc_data)
    rate.sleep()
def lat_callback(data):
    lat_data = '{"GPS Lat":'+str(data.data)+'}'
    s.sendto(lat_data.encode('utf-8'), (server_addr, server_port))
    print(lat_data)
    rate.sleep()
def lon_callback(data):
    lon_data = '{"GPS Lon":'+str(data.data)+'}'
    s.sendto(lon_data.encode('utf-8'), (server_addr, server_port))
    print(lon_data)
    rate.sleep()
def hdg_callback(data):
    hdg_data = '{"GPS Hdg":'+str(data.data)+'}'
    s.sendto(hdg_data.encode('utf-8'), (server_addr, server_port))
    print(hdg_data)
    rate.sleep()

def client():
    rospy.init_node('hb_client', anonymous=True)
    rospy.Subscriber("/wamv/torqeedo/motor_cmd", String, mc_callback)
    rospy.Subscriber("/wamv/sensors/gps/lat", Float64, lat_callback)
    rospy.Subscriber("/wamv/sensors/gps/lon", Float64, lon_callback)
    rospy.Subscriber("/wamv/sensors/gps/hdg", Float64, hdg_callback)
    while not rospy.is_shutdown():
        #send_data = '{'+mc_data+','+lat_data+','+lon_data+','+hdg_data+'}'
        #print(send_data)
        #s.sendto(send_data.encode('utf-8'), (server_addr, server_port))
        rate.sleep()

if __name__ == '__main__':
    try:
        client()
    except rospy.ROSInterruptException:
        pass

s.close()
