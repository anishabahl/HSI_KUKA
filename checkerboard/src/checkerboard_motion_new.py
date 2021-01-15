#!/usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi 
from std_msgs.msg import String 
from moveit_commander.conversions import pose_to_list 
from geometry_msgs.msg import PoseStamped
import math
import copy

# see other examples http://docs.ros.org/en/kinetic/api/moveit_tutorials/html/doc/move_group_python_interface/move_group_python_interface_tutorial.html
if __name__ == '__main__':
    rospy.init_node('moveit_motion_checkerboard')

    name = 'med7pf_arm'
    group = moveit_commander.MoveGroupCommander(name)
    group.set_max_velocity_scaling_factor(0.01)

    # move to a named target
    target = 'home'
    group.set_named_target(target)
    rospy.loginfo('Moving to named target "{}"...'.format(target))
    group.go()
    group.stop()
    rospy.loginfo('Done.')   

    # move to joint position
    current_joint_position = group.get_current_joint_values()
    #current_joint_position[1] += math.pi/3.
    #current_joint_position[3] -= math.pi/3.
    #current_joint_position[5] += math.pi/3.
    current_joint_position[3] -= math.pi/2.
    current_joint_position[5] += math.pi/2.
    rospy.loginfo('Moving to joint goal...')
    group.go(current_joint_position)
    group.stop()
    rospy.loginfo('Done.')

    # point to point motion (PTP)
    pose = group.get_current_pose().pose
    rospy.loginfo('Pose.')
    waypoints = []
    pose.position.y += 0.31
    pose.position.z -= 0.1
    waypoints.append(copy.deepcopy(pose))
    j = 0
    for j in range(8): 
        i = 0 
        for i in range(5):# move along negative x
    	    pose.position.x -= 0.03
    	    waypoints.append(copy.deepcopy(pose))
    	    i = i+1
        if j == 3:
            pose.position.y -= 0.03
            waypoints.append(copy.deepcopy(pose))
        pose.position.y -= 0.03
        pose.position.x += 0.15
        waypoints.append(copy.deepcopy(pose))
        j = j+1

    plan, fraction = group.compute_cartesian_path(waypoints, eef_step=0.01, jump_threshold=0.)
    rospy.loginfo('Moving along cartesian path...')
    group.execute(plan)
    group.stop()
    rospy.loginfo('Done.')

    # move to a named target
    target = 'home'
    group.set_named_target(target)
    rospy.loginfo('Moving to named target "{}"...'.format(target))
    group.go()
    group.stop()
    rospy.loginfo('Done.')    

    rospy.spin()
