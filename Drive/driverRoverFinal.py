'''
Code to drive the rover motors - to communicate to arduino (which drives the motors)
Authors: Nikhil Chandra BS, Rakshak
'''
import socket
from time import sleep
from smbus import SMBus
#import json
#import requests
#import sys

addr = 0x8 # bus address
bus = SMBus(0)



def readWrite():
    read =0
    b=0
    while True:
        moves,_ = s.recvfrom(1024)
        #move = b'1250,1500,1750,'
        #print(moves)
        moves = moves.decode("utf-8").split(',')[-15:-1]
        #print(moves)

        if read ==0:
            numbers = [int(i) for i in moves]
            print(numbers)
            numbers = [int(i/10) for i in numbers]
            bus.write_block_data(addr,6,numbers)
            #print("first print")
            b = b+1
            if(b==1):
                b=0
                read = 1
        elif read == 1:
            n=7
            currentValues= []
	    CurrentValues= []
            for i in range(n):
                currentValues.append(bus.read_byte_data(addr,200)*5)#4
	    #print("Agadu")
            #print(currentValues)
 	    index = currentValues.index(1020)
	
 	    CurrentValues = currentValues[index:] + currentValues[:index]
	    #CurrentValues.reverse()
	    #print("Evagnodu")
	    print(CurrentValues)

#            current_dict = {"CFL":currentValues[1],"CFR":currentValues[2],"CML":currentValues[3],"CMR":currentValues[4],"CBL":currentValues[5],"CBR":currentValues[6]}
#            string_current = json.dumps(current_dict)		
#	    r = requests.get("http://192.168.1.22:5000/retrieval/set_retrieval?json="+string_current)      
            read = 0

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the port on which you want to connect
port = 6589

# connect to the server on local computer
s.bind(('192.168.1.33', port))

while(True):
    try:
        readWrite()
    except Exception as e:
        print(e)
        #print("Print 2")
        #print('closing the socket')
        #s.close()
        #readWrite()
        pass
