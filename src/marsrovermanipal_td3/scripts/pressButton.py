#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Pose
from math import radians
import copy 
from gripperControl import *
from std_msgs.msg import Bool

flag = True
def callback( data):
    flag = not data.data


def press(id, move_group):
    move_group.go([radians(0), radians(-120),radians(100),radians(20),radians(90), radians(-90)])
    gripperPos("close")
    pose = rospy.get_param('tag'+str(id))
    position =  pose[0]
    button = Pose()
    currentPose = move_group.get_current_pose().pose
    waypoints = []
    currentPose.position.y = position[1]
    currentPose.position.z = position[2]-0.04
    waypoints.append(copy.deepcopy(currentPose))
    (plan, fraction) = move_group.compute_cartesian_path(waypoints, .01, 0.0 )  
    move_group.execute(plan, wait=True)
    rospy.Subscriber("/button"+str(id),Bool, callback)
    while flag:
        waypoints = []
        currentPose = move_group.get_current_pose().pose
        currentPose.position.x += 0.005
        (plan, fraction) = move_group.compute_cartesian_path(
        waypoints, 0.005, 0.0  
        )  
        move_group.execute(plan, wait=True)
    move_group.go([radians(0), radians(-120),radians(100),radians(20),radians(90), radians(-90)])



