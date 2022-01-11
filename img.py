import cv2
import numpy as np
import time

cam = cv2.VideoCapture(0)

start_time = time.time()
while True:
	current_time = time.time()
	
	# read the client's name and addr	
	# get a frame from webcam
	ret, img = cam.read()
	
	# copy the frame image
	vis = img.copy()
	cv2.rectangle(vis, (int(vis.shape[1]/4), int(vis.shape[0]/4)), (int(3*vis.shape[1]/4), int(3*vis.shape[0]/4)), (0, 255, 0), 3)
	cv2.imshow('getCamera', vis)
	
	if current_time - start_time > 5:
		cv2.imshow('rectangle', vis[ int(vis.shape[0]/4):int(3*vis.shape[0]/4), int(vis.shape[1]/4):int(3*vis.shape[1]/4),:])
		start_time = current_time
		
	# if the key is pressed, break the loop
	if 0xFF == ord('q') & cv2.waitKey(1):
		break
	
cv2.destroyAllWindows()