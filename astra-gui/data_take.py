import sys,json

def read_data():
	f = open("data.txt",'r+')
	data_string = "{"
	for i in f:
		data_string = data_string+i+','
	data_string  = data_string+'}'	
	print(data_string)
	f.close()

if __name__=="__main__":
		read_data()
				
