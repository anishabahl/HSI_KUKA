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
from std_msgs.msg import String
from cv_bridge import CvBridge

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

#def camera_stream(dir_output, settings = [], usedummy=0, vis='scale'):
#    #connects to dummy or camera
#    if usedummy == 1:
#        camera = interventionalhsi.io.photonfocus.PhotonfocusDummy(
#            gain = settings[1],
#            exposure_time = settings[0]/1000,
#            is_monitor_camera = False,
#            pixel_format = "Mono10",
#            verbose = False,
#        )
#    if usedummy == 0:
#        camera = interventionalhsi.io.photonfocus.Photonfocus(
#            gain=settings[1],
#            exposure_time=settings[0]/1000,
#            is_monitor_camera=False,
#            pixel_format="Mono10",
#            verbose=False,
#        )
#    height = camera.height
#    width = camera.width
#    bridge = CvBridge()
#    pub = rospy.Publisher('image_publisher', Image, queue_size=10)
#    rospy.init_node('camera_stream', anonymous=True)
#    rate = rospy.Rate(10)
#    while not rospy.is_shutdown():
#    #while (True):
#        # shows window with video stream of images
#        nda_1d = camera.get_data()[0]
#        nda = nda_1d.reshape(height, width)
#        #nda2 = nda.astype(np.float32)
#        # rescale for visualisation
#        nda2 = nda.astype(np.float32)
#        if vis=='norm':
#            nda2 = (nda2-nda2.min())/(nda2.max()-nda2.min())
#            #print([nda2.min(), nda2.max()])
#            nda2=255*nda2.astype(np.uint8)
#            #print([nda2.min(), nda2.max()])
#        if vis=='scale':
#            nda2 = ((nda2 /nda2.max())*255).astype(np.uint8)
#        if vis=='none':
#            nda2 = nda2.astype(np.uint8)
#        nda2 = bridge.cv2_to_imgmsg(nda2, 'passthrough')
#        #rospy.loginfo('Image published')
#        pub.publish(nda2)
#        rate.sleep()

        #cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        #cv2.imshow('frame', nda2)
        #saveto = '/home/ab20/Documents/testing_ihsikuka_viewer/'
        #k = cv2.waitKey(1) & 0xFF
        #if k == ord('q'): #press q to exit
        #    break
        #if k == ord('s'): #press s to save snapshot to same location - for testing is specified location
        #    saved = camera.write_snapshot(dir_output)
        #    print(saved)
#    camera.terminate()

def camera_stream(dir_output, settings = [], usedummy=0, vis='scale'):
    #connects to dummy or camera
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
    height = camera.height
    width = camera.width
    while (True):
        # shows window with video stream of images
        nda_1d = camera.get_data()[0]
        nda = nda_1d.reshape(height, width)
        #nda2 = nda.astype(np.float32)
        # rescale for visualisation
        nda2 = nda.astype(np.float32)
        if vis=='norm': #does not work I think because of region outside FOV
            nda2 = (nda2-nda2.min())/(nda2.max()-nda2.min())
            #print([nda2.min(), nda2.max()])
            nda2=255*nda2.astype(np.uint8)
            #print([nda2.min(), nda2.max()])
        if vis=='scale':
            #nda2 = (nda2/nda2.max() * 255).astype(np.uint8)
            #print([nda2.min(), nda2.max()])
            #nda2 = ((nda/ float(nda.max()))* 255).astype(np.uint8)
            nda2 = ((nda2 /nda2.max())*255).astype(np.uint8)
        if vis=='none':
            nda2 = nda2.astype(np.uint8)

        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        cv2.imshow('frame', nda2)
        #saveto = '/home/ab20/Documents/testing_ihsikuka_viewer/'
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'): #press q to exit
            break
        if k == ord('s'): #press s to save snapshot to same location - for testing is specified location
            saved = camera.write_snapshot(dir_output)
            print(saved)
    camera.terminate()

def main():
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

    if args.dummy is False:
        usedummyvalue = 0
    else:
        usedummyvalue = 1

    settings = get_settings(dir_output)
    print(settings)
    #settings = [3, 2]
    camera_stream(dir_output, settings, usedummy=usedummyvalue, vis='scale')

if __name__ == "__main__":
    main()
