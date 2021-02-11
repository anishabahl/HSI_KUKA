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


# def initialise():
# pub = rospy.Publisher('commands', String, queue_size=10)
# rospy.init_node('send_command', anonymous=True)
def send_command():
    pub = rospy.Publisher('commands', String, queue_size=1)
    command = 'saved'
    # rospy.loginfo('sent save command')
    pub.publish(command)
#def callback(data, connected):
#     connected += 1
# def receive_notification(connected):
#     #rospy.init_node('check_camera', anonymous=True)
#     rospy.Subscriber('connection', String, callback, callback_args = connected)
#     rospy.loginfo('received connection')
#     rospy.spin()

# see other examples http://docs.ros.org/en/kinetic/api/moveit_tutorials/html/doc/move_group_python_interface/move_group_python_interface_tutorial.html
if __name__ == '__main__':
    rospy.init_node('moveit_motion_checkerboard', anonymous=True)
    #connected = 0
    name = 'med7pf_arm'
    group = moveit_commander.MoveGroupCommander(name)
    group.set_max_velocity_scaling_factor(0.01)
    pose = group.get_current_pose().pose
    send_command() #First one never works so don't expect this to save not sure why though
    # waypoints.append(copy.deepcopy(pose))
    #receive_notification(connected)
    msg = rospy.wait_for_message("connection", String)
    #print('received')
    #connected += 1
    #if connected == 1:
    pose.position.y += 0.35
    pose.position.z -= 0.1
    waypoints = []
    waypoints.append(copy.deepcopy(pose))
    plan, fraction = group.compute_cartesian_path(waypoints, eef_step=0.01, jump_threshold=0.)
    group.execute(plan)
    group.stop()
    # print('I did it')
    j = 0
    for j in range(8):
        i = 0
        print(i, j)
        send_command()
        for i in range(5):  # move along negative x
            pose.position.x -= 0.03
            waypoints = []
            waypoints.append(copy.deepcopy(pose))
            plan, fraction = group.compute_cartesian_path(waypoints, eef_step=0.01, jump_threshold=0.)
            group.execute(plan)
            group.stop()
            print(i, j)
            send_command()
            i = i + 1
            # send_command()
        pose.position.y -= 0.03
        pose.position.x += 0.15
        waypoints = []
        waypoints.append(copy.deepcopy(pose))
        plan, fraction = group.compute_cartesian_path(waypoints, eef_step=0.01, jump_threshold=0.)
        group.execute(plan)
        group.stop()
        if j == 3:
            pose.position.y -= 0.03
            waypoints = []
            waypoints.append(copy.deepcopy(pose))
            plan, fraction = group.compute_cartesian_path(waypoints, eef_step=0.01, jump_threshold=0.)
            group.execute(plan)
            group.stop()
        # send_command()
        j = j + 1

    # plan, fraction = group.compute_cartesian_path(waypoints, eef_step=0.01, jump_threshold=0.)
    # rospy.loginfo('Moving along cartesian path...')
    # group.execute(plan)
    # group.stop()
    rospy.loginfo('Done.')

    rospy.spin()
