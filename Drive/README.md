#Drive system of the Rover

These 2 codes are the programs to control the rover from base station according to signals from the base station.

##Usage guidance

- driverRoverFinal.py is the code which takes care of driving the rover from base station. Signals to the receiver connected to the laptop is obtained from the controller which is sent to Jetson or Rpi through a socket. This socket data is taken and sent to arduino to drive the motors of the rover. This code is run on the base station. 
