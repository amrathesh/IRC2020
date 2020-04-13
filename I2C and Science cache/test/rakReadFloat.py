import struct
from smbus import SMBus
import time
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus1 = SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

def get_data():
    return bus1.read_i2c_block_data(address, 0);

def get_float(data, index):
    bytes = data[4*index:(index+1)*4]
    return struct.unpack('f', "".join(map(chr, bytes)))[0]


while True:
    try:

	data = get_data()
        a = (get_float(data, 0))
        data = get_data()
        b=(get_float(data, 0))
	

	#index = a.index(3)
	
	#A = a[index:] + a[:index]
	#A.reverse()
        print(a,b)
    except Exception as e:
	print(e)
        pass

