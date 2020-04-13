import sys,time
import requests
import json
from urllib.parse import parse_qs, urlparse

battery = 100
compass = -180
latitude = 13.0419608
longitude = 77.5046096


'''
	time.sleep(0.5)
	battery = (battery-1)%100
	compass = (compass+10)%360
	longitude = longitude-0.000052
	data = {"battery":battery,"compass":compass,"location":{"lat":latitude,"long":longitude}}
	print(f"Battery: {battery}\nCompass: {compass}\n")
	string_data = json.dumps(data)
	r1 = requests.get("http://localhost:5000/set_values?json="+string_data)
'''	
while(1):
    time.sleep(0.5) 
    data_string = requests.get("http://localhost:5000/send_values").text
    power = json.loads(data_string)['power']
    print(power)
			
