from smbus import SMBus
 
addr = 0x8 # bus address
bus = SMBus(0) # indicates /dev/ic2-0

n=1
a = []
for i in range(n):
    a.append(bus.read_byte_data(addr,200))
print(a)
