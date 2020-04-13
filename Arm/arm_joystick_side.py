'''
code to take input from joystick and transmit them to the rover
Authors : Nikhil Shetty, Nikhil Chandra BS, Amrathesh
'''
# first of all import the socket library
import socket
from time import sleep
#import time

import pygame
from pprint import pprint

def logitech_3d_controller():

    moves = {'vertical':0, 'horizontal':0, 'rotate':0, 'throttle':0, 'base' : 0, 'wrist' : 0, 'grip' : 0}
    convert = {1:'vertical', 0:'horizontal', 2:'rotate', 3:'throttle'}

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTI
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        name = joystick.get_name()
        axes = joystick.get_numaxes()
        # print(screen, "Number of axes: {}".format(axes) )
        for i in range( axes ):
            axis = joystick.get_axis( i )
            # print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
            moves[convert[i]] = axis

        # buttons 2 & 3 are for base motor
        if(joystick.get_button(6) == 1):
            moves['base'] = 1
        elif(joystick.get_button(7) == 1):
            moves['base'] = -1
        else:
            moves['base'] = 0

        # buttons 4 & 5 are for wrist motor
        if(joystick.get_button(10) == 1):
            moves['wrist'] = 1
        elif(joystick.get_button(11) == 1):
            moves['wrist'] = -1
        else:
            moves['wrist'] = 0

        # buttons 6 & 7 for grip motor
        if(joystick.get_button(8) == 1):
            moves['grip'] = 1
        elif(joystick.get_button(9) == 1):
            moves['grip'] = -1
        else:
            moves['grip'] = 0

    return moves

def parse_data(moves):
    str_data = ""

    # pprint(moves)

    if(moves['vertical'] < -0.5):
        str_data += "1"
    elif(moves['vertical'] > 0.5):
        str_data += "-1"
    else:
        str_data += "0"

    str_data += ","

    if(moves['horizontal'] < -0.5):
        str_data += "1"
    elif(moves['horizontal'] > 0.5):
        str_data += "-1"
    else:
        str_data += "0"

    str_data += ","

    # str_data += str(moves['rotate'])

    if(moves['rotate'] > 0.5):
        str_data += "1"
    elif(moves['rotate'] < -0.5):
        str_data += "-1"
    else:
        str_data += "0"

    str_data += ","

    if(moves['throttle'] > 0.5):
        str_data += "1"
    elif(moves['throttle'] < -0.5):
        str_data += "-1"
    else:
        str_data += "0"

    str_data += ","

    if(moves['base'] > 0.5):
        str_data += "1"
    elif(moves['base'] < -0.5):
        str_data += "-1"
    else:
        str_data += "0"

    str_data += ","

    if(moves['wrist'] > 0.5):
        str_data += "1"
    elif(moves['wrist'] < -0.5):
        str_data += "-1"
    else:
        str_data += "0"

    str_data += ","

    if(moves['grip'] > 0.5):
        str_data += "1"
    elif(moves['grip'] < -0.5):
        str_data += "-1"
    else:
        str_data += "0"

    str_data += ","

    return str_data

pygame.init()

screen = "1:"

clock = pygame.time.Clock()
pygame.joystick.init()# print(GPIO.RPI_INFO)

# next create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 6599 #all the programs use this, change the ports

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
addr = ('192.168.1.32', port)
#s.bind(addr)
print("socket binded to %s" %(port))

# put the socket into listening mode
#s.listen(5)
print ("socket is listening")

#c, addr = s.accept()

# a forever loop until we interrupt it or
# an error occurs
while True:

   # Establish connection with client.

   # print(c, addr)
   # print('Got connection from', addr )

   # send a thank you message to the client.

    moves = {}
    moves = logitech_3d_controller()

    # pprint(moves)

    data_parsed = parse_data(moves).encode()

    #pprint(data_parsed)#previously printed
    #print(data_parsed)
    #print(data_parsed[-8:-1])

    s.sendto(data_parsed,addr)
    #c.send(data_parsed)
    #pprint(data_parsed[8])
    moves_here = data_parsed.decode("utf-8").split(',')[-8:-1] #moves_here is 'str'
    print(moves_here)
    if(moves_here[4] == '1'):#1
        print("inside stepper 1")
        sleep(0.002)
    if(moves_here[4] == '-1'):#1
        print("inside stepper -1")
        sleep(0.002)
    if(moves_here[5] == '1'):#1
        print("inside rhino 1")
        sleep(0.0002)
    if(moves_here[5] == '-1'):#1
        print("inside rhino -1")
        sleep(0.0002)

# Close the connection with the client
s.close()
#b'0,0,0,0,0,0,0,'
