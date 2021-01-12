cmake_minimum_required(VERSION 3.10.2)
project(med7pf_gazebo)

find_package(catkin REQUIRED)
catkin_package()

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
install(DIRECTORY worlds DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
