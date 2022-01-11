import numpy as np

# ref: https://silverwind1982.pixnet.net/blog/post/167680859
class Kalman:
	def __init__(self, X, P, F, Q, H, R, I, B):
		# X: estimate value
		# P: covariance of estimate value
		# F: state change matrix
		# Q: state change model covariance(noise)
		# H: measurement change matrix
		# R: measurement model covariance(noise)
		# I: identity matrix
		# K: Kalman gain
		# B: input state change matrix
		# U: input of the state
		self.X = X
		self.P = P
		self.F = F
		self.Q = Q
		self.H = H
		self.R = R
		self.I = I
		self.K = 0
		self.B = B
		
	def calculate(self, X, U, Z):
		# Z: measurement
		self.X = self.F * X + self.B * U
		self.P = self.P + self.Q
		self.K = self.P / (self.P + self.R)
		self.X = self.X + self.K * (Z - self.H * self.X)
		self.P = (self.I - self.K) * self.P
		return self.X
		
if __name__ == '__main__':
	kalman = Kalman(X = 0, P = 3, F = 1, Q = 4, H = 1, R = 4, I = 1, B = 0)
	X = 0
	for i in range(100):
		z = 19 + np.random.random() % 201 / 100
		X = kalman.calculate(X, 0, z)
		print(X)