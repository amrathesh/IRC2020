import os
import sys
#all data input should be  in format of degMin.seconds 
def gpsdegtoxy(deg, mins ,sec):
	x=deg+(float)(mins)/60+(float)(sec)/(3600*10000000)
	return x	

def main(sourcelat, sourcelong, ball1lat, ball1long , ball2lat, ball2long , arlat, arlong):
	command1 = 'python auto_stage1.py '+str(sourcelat)+' '+str(sourcelong)+' '+str(ball1lat)+' '+str(ball1long)
	os.system(command1)
	command2 ='sudo  python kinect_code.py '+str(ball1lat)+' '+str(ball1long)+' '+str(ball2lat)+' '+str(ball2long)
	#in kinect_code, make a call to dynamic with  obstacle array passed
	os.system(command2)
	command3 = 'python stage3_obs.py '+str(ball2lat)+' '+str(ball2long)+' '+str(arlat)+' '+str(arlong)
	os.system(command3)
	command4  = 'python follow_arrow.py'
	os.system(command4)	


if __name__ == '__main__':
	#sourcelat, sourcelong, ball1lat, ball1long , ball2lat, ball2long , arlat, arlong
	'''
	pass parameters after converting from degree-min-sec to gps format
	'''
	
	main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6] ,sys.argv[7] ,sys.argv[8])


