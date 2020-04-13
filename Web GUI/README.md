# Astra GUI

This is the web application which runs on a flask server to enable a smoother monitoring of the rover as the tasks are performed. 

##  Getting around

- templates folder contains the various HTML files that are used and run accordingly. 
- static folder contains the images, videos used. 
- The python files:
  - main.py runs the main flask server to do HTTP routing and the backend logic for it
  - Drive_system.py runs the drive system backend to send data from device to web page and back to device
  - Science_cache.py runs the science cache backend to send data from device to web page and back to device
- The files in the test folder may be ignored and are only for testing backend data flow.
