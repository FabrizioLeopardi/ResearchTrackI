#!/usr/bin/env python
"""
.. module:: status_service
	:platform: Unix
	:synopsis: A service that when called returns the number of goal reached and cancelled
.. moduleauthor:: Fabrizio Francesco Leopardi

This file implements point (b) of RT1 assignment.
It implements a service that when called returns the number of goal reached and cancelled.


Subscribes to:
	/reaching_goal/result

"""

import rospy
from assignment_2_2022.msg import PlanningActionResult
from assignment_2_2022.srv import Reached, ReachedResponse

def callback(data):
	"""
	This function is the callback of the subscriber to the /reaching_goal/result topic. It updates the number of the goals reached and cancelled.
	To do this it checks for the *'status'* of the goal which is a numerical variable in the field status of the type PlanningActionResult.
	
	Args:
	data(PlanningActionResult): the variable needed to know the status of the goal (reached, cancelled, something else)
	
	"""
	global number_goal_cancelled_,number_goal_reached_
	if data.status.status==2:
		number_goal_cancelled_=number_goal_cancelled_+1
	if data.status.status==3:
		number_goal_reached_=number_goal_reached_+1

def serve(req):
	"""
	This function is the callback of the service server. It fills the fields of the service ReachedResponse, a custom service.
	
	Args:
	req(Reached): The request (empty field)
	
	Returns:
	ReachedResponse(reached,cancelled): The actual response.
	
	"""
	global number_goal_cancelled_,number_goal_reached_
	cancelled = number_goal_cancelled_
	reached = number_goal_reached_
	return ReachedResponse(reached,cancelled)

def my_server():
	"""
	This function is the 'main' function of this script. It starts a ROS node ``my_service_Server``. It creates 2 global variable that 
	will count how many goals have been reached and how many have been cancelled. Then it actually computes these values.
	
	"""
	rospy.init_node('my_service_Server',anonymous=True)
	global number_goal_cancelled_,number_goal_reached_
	number_goal_cancelled_=0
	number_goal_reached_=0
	rospy.Subscriber('/reaching_goal/result',PlanningActionResult,callback)
	s=rospy.Service('reached', Reached, serve)
	print("Service ready.")
	rospy.spin()

if __name__=="__main__":
	my_server()
