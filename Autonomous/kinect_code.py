# coding: utf-8

import numpy as np
import cv2
import sys
import time
import gps_mag as  gpsxy
import math
from enum import Enum
import matplotlib.pyplot as plt
import conversion as conv
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel
from smbus import SMBus
import gps_mag as  gpsxy
addr = 0x8 # bus address
bus = SMBus(0)
obs = []
########################################################################################
class Location(object):
    def __init__(self , latitude , longitude):
        self.latitude = latitude
        self.longitude = longitude
#############################################################################################
def findPosition():
    
    #get latitude and longitude from arduino
    a1 , b1 , c = gpsxy.gps_mag_data()
    pos = np.array([a1 , b1])
    print (pos.latitude ,'  ', pos.longitude)
    return pos
#############################################################################################
#############################################################################################
def turnLeft():
    #call api provided by drive system
    #print('left')
    num = [1700,1400,1750]
    bus.write_block_data(addr,6,num)
    	
##############################################################################################
##############################################################################################
def turnRight():
    #call api provided by drive system
    #print('right')
    num = [1300,1400,1750]
    bus.write_block_data(addr,6,num)
############################################################################################
###########################################################################################
def moveforward():
    #call api provided by drive system
    print('forward')
    num = [1500,1400,1750]
    bus.write_block_data(addr,6,num)
###########################################################
###########################################################
def stopMoving():
    #call api provided by drive system
    print('stopped')
    num = [1500,1500,1500]
    #[1500,1400,1250]backward
    bus.write_block_data(addr,6,num)
###########################################################
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


def create_obs( obstacles):
    ob = obstacles
    return ob

def dwa_control(x, config, goal, ob):
    """
    Dynamic Window Approach control
    """

    dw = calc_dynamic_window(x, config)

    u, trajectory = calc_final_input(x, dw, config, goal, ob)

    return u, trajectory


class RobotType(Enum):
    circle = 0
    rectangle = 1


class Config:
    """
    simulation parameter class
    """

    def __init__(self):
        # robot parameter
        self.max_speed = 1.0  # [m/s]
        self.min_speed = -0.5  # [m/s]
        self.max_yawrate = 40.0 * math.pi / 180.0  # [rad/s]
        self.max_accel = 0.2  # [m/ss]
        self.max_dyawrate = 40.0 * math.pi / 180.0  # [rad/ss]
        self.v_reso = 0.01  # [m/s]
        self.yawrate_reso = 0.1 * math.pi / 180.0  # [rad/s]
        self.dt = 0.1 # [s] Time tick for motion prediction
        self.predict_time = 3.0  # [s]
        self.to_goal_cost_gain = 0.15
        self.speed_cost_gain = 1.0
        self.obstacle_cost_gain = 1.0
        self.robot_type = RobotType.rectangle

        # if robot_type == RobotType.circle
        # Also used to check if goal is reached in both types
        self.robot_radius = 1.5  # [m] for collision check

        # if robot_type == RobotType.rectangle
        self.robot_width = 0.5  # [m] for collision check
        self.robot_length = 1.2  # [m] for collision check

    @property
    def robot_type(self):
        return self._robot_type

    @robot_type.setter
    def robot_type(self, value):
        if not isinstance(value, RobotType):
            raise TypeError("robot_type must be an instance of RobotType")
        self._robot_type = value


def motion(x, u, dt):
    """
    motion model
    """

    x[2] += u[1] * dt
    x[0] += u[0] * math.cos(x[2]) * dt
    x[1] += u[0] * math.sin(x[2]) * dt
    x[3] = u[0]
    x[4] = u[1]

    return x


def calc_dynamic_window(x, config):
    """
    calculation dynamic window based on current state x
    """

    # Dynamic window from robot specification
    Vs = [config.min_speed, config.max_speed,
          -config.max_yawrate, config.max_yawrate]

    # Dynamic window from motion model
    Vd = [x[3] - config.max_accel * config.dt,
          x[3] + config.max_accel * config.dt,
          x[4] - config.max_dyawrate * config.dt,
          x[4] + config.max_dyawrate * config.dt]

    #  [vmin,vmax, yaw_rate min, yaw_rate max]
    dw = [max(Vs[0], Vd[0]), min(Vs[1], Vd[1]),
          max(Vs[2], Vd[2]), min(Vs[3], Vd[3])]

    return dw


