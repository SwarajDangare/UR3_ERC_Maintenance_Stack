# UR3_ERC_Maintenance_Stack

This repository contains the Maintenance Stack for the ERC Remote competition. 

## Table of Contents
1. [Requirements](#Requirements)
    1. [Download UR3 simulation](#Download-UR3-simulation)
    1. [Run simulation](#Run-simulation)
1. [Building](#building)
1. [Running the Simulation](#Running-the-Simulation)
    1. [Launching the Objective](#Launching-the-Objective)

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
If you don’t want to have to source the setup file every time you open a new shell, then you can add the commands to your shell startup script:
```sh
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
echo "source ~/UR3_ERC_Maintenance_Stack/devel/setup.bash" >> ~/.bashrc
```
## Running the Simulation
Before running the launch file, you will need to make all the python file as excecutable.

To do that navigate to the `scripts` folder of that pakage, and run the following command
```sh
chmod +x *.py 
```
### Launching the Objective
To run the simulation, launch the `roslaunch <package_name> obj<objective_no>.launch` and parameters if any.

Example:

- objective 1
```sh
roslaunch marsrovermanipal_c obj1.launch
```
- objective 2
```sh
roslaunch marsrovermanipal_c obj2.launch tags:="1, 2, 3, 4"
```
- objective 3
```sh
roslaunch marsrovermanipal_c obj3.launch
```
- objective 4
```sh
roslaunch marsrovermanipal_c obj4.launch angle:=45
```
- objective 5
```sh
roslaunch marsrovermanipal_c obj5.launch
```
- objective 6
```sh
roslaunch marsrovermanipal_c obj6.launch
```
- objective 7
```sh
roslaunch marsrovermanipal_c obj7.launch
```
- objective 8
```sh
roslaunch marsrovermanipal_c obj8.launch
```
- objective 9
```sh
roslaunch marsrovermanipal_c obj9.launch tag:=5
```
- objective 10
```sh
roslaunch marsrovermanipal_c obj10.launch
```
