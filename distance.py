from geopy.geocoders import GoogleV3
import requests
import math
import vincenty
import time
import datetime
from functools import reduce
def calDistance(address):
	freeip = "http://freegeoip.net/json"
	geo = requests.get(freeip)
	geo_json = geo.json()

	geolocator = GoogleV3()
	loc = geolocator.geocode(address)
	lat = loc.latitude
	lon = loc.longitude
	org = (lat, lon)

	user_position = (geo_json["latitude"], geo_json["longitude"])
	distance = vincenty.vincenty(org, user_position, miles=True)
	return distance

def operation(start, end, current):
	#today = datetime.date.today()
	start_time = datetime.time(start[0], start[1])
	end_time = datetime.time(end[0], end[1])
	temp_current = current.time()
	if start_time < temp_current and end_time > temp_current:
		return True
		#end_time = datetime.datetime.combine(today, end_time)
		#time_left = ((end_time - current).seconds)/3600
def sort(organization):
	first_sort = sorted(organization, key = lambda i: i[1], reverse = True)
	num = 0
	compare = first_sort[0]
	frequence = [0 for i in first_sort]
	for i in first_sort:
		if i[1] == compare[1]:
			frequence[num] += 1
		else:
			compare = i
			num += 1
			frequence[num] += 1
	count = list(filter(lambda x: x > 0, frequence))
	second_sort = []
	start = 0
	for j in count:
		end = start + j
		second_sort.append(first_sort[start:end])
		start = end
	for k in range(len(second_sort)):
		second_sort[k] = sorted(second_sort[k], key = lambda i: i[2])
	result = reduce((lambda x, y: x + y), second_sort)
	return result






if __name__ == "__main__":
	a = calDistance("655 Village Square Dr, Stone Mountain, GA 30083")
	print (a)