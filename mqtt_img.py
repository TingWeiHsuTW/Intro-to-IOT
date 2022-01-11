import base64
import cv2
import json
import paho.mqtt.client as mqtt
import time

cam = cv2.VideoCapture(0)
host = '127.0.0.1'

client = mqtt.Client()
client.connect(host, 1883, 60)

while True:
		# get a frame from webcam
		ret, img = cam.read()
		
		# copy the frame image
		vis = img.copy()
		#cv2.imshow('getCamera', vis)
		
		# convert the image to base64 form
		jpg_as_text = base64.b64encode(vis)
		
		# publish the image
		client.publish("images", jpg_as_text)
		print('publish a frame')
		
		time.sleep(1)
		
		# if the key is pressed, break the loop
		if 0xFF == ord('q') & cv2.waitKey(1):
			break
