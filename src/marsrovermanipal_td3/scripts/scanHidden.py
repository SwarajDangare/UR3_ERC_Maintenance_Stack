#!/usr/bin/env python3

from operator import imod
from re import I
import sys
import copy
import rospy
import math
import numpy as np
from math import radians
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import cos, pi, sin
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from geometry_msgs.msg import Pose, Point, Quaternion
from math import pi
from std_msgs.msg import String
from moveit_msgs.msg import MoveGroupActionResult
from fiducial_msgs.msg import FiducialTransform, FiducialTransformArray
from gripperControl import *
from panel import *
import os

flag = True
def callback(data): 
    if len(data.transforms)>0:
        for i in range(len(data.transforms)):
            frame = data.transforms[i]
            if frame.fiducial_id > 0 and frame.fiducial_id<10:
                rospy.set_param('hiddenButton', frame.fiducial_id)
                print(frame.fiducial_id)
                os.system("rosnode kill aruco_detect_hidden")
                os.system("rosnode kill scanHidden")

rospy.init_node("scanHidden", anonymous=False)
group_name = "manipulator"
pose_goal = Pose()
moveit_commander.roscpp_initialize(sys.argv)
move_group = moveit_commander.MoveGroupCommander(group_name)
robot = moveit_commander.RobotCommander()
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)
# arucoID = 12
Inspec_panel = rospy.get_param('tag12')[0]#[0.33565261545991887, -0.2745230369010141, 0.2059755184403631]
GoToScan(Inspec_panel, move_group)

rospy.Subscriber('fiducial_transforms', FiducialTransformArray, callback)
while flag:
    rospy.spin()
