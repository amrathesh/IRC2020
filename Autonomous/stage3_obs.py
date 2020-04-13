# coding: utf-8

import numpy as np
import cv2
import sys
import time
import gps_mag as  gpsxy
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel


########################################################################################
class Location(object):
    def __init__(self , latitude , longitude):
        self.latitude = latitude
        self.longitude = longitude
#############################################################################################
def findPosition():
    #get latitude and longitude from arduino
    a1 , b1 , c = gpsxy.gps_mag_data()
    a1 = conv.convert_gps(a1)
    b1 = conv.convert_gps(b1)
    pos = Location(a1 , b1)
    print (pos.latitude ,'  ', pos.longitude)
    return pos
#############################################################################################
##############################################################################################
def findBearing(LocA , LocB):
    dl = LocB.longitude - LocA.longitude
    x = math.cos(LocB.latitude) * math.sin(dl)
    y = math.cos(LocA.latitude) * math.sin(LocB.latitude) - math.sin(LocA.latitude) * math.cos(LocB.latitude) * math.cos(dl)
    bearing = math.atan2(x,y) * 180/math.pi
    if bearing > 0:
    	bearing  = 360 - math.abs(bearing)
    else:
    	bearing = math.abs(bearing)
    #bearing = 43.2
    return bearing
##############################################################################################
#############################################################################################
def findDistance(LocA, LocB):
	LocA.latitude = LocA.latitude*math.pi / 180
	LocA.longitude =LocA.longitude *math.pi / 180
	LocB.latitude =LocB.latitude *math.pi  / 180
	LocB.longitude =LocB.longitude *math.pi / 180
	dlat = LocA.latitude - LocB.latitude
	dl  = LocA.longitude - LocB.longitude
    a = math.sin(dlat/2)**2 + math.cos(LocA.latitude)*math.cos(LocB.latitude)*math.sin(dl/2)**2
    c = 2 * math.atan2(sqrt(a),sqrt(1-a))
    dist = 6371*c
    return dist
##############################################################################################
##############################################################################################
def findHeading():
    a, b , heading = gpsxy.gps_mag_data()
    print (heading)
    return heading
##############################################################################################
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
def main(lata , longa, latb,  longb):
	lata= float(lata)
	latb=float(latb)
	longa = float(longa)
	longb = float(longb)
	LocA = Location(lata,longa)
    LocB = Location(latb,longb)
    findPosition()
    #bearing gives the angle between the locB gps coordinate with the north axis
    distance = findDistance(LocA , LocB)
    
	try:
		from pylibfreenect2 import OpenGLPacketPipeline
		pipeline = OpenGLPacketPipeline()
	except:
		try:
		    from pylibfreenect2 import OpenCLPacketPipeline
		    pipeline = OpenCLPacketPipeline()
		except:
		    from pylibfreenect2 import CpuPacketPipeline
		    pipeline = CpuPacketPipeline()
	print("Packet pipeline:", type(pipeline).__name__)

	###############################################################


	# Create and set logger
	logger = createConsoleLogger(LoggerLevel.Debug)
	setGlobalLogger(logger)

	fn = Freenect2()
	num_devices = fn.enumerateDevices()
	if num_devices == 0:
		print("No device connected!")
		sys.exit(1)

	serial = fn.getDeviceSerialNumber(0)
	device = fn.openDevice(serial, pipeline=pipeline)

	listener = SyncMultiFrameListener(
		FrameType.Color | FrameType.Ir | FrameType.Depth)

	# Register listeners
	device.setColorFrameListener(listener)
	device.setIrAndDepthFrameListener(listener)

	device.start()

	# NOTE: must be called after device.start()
	registration = Registration(device.getIrCameraParams(),
		                        device.getColorCameraParams())

	undistorted = Frame(512, 424, 4)
	registered = Frame(512, 424, 4)

	# Optinal parameters for registration
	# set True if you need
	need_bigdepth = False
	need_color_depth_map = False

	bigdepth = Frame(1920, 1082, 4) if need_bigdepth else None
	color_depth_map = np.zeros((424, 512),  np.int32).ravel() \
		if need_color_depth_map else None
	flag = 1
	while True:
		if findDistance(findPosition(),locB) >=0.0015:
			bearing = findBearing(LocA , LocB)
   	    	heading = findHeading()
	    	#right	    	
		    	
		    while ( abs(heading -  bearing) > 7 ):
		    	if (bearing > 180) and (bearing <= 360):
					if ( heading > 0 and heading < (bearing-180)) or (heading > bearing and heading < 360):
						print("right")
						turnRight()
						print (heading)
						#time.sleep(0.5)
					else:
						print("Left")
						turnLeft()
						print (heading)
						#time.sleep(0.5)
			
				if (bearing >= 0) and (bearing <= 180):
					if ( heading > bearing and heading < (bearing+180)):
						print("right")
						turnRight()
						print (heading)
						#time.sleep(0.5)
					else:
						print("Left")
						turnLeft()
						print (heading)
						#time.sleep(0.5)
	    	moveForward()
			frames = listener.waitForNewFrame()
			depth = frames["depth"]
			registration.apply(depth,registered)
			cv2.imshow("depth", depth.asarray() / 4500.)
		
			#Comment the coming lines
			print('center value is:',depth.asarray(np.float32).item((212,256)))
			print('down1 value is:',depth.asarray(np.float32).item((270,256)))
			'''print('up1 value is:',depth.asarray(np.float32).item((150,256)))
			print('up2 value is:',depth.asarray(np.float32).item((100,256)))
		
			print('down2 value is:',depth.asarray(np.float32).item((350,256)))
			print('right1 value is:',depth.asarray(np.float32).item((212,300)))
			print('right2 value is:',depth.asarray(np.float32).item((212,350)))
			print('left1 value is:',depth.asarray(np.float32).item((212,200)))
			print('left2 value is:',depth.asarray(np.float32).item((212,150)))'''
		
		
			x = depth.asarray(np.float32)
			y = np.logical_and(np.greater(x, 1000) , np.less(x, 1200))
			#print(np.extract(y, x))
			no_of_pixels = np.count_nonzero(np.extract(y, x))
			print(no_of_pixels)		
			if no_of_pixels >  10000: #approx distance from the camera = 1.5 m
				print('big Obstacle found, stop!!!')
				flag  = 2
			if flag == 2:
				flag = 1
				turnRight()
				continue
			else:
				moveforward()
				 
			#cv2.imshow("color", cv2.resize(color.asarray(),(int(1920 / 3), int(1080 / 3))))
			#cv2.imshow("registered", registered.asarray(np.uint8))

		

			listener.release(frames)
			#time.sleep(20)
			key = cv2.waitKey(delay=1) & 0xFF
			if key == ord('q'):
				break
		
	device.stop()
	device.close()
	
		#sys.exit(1)
	
	
if __name__ == '__main__':
    #main (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
     #degminute.seconds in argument
    '''
    a = conv.convert_gps(arg[1])
    b = conv.convert_gps(arg[2])
    c = conv.convert_gps(arg[3])
    d = conv.convert_gps(arg[4])
    main(a,b,c,d)
    '''
    main (0, 0, 10, 10)
