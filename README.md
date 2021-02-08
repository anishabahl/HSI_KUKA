# HSI_KUKA 
Repository to be used in conjunction with fri_ros and InterventionalHSI repositories for controlling KUKA with HSI cameras. 
## Set up 
First set up as recommended in the fri_ros repository. Then use 
``` shell 
cd fri_ros_ws/src
git submodule add https://github.com/anishabahl/HSI_KUKA 
```
## To launch simulation 
Enter the following command when in fri_ros_ws folder with ROS and Moveit sourced.  
``` shell 
roslaunch med7pf_moveit_config moveit_planning_execution.launch sim:=true 
```
## To obtain checkerboard data 
Open a second terminal and source as above. Run the following command to move to the initial position. 
``` shell 
roslaunch checkerboard moveit_initial_motion.launch 
```
Open a third terminal and run the ihsi_viewer from the InterventionalHSI repository using the -o option to save to a specified destination (also use -d if simulating or --overwrite to overwrite existing folder.) Set exposure and gain/auto-adjust parameters. Close this viewer/terminal. 

Open a new terminal and source as before. Run the following command to move across the checkerboard and save images at each location using the settings from the ihsi_viewer: 
``` shell 
roslaunch nodes nodes.launch my_args:="same arguments as ihsi_viewer"
```
Note that the path passed to my_args must be absolute and identical to that used with the -o option in ihsi_viewer. 

## To change path 
Change checkerboard_publisher.py file in HSI_KUKA/checkerboard/src

