from smbus import SMBus
 
addr = 0x8 # bus address
bus = SMBus(0) # indicates /dev/ic2-0
 
numb = 1
 
while numb == 1:
    
    read = input("Read madthya write ah? ");
    if read == 0:
        #commands = input(">>>>   ")
        #numbers = [int(i) for i in list(commands.split(" "))]
        num = [12,13,14]
        bus.write_block_data(addr,6,num)
    elif read == 1:
        n=3
        a = []
        for i in range(n):
            a.append(bus.read_byte_data(addr,200))
        print(a)
        
    else:
        numb = 0
