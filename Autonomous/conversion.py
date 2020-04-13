import math
from time import sleep
import struct
import argparse

def gpsdegtoxy(deg, mins ,sec):
	x=deg+(float)(mins)/60+(float)(sec)/(3600*10000000)
	return x
		
def get_degree_gps(data):
			a = data
			ad = (int)(a) / 100
			am = (int)(a) % 100
			t = a
			tl = t-(int)(a)
			asec=((int)(tl*1000000000))
			u_lat = gpsdegtoxy(ad,am,asec)
			     
			
			print(a)
			print(u_lat)
			
			print("lat degree: "+str(ad)+" min "+str(am))
			return ad,am,asec 
			
def convert_gps(data):
			a = data
			ad = (int)(a) / 100
			am = (int)(a) % 100
			t = a
			tl = t-(int)(a)
			asec=((int)(tl*1000000000))
			u_lat = gpsdegtoxy(ad,am,asec)
			     
			
			print(a)
			print(u_lat)
			
			print("lat degree: "+str(ad)+" min "+str(am))
			return  u_lat
			
	
if __name__ == '__main__':
	lat1 = convert_gps( arg[1])
	lon1  = convert_gps(arg[2])
	lat2 = convert_gps( arg[3])
	lon2  = convert_gps(arg[4])
	
	
		
