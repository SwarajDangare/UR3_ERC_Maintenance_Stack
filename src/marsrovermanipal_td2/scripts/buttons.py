#!/usr/bin/env python3
import sys
import rospy
import tf
import moveit_commander 
import random
from math import radians
from geometry_msgs.msg import Pose, Point, Quaternion
from math import pi
def row2():    
    return [-1.117010721276371, -1.2042771838760873, 2.4085543677521746, -1.1868238913561442, 0.4886921905584123, -1.5707963267948966]
def up():
    return [0,-(pi/2), 0, -(pi/2), 0, 0]
def scan0():
    return [radians(91), radians(-128), radians(115), radians(-97), radians(-116), radians(117)]
def scan1():
    return [radians(78), radians(-98), radians(61), radians(23), radians(147), radians(-105)]
def scan2():
    return [radians(93), radians(13), radians(-89), radians(-104), radians(144), radians(90)]
def scan3():
    return [radians(98), radians(-45), radians(-106), radians(-101), radians(110), radians(44)]