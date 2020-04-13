from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=1,
	help="max buffer size")
args = vars(ap.parse_args())

#greenLower = (25, 75, 85)
#greenUpper = (50, 220, 255)
greenLower = (30, 70, 80)
greenUpper = (80,200 ,255 )

pts = deque(maxlen=args["buffer"])

vs = VideoStream(src=1).start() #reference to the webcam

 
time.sleep(2.0)# allow the camera or video file to warm up

while True:
	
	frame = vs.read()
 
	if frame is None:
		break
	
	frame = imutils.resize(frame, width=1000)     # resize the frame, blur it, and convert it to the HSV color space
	blurred = cv2.GaussianBlur(frame, (15, 15), 0)

	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
 
	mask = cv2.inRange(hsv, greenLower, greenUpper)

	cv2.imshow("msk", mask)
	
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
 
	if len(cnts) > 0:        # only proceed if at least one contour was found
		
		c = max(cnts, key=cv2.contourArea)     # only proceed if the radius meets a minimum size
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		
		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
	 #to draw the connecting line between two positions (have not used this that much)
	pts.appendleft(center)
	
	for i in range(1, len(pts)):
		if pts[i - 1] is None or pts[i] is None:
			continue

		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):           # if the 'q' key is pressed, stop the loop
		break


else:
	vs.release()

cv2.destroyAllWindows()
	
	
	

