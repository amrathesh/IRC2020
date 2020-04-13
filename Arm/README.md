# Arm control

The robotic arm which may be mounted on the rover is controlled by the help of GPIO pins which helps to control multiple servos with controls using a joystick

## Usage guidance

- arm\_for\_jetson.py is the arm code on the jetson or rpi side which is on the rover to control the arm based on the signals received through the socket which is bound accordingly. Change IP address of socket to reuse as specification permits. This enables control for the arm and to give the right amount of power as required. This code must be running on the rover for the arm to work as per communication from the base station.

- arm\_joystick\_side.py is the code on the base station laptop. The laptop is connected to the joystick and the signals are sent through a network socket. This code takes the input from joystick and translates it accordingly to send to Jetson or Rpi for control of the arm. This code must be running on the base station to transmit signals for control.

- test.py is just a test code to check for the arm's working.
