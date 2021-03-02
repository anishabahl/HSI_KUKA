# Calibrating camera 
## Setting up nodes
Use camera_calibration_nodes folder and modify python file to connect to correct camera, and cpp and launch file to set correct camera name (eg. photonfocusNIR). Before using ensure catkin_make command has been run. 
## Running nodes 
First use the ihsi_viewer to set the camera settings as described in the README. Open a terminal and source the ROS distribution. Run the command roscore to start the ros interface. Open a second terminal in a similar way and run the following command: 
``` shell 
roslaunch camera_calibration_nodes driver.launch my_args:="args for ihsi_viewer"
```
##camera_calibration package 
Follow this tutorial: http://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration but substitute 'camera' for the camera name used in the cpp and launch file (eg. photonfocusNIR). 
##Eye-in-hand calibration
Use the MoveIt! package to perform an eye-in-hand calibration of the Kuka with the camera as shown in this link: https://ros-planning.github.io/moveit_tutorials/doc/hand_eye_calibration/hand_eye_calibration_tutorial.html#:~:text=The%20MoveIt%20Calibration%20package%20provides,eye%2Din%2Dhand).
