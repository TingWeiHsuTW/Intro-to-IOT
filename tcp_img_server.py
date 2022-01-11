import cv2
import imutils
import pickle
import struct
import socket
import time
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from classification import classify, classify_whole, test
from crawler import get_predict_tide
from image_segmentation import segmentation
from kalman import Kalman
from model import Classifier
from PIL import Image

# reference https://www.jianshu.com/p/913b2013a38f
# global server proxy https://dashboard.ngrok.com/get-started/your-authtoken
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#host_name  = socket.gethostname()
#host_ip = socket.gethostbyname(host_name)
host_ip = '192.168.137.1'
print('HOST IP:',host_ip)

port = 10050
socket_address = (host_ip,port)
print('Socket created')

# bind the socket to the host. 
#The values passed to bind() depend on the address family of the socket
server_socket.bind(socket_address)
print('Socket bind complete')

#listen() enables a server to accept() connections
#listen() has a backlog parameter. 
#It specifies the number of unaccepted connections that the system will allow before refusing new connections.
server_socket.listen(5)
print('Socket now listening')

#'b' or 'B'produces an instance of the bytes type instead of the str type
#used in handling binary data from network connections
data = b""
# Q: unsigned long long integer(8 bytes)
payload_size = struct.calcsize("Q")

# load the ML model
def load_checkpoint(checkpoint_path, model):
	state = torch.load(checkpoint_path, map_location = torch.device('cpu'))
	model.load_state_dict(state['state_dict'])
	print('model loaded from %s' % checkpoint_path)

# load digit classifier
#net = Classifier()
path = "train_best.pth"
#net.load_checkpoint(path, net)
net = torchvision.models.resnet50(pretrained = False)
net.fc = nn.Sequential(
	nn.Linear(2048, 64),
	nn.ReLU(),
	nn.Linear(64, 1),
)
load_checkpoint(path, net)

# GPU enable
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
print('Device used:', device)
net = net.to(device)
print(net)

test_transform = transforms.Compose([
	transforms.Resize([28, 28]),
	transforms.ToTensor(),
	transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
])

# Kalman filter
kalman = Kalman(X = 0, P = 3, F = 1, Q = 4, H = 1, R = 20, I = 1, B = 0)

while True:
	# accept the client
	client_socket,addr = server_socket.accept()
	print('Connection from:',addr)
	
	if client_socket:
		
		# get current time
		localtime = time.localtime(time.time())
		previous_hour = localtime.tm_hour
		
		# get the predict from the database
		predict_num = float(get_predict_tide())
		
		while True:
			# get current time
			localtime = time.localtime(time.time())
		
			# receive frame
			while len(data) < payload_size:
				packet = client_socket.recv(4*1024)
				if not packet: break
				data+=packet
			packed_msg_size = data[:payload_size]
			data = data[payload_size:]
			msg_size = struct.unpack("Q",packed_msg_size)[0]
			while len(data) < msg_size:
				data += client_socket.recv(4*1024)
			frame_data = data[:msg_size]
			data  = data[msg_size:]
			frame = pickle.loads(frame_data)
			
			# pass the frame to the model to get the predict number
			measure_num = float(classify_whole(net, test_transform, frame).item())
			
			GPS = [-1, -1]
			
			# pass one hour, get the prediction of the next hour
			if localtime.tm_hour != previous_hour:
				predict_num = get_predict_tide()
				previous_hour = localtime.tm_hour
			
			# calculate the optimize prediction from kalman filter
			opt_num = float(kalman.calculate(predict_num, 0, measure_num))
			
			print(f'predict: {predict_num}\tmeasure: {measure_num}, optimize: {opt_num}, GPS Pos: ({GPS[0]}, {GPS[1]})')
			
			# send the predict number back
			message = struct.pack("f", opt_num)
			client_socket.sendall(message)
			
			key = cv2.waitKey(10) 
			if key ==13:
				client_socket.close()