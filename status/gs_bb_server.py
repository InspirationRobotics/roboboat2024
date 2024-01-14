import socket
import pickle
import serial
import threading
import json
import serial
import time

lstat = 0
ip = '192.168.1.10'
port = 10001

bb_adr = '192.168.1.5'
gs_adr = '192.168.1.117'

buf_size = 64
Sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
Sock.bind((ip, port))

ser = serial.Serial('/dev/ttyACM4', 9600)

lstat = 0
last = 0

while(True):
    #ser.write(b'1\n')
    bytes_address = Sock.recvfrom(buf_size)
    msg = bytes_address[0]
    adr = bytes_address[1]

    print(adr[0])
    
    msg = pickle.loads(msg)
    print(msg)
    
    if adr[0] == bb_adr:
        if str(msg[0]) == '11':
            lstat = b'3\n'
            
        elif (str(msg[0]) == '00'):
            lstat = b'2\n'

        if str(msg[1]) == '01':
            lstat = b'1\n'

    #if (lstat != last):
    #    ser.write(lstat)

    ser.write(lstat)
    #last = lstat

    while (ser.in_waiting > 0):
        ser.read()
