#!/usr/bin/env python3

from re import I
import sys
from moveit_msgs.msg import Constraints, OrientationConstraint
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
import csv


def euler_to_quaternion(roll, pitch, yaw):

  qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
  qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
  qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
 
  return [qx, qy, qz, qw]
def quaternion_to_euler(x, y, z, w):
    
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    X = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    Z = math.degrees(math.atan2(t3, t4))

    return X, Y, Z


def setConstrains(move_group):
    
    end = move_group.get_end_effector_link()
    pose = move_group.get_current_pose(end)
    
    constraints = Constraints()
    constraints.name = "Keep gripper as it is"

    # Create an orientation constraint for the right gripper
    orientation_constraint = OrientationConstraint()
    orientation_constraint.header = pose.header
    orientation_constraint.link_name = move_group.get_end_effector_link()
    #orientation_constraint.orientation.w = 1.0
    orientation_constraint.absolute_x_axis_tolerance = 0.1
    orientation_constraint.absolute_y_axis_tolerance = 3.14
    orientation_constraint.absolute_z_axis_tolerance = 0.1
    constraints.orientation_constraints.append(orientation_constraint)
    move_group.set_path_constraints(constraints)

    # constraints = Constraints()
    # constraints.name = "Keep gripper as it is1"

    # # Create an orientation constraint for the right gripper
    # orientation_constraint = OrientationConstraint()
    # orientation_constraint.header = pose.header
    # orientation_constraint.link_name = "wrist_2_link"
    # orientation_constraint.orientation = Quaternion(-0.22, 0.41, -0.727, 0.5)
    # orientation_constraint.absolute_x_axis_tolerance = 0.0
    # orientation_constraint.absolute_y_axis_tolerance = 0.0
    # orientation_constraint.absolute_z_axis_tolerance = 0.0
    # constraints.orientation_constraints.append(orientation_constraint)
    # move_group.set_path_constraints(constraints)

    constraints = Constraints()
    constraints.name = "Rotate from back"

    orientation_constraint = OrientationConstraint()
    orientation_constraint.header = pose.header
    orientation_constraint.link_name = "shoulder_link"
    orientation_constraint.orientation = Quaternion(0.0, 0.0, 0.707, 0.707)
    orientation_constraint.absolute_x_axis_tolerance = 3.14
    orientation_constraint.absolute_y_axis_tolerance = 3.14
    orientation_constraint.absolute_z_axis_tolerance = pi/2
    orientation_constraint.weight = 1.0

    constraints.orientation_constraints.append(orientation_constraint)
    move_group.set_path_constraints(constraints)

def goToUp(move_group):

    # home = [radians(0), radians(-120), radians(100), radians(20), radians(90), radians(-90)]
    # move_group.go(home)

    up = [radians(0), radians(-90), radians(0),
          radians(-90), radians(0), radians(90)]
    move_group.go(up)

    # aboveStorage = [radians(155), radians(-87), radians(-81),
    #                 radians(-68), radians(92), radians(88)]
    # move_group.go(aboveStorage)

    # mid = [radians(91), radians(-84), radians(-108), radians(-66), radians(122), radians(21)]
    # move_group.go(mid)


def GripperState(gripperState):
    pub = rospy.Publisher('/gripper_command', String, queue_size=1)
    rospy.sleep(1)
    for _ in range(500):
        pub.publish(gripperState)
    print(gripperState)


def PickLid(box, move_group):

    move_group.clear_path_constraints()
    end = move_group.get_end_effector_link()
    
    eular = quaternion_to_euler(box[3], box[4], box[5], box[6])
    print(eular)

    # got to middle potition to get the required joint angle
    mid = [radians(153), radians(-16), radians(-130),
           radians(-90), radians(96), radians(92)]
    move_group.go(mid)

    setConstrains(move_group)



    jmax1 = radians(167+20)
    jmin1 = radians(167-20)
    jmax2 = radians(-55+20)
    jmin2 = radians(-55-20)
    jmax3 = radians(-102+20)
    jmin3 = radians(-102-20)
    jmax4 = radians(101+20)
    jmin4 = radians(101-20)
    jmax5 = radians(-88+20)
    jmin5 = radians(-88-20)

    wpose = move_group.get_current_pose(end).pose
    midPoint = [0.07, -0.14, 0.22, pi, 0.6, eular[2] - radians(90)]
    move_group.set_pose_target(midPoint)
    move_group.go(wait=True)

    gripper_position = move_group.get_current_joint_values()
    print("gripper_position")
    print(gripper_position)
    
    while((gripper_position[0] < jmax1 and gripper_position[0] > jmin1) and (gripper_position[1] < jmax2 and gripper_position[1] > jmin2) and (gripper_position[2] < jmax3 and gripper_position[2] > jmin3) and (gripper_position[3] < jmax4 and gripper_position[3] > jmin4) and (gripper_position[4] < jmax5 and gripper_position[4] > jmin5)):
        wpose = move_group.get_current_pose(end).pose
        # mid = [radians(153), radians(-16), radians(-130),
        #        radians(-90), radians(90), radians(80)]
        # move_group.go(mid)
        
        print("in while")
        
        move_group.clear_path_constraints()
        
        up = [radians(0), radians(-90), radians(0),
            radians(-90), radians(0), radians(90)]
        move_group.go(up)
        # mid = [radians(150), radians(-20), radians(-150),
        #     radians(-90), radians(90), radians(97)]
        # move_group.go(mid)
        mid = [radians(153), radians(-16), radians(-130),
            radians(-90), radians(96), radians(92)]
        move_group.go(mid)
        
        setConstrains(move_group)
        
        midPoint = [0.07, -0.14, 0.22,  pi, 0.6, eular[2] - radians(90)]
        move_group.set_pose_target(midPoint)
        move_group.go()

        gripper_position = move_group.get_current_joint_values()

    # move_group.go(gripper_position)

    move_group.clear_path_constraints()

    waypoints = []
    end = move_group.get_end_effector_link()
    wpose = move_group.get_current_pose(end).pose
    # print(wpose)

    wpose.position.x = box[0] + 0.01
    wpose.position.y = box[1] - 0.0032
    wpose.position.z = box[2] + 0.125

    waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = move_group.compute_cartesian_path(
      waypoints, 0.01, 0.0, True)
    move_group.execute(plan, wait=True)
    eular = list(eular)

    # z = eular[2]-radians(90)
    # rpy =(pi, 0.6, z)
    # move_group.set_rpy_target(rpy)

    print("Reached Lid Potition")
    wpose = move_group.get_current_pose(end).pose
    print(wpose)
    print("")

    return (wpose.position.x, wpose.position, wpose.position.z)

