'''
Code for robotic ARM along with base rotation - rhino motor_clk
Authors: Nikhil Shetty, Nikhil Chandra BS, Amrathesh
'''
import socket
import Jetson.GPIO as GPIO
from time import sleep

actuator_1_control_pin_1 = 11#pin 11#162
actuator_1_control_pin_2 = 12#pin 12#11
actuator_2_control_pin_1 = 13#pin 13#38
actuator_2_control_pin_2 = 15#pin 15#511
actuator_3_control_pin_1 = 16#pin 16#37
actuator_3_control_pin_2 = 18#pin 18#184

stepper_motor_1_drive = 29#pin 29 #219#direction
stepper_motor_1_step = 31#pin 31#186
stepper_motor_1_enable = 33#pin 33#63

rhino_dir1 = 35#pin 35#8
rhino_p1 = 38#pin 38#9

motor_clk = 32#pin 32#36
motor_anti_clk = 40#pin 40#10

def init_rpi():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(actuator_1_control_pin_1, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(actuator_1_control_pin_2, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(actuator_2_control_pin_1, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(actuator_2_control_pin_2, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(actuator_3_control_pin_1, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(actuator_3_control_pin_2, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(stepper_motor_1_drive, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(stepper_motor_1_step, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(stepper_motor_1_enable, GPIO.OUT, initial = GPIO.HIGH)#MAKE IT HIGH
    GPIO.setup(rhino_dir1, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(rhino_p1, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(motor_clk, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(motor_anti_clk, GPIO.OUT, initial = GPIO.HIGH)
    
def actuator_moves(actuator_control_pin_1_number, actuator_control_pin_2_number, move_value):
    if move_value == '0':
        GPIO.output(actuator_control_pin_1_number, GPIO.HIGH)
        GPIO.output(actuator_control_pin_2_number, GPIO.HIGH)
    elif move_value == '1':
        GPIO.output(actuator_control_pin_1_number, GPIO.HIGH)
        GPIO.output(actuator_control_pin_2_number, GPIO.LOW)
    elif move_value == '-1':
        GPIO.output(actuator_control_pin_1_number, GPIO.LOW)
        GPIO.output(actuator_control_pin_2_number, GPIO.HIGH)

def stepper_moves(drive_pin_number, step_pin_number, enable_pin_number, move_value):
    if move_value == '0':
        GPIO.output(enable_pin_number, GPIO.HIGH)
    elif move_value == '1':
        GPIO.output(enable_pin_number, GPIO.LOW)
        GPIO.output(drive_pin_number, GPIO.HIGH)
        GPIO.output(step_pin_number, GPIO.LOW)
        sleep(0.001)
        GPIO.output(step_pin_number, GPIO.HIGH)
        sleep(0.001)
    elif move_value == '-1':
        GPIO.output(enable_pin_number, GPIO.LOW)
        GPIO.output(drive_pin_number, GPIO.LOW)
        GPIO.output(step_pin_number, GPIO.LOW)
        sleep(0.001)
        GPIO.output(step_pin_number, GPIO.HIGH)
        sleep(0.001)
        
def rhino_moves(rhino_dir1,rhino_p1,move_value):
    #a=0 #should come from joystick
    if(move_value == '0'):
        GPIO.output(rhino_p1, GPIO.LOW)
    elif(move_value == '1'):
        print("inside 1")
        GPIO.output(rhino_p1, GPIO.HIGH)
        sleep(0.00001)
        GPIO.output(rhino_p1, GPIO.LOW)
        sleep(0.00001)
        GPIO.output(rhino_dir1, GPIO.HIGH)
    elif(move_value == '-1'):
        print("inside -1")
        GPIO.output(rhino_p1, GPIO.HIGH)
        sleep(0.00001)
        GPIO.output(rhino_p1, GPIO.LOW)
        sleep(0.00001)
        GPIO.output(rhino_dir1, GPIO.LOW)


def arm(moves):
    actuator_moves(actuator_1_control_pin_1, actuator_1_control_pin_2, moves[0])
    actuator_moves(actuator_2_control_pin_1, actuator_2_control_pin_2, moves[1])
    actuator_moves(motor_clk, motor_anti_clk, moves[2])
    actuator_moves(actuator_3_control_pin_1, actuator_3_control_pin_2, moves[3])
    stepper_moves(stepper_motor_1_drive, stepper_motor_1_step, stepper_motor_1_enable, moves[4])
    rhino_moves(rhino_dir1,rhino_p1,moves[5])
    #stepper_moves(stepper_motor_2_drive, stepper_motor_2_step, stepper_motor_2_enable, moves[5])
    


if __name__=='__main__':
    init_rpi()
    
    # Create a socket object 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Define the port on which you want to connect 
    port = 6599
    
    # connect to the server on local computer 
    s.bind(('192.168.1.32', port)) 
    
    # receive data from the server
    print('going into try catch block')
    try:
        while True:
            # .decode("utf-8").split(',')[-8:-1]
            moves,_ = s.recvfrom(1024)
            moves = moves.decode("utf-8").split(',')[-8:-1]
            print(moves)
            arm(moves)
    except Exception as e:
        print(e)
    print('closing the socket')
    # close the connection 
    s.close()


