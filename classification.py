import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from image_segmentation import segmentation
from model import Classifier
from PIL import Image

def test(model, data):
	# set the model to the evaluation mode
	model.eval()
	
	data = data.unsqueeze(0)
	
	output = model(data)
	#pred = output.max(1, keepdim = True)[1] # get the index of the max log-probability
	
	return output
	return pred[0, 0].numpy()
	
def classify(model, transform, img_):
	word = segmentation(img_)
	num = 0
	for i,j in enumerate(word):
		# convert to RGB
		word_torch = cv2.cvtColor(word[1], cv2.COLOR_BGR2RGB)
		
		# conver to PIL
		word_torch = Image.fromarray(word_torch)
		
		# transform the image to torch tensor
		word_torch = transform(word_torch)
		
		# predict the number
		num *= 10
		num += test(model, word_torch)
	
	num /= 10
	
	return num
	
def classify_whole(model, transform, img_):
	# convert to RGB
	img_ = cv2.cvtColor(img_, cv2.COLOR_BGR2RGB)
	
	# conver to PIL
	img_ = Image.fromarray(img_)
	
	# transform the image to torch tensor
	img_ = transform(img_)
	
	num = test(model, img_)
	
	return num / 10

if __name__ == '__main__':
	
	# load digit classifier
	net = Classifier()
	path = "Classifier.pth"
	net.load_checkpoint(path, net)
	
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
	
	# read image
	img_ = cv2.imread('img/card9.jpg')  # 讀取圖片
	
	print(classify(net, test_transform, img_))