def PickLid_Backup1(box, move_group):    
    
    aboveStorage = [radians(155), radians(-87), radians(-81), radians(-68), radians(92), radians(88)]
    move_group.go(aboveStorage)
    
    waypoints = []
    end = move_group.get_end_effector_link()
    wpose = move_group.get_current_pose(end).pose
    # print(wpose)
    
    # qua = euler_to_quaternion(rpy_d[0],rpy_d[1],rpy_d[2])
    # print(qua)
    wpose.position.x = box[0] +0.01
    wpose.position.y = box[1] -0.0032
    wpose.position.z = box[2] +0.125
    # wpose.orientation.x = qua[0]
    # wpose.orientation.y = qua[1]
    # wpose.orientation.z = qua[2]
    # wpose.orientation.w = qua[3]

    waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = move_group.compute_cartesian_path(waypoints, 0.01, 0.0,True)
    move_group.execute(plan, wait=True)
    print("Reached Lid Potition")
    wpose = move_group.get_current_pose(end).pose
    print(wpose) 
    print("")  
    
    return (wpose.position.x,wpose.position,wpose.position.z)
    
    

def StoreLid(lidStorage, move_group):

    end = move_group.get_end_effector_link()
    wpose = move_group.get_current_pose(end).pose
    # print(wpose)

    waypoints = []
    wpose.position.z += 0.02
    waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = move_group.compute_cartesian_path(
        waypoints, 0.01, 0.0, True)
    move_group.execute(plan, wait=True)
    print("up")

    waypoints = []
    wpose.position.x = lidStorage[0] - 0.068
    wpose.position.y = lidStorage[1] - 0.068

    waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = move_group.compute_cartesian_path(
        waypoints, 0.01, 0.0, True)
    move_group.execute(plan, wait=True)
    print("back")

    waypoints = []
    wpose.position.z = lidStorage[2] + 0.1

    waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = move_group.compute_cartesian_path(
        waypoints, 0.01, 0.0, True)
    move_group.execute(plan, wait=True)
    print("down")
    print("")

    lid_position = move_group.get_current_joint_values()
    print("Reached Lid Stoage Position")
    print(lid_position)
    print("")

    return lid_position


def GoToScan(box, move_group):

    end = move_group.get_end_effector_link()
    wpose = move_group.get_current_pose(end).pose
    # print(wpose)

    waypoints = []
    wpose.position.z = box[2] + 0.125

    waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = move_group.compute_cartesian_path(
        waypoints, 0.01, 0.0, True)
    move_group.execute(plan, wait=True)

    waypoints = []
    wpose.position.x = box[0] + 0.005
    wpose.position.y = box[1] - 0.0032

    waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = move_group.compute_cartesian_path(
        waypoints, 0.01, 0.0, True)
    move_group.execute(plan, wait=True)
    print("Sanning Position Reached")
    print("")


def GoToLid(lid_position, move_group):

    move_group.go(lid_position)
    print("Reached Lid Storage Position")
    print("")


def PlaceLid(box, move_group):

    waypoints = []

    wpose = move_group.get_current_pose().pose
    wpose.position.z = box[2] + 0.2

    waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = move_group.compute_cartesian_path(
        waypoints, 0.01, 0.0, True)
    move_group.execute(plan, wait=True)
    print("up")

    waypoints = []
    wpose = move_group.get_current_pose().pose
    wpose.position.x = box[0] + 0.01
    wpose.position.y = box[1] - 0.0032

    waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = move_group.compute_cartesian_path(
        waypoints, 0.01, 0.0, True)
    move_group.execute(plan, wait=True)

    waypoints = []
    wpose = move_group.get_current_pose().pose

    wpose.position.z = box[2] + 0.125

    waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = move_group.compute_cartesian_path(
        waypoints, 0.01, 0.0, True)
    move_group.execute(plan, wait=True)

    print("Lid Placed")
