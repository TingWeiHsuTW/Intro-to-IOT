import requests
import time
from bs4 import BeautifulSoup

def get_predict_tide():
	# get current time
	localtime = time.localtime(time.time())

	# update the url with current time
	url = 'https://tide.twport.com.tw/maps/getSeaData/KL/501/1d/' + str(localtime.tm_year) + '/' + str(localtime.tm_mon) + '/' + str(localtime.tm_mday) + '/all/all'

	# create session
	session = requests.session()

	# get response
	response = session.post(url)

	# use soup to read the html
	soup = BeautifulSoup(response.text, "html.parser")

	# select the title "tabledata"
	items = soup.select('tabledata')

	for i in items:
		# get hh from "yyyy-mm-dd hh:mm:ss"
		hour = i.get('forecasttime').split(' ')[1].split(':')[0]
		
		# find the forecast tide of current hour 
		if int(hour) == localtime.tm_hour:
			return i.get('forecasttide')
			
if __name__ == '__main__':
	predict_tide = get_predict_tide()
	print(predict_tide)