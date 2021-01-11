# HSI_KUKA 
Repository to be used in conjunction with fri_ros repository for controlling KUKA with HSI cameras. 
## Set up 
First set up as recommended in the fri_ros repository. Then use 
``` shell 
cd fri_ros_ws/src
git submodule add https://github.com/anishabahl/HSI_KUKA 
```
## To launch simulation 
Enter the following command when in fri_ros_ws folder with ROS and Moveit sourced. 
``` shell 
roslaunch med7pf_moveit_config demo_gazebo.launch
```
or: 
``` shell 
roslaunch med7pf_moveit_config moveit_planning_execution.launch sim:=true 
```

##To move in checkerboard path 
Enter the following command 
``` shell 
roslaunch checkerboard moveit_checkerboard_motion.launch #currently returns error
```
To change the path edit the checkerboard_motion.py file in HSI_KUKA/checkerboard/src. 
