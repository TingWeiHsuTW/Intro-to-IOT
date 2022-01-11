import cv2
import glob
import imutils
import pickle
import random
import socket
import struct
import time

# Client socket
# create an INET, STREAMing socket : 
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.137.1'# Standard loopback interface address (localhost)
port = 10050 # Port to listen on (non-privileged ports are > 1023)

# now connect to the web server on the specified port number
client_socket.connect((host_ip,port)) 

#'b' or 'B'produces an instance of the bytes type instead of the str type
#used in handling binary data from network connections
data = b""

# Q: unsigned long long integer(8 bytes)
payload_size = struct.calcsize("Q")
	
vid = cv2.VideoCapture(0)

start_time = time.time()

while True:
	# current time
	current_time = time.time()

	# read frame
	img,frame = vid.read()
	cv2.rectangle(frame, (int(frame.shape[1]/4), int(frame.shape[0]/4)), (int(3*frame.shape[1]/4), int(3*frame.shape[0]/4)), (0, 255, 0), 3)
	cv2.imshow('Camera',frame)
	
	if current_time - start_time > 5:
		frame = frame[ int(frame.shape[0]/4):int(3*frame.shape[0]/4), int(frame.shape[1]/4):int(3*frame.shape[1]/4),:]
		cv2.imshow('Crop',frame)
		
		# send frame
		a = pickle.dumps(frame)
		message = struct.pack("Q",len(a))+a
		client_socket.sendall(message)
		
		# receive the predict number
		packet = client_socket.recv(4)
		num = struct.unpack("f", packet)
		print(f'predict number: {num[0]:.1f}')
		
		start_time = current_time
	
	key = cv2.waitKey(10) 
	if key  == 13:
		break
client_socket.close()