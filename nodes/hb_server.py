import socket
import sys
import threading
import serial
import json
import subprocess

# Create a UDP socket
r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ("192.168.0.218", 8001)
r.bind(server_address)

while True:
    data, address = r.recvfrom(4096)
    s = subprocess.getstatusoutput(data)
    print(s)
