import cv2
from matplotlib import pyplot as plt
## 根據每行和每列的黑色和白色畫素數進行圖片分割。

def segmentation(img_):
	# 1、讀取影像，並把影像轉換為灰度影像並顯示
	img_ = cv2.resize(img_, (256, 256))
	img_gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)  # 轉換了灰度化
	#cv2.imshow('gray', img_gray)  # 顯示圖片
	cv2.waitKey(0)

	# 2、將灰度影像二值化，設定閾值是100
	#img_thre = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
	ret, img_thre = cv2.threshold(img_gray, 125, 255, cv2.THRESH_BINARY_INV)
	#cv2.imshow('white_black image', img_thre)  # 顯示圖片
	cv2.waitKey(0)

	# 4、分割字元
	white = []  # 記錄每一列的白色畫素總和
	black = []  # ..........黑色.......
	height = img_thre.shape[0]
	width = img_thre.shape[1]
	white_max = 0
	black_max = 0
	# 計算每一列的黑白色畫素總和
	for i in range(width):
		s = 0  # 這一列白色總數
		t = 0  # 這一列黑色總數
		for j in range(height):
			if img_thre[j][i] == 255:
				s += 1
			if img_thre[j][i] == 0:
				t += 1
		white_max = max(white_max, s)
		black_max = max(black_max, t)
		white.append(s)
		black.append(t)
		# print(s)
		# print(t)

	arg = False  # False表示白底黑字；True表示黑底白字
	if black_max > white_max:
		arg = True

	# 分割影像
	def find_end(start_):
		end_ = start_ + 1
		for m in range(start_ + 1, width - 1):
			if (black[m] if arg else white[m]) > (0.85 * black_max if arg else 0.85 * white_max):  # 0.95這個引數請多調整，對應下面的0.05（針對畫素分佈調節）
				end_ = m
				break
		return end_

	n = 1
	start = 1
	end = 2
	word = []
	while n < width - 2:
		n += 1
		if (white[n] if arg else black[n]) > (0.15 * white_max if arg else 0.15 * black_max):
			# 上面這些判斷用來辨別是白底黑字還是黑底白字
			# 0.05這個引數請多調整，對應上面的0.95
			start = n
			end = find_end(start)
			n = end
			if end - start > 20:
				cj = img_[1:height, start:end]
				cj = cv2.resize(cj, (15, 30))
				word.append(cj)
	
	return word

if __name__ == '__main__':
	img_ = cv2.imread('img/card11.jpg')  # 讀取圖片
	
	word = segmentation(img_)
	print(len(word))
	
	for i,j in enumerate(word):
		plt.subplot(1,len(word),i+1)
		plt.imshow(word[i],cmap='gray')
		#cv2.imwrite(str(i)+'.png', word[i])
		
	plt.show()
