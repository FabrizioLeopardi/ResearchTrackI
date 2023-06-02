#! /usr/bin/env python
"""
.. module:: client
	:platform: Unix
	:synopsis: The client, it allows to set or cancel a goal
.. moduleauthor:: Fabrizio Francesco Leopardi

This file implements the main part of point (a) of RT1 assignment.
It allows the user to set or to cancel a goal.

Subscribes to:
	/reaching_goal/result

"""

import rospy
import actionlib
import assignment_2_2022.msg
from geometry_msgs.msg import PoseStamped
from assignment_2_2022.msg import PlanningActionResult

client = actionlib.SimpleActionClient('/reaching_goal',assignment_2_2022.msg.PlanningAction)

def goal_callback(data):
	"""
	A callback that continously check if the goal has been cancelled or reached to set the value of the global variable ``goal_set_`` to false.
	This allows the user to never cancel a goal and yet been able to set another one if the previous has been reached.
	
	Args:
	data(PlanningActionResult): the variable needed to know the status of the goal
	
	"""	
	global goal_set_
	if data.status.status==2 or data.status.status==3:
		goal_set_=False

def target_client(a,b):
	"""
	A function that set the goal coordinates of the goal ignoring the other fields of the PoseStamped object ``o``
	
	Args:
	a: x-coordinate of the goal the user want to set
	b: y-coordinate of the goal the user want to set
	
	"""
	client.wait_for_server()
	o = PoseStamped()
	o.header.seq=0
	o.header.stamp.secs=0
	o.header.stamp.nsecs=0
	o.header.frame_id=""
	o.pose.position.x=a
	o.pose.position.y=b
	o.pose.position.z=0
	o.pose.orientation.x=0
	o.pose.orientation.y=0
	o.pose.orientation.z=0
	o.pose.orientation.w=0
	goal = assignment_2_2022.msg.PlanningGoal(o)
	client.send_goal(goal)



def main():
	"""
	The main function of the client script and indeed of the assignment. The ``main()`` function initializes the ROS node 	
	``target_client_py``. It creates a simple user interface that, in principle, never stops 
	(uses ``while not rospy.is_shutdown()``) and allows the user to set or to cancel a goal. No check on the coordinates is done so the user
	should be careful when setting the goal to set a *reachable* (i.e. inside the world borders) goal.
	
	.. warning: This node is not launched by the assignment2.launch file, so it should be launched manually after the launchfile.
		
	"""
	rospy.init_node('target_client_py')
	global goal_set_
	goal_set_ = False
	client = actionlib.SimpleActionClient('/reaching_goal',assignment_2_2022.msg.PlanningAction)
	P=rospy.Subscriber('/reaching_goal/result',PlanningActionResult,goal_callback)
	while not rospy.is_shutdown():
		if goal_set_==False:
			print("Please select the coordinates of a goal")
			a=float(input("x-axis: "))
			b=float(input("y-axis: "))
			target_client(a,b)
			goal_set_ = True
		else:
			print("A goal has been set, would you like to cancel it? (y/n)")
			c=input()
			if c=='y':
				client.cancel_all_goals()
				goal_set_=False


if __name__=="__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		print("execution interrupted",file=sys.stderr)
