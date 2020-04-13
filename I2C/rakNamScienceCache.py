from smbus import SMBus
#import requests,json
 
addr = 0x8 # bus address
bus = SMBus(0) # indicates /dev/ic2-0
 
numb = 1
#power = 0
while True:
	try:
		while True:
			#data_string = requests.get("http://localhost:5000/send_values").text
			#power = json.loads(data_string)['power']	
			n=13
			cache = []
			scienceCache =[]
			for i in range(n):
			    cache.append(bus.read_byte_data(addr,200))
			print("Cache")
			print(cache)
			index = cache.index(123)
	
			scienceCache = cache[index:] + cache[:index]
			#scienceCache = cache[:index] + cache[index:]
			
			scienceCache.reverse()
			
			#science_dict = {'atmospheric_pressure':scienceCache[0],
			#'air_temperature':scienceCache[1],
			#'air_humidity':scienceCache[2],
			#'soil_temperature':scienceCache[3],
			#'soil_humidity':scienceCache[4],
			#'CO':scienceCache[5],
			#'CO2':scienceCache[6],
			#'CH4':scienceCache[7],
			#'phosphor':scienceCache[8],
			#'potassium':scienceCache[9],
			#'nitrogen':scienceCache[10],
			#'pH':scienceCache[11],
			#'elevation':scienceCache[12]}
	
			print("Science Cache")
			print(scienceCache)
#           string_science = json.dumps(science_dict)		
#	        r = requests.get("http://192.168.1.22:5000/science/set_science?json="+string_science) 
	except Exception as e:
		print(e)
		pass



