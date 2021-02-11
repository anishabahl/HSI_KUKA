cmake_minimum_required(VERSION 3.0.2)
project(pf_ros)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_package()

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
catkin_install_python(PROGRAMS
   scripts/ihsikuka_viewer_publisher.py
   scripts/ihsikuka_viewer_subscriber.py
   scripts/middleman.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

