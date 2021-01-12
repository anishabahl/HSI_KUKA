cmake_minimum_required(VERSION 3.10.2)
project(photonfocus_camera_description)

find_package(catkin REQUIRED)
catkin_package()

install(DIRECTORY meshes DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
install(DIRECTORY urdf DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
