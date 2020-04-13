from smbus import SMBus
import sys,json,requests
 
addr = 0x8 # bus address
bus = SMBus(0) # indicates /dev/ic2-0
 
numb = 1

while True:
	try:
		while True:
			n=8
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
			'''
To Naman, 
	Put dictionary with name sensor_dict. Modify and give all in place of this comment
'''
			string_data = json.dumps(sensor_dict)
   		 	r = requests.get("http://"+sys.argv[1]"+:5000/science/set_science?json="+string_data)
			print("Science Cache")
			print(scienceCache)
	except Exception as e:
		print(e)
		pass

