#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to stream images from photonfocus camera to incorporate with ROS for camera_calibration
"""
import interventionalhsi.io.photonfocus as pf
import os
import sys
sys.path.append('/opt/ros/noetic/include/')
#print(sys.path)
import cv2
import numpy as np
import interventionalhsi
import interventionalhsi.visualization.gui
import interventionalhsi.io.argparse as argparse
import rospy
import roslib
import camera_info_manager
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
from cv_bridge import CvBridge
import time

def get_settings(dir_output):
    #finding last used settings of ihsi_viewer - should have been used to obtain the white and dark references
    for file in os.listdir(dir_output):
        if file.endswith('.log'):
            source = []
            indexes = []
            with open(dir_output+'/'+file) as f:
                for line in f:
                    index = line.find("Camera settings written to")
                    if index != -1:
                        source.append(line)
                        indexes.append(index)
    print(source[-1])
    start = indexes[-1] + 27
    end = -1
    path = source[-1][start:end]
    for position, line in enumerate(open(path)):
        if position==56:
            exposure = line[13:-1]
            exposure = float(exposure)
        if position==58:
            gain = line[5:-1]
            gain = float(gain)
    return [exposure, gain]

def image_publisher(pub, image_2d, seq):
    bridge = CvBridge()
    image_2d = bridge.cv2_to_imgmsg(image_2d, '16UC1')
    image_2d.header.seq = seq 
    image_2d.header.stamp = rospy.Time.now()
    image_2d.header.frame_id = ''
    pub.publish(image_2d)

def main():
    #print('started')
    parser = argparse.ArgumentParser(
        description="iHSI Driver",
    )

    parser.add_argument(
        "-o", "--output",
        help="Specify path to output directory of ihsi_viewer",
    )
    parser.add_argument(
        "name",
        help = "From launch file",
    )
    parser.add_argument(
        "log",
        help="From launch file",
    )
    args = parser.parse_args()
    if args.output is None:
        raise ValueError("-o/--output argument required")
    dir_output = os.path.realpath(args.output)
    settings = get_settings(dir_output)
    print(settings)
    camera = interventionalhsi.io.photonfocus.Photonfocus(
        gain=settings[1],
        exposure_time=(settings[0]/1000),
        is_monitor_camera=False,
        pixel_format="Mono10",
        verbose=False,
    )
    rospy.init_node('send_images', anonymous=True)
    pub = rospy.Publisher('Camera_publisher', Image, queue_size=1)
    height = camera.height
    width = camera.width
    rate = rospy.Rate(100)
    seq = 0
    while not rospy.is_shutdown():
        nda_1d = camera.get_data()[0]
        nda = nda_1d.reshape(height, width)
        image_publisher(pub, nda, seq)
        seq += 1
        rate.sleep()
        #inf_mng.camera_info = inf_msg
    camera.terminate()

if __name__ == '__main__':
    main()
