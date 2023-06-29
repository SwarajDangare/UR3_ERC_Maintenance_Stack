#!/usr/bin/env python3
from multiprocessing.connection import wait
import sys
import rospy
from arucoPos import *
from erc_aruco_msg.srv import ErcArucoRequest, ErcArucoResponse, ErcAruco
import tf2_geometry_msgs
import moveit_commander 
import multiprocessing
import threading
import copy
from geometry_msgs.msg import Pose, Point, Quaternion
from math import pi
from buttons import *
import moveit_msgs.msg
from buttons import *
from std_msgs.msg import String


group_name = "manipulator"
pose_goal = Pose()
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('ur3_move',anonymous=True)
move_group =moveit_commander.MoveGroupCommander(group_name) 
robot = moveit_commander.RobotCommander()
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory,queue_size=20)
def setPosePlan(pose):
    move_group.clear_pose_targets()
    pose_goal = Pose()
    pose_goal.position.x = pose[0][0] -.22
    pose_goal.position.y = pose[0][1]
    pose_goal.position.z = pose[0][2]
    pose_goal.orienation.x = pose[1][0]
    pose_goal.orienation.y = pose[1][1]
    pose_goal.orienation.z = pose[1][2]
    pose_goal.orienation.w = pose[1][3]
    move_group.set_pose_target(pose_goal) 
    return move_group.plan()
def begin():
    print('in begin')
    start = move_group.get_current_joint_values()
    move_group.go(up())
    move_group.go(scan0())
    move_group.go(scan1())
    move_group.go(scan2())
    move_group.go(scan3())
    #eef = move_group.get_current_pose(end_effector_link="camera_pose")
    # while not rospy.is_shutdown():
    #     waypoints = []
    #     wpose = move_group.get_current_pose().pose
    #     scale=float(input("Enter X Scale:"))
    #     wpose.position.x += scale * 0.01 
    #     scale=float(input("Enter Y Scale:"))
    #     wpose.position.y += scale * 0.01 
    #     scale=float(input("Enter Z Scale:"))
    #     wpose.position.z += scale * 0.01 
    #     waypoints.append(copy.deepcopy(wpose))


    #     (plan, fraction) = move_group.compute_cartesian_path(
    #     waypoints, 0.01, 0.0  
    #     )  
    #     move_group.execute(plan, wait=True)
    #     print(move_group.get_current_pose().pose)

    # moveit_commander.roscpp_shutdown()
def killer(toKill, aruco):
    print('in Killer')
    while True:
        if(len(aruco.aruco)>13):
            rospy.wait_for_service("erc_aruco_score")
        try:
            service_proxy = rospy.ServiceProxy('erc_aruco_score',ErcAruco)
            # create object of the request type for the Service (14 tags)
            service_msg = ErcArucoRequest()

            service_msg.tag1=aruco.aruco[1][0]
            service_msg.tag2=aruco.aruco[2][0]
            service_msg.tag3=aruco.aruco[3][0]
            service_msg.tag4=aruco.aruco[4][0]
            service_msg.tag5=aruco.aruco[5][0]
            service_msg.tag6=aruco.aruco[6][0]
            service_msg.tag7=aruco.aruco[7][0]
            service_msg.tag8=aruco.aruco[8][0]
            service_msg.tag9=aruco.aruco[9][0]
            service_msg.tag10=aruco.aruco[10][0]
            service_msg.tag11=aruco.aruco[11][0]
            service_msg.tag12=aruco.aruco[12][0]
            service_msg.tag13=aruco.aruco[13][0]
            service_msg.tag14=aruco.aruco[14][0]

            # call the service with your message through service proxy
            # and receive the response, which happens to be your score
            service_response = service_proxy(service_msg)
            print(f"You received score {service_response.score}")
        except rospy.ServiceException as e:
            print(f"Service call failed: {e}")
        
        press_buttons = list(map(int,rospy.get_param('~tags').split(',')))
        pub = rospy.Publisher('gripper_command', String, queue_size=10)
        pub.publish("close")
        for i in press_buttons:
            move_group.execute(setPosePlan(aruco.aruco[i]),wait=True)
            waypoints = []
            wpose = move_group.get_current_pose().pose
            wpose.position.x += 5.5 * 0.01 
            (plan, fraction) = move_group.compute_cartesian_path(waypoints, 0.01, 0.0 )  
            move_group.execute(plan, wait=True)
        break
aruco = arucoPos()
t1 = threading.Thread(target=aruco.exec)
t2 = threading.Thread(target=begin)
t3 = threading.Thread(target=killer, args=(t1, aruco))
t1.start()
t2.start()
t3.start()
print(aruco.aruco)