def predict_trajectory(x_init, v, y, config):
    """
    predict trajectory with an input
    """

    x = np.array(x_init)
    traj = np.array(x)
    time = 0
    while time <= config.predict_time:
        x = motion(x, [v, y], config.dt)
        traj = np.vstack((traj, x))
        time += config.dt

    return traj


def calc_final_input(x, dw, config, goal, ob):
    """
    calculation final input with dynamic window
    """

    x_init = x[:]
    min_cost = float("inf")
    best_u = [0.0, 0.0]
    best_trajectory = np.array([x])

    # evaluate all trajectory with sampled input in dynamic window
    for v in np.arange(dw[0], dw[1], config.v_reso):
        for y in np.arange(dw[2], dw[3], config.yawrate_reso):

            trajectory = predict_trajectory(x_init, v, y, config)

            # calc cost
            to_goal_cost = config.to_goal_cost_gain * calc_to_goal_cost(trajectory, goal)
            speed_cost = config.speed_cost_gain * (config.max_speed - trajectory[-1, 3])
            ob_cost = config.obstacle_cost_gain * calc_obstacle_cost(trajectory, ob, config)

            final_cost = to_goal_cost + speed_cost + ob_cost

            # search minimum trajectory
            if min_cost >= final_cost:
                min_cost = final_cost
                best_u = [v, y]
                best_trajectory = trajectory
    
    print (best_u)
    if (abs(y)<=0.15):
        print ("forward")
        moveForward()
    if (abs(y)>0.15):
        if (y>0):
            print ("turn left")
            turnLeft()
        else:
            print ("turn right")
            turnRight()
    return best_u, best_trajectory


def calc_obstacle_cost(trajectory, ob, config):
    """
        calc obstacle cost inf: collision
    """
    ox = ob[:, 0]
    oy = ob[:, 1]
    dx = trajectory[:, 0] - ox[:, None]
    dy = trajectory[:, 1] - oy[:, None]
    r = np.hypot(dx, dy)

    if config.robot_type == RobotType.rectangle:
        yaw = trajectory[:, 2]
        rot = np.array([[np.cos(yaw), -np.sin(yaw)], [np.sin(yaw), np.cos(yaw)]])
        rot = np.transpose(rot, [2, 0, 1])
        local_ob = ob[:, None] - trajectory[:, 0:2]
        local_ob = local_ob.reshape(-1, local_ob.shape[-1])
        #local_ob = np.array([local_ob @ x for x in rot])
        testlist = [x.astype(float) for x in rot]
        local_ob = np.array([np.matmul(local_ob.astype(float) , testlist)])
        #print(local_ob)
        #print(rot)
        local_ob = local_ob.reshape(-1, local_ob.shape[-1])
        upper_check = local_ob[:, 0] <= config.robot_length / 2
        right_check = local_ob[:, 1] <= config.robot_width / 2
        bottom_check = local_ob[:, 0] >= -config.robot_length / 2
        left_check = local_ob[:, 1] >= -config.robot_width / 2
        if (np.logical_and(np.logical_and(upper_check, right_check),
                           np.logical_and(bottom_check, left_check))).any():
            return float("Inf")
    elif config.robot_type == RobotType.circle:
        if (r <= config.robot_radius).any():
            return float("Inf")

    min_r = np.min(r)
    return 1.0 / min_r  # OK


def calc_to_goal_cost(trajectory, goal):
    """
        calc to goal cost with angle difference
    """

    dx = goal[0] - trajectory[-1, 0]
    dy = goal[1] - trajectory[-1, 1]
    error_angle = math.atan2(dy, dx)
    cost_angle = error_angle - trajectory[-1, 2]
    cost = abs(math.atan2(math.sin(cost_angle), math.cos(cost_angle)))

    return cost


