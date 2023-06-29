# UR3_ERC_Maintenance_Stack

This repository the Maintenance Stack for the ERC Remote competition. 

## Table of Contents
1. [Requirements](#Requirements)
    1. [Download UR3 simulation](#Download-UR3-simulation)
    1. [Run simulation](#Run-simulation)
1. [Building](#building)

## Requirements

The simulation requires ROS and simulations of the Universal Robots UR3 robot created for the ERC competition
 - [ROS Noetic Ninjemys](http://wiki.ros.org/noetic/Installation/) on [Ubuntu 20.04 Focal Fossa](https://releases.ubuntu.com/20.04/)
 - [ERC-Remote-Maintenance-Sim](https://github.com/EuropeanRoverChallenge/ERC-Remote-Maintenance-Sim)

### Download UR3 simulation

For the simulation to work on your system you must install dependencies and download repositories by running the following commands:

```sh
source /opt/ros/noetic/setup.bash
sudo apt-get update && apt-get upgrade -y && apt-get install -y lsb-core g++
sudo apt-get install git
rosdep init && rosdep update
sudo apt install ros-noetic-moveit -y
sudo apt install ros-noetic-ros-controllers* -y
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
git clone -b kinetic-devel https://github.com/ros-industrial/universal_robot.git
sudo rm -r universal_robot/ur_msgs
git clone https://github.com/roboticsgroup/roboticsgroup_gazebo_plugins
git clone https://github.com/Michal-Bidzinski/UR3_sim.git
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```
### Run simulation
To run UR3 simulation in Gazebo with MoveIt!, and RVzi GUI, including an example cell:
```sh
roslaunch ur3_sim simulation.launch
```
To run UR3 simulation in Gazebo with MoveIt!, and RVzi GUI, containing only a robot with a grapple and a camera (as per real setup):
```sh
roslaunch ur3_sim real_station.launch
```

## Building
This repository contains all the competition submitions.

To clone the repo, navigate to you root directory:
```sh
cd
```
clone this repository:
```sh
git clone https://github.com/SwarajDangare/UR3_ERC_Maintenance_Stack.git
```
Navigate to the reposetory:
```sh
cd UR3_ERC_Maintenance_Stack
```
Now, use the `catkin_make` tool build the workspace:
```sh
catkin_make
```
Make sure you source the devel space on each terminal session you want to use the simulation on:
```sh
source /opt/ros/noetic/setup.bash
```
