"""
	When done, run with:
	$ python2 run.py assignement.py

"""

from __future__ import print_function

import time
from sr.robot import *

#Useful values
    
a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

#My Robot
R = Robot()
""" instance of the class Robot"""

#Functions

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

#My functions

def find_silver():
	'''
	Function to create one list for all the visible and pickable silver tokens, 
	reporting: the code, the distance and the and the angle of each of them	
	'''
	#create one empty lists in which memorize the seen tokens 
	silver=list()
	markers = R.see()
	#control all the tokens
	for m in markers:
	    if (m.info.marker_type in (MARKER_TOKEN_SILVER)) and (m.info.code not in silver_taken):
		t=[m.info.code, m.dist, m.rot_y]
		#collect the silver token's useful information
		silver.append(t)
	#I need to be able of always seeing at least one silver token
	if len(silver)==0:
		print("Can't see any silver")
		turn(10,1)
		return(find_silver())
	else:
		print("I see these silver tokens:\n",silver)
		return(silver)
		
		
def find_gold():
	'''
	Function to create one list for all the visible and pickable gold tokens, 
	reporting: the code, the distance and the and the angle of each of them	
	'''
	#Same implementation of find_silver()
	gold=list()
	markers = R.see()
	for m in markers:
	    if m.info.marker_type in (MARKER_TOKEN_GOLD) and (m.info.code not in gold_taken):
		t=[m.info.code, m.dist, m.rot_y]
		gold.append(t)
	if len(gold)==0:
		print("Can't see any gold")
		turn(15,1)
		return(find_gold())
	else:
		print("I see these gold tokens:\n",gold)
		return(gold)

def update(list_token):
	"""
	Function to sort the tokens with respect to the closest one
	
	Arg: list_token (list): silver or gold, the list to update
	"""
	#sort the list of lists with respect to the second element which is the distance
	lt= sorted(list_token, key=lambda x: x[1])
    	#save the code, the distance and the angle of the closest token (the first of the sorted list)
    	c=lt[0][0]
        d=lt[0][1]
        r=lt[0][2]
        return(c,d,r)
    		
def reach_closest_token(r,d):
	"""
	Function to reach the closest token
	
	Args: r (float) : rotation of the closest token
	      d (float) : distance of the closest token
	"""
	#if the distance of the token is less than the threshold
	if d<d_th:
		#if the angle of the token is inside the threshold 
		if abs(r)<a_th:
			print("Here we are")
		#else turn left or right depending on the angle of the token
		elif r>a_th:
			print("Turn right a little bit")
			turn(3,1)
		elif r<-a_th:
			print("Turn left a little bit")
			turn(-3,1)  
        #the token is far from the robot
        else:
        	#fix the inclination in the same way as before
    		if abs(r)<a_th:
			print("Here we are")
		elif r>a_th:
			print("Turn right a little bit")
			turn(3,1)
		elif r<-a_th:
			print("Turn left a little bit")
			turn(-3,1)  
		print("We are far far away, let's go on")
		#and drive in that direction
		drive(10,2)
 
def silver_action(code):
	"""
	Function to grab the cube
	
	Arg: code (int) : the code of the token to pick 
	"""
	#if the robot grabs the token
	if R.grab()==True:
		#add the token code the the list of picked token
		print("I got you")
		silver_taken.append(code)		
	else:
		print("Oops!")
		
def gold_action(code,d,r):
	"""
	Function to release the cube
	
	Args: code (int) : the code of the token i want to pick
	      d (float)  : distance of the token i want to pick
	      r (float)  : rotation of the token i want to pick
	"""
	#if the distance of the token is less than the threhold plus a coefficient due to the robot carryng a token 
	if d<(d_th+0.2):
		#release the silver token and add the gold's code the the list of used token
		R.release()
		print("You are a couple")
		gold_taken.append(code)
	else:
		print("not yet")
	
	
	
#Main
start=time.time()
silver_taken=list()          #Initialize two empty list to fill up with the taken tokens
gold_taken=list()

#main loop, the procedure is repeated since all the silver token are taken, in this map 6
while len(silver_taken)<6:

    #Robot seeks for a silver token
    print("let's go!")
    print("I search a silver token")
    silver=find_silver()
    print("select the closest one of", silver)
    (c,d,r)=update(silver)
    
    #Robot reach the closest silver token 
    while c not in silver_taken:
    	print("searching the silver:",c)
    	#update the closest token
    	silver=find_silver()
    	(c,d,r)=update(silver)
    	#move nearest the token
    	reach_closest_token(r,d)
    	#try to grab it, if not start again
    	silver_action(c)
    
    #Robot seeks for a gold token	
    print("Now i search gold token")
    gold=find_gold()
    print("select the closest one of", gold)
    (c,d,r)=update(gold)
    
    #Robot reach the closest gold token 
    while c not in gold_taken:
    	print("searching the gold:",c)
    	#update the closest token
    	gold=find_gold()
    	(c,d,r)=update(gold)
    	#move nearest the token
    	reach_closest_token(r,d)
    	#if it is near enough drop the token, if not start again
    	gold_action(c,d,r)   
    	
    print("Taken silver token:",silver_taken)
    print("Taken gold token:",gold_taken)
    
print("I matched all the tokens")
end=time.time()
print(end-start)

