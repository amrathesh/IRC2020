# Autonomous task

The codes on this folder are the various codes around the autonomous task in IRC 2020

##  Stage 1

Stage 1 of autonomous task in IRC 2020 consisted of tracking for a tennis ball using cameras. Tennis ball was to be located and followed using GPS and adjusting direction of the rover. This complete code with bugs is there in auto_stage1.py. tennisbal1.py has the code for detection of tennis ball.

##  Stage 2

Stage 2 of autonomous task in IRC 2020 consisted of avoiding obstacles put in our way and maneuvering around it. This was implemented using an XBox Kinect RGB-D sensor along with dynamic path following and obstacle avoidance algorithm with inputs of final destinations. This complete code with bugs again is there in kinect\_code.py. dynamic.py implements the routing algorithm, along with a simulation. 

##  Stage 3

Stage 3 of autonomous task in IRC 2020 consisted of following arrow directions, which would say left or right accordingly. This was implemented purely using image processing and turning rover with help of magnetometer. This complete code with bugs is there in stage3_obs.py. The image processing code for following arrow is in follow\_arrow.py. 

##  Support codes

- conversion.py -- contains functions which help for transformation of gps coordinates input from sensor
- gps_mag.py -- constants functions which help retrieve data from the gps and magnetometer, along with error handling
- start.py -- starts the continous codes for the 3 stages by taking inputs of coordinates as arguments for the program to be used quickly

##  Caution

Most of the codes in this folder are buggy or need to be optimised. Please use with discretion. Thank you!
