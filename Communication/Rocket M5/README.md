# Rocket M5

Rocket M5 is the device which helps to communicate between the rover and the base station. The steps to setup the M5s is written below along with screenshots.

## STEPS TO SETUP COMMUNICATION FOR ROVER

#### Setup both routers IP addresses

1.	Reset both the rocket m5s.

2.	Always use the rocket m5s with the antennas connected. Do not power them without the antennas.

3.	Connect one rocket m5 to the base station pc

4.	Go to Chrome(browser). Go to 192.168.1.20 to access the airOS page.

5.	Username and password is “ubnt” by default. Retain them. (If country is asked, select India and then check the box at the bottom of the page)

6.	In the “wireless” tab, set the mode to “Access Point”.

7.	Set the SSID to “astraserver”.

8.	Click on “change” button at the bottom of the page.

9.	In the “network” tab: 
    `IP address: 192.168.1.21`
	`Netmask: 255.255.255.0`
	`Gateway IP: 192.168.1.1`
	
10.	Click on “change” button at the bottom of the page.

11.	Click on “Apply” at the top of the page.

12.	The airOS page cannot be accessed now.

13.	Go to the Ethernet settings in the base station pc.
    >Path: Control Panel – Network and Internet – Network connections – you can find Ethernet here

14.	Double click on “Ethernet” – go to “properties” – double click on “Internet Protocol Version 4 (TCP/IPv4)

15.	Fill the following in the window which pops up
    `IP address: 192.168.1.22`
	`Netmask: 255.255.255.0`
	`Gateway IP: 192.168.1.21`

16.	Now access the airOS page in the browser using 192.168.1.21

	
#### Now at the rover pc side:

1.	Go to Chrome(browser) in rover pc. Go to 192.168.1.20 to access the airOS page.

2.	Username and password is “ubnt” by default. Retain them. (If country is asked, select India and then check the box at the bottom of the page)

3.	In the “network” tab: 
    `IP address: 192.168.1.31`
	`Netmask: 255.255.255.0`
	`Gateway IP: 192.168.1.1`
	
4.	Click on “change” button at the bottom of the page.

5.	In the “wireless” tab, set the mode to “Station”.

6.	Click on “change” button at the bottom of the page.

7.	Click on “Apply” at the top of the page.

8.	The airOS page cannot be accessed now.

9.	Go to the Ethernet settings in the rover station pc.
    >Path: Control Panel – Network and Internet – Network connections – you can find Ethernet here
    
10.	Double click on “Ethernet” – go to “properties” – double click on “Internet Protocol Version 4 (TCP/IPv4) 

11.	Fill the following in the window which pops up
    `IP address: 192.168.1.32`
    `Netmask: 255.255.255.0`
    `Gateway IP: 192.168.1.31`
        
12.	Now access the airOS page in the browser using 192.168.1.31

13.	Keep the base station rocket m5 powered on (all connections with the pc to be intact)

14.	In the “wireless” tab, for the SSID field, click on “Select” and select “astraserver” which appears in the search results. Select it and click on “Lock to AP”.

15.	Click on “change” button at the bottom of the page.

16.	Click on “Apply” at the top of the page.


#### Now ping and check the connection:

1.	All the lights in both the rocket m5s have to be switched on now.

2.	From base station pc, ping rover rocket m5 and rover pc (192.168.1.31 and 192.168.1.32)

3.	From rover station pc, ping base station rocket m5 and base station pc (192.168.1.21 and 192.168.1.22)

4.	Check the IPs in wireless network watcher too on both rover pc and base station pc. (all 4 IPs should be displayed)
    >When we did, 192.168.1.31 was displayed and the same changed to 192.168.1.32 – this wasn’t a problem since ping worked.
    

#### Verification

Screenshots attached in the respective folders for the steps should confirm if you got it working right! 


#### Contact, if problems arise
Nikhil Chandra : `9964996766`
Amrathesh:  `8105962447`
