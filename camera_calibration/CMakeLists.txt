cmake_minimum_required(VERSION 3.0.2)
project(camera_calibration)
find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_package()
add_executable(camera_calibration cppdriver.cpp)

catkin_install_python(PROGRAMS
   driver.py
   driver.launch
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

