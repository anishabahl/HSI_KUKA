#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to stream images from photonfocus camera to incorporate with ROS for KUKA use
"""
import interventionalhsi.io.photonfocus as pf
import os
import cv2
import numpy as np
import interventionalhsi
import interventionalhsi.visualization.gui
import interventionalhsi.io.argparse as argparse
import interventionalhsi.io.data_reader as dr
import interventionalhsi.io.data_writer as dw
import rospy
import roslib
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
from cv_bridge import CvBridge
import datetime

class SaveImages:
    def __init__(self, path):
        self.image = None
        self.path = path
        self.image_subscriber = rospy.Subscriber('images', Image, self.callback)
        #self.image_subscriber = rospy.Subscriber("/output/image_raw/compressed", CompressedImage, queue_size=10)
        self.command_subscriber = rospy.Subscriber('commands', String, self.callback2)

    def callback(self, data):
        bridge = CvBridge()
        self.image = bridge.imgmsg_to_cv2(data, '16UC1')
        #self.image = np.fromstring(data.data, np.uint16)
        #self.image = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
        #self.image = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE) #need to change this to read other types of images but for photonfocus 5x5 works

    def callback2(self, data):
        #path = args[0]
        #self.image = args[1]
        now = datetime.datetime.now()
        filename='/'+now.strftime('%Y')+now.strftime('%m')+now.strftime('%d')+'_'+now.strftime('%H')+now.strftime('%M')+now.strftime('%S')+'_'+now.strftime('%f')+'.png'
        #cv2.imwrite(output_dir+filename+'.png', self.image)
        dw.DataWriter.write_image(self.image, self.path+filename, verbose=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="iHSI KUKA Viewer",
    )

    parser.add_argument(
        "-o", "--output",
        help="Specify path to output directory of ihsi_viewer",
    )
    parser.add_argument(
        "-d", "--dummy",
        action="store_true",
        help="If given, only a dummy interface is opened.",
    )
    parser.add_argument(
        "name",
        help="From launch file",
    )
    parser.add_argument(
        "log",
        help="From launch file",
    )
    args = parser.parse_args()
    if args.output is None:
        raise ValueError("-o/--output argument required")
    dir_output = os.path.realpath(args.output)

    if args.dummy is False:
        usedummy = 0
    else:
        usedummy = 1
    rospy.init_node('listener', anonymous=True)
    SaveImages(path=dir_output)
    rospy.spin()