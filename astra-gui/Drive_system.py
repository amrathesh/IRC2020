import sys,json,random,time,os

def write_drive():
	currentValues = [0,0,0,0,0,0]
	for i in range(6):
		currentValues[i] = random.randint(4,8)
	current_dict = {"drive_system":{"CFL":currentValues[0],"CFR":currentValues[1],"CML":currentValues[2],"CMR":currentValues[3],"CBL":currentValues[4],"CBR":currentValues[5]}}
	string_current = json.dumps(current_dict)
	f = open("data.txt",'a')
	f.write(string_current+"\n")
	f.close()
	
if __name__=="__main__":
	try:
		write_drive()
	except:
		sys.exit()	
