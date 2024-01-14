import socket
import sys
import threading
import serial
import json

leftpower = 0
rightpower = 0
leftangle = 0
rightangle = 0

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ("192.168.1.5", 8000)
s.bind(server_address)

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


def setThrust():
    global leftpower
    global rightpower
    global leftangle
    global rightangle
    with serial.Serial('/dev/ttyS1', 115200) as ser:
        while True:
            ser.write(build_thrust_msg(bytes.fromhex('09'), bytes.fromhex('01'), leftpower.to_bytes(2, "little", signed=True), bytes.fromhex('00'), bytes.fromhex('01'), rightpower.to_bytes(2, "little", signed=True), bytes.fromhex('00'), bytes.fromhex('01')))

            ser.write(build_steering_msg(bytes.fromhex('05'), bytes.fromhex('11'), leftangle.to_bytes(2, "little", signed=True), rightangle.to_bytes(2, "little", signed=True)))

thread = threading.Thread(target=setThrust)
thread.start()

while True:
    data, address = s.recvfrom(4096)
    command = data.decode('utf-8')
    command_json = json.loads(command, parse_int=int)
    leftpower = command_json['lp']
    rightpower = command_json['rp']
    leftangle = command_json['la']
    rightangle = command_json['ra']
    
    print("lp: "+str(command_json['lp']))
    print("rp: "+str(command_json['rp']))
    #leftpower = int(data.decode('utf-8')[:1])
    #rightpower = int(data.decode('utf-8')[1:])
