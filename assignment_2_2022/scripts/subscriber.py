#!/usr/bin/env python
"""
.. module:: subscriber
	:platform: Unix
	:synopsis: A subscriber that prints distance and average speed
.. moduleauthor:: Fabrizio Francesco Leopardi

This file implements the point (c) of RT1 assignment.
It implements a subscriber that listens on the topic /chatter and compute the distance of the robot to the goal and the average linear speed of the robot.
The angular speed is not used even though one may think to print it.
By design this node should never be run alone as it relies on the definition of print_freq_one. This is the frequency (Hz) the code publishes information. It is get from the ROS parameter server, it is set in this project by assignment2.launch file
	

Subscribes to:
	/chatter

"""

import rospy
from assignment_2_2022.msg import Kinematic
import math

def update_avgspeed(vel_x):
	"""
	A simple function that updates the average speed computing the arithmetic mean of the samples of the linear speed. 
	This is just an approximation based on the hypotesis that between two samples of linear velocity 
	the vel_x variable won't change much.
	
	Args:
	vel_x: the x velocity of the robot
	
	"""
	global counter_,avgspeed_
	avgspeed_ = ((avgspeed_*counter_)+vel_x)/(counter_+1)

def compute_dist(x,t_x,y,t_y):
	"""
	A simple function that computes the Euclidean distance between the robot and the goal
	
	Args:
	x: the x position of the robot
	t_x: the x position of the target (i.e. goal)
	y: the y position of the robot
	t_y: the y position of the target (i.e. goal)
	
	Returns:
	The distance robot-goal
	
	"""
	return math.sqrt((x-t_x)*(x-t_x)+(y-t_y)*(y-t_y))

def callback(data):
	"""	
	This function is the callback of the subscriber each time data are published on the topic /chatter 
	it updates the internal parameters.
	This function retrieves also the parameters des_pos_x and des_pos_y from the ROS parameter server 
	which are updated by the bug_as.py script.
	These parameters always contain the x and the y position of the current goal.
	
	Args:
	data(Kinematic): the x,y position and linear,angular velocity of the robot
	
	"""
	global counter_,distance_,avgspeed_
	counter_ = counter_+1
	t_x = rospy.get_param('des_pos_x') #target x retrieved from parameter server
	t_y = rospy.get_param('des_pos_y') #target y retrieved from parameter server
	#print(rospy.get_param('des_pos_x'))
	#print(rospy.get_param('des_pos_y'))
	x=data.x
	y=data.y
	vel_x=data.vel_x
	vel_z=data.vel_z
	distance_= compute_dist(x,t_x,y,t_y)
	update_avgspeed(vel_x)

def listener():
	"""
	This function initializes the ROS node 'listener', subscribes to the topic /chatter to retrieve 
	odometry info published by :mod:`scripts.publisher`.
	As a result the distance of the robot to the goal is printed as well as the average speed.
	
	""" 
	global counter_,distance_,avgspeed_
	counter_=0
	distance_=0
	avgspeed_=0
	rospy.init_node('listener',anonymous=True)
	rospy.Subscriber('chatter', Kinematic, callback)
	frequency=rospy.get_param('print_freq_one')
	#frequency = 1
	rate = rospy.Rate(frequency)
	while not rospy.is_shutdown():
		rospy.loginfo("distance: "+str(distance_))
		rospy.loginfo("average speed: "+str((avgspeed_)))
		rate.sleep()

if __name__ == '__main__':
	listener()
