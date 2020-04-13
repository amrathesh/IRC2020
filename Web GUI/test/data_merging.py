import os,sys
from select import select

def merge_and_read():
	f = open("data.txt",'w')
	f.seek(0)
	f.write('')
	f.close()

	os.system("python3 Drive_system.py")
	os.system("python3 Science_cache.py")
	
	f = open("data.txt",'r')
	f.seek(0)
	data_string = '{'
	for string in f:
		data_string = data_string + string + ','
	_ = data_string.split()
	_[-1] = '}'
	data_string = ''.join(_)
	print(data_string)	
	
	
if __name__=="__main__":
	try:
		merge_and_read()
	except:
		sys.exit()	
