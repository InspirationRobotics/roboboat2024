import socket
import time
import sys
import threading
import serial
import json
import pickle
from threading import Thread, Lock

mutex = Lock()

leftpower = 0
rightpower = 0
leftangle = 0
rightangle = 0

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
p = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ("192.168.1.5", 8000)
status_server_address = ("192.168.1.10", 10001)
s.bind(server_address)

power_changed = False

ser = serial.Serial('/dev/ttyS1', 115200)
srr = '00'
kill = '00'
changed = 0

def build_steering_msg(length, msg_type, port_pos, star_pos):
    checksum = 0
    build = bytes.fromhex('aa')
    build += bytes.fromhex('55') 
    build += length 
    #print(bytes(build).hex())
    checksum += int(length.hex(), 16) 
    #print(checksum)

    build +=  msg_type
    #print(bytes(build).hex())
    checksum += int(msg_type.hex(), 16)
    #print(checksum)

    build+=port_pos
    #print(bytes(build).hex())
    checksum = (checksum+ port_pos[0])%256
    checksum = (checksum+ port_pos[1])%256
    #print(checksum)

    build+=star_pos
    #print(bytes(build).hex())
    checksum = (checksum+ star_pos[0])%256
    checksum = (checksum+ star_pos[1])%256
    #print(checksum)

 
    build+= (checksum %256).to_bytes(1, "little")
    #print(bytes(build).hex())
    return build


def build_motor_status_cmd(length, msg_type):
    checksum = 0
    build = bytes.fromhex('aa')
    build += bytes.fromhex('55') 
    build += length 
    #print(bytes(build).hex())
    checksum += int(length.hex(), 16) 
    #print(checksum)

    build +=  msg_type
    #print(bytes(build).hex())
    checksum += int(msg_type.hex(), 16)
    #print(checksum)

    build+= (checksum %256).to_bytes(1, "little")
    #print(bytes(build).hex())
    return build


   
def build_thrust_msg(length, msg_type, leftpower_speed, le_stop, l_run, rightpower_speed, re_stop, r_run ):
    checksum = 0
    build = bytes.fromhex('aa')
    build += bytes.fromhex('55') 
    build += length 
    #print(bytes(build).hex())
    checksum += int(length.hex(), 16) 
    #print(checksum)

    build +=  msg_type
    #print(bytes(build).hex())
    checksum += int(msg_type.hex(), 16)
    #print(checksum)

    build+=leftpower_speed
    #print(bytes(build).hex())
    checksum = (checksum+ leftpower_speed[0])%256
    checksum = (checksum+ leftpower_speed[1])%256
    #print(checksum)

    build+=le_stop
    #print(bytes(build).hex())
    checksum += int(le_stop.hex(), 16)
    #print(checksum)

    build+=l_run
    #print(bytes(build).hex())
    checksum += int(l_run.hex(), 16)
    #print(checksum)

    build+=rightpower_speed
    #print(bytes(build).hex())
    checksum = (checksum+ rightpower_speed[0])%256
    checksum = (checksum+ rightpower_speed[1])%256
    #print(checksum)

    build+=re_stop
    #print(bytes(build).hex())
    checksum += int(re_stop.hex(), 16)
    #print(checksum)

    build+=r_run
    #print(bytes(build).hex())
    checksum += int(r_run.hex(), 16) 
    #print(checksum)
 
    build+= (checksum %256).to_bytes(1, "little")
    #print(bytes(build).hex())
    return build

def getStatus():

    global leftpower
    global rightpower
    global leftangle
    global rightangle
    global ser
    global srr
    global kill
    global p
    global changed
    global mutex
    while True:
            time.sleep(0.5)
                       
 # Read from serial
            resp = []
            while True:
                #mutex.acquire()
                if (ser.in_waiting >0): # Check if there are bytes in the buffer
                    byte1 = ser.read(1).hex()
                    if (byte1 == 'aa'): 
                        byte2 = ser.read(1).hex()
                        if (byte2 == '55'): 
                            byte3 = ser.read(1).hex()
                            byte4 = ser.read(1).hex()
                            #print(byte1)
                            #print(byte2)
                            if (byte1 == 'aa') and (byte2 == '55'): 
                                if (byte4 == '42'):
                                    byte = ser.read(1).hex()
                                    byte = ser.read(1).hex()
                                    byte = ser.read(1).hex()
                                    byte = ser.read(1).hex()
                                    byte = ser.read(1).hex()
                                    
                                    srr = ser.read(1).hex()
                                    ser.read(6).hex()
                                    print("Got SRR: " , srr)
                                    mutex.acquire()
                                    ser.write(build_motor_status_cmd(bytes.fromhex('01'), bytes.fromhex('02')))
                                    mutex.release()
                                if (byte4 == '02'):
                                    kill = ser.read(1).hex()
                                    ser.read(1).hex()
                                    break;

               # mutex.release()



def setThrust():
    global leftpower
    global rightpower
    global leftangle
    global rightangle
    global power_changed
    global ser
    global mutex
    while True:
            if(power_changed == True):
                power_changed = False
                mutex.acquire()
                ser.write(build_thrust_msg(bytes.fromhex('09'), bytes.fromhex('01'), leftpower.to_bytes(2, "little", signed=True), bytes.fromhex('00'), bytes.fromhex('01'), rightpower.to_bytes(2, "little", signed=True), bytes.fromhex('00'), bytes.fromhex('01')))

                ser.write(build_steering_msg(bytes.fromhex('05'), bytes.fromhex('11'), leftangle.to_bytes(2, "little", signed=True), rightangle.to_bytes(2, "little", signed=True)))
                mutex.release()
            time.sleep(0.01)


def sendStatus():
    global srr
    global kill
    global changed
    while True:
        time.sleep(1)
        #print("Sending status")
        #print(kill)
        msg = [srr, kill]
        print(msg)
        p.sendto(pickle.dumps(msg), status_server_address)
        
thread = threading.Thread(target=setThrust)
thread.start()

thread2 = threading.Thread(target=getStatus)
thread2.start()

thread3 = threading.Thread(target=sendStatus)
thread3.start()
while True:
        data, address = s.recvfrom(4096)
        command = data.decode('utf-8')
        command_json = json.loads(command, parse_int=int)
        leftpower = command_json['lp']
        rightpower = command_json['rp']
        leftangle = command_json['la']
        rightangle = command_json['ra']
        power_changed = True
    
        print("lp: "+str(command_json['lp']))
        print("rp: "+str(command_json['rp']))
        #leftpower = int(data.decode('utf-8')[:1])
        #rightpower = int(data.decode('utf-8')[1:])