def plot_arrow(x, y, yaw, length=0.5, width=0.1):  # pragma: no cover

    
    plt.arrow(x, y, length * math.cos(yaw), length * math.sin(yaw),
              head_length=width, head_width=width)
    plt.plot(x, y)


def plot_robot(x, y, yaw, config):  # pragma: no cover
    if config.robot_type == RobotType.rectangle:
        outline = np.array([[-config.robot_length / 2, config.robot_length / 2,
                             (config.robot_length / 2), -config.robot_length / 2,
                             -config.robot_length / 2],
                            [config.robot_width / 2, config.robot_width / 2,
                             - config.robot_width / 2, -config.robot_width / 2,
                             config.robot_width / 2]])
        Rot1 = np.array([[math.cos(yaw), math.sin(yaw)],
                         [-math.sin(yaw), math.cos(yaw)]])
        outline = (outline.T.dot(Rot1)).T
        outline[0, :] += x
        outline[1, :] += y
        plt.plot(np.array(outline[0, :]).flatten(),
                 np.array(outline[1, :]).flatten(), "-k")
    elif config.robot_type == RobotType.circle:
        circle = plt.Circle((x, y), config.robot_radius, color="b")
        plt.gcf().gca().add_artist(circle)
        out_x, out_y = (np.array([x, y]) +
                        np.array([np.cos(yaw), np.sin(yaw)]) * config.robot_radius)
        plt.plot([x, out_x], [y, out_y], "-k")



