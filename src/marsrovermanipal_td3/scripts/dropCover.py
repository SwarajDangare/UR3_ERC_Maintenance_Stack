#!/usr/bin/env python3

import sys
import rospy
import moveit_commander
import moveit_msgs.msg
from gripperControl import *

rospy.init_node("dropCover", anonymous=False)
group_name = "manipulator"
moveit_commander.roscpp_initialize(sys.argv)
move_group = moveit_commander.MoveGroupCommander(group_name)
robot = moveit_commander.RobotCommander()
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)

gripperPos("open")