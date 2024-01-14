import socket
import pickle
import time

IP = '192.168.1.10'
PORT = 10001
msg = ['command']
MSG = pickle.dumps(msg)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
while True:
	sock.sendto(MSG, (IP, PORT))
	time.sleep(0.1)
