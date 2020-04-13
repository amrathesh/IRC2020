import sys,json,random,time,os,requests

sensorValues = [0,0,0,0,0,0,0,0,0,0,0]
while(1):
    time.sleep(0.5)
    for i in range(9):
	    sensorValues[i] = random.randint(1,13)
    sensor_dict = {"atmospheric_pressure":sensorValues[0],
                    "air_temperature":sensorValues[1],
                    "air_humidity":sensorValues[2],
                    "soil_temperature":sensorValues[3],
                    "soil_humidity":sensorValues[4],   
                    "nitrogen":sensorValues[6],
                    "phosphor":sensorValues[7],
                    "potassium":sensorValues[8]}
    if(sensorValues[5]<7):
        sensor_dict['gases'] = 'Low'
    else:
        sensor_dict['gases'] = 'High'                    
    string_data = json.dumps(sensor_dict)
    r = requests.get("http://localhost:5000/science/set_science?json="+string_data)               
