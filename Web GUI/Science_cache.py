import sys,json,random,time,os

def write_science():
	sensorValues = [0,0,0]
	for i in range(3):
		sensorValues[i] = random.randint(20,35)
	sensor_dict = {"science":{"temperature":sensorValues[0],"humidity":sensorValues[1],"something":sensorValues[2]}}
	string_sensor = json.dumps(sensor_dict)
	f = open("data.txt",'a')
	f.write(string_sensor+"\n")
	f.close()	
	
if __name__=="__main__":
	try:
		write_science()
	except:
		sys.exit()	
