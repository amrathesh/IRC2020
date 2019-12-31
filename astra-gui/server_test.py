import sys,time
import requests
import json

battery = 100
compass = -180
latitude = 13.0419608
longitude = 77.5046096

while(1):
	time.sleep(0.5)
	battery = (battery-1)%100
	compass = (compass+10)%360
	longitude = longitude-0.000052
	data = {"battery":battery,"compass":compass,"location":{"lat":latitude,"long":longitude}}
	print(f"Battery: {battery}\nCompass: {compass}\n")
	string_data = json.dumps(data)
	r = requests.get("http://"+sys.argv[1]+":5000/set_values?json="+string_data)
			
