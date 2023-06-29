#!/usr/bin/env python3

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
from gripperControl import *
import geometry_msgs.msg
import tf
from copy import deepcopy
from math import pi, degrees
from std_msgs.msg import String
from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion
from moveit_commander.conversions import pose_to_list
from moveit_msgs.msg import MoveGroupActionResult

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node("pickIMU", anonymous=False)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()

# intialising movement groups
arm_group = moveit_commander.MoveGroupCommander("manipulator")
gripper_group = moveit_commander.MoveGroupCommander("gripper")

# arm_group.set_pose_reference_frame('base_link')
end_effector_link = arm_group.get_end_effector_link()
print(end_effector_link)

IMU_Module = rospy.get_param('tag10')[0]  # -0.707, 0.707, 0, 0 xyzw
Panel = rospy.get_param("tag11")[0]

display_trajectory_publisher = rospy.Publisher(
        "/move_group/display_planned_path",
        moveit_msgs.msg.DisplayTrajectory,
        queue_size=20,
    )

group_variables = arm_group.get_current_joint_values()
group_variables[0] = 0
group_variables[1] = -2.094395
group_variables[2] = 1.745329
group_variables[3] = 0.349065
group_variables[4] = 1.570796
group_variables[5] = -1.570796
arm_group.set_joint_value_target(group_variables)
plan = arm_group.go(wait=True)

# get the home pose data and intialise it as starting pose
start_pose = arm_group.get_current_pose(end_effector_link).pose
print(start_pose)
quat = [start_pose.orientation.x, start_pose.orientation.y,
        start_pose.orientation.z, start_pose.orientation.w]
eu = euler_from_quaternion(quat)
eu = [degrees(eu[0]), degrees(eu[1]), degrees(eu[2])]
print(eu)

# prepare to grab the IMU
grab_pose_goal = [IMU_Module[0], IMU_Module[1], IMU_Module[2]+0.044, 0, pi, pi/2]
arm_group.set_pose_target(grab_pose_goal)
plan = arm_group.go(wait=True)

# grab the IMU by closing the gripper
gripperPos("semi_open")
rospy.sleep(1)
arm_group.go([0,-(pi/2), 0, -(pi/2), 0, 0])
