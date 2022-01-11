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
host_ip = '127.0.0.1'# Standard loopback interface address (localhost)
port = 10050 # Port to listen on (non-privileged ports are > 1023)

# now connect to the web server on the specified port number
client_socket.connect((host_ip,port)) 

#'b' or 'B'produces an instance of the bytes type instead of the str type
#used in handling binary data from network connections
data = b""

# Q: unsigned long long integer(8 bytes)
payload_size = struct.calcsize("Q")
	
#vid = cv2.VideoCapture(0)
file_name = glob.glob('training_img2/*')#['img/card7.jpg', 'img/card8.jpg', 'img/card9.jpg', 'img/card10.jpg', 'img/card11.jpg']

while True:
	# read frame
	i = random.randint(0, len(file_name) - 1)
	frame = cv2.imread(file_name[i])
	frame = cv2.resize(frame, (256, 256))
	cv2.imshow('Sending...',frame)
	time.sleep(3)
	
	# send frame
	a = pickle.dumps(frame)
	message = struct.pack("Q",len(a))+a
	client_socket.sendall(message)
	
	# receive the predict number
	packet = client_socket.recv(4)
	num = struct.unpack("f", packet)
	print(f'predict number: {num[0]:.1f}')
	
	time.sleep(2)
	
	key = cv2.waitKey(10) 
	if key  == 13:
		break
client_socket.close()