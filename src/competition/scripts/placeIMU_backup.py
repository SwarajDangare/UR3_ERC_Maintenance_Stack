#!/usr/bin/env python3

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf
from gripperControl import *
from std_msgs.msg import Bool

from copy import deepcopy
from math import pi, degrees
from std_msgs.msg import String
from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion
from moveit_commander.conversions import pose_to_list
from moveit_msgs.msg import MoveGroupActionResult

IMU_orientation = float(rospy.get_param('angle'))
Panel = rospy.get_param("tag11")[0]

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node("placeIMU", anonymous=False)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()

# intialising movement groups
arm_group = moveit_commander.MoveGroupCommander("manipulator")
gripper_group = moveit_commander.MoveGroupCommander("gripper")

# arm_group.set_pose_reference_frame('base_link')
end_effector_link = arm_group.get_end_effector_link()
print(end_effector_link)

display_trajectory_publisher = rospy.Publisher(
    "/move_group/display_planned_path",
    moveit_msgs.msg.DisplayTrajectory,
    queue_size=20,
)

# bring IMU near the panel 5cm above the velcro
panel_pose_goal = [Panel[0]-0.08520, Panel[1]-0.09954, Panel[2]-0.15, pi/2, 0, 3/5*pi]
arm_group.set_pose_target(panel_pose_goal)
plan = arm_group.go(wait=True)

#orient the IMU
orientation_pose_goal = [Panel[0]-0.08520, Panel[1]-0.09954, Panel[2]-0.15, pi/2, pi/180*IMU_orientation, 3/5*pi]
arm_group.set_pose_target(orientation_pose_goal)
plan = arm_group.go(wait=True)

#place the IMU by moving towards the velcro panel
waypoints = []
wpose = arm_group.get_current_pose().pose
wpose.position.x += Panel[0]-0.06599
wpose.position.y += Panel[1]-0.09330
waypoints.append(copy.deepcopy(wpose))
(plan,fraction)=arm_group.compute_cartesian_path(waypoints,0.001,0.0,True)
arm_group.execute(plan)

#release the IMU
gripperPos("open")
rospy.sleep(2)
try:
    service_proxy = rospy.ServiceProxy('erc_score',Bool)
    service_response = service_proxy(True)
except rospy.ServiceException as e:
    print(f"Service call failed: {e}")
arm_group.go([0,-(pi/2), 0, -(pi/2), 0, 0])