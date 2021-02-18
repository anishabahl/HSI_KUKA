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
import rospy
import roslib
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

def notify_connection(pub):
    #pub = rospy.Publisher('connection', String, queue_size=10)
    command = 'connected'
    # rospy.loginfo('sent save command')
    pub.publish(command)
    #print('notified')

def send_image(pub2, image_2d):
    #pub2 = rospy.Publisher('images', Image, queue_size=10)
    #pub2 = rospy.Publisher('images', CompressedImage, queue_size=10)
    #pub2 = rospy.Publisher("/output/image_raw/compressed", CompressedImage, queue_size=10)
    bridge = CvBridge()
    #image_2d = cv2.resize(image_2d, (2, 2))
    image_2d = bridge.cv2_to_imgmsg(image_2d, '16UC1')
    #msg = CompressedImage()
    #msg.header.stamp = rospy.Time.now()
    #msg.format = "png"
    #msg.data = np.array(cv2.imencode('.jpg', image_2d)[1]).tostring()
    pub2.publish(image_2d)

def main():
    #print('started')
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
    #print('got path')
    if args.dummy is False:
        usedummy = 0
    else:
        usedummy = 1
    #print(usedummy)
    settings = get_settings(dir_output)
    print(settings)
    if usedummy == 1:
        camera = interventionalhsi.io.photonfocus.PhotonfocusDummy(
            gain = settings[1],
            exposure_time = (settings[0]/1000),
            is_monitor_camera = False,
            pixel_format = "Mono10",
            verbose = False,
        )
    if usedummy == 0:
        camera = interventionalhsi.io.photonfocus.Photonfocus(
            gain=settings[1],
            exposure_time=(settings[0]/1000),
            is_monitor_camera=False,
            pixel_format="Mono10",
            verbose=False,
        )
    start = time.time_ns()
    rospy.init_node('send_images', anonymous=True)
    print('Time passed: {}s'.format((time.time_ns() - start) * 1.e-9))
    pub = rospy.Publisher('connection', String, queue_size=10)
    pub2 = rospy.Publisher('images', Image, queue_size=10)
    #pub2 = rospy.Publisher('images', Image, queue_size=10)
    height = camera.height
    width = camera.width
    #while (True):
    rate = rospy.Rate(100)
    #notify_connection()
    i = 0
    while not rospy.is_shutdown():
        nda_1d = camera.get_data()[0]

        nda = nda_1d.reshape(height, width)
        #start = time.time_ns()
        send_image(pub2, nda)
        #print('Time passed: {}s'.format((time.time_ns() - start) * 1.e-9))
        # rescale for visualisation
        nda2 = nda.astype(np.float32)
        nda2 = ((nda2 / nda2.max()) * 255).astype(np.uint8)
        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        cv2.imshow('frame', nda2)
        k = cv2.waitKey(1) & 0xFF
        if i > 100:
            notify_connection(pub)
        i += 1
        # save_image(camera, dir_output)
        #rospy.spin()
        rate.sleep()
    camera.terminate()

if __name__ == '__main__':
    main()