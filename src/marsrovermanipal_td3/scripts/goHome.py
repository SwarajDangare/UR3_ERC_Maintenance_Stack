#!/usr/bin/env python3
import sys
import rospy
import moveit_commander
from math import pi

group_name = "manipulator"
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('secretButton',anonymous=False)
move_group =moveit_commander.MoveGroupCommander(group_name) 
robot = moveit_commander.RobotCommander()
move_group.go(rospy.get_param('start'))
rospy.sleep(5)
print('back home')