def target(gx, gy,initialx , initialy, robot_type=RobotType.rectangle):
    print(__file__ + " start!!")
    
    # initial state [x(m), y(m), yaw(rad), v(m/s), omega(rad/s)]
    x = np.array([initialx, initialy, math.pi / 8.0, 0.0, 0.0])
    # goal position [x(m), y(m)]
    goal = np.array([gx, gy])
    # obstacles [x(m) y(m), ....]
    #ob = np.array([[5,5]])
    # input [forward speed, yaw_rate]
	#print(ob)
    config = Config()
    config.robot_type = robot_type
    trajectory = np.array(x)

    while True:
        u, predicted_trajectory = dwa_control(x, config, goal, obs)
        x = motion(x, u, config.dt)  # simulate robot
        trajectory = np.vstack((trajectory, x))  # store state history

        if show_animation:
            plt.cla()
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect('key_release_event',
                    lambda event: [exit(0) if event.key == 'escape' else None])
            plt.plot(predicted_trajectory[:, 0], predicted_trajectory[:, 1], "-g")
            plt.plot(x[0], x[1], "xr")
            plt.plot(goal[0], goal[1], "xb")

            plt.plot(ob[:, 0], ob[:, 1], "ok")
            plot_robot(x[0], x[1], x[2], config)
            plot_arrow(x[0], x[1], x[2])
            plt.axis("equal")
            plt.grid(True)
            plt.pause(0.0001)

        # check reaching goal
        dist_to_goal = math.hypot(x[0] - goal[0], x[1] - goal[1])
        if dist_to_goal <= config.robot_radius:
            print("Goal!!")
            break

    found = findTennisBall()
    if show_animation:
        plt.plot(trajectory[:, 0], trajectory[:, 1], "-r")
        plt.pause(0.0001)

    plt.show()
    if found == 1:
    	print("Done")
    	return
    


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###################################################################
def main(lata , longa, latb,  longb):
	lata = conv.convert_gps(float(lata))
	longa=conv.convert_gps(float(longa))
	latb=conv.convert_gps(float(latb))
	longb=conv.convert_gps(float(longb))
	try:
		from pylibfreenect2 import OpenGLPacketPipeline
		pipeline = OpenGLPacketPipeline()
	except:
		try:
		    from pylibfreenect2 import OpenCLPacketPipeline
		    pipeline = OpenCLPacketPipeline()
		except:
		    from pylibfreenect2 import CpuPacketPipeline
		    pipeline = CpuPacketPipeline()
	print("Packet pipeline:", type(pipeline).__name__)
	#create list for gps location of obstacles


	
	###############################################################


	# Create and set logger
	logger = createConsoleLogger(LoggerLevel.Debug)
	setGlobalLogger(logger)

	fn = Freenect2()
	num_devices = fn.enumerateDevices()
	if num_devices == 0:
		print("No device connected!")
		sys.exit(1)

	serial = fn.getDeviceSerialNumber(0)
	device = fn.openDevice(serial, pipeline=pipeline)

	listener = SyncMultiFrameListener(
		FrameType.Color | FrameType.Ir | FrameType.Depth)

	# Register listeners
	device.setColorFrameListener(listener)
	device.setIrAndDepthFrameListener(listener)

	device.start()

	# NOTE: must be called after device.start()
	registration = Registration(device.getIrCameraParams(),
		                        device.getColorCameraParams())

	undistorted = Frame(512, 424, 4)
	registered = Frame(512, 424, 4)

	# Optinal parameters for registration
	# set True if you need
	need_bigdepth = False
	need_color_depth_map = False

	bigdepth = Frame(1920, 1082, 4) if need_bigdepth else None
	color_depth_map = np.zeros((424, 512),  np.int32).ravel() \
		if need_color_depth_map else None

	while True:
		frames = listener.waitForNewFrame()
		#time.sleep(5)
		color = frames["color"]
		ir = frames["ir"]
		depth = frames["depth"]

		registration.apply(color, depth, undistorted, registered,
		                   bigdepth=bigdepth,
		                   color_depth_map=color_depth_map)

		# NOTE for visualization:
		# cv2.imshow without OpenGL backend seems to be quite slow to draw all
		# things below. Try commenting out some imshow if you don't have a fast
		# visualization backend.
		#cv2.imshow("ir", ir.asarray() / 65535.)
		#time.sleep(2)
		cv2.imshow("depth", depth.asarray() / 4500.)
		
		#Comment the coming lines
		print('center value is:',depth.asarray(np.float32).item((212,256)))
		print('down1 value is:',depth.asarray(np.float32).item((270,256)))
		'''print('up1 value is:',depth.asarray(np.float32).item((150,256)))
		print('up2 value is:',depth.asarray(np.float32).item((100,256)))
		
		print('down2 value is:',depth.asarray(np.float32).item((350,256)))
		print('right1 value is:',depth.asarray(np.float32).item((212,300)))
		print('right2 value is:',depth.asarray(np.float32).item((212,350)))
		print('left1 value is:',depth.asarray(np.float32).item((212,200)))
		print('left2 value is:',depth.asarray(np.float32).item((212,150)))'''
		

		x = depth.asarray(np.float32)
		y = np.logical_and(np.greater(x, 1200) , np.less(x, 1500))
		#print(np.extract(y, x))
		no_of_pixels = np.count_nonzero(np.extract(y, x))
		print(no_of_pixels)
		#get gps coordinate at this location########	
		'''
		assumingthegps received is lat,long variables:
		obs.append([lat,long])
		this is to be retrieved in the path planning code.
		'''	
		if no_of_pixels >  14000: #approx distance from the camera = 1.5 m
		    print('big Obstacle found, stop!!!')
		    obs.append(findPosition())			
		elif no_of_pixels >  8000: #approx distance from the camera = 1.5 m
		     print('small Obstacle found!!')
		     obs.append(findPosition())
		#cv2.imshow("color", cv2.resize(color.asarray(),(int(1920 / 3), int(1080 / 3))))
		#cv2.imshow("registered", registered.asarray(np.uint8))

		if need_bigdepth:
		    cv2.imshow("bigdepth", cv2.resize(bigdepth.asarray(np.float32),
		                                      (int(1920 / 3), int(1082 / 3))))
		if need_color_depth_map:
		    cv2.imshow("color_depth_map", color_depth_map.reshape(424, 512))

		listener.release(frames)
		#time.sleep(20)
		key = cv2.waitKey(delay=1) & 0xFF
		if key == ord('q'):
		    break

	#######################################################

	target(latb , longb , lata, longa)
	#stage3.py main  fnc
	#######################################################
	device.stop()
	device.close()
	
	#sys.exit(1)
	
	
if __name__ == '__main__':
    #main (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    main (0, 0, 10, 10)
