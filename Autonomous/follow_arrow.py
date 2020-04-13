import cv2
import numpy as np
import imutils
import time
import gps_mag as  gpsxy
from smbus import SMBus
addr = 0x8 # bus address
bus = SMBus(0)

#############################################################################################
def turnLeft():
    #call api provided by drive system
    #print('turn left')
    
    x ,y,heading = gpsxy.gps_mag_data()
    if heading > 270:
    	final_angle = heading + 90 - 360
    	print('final angle',final_angle)
    	while(heading < 360 and heading > 270):
    		print('left')
    		num = [12,13,14]
    		#bus.write_block_data(addr,6,num)
    		x ,y,heading = gpsxy.gps_mag_data()
    	while(heading <=final_angle ):
    		print('left')
    		num = [12,13,14]
    		#bus.write_block_data(addr,6,num)
    		x ,y,heading = gpsxy.gps_mag_data()
    		if heading > final_angle:
    			break
    		
    else:
    	final_angle = heading+90
    	print('final angle',final_angle)
    	while(heading < final_angle):
    		print('left')
    		num = [12,13,14]
    		#bus.write_block_data(addr,6,num)
    		x ,y,heading = gpsxy.gps_mag_data()
    		if heading > final_angle:
    			break
    return
    #bus.write_block_data(addr,6,num)
    	
##############################################################################################
##############################################################################################
def turnRight():
    #call api provided by drive system
    #print('turn right')
    x ,y,heading = gpsxy.gps_mag_data()
    if heading < 90:
    	final_angle = heading - 90 + 360
    	print('final angle',final_angle)
    	while(heading > 0 and heading < 90):
    		print('right')
    		num = [12,13,14]
    		#bus.write_block_data(addr,6,num)
    		x ,y,heading = gpsxy.gps_mag_data()
    	heading = 360
    	while(heading > final_angle ):
    		print('right')
    		num = [12,13,14]
    		#bus.write_block_data(addr,6,num)
    		x ,y,heading = gpsxy.gps_mag_data()
    		if(heading < final_angle):
    			break
    else:
    	final_angle = heading-90
    print('final angle',final_angle)
    while(heading >= final_angle):
    	print('right')
    	num = [12,13,14]
    	#bus.write_block_data(addr,6,num)
    	x ,y,heading = gpsxy.gps_mag_data()
    	if heading < final_angle:
    		break
    		
    return
    
############################################################################################
#############################################################################################
def turnLeft():
    #call api provided by drive system
    #print('left')
    num = [1700,1400,1750]
    bus.write_block_data(addr,6,num)
    	
##############################################################################################
##############################################################################################
def turnRight():
    #call api provided by drive system
    #print('right')
    num = [1300,1400,1750]
    bus.write_block_data(addr,6,num)
############################################################################################
###########################################################################################
def moveforward():
    #call api provided by drive system
    print('forward')
    num = [1500,1400,1750]
    bus.write_block_data(addr,6,num)
###########################################################
###########################################################
def stopMoving():
    #call api provided by drive system
    print('stopped')
    num = [1500,1500,1500]
    #[1500,1400,1250]backward
    bus.write_block_data(addr,6,num)
###########################################################

def trigger():

	name1 = 'templateleft.jpg'
	name2 = 'templat0eright.jpg'

	template1 = cv2.imread(name1,0)
	face_w1, face_h1 = template1.shape[::-1]

	template2 = cv2.imread(name2,0)
	face_w2, face_h2 = template2.shape[::-1]

	cv2.namedWindow('image')

	cap = cv2.VideoCapture(1)

	threshold = 0.8
	ret = True
	flag = 0
	while ret :    
	
		ret, img = cap.read()
		img = imutils.resize(img, width=1000) 
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		res1 = cv2.matchTemplate(img_gray,template1,cv2.TM_CCOEFF_NORMED)
		threshold = 0.85
		
		if len(res1):
		
			location1 = np.where(res1 >= threshold)
			for pt in zip(*location1[::-1]):
				cv2.rectangle(img, pt, (pt[0] + face_w1, pt[1] + face_h1), (0,255,255), 2)
				print('left')
				ret, img = cap.read()
				turn
				ret, img = cap.read()
				flag = 1
				break
			
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		res2 = cv2.matchTemplate(img_gray,template2,cv2.TM_CCOEFF_NORMED)
		threshold2 = 0.75

		if len(res2):
			location2 = np.where(res2 >= threshold2)
			for pt in zip(*location2[::-1]):
				cv2.rectangle(img, pt, (pt[0] + face_w2, pt[1] + face_h2), (0,0,255), 2)
				print('right')
				ret, img = cap.read()
				turnRight()
				ret, img = cap.read()
				flag = 1
				break
		if flag !=1:
			print('forward')	
		if flag == 1 :
			flag=0
			
			
		cv2.imshow('image',img)
	
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break
	cv2.destroyAllWindows()
	
	
if __name__ == '__main__':
	forward=True
	while forward:
		trigger()
	#Left()
