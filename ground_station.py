from guizero import App, Text, Box, PushButton
import socket
import sys
import threading
import serial
import json
from html2image import Html2Image
import time

hti = Html2Image()
left = 0
right = 0
server_addr = "127.0.0.1"
server_port = 8000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)


 # Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ("192.168.0.169", 8000)
s.bind(server_address)

# def init():
#     print("Button was pressed")
#     send_data = "./wamv_init.sh"
#     s.sendto(send_data.encode('utf-8'), (server_addr, server_port))
#     print("Init script started")

#     hti.screenshot(
#     html_file='/Users/ashiriagoel/Documents/inspiration_robotx2022/Code/mymap.html', save_as='out.png'
# )
# def qual():
#     print("Button was pressed")
#     send_data = "python gps_navigator.py"
#     s.sendto(send_data.encode('utf-8'), (server_addr, server_port))
#     print("Init script started")

#     hti.screenshot(
#     html_file='/Users/ashiriagoel/Documents/inspiration_robotx2022/Code/mymap.html', save_as='out.png'
# )
    # imgkit.from_file('/Users/ashiriagoel/Documents/inspiration_robotx2022/Code/mymap.html', '/Users/ashiriagoel/Documents/out.jpg')
app = App(title="Team Inspiration Ground Station")
gps_lat = 0
gps_lon = 0
gps_hdg = 0

def settext():
    lat.value = "GPS Lat: "+str(gps_lat)
    lon.value = "GPS Lon: "+str(gps_lon)
    hdg.value = "GPS Hdg: "+str(gps_hdg)

title = Text(app, text="Team Inspiration Ground Station",size=30, font="Times New Roman", color="#002e85")
while True:
    time.sleep(1)
    data, address = s.recvfrom(4096)
    info = data.decode('utf-8')
    info_json = json.loads(info, parse_int=int)

    lat = Text(app, text="GPS Lat: "+str(gps_lat),size=20, font="Times New Roman", color="#002e85")
    lon = Text(app, text="GPS Lon: "+str(gps_lon),size=20, font="Times New Roman", color="#002e85")
    hdg = Text(app, text="GPS Hdg: "+str(gps_hdg),size=20, font="Times New Roman", color="#002e85")
    

   

    def get_lat():
            try:
                gps_lat = info_json['GPS Lat']
                lat.set("GPS Lat: "+str(gps_lat))
                lat.after(500, get_lat())
            except:
                pass
    def get_lon():        
            try:
                gps_lon = info_json['GPS Lon']
                lon.set("GPS Lat: "+str(get_lon))
                lon.after(500, get_lon())
            except:
                pass
    def get_hdg():
            try:
                gps_hdg = info_json['GPS Hdg'] 
                hdg.set("GPS Lat: "+str(gps_hdg))
                hdg.after(500, gps_hdg())
            except:
                pass

        
    # lat = Text(app, text="GPS Lat: 0.000001",size=15, font="Times New Roman", color="#002e85")
    # lon = Text(app, text="GPS Lon: 0.0000001",size=15, font="Times New Roman", color="#002e85")
    # hdg = Text(app, text="GPS Hdg: 0.0000001",size=15, font="Times New Roman", color="#002e85")
    # init = PushButton(app, command=init, text="Init Data")
    # qual = PushButton(app, command=init, text="Start Qualification")

app.display()