#!/usr/bin/env python3

import interventionalhsi.io.photonfocus as pf
import os
import cv2
import numpy as np
import interventionalhsi
import interventionalhsi.visualization.gui
import interventionalhsi.io.argparse as argparse
import rospy
from std_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def callback(data):
    rospy.loginfo('Image received')
    bridge = CvBridge()
    nda2 = bridge.imgmsg_to_cv2(data, 'passthrough')
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.imshow('frame', nda2)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('image_publisher', Image, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()