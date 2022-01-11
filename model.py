import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.autograd import Variable

class Classifier(nn.Module):
	def __init__(self):
		super().__init__()
		self.conv1 = nn.Conv2d(3, 6, 5)
		self.pool = nn.MaxPool2d(2, 2)
		self.conv2 = nn.Conv2d(6, 16, 5)
		self.fc1 = nn.Linear(16 * 4 * 4, 128)
		self.fc2 = nn.Linear(128, 64)
		self.fc3 = nn.Linear(64, 1)

	def forward(self, x):
		x = self.pool(F.relu(self.conv1(x)))
		x = self.pool(F.relu(self.conv2(x)))
		x = torch.flatten(x, 1) # flatten all dimensions except batch
		x = F.relu(self.fc1(x))
		x = F.relu(self.fc2(x))
		x = self.fc3(x)
		return x

	def load_checkpoint(self, checkpoint_path, model):
		state = torch.load(checkpoint_path, map_location = torch.device('cpu'))
		model.load_state_dict(state['state_dict'])
		print('model loaded from %s' % checkpoint_path)

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
	