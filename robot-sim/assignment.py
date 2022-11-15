from __future__ import print_function

import time
from sr.robot import *

a_th=2.0
d_th=0.4

search = True
silver = True
smooth = False
golden_paired=[0,0,0,0,0,0]
silver_paired=[0,0,0,0,0,0]
num_paired=0
size=6
sampling_T=0.05

R=Robot()

def drive(speed,seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed,seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

""" checks if the golden box is already paired """
def golden_already(code):
    for i in range(size):
        if golden_paired[i] == code:
            return 1
    return 0

""" checks if the silver box is already paired """
def silver_already(code):
    for i in range(size):
        if silver_paired[i] == code:
            return 1
    return 0

""" rotate the robot until it finds the nearest golden box not already paired"""
def search_closest_golden():
    print("Searching for the closest free golden token...")
    dist = 100
    box = -1
    for t in range(int(4/(0.2*sampling_T))):
        turn(30,0.2*sampling_T)
        for token in R.see():
            if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
                if golden_already(token.info.code)==0:
                    dist = token.dist
                    box = token.info.code
    print("Found! It is box "+str(box))
    return box

""" rotate the robot until it finds the nearest silver box not already paired"""
def search_closest_silver():
    print("Searching for the closest free silver token...")
    dist = 100
    box = -1
    for t in range(int(4/(0.2*sampling_T))):
        turn(30,0.2*sampling_T)
        for token in R.see():
            if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
                if silver_already(token.info.code)==0:
                    dist = token.dist
                    box = token.info.code
    print("Found! It is box "+str(box))
    return box
    
""" returns the distance and the angle to the silver token with code 'box'"""
def find_silver_token(box):
    dist = 100
    for token in R.see():
        if token.info.code == box and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist = token.dist
            rot_y = token.rot_y
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y
        
""" returns the distance and the angle to the golden token with code 'box'"""
def find_golden_token(box):
    dist = 100
    for token in R.see():
        if token.info.code == box and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist = token.dist
            rot_y = token.rot_y
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y

""" it pre-alligns the robot to the box, notice that while the robot moves it might still need to rotate a bit """
def align(box,silver):
    if silver == True:
        dist,rot_y = find_silver_token(box)
        while rot_y > a_th or rot_y < -a_th or dist == -1:
            turn(-30,0.2*sampling_T)
            dist,rot_y = find_silver_token(box)
    else:
        dist,rot_y = find_golden_token(box)
        while rot_y > a_th or rot_y < -a_th or dist == -1:
            turn(-30,0.2*sampling_T)
            dist,rot_y = find_golden_token(box)

""" First it drives straight a bit to have more space and then it starts the execution"""
drive(25,1)
while num_paired<size:
    if silver == True:
        if search == True:
            box=search_closest_silver() #search for best silver token
            search=False
            align(box,silver)
        else:
            dist, rot_y = find_silver_token(box) #goes to grab it
            if dist == -1:
                turn(20,sampling_T)
            else:
                if dist >= d_th and (smooth or -a_th <= rot_y <= a_th):
                    drive(50,2*sampling_T)
                if rot_y>a_th:
                    turn(2,sampling_T)
                if rot_y<-a_th:
                    turn(-2,sampling_T)
                if dist < d_th:
                    R.grab()
                    search = True
                    silver_paired[num_paired]=box
                    silver = False
    else:
        if search == True:
            box=search_closest_golden() #search for best golden token
            search = False
            align(box,silver)
        else:
            dist, rot_y = find_golden_token(box) #goes to release the silver token
            if dist == -1:
                turn(20,sampling_T)
            else:
                if dist >= 1.5*d_th and (smooth or -a_th <= rot_y <= a_th):
                    drive(50,2*sampling_T)
                if rot_y > a_th:
                    turn(2,sampling_T)
                if rot_y < -a_th:
                    turn(-2,sampling_T)
                if dist < 1.5*d_th:
                    R.release()
                    search = True
                    golden_paired[num_paired]=box
                    silver = True
                    num_paired = num_paired+1
                    drive(-20,2)
print("Finish!")
