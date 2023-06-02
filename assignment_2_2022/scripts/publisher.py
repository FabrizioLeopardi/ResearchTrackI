#!/usr/bin/env python
"""
.. module:: publisher
	:platform: Unix
	:synopsis: A publisher of robot position and velocity
.. moduleauthor:: Fabrizio Francesco Leopardi

This file implements the second part of point (a) of RT1 assignment.
It implements a publisher that publishes a custom message ``(x,y,vel_X,vel_z)`` defined in the msg folder ``Kinematic.msg`` relying on the values published to the topic /odom. It relies on the Odometry of the robot so in a real application this would be sensitive to noise.

Subscribes to:
	/odom

Publishes to:
	/chatter

"""

import rospy
from nav_msgs.msg import Odometry
from assignment_2_2022.msg import Kinematic

p=rospy.Publisher('chatter',Kinematic,queue_size=100)

def pub(data):
	"""
	The callback function of the Subscriber() initialized in the ``talker()`` function. It publishes an Kinematic object on the topic '/chatter'
	
	Args:
	data(Odometry): position and twist data of the robot as computed via odometry --> some small errors may be present.
	
	"""
	o=Kinematic()
	o.x=data.pose.pose.position.x
	o.y=data.pose.pose.position.y
	o.vel_x=data.twist.twist.linear.x
	o.vel_z=data.twist.twist.angular.z
	p.publish(o)

def talker():
	"""
	This function initializes the ROS node ``talker``, subscribes to the topic /odom to retrieve odometry info.
	As a result robot planar position ``(x,y)``  linear velocity along its x-axis and rotation along the axis z 
	orthogonal to the plane of the robot is published. The published data will be retrieved by the :mod:`scripts.subscriber`
	
	""" 
	rospy.init_node('talker',anonymous=True)
	rospy.Subscriber('/odom',Odometry,pub)
	rospy.spin()


if __name__=='__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
