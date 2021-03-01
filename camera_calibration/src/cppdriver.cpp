#include <ros/ros.h>
#include <image_transport/image_transport.h> 
#include <cv_bridge/cv_bridge.h> 
#include <sstream>
#include <camera_info_manager/camera_info_manager.h>
#include <iostream>
#include <string>

void imageCallback(const sensor_msgs::ImageConstPtr& msg, image_transport::Publisher pub_img, ros::Publisher pub_info, camera_info_manager::CameraInfoManager& caminfo, sensor_msgs::CameraInfo& ci)
{ //use camera_info_manager to create header for camera_info topic
    //int height = sizeof(msg);
    //int width = sizeof(msg[0]);
    //sensor_msgs::CameraInfo ci;
    //ci = caminfo.getCameraInfo();
    ci.header.stamp = ros::Time::now(); 
    //ci.header.frame_id = "";
    //ci.header.height = height; 
    //ci.header.width = width;
    ci.distortion_model = "plumb_bob";
    caminfo.setCameraInfo(ci);
    // publish camera_info and image_raw with camera_info_manager and image_transport 
    pub_img.publish(msg);
    pub_info.publish(ci);
}

int main(int argc, char **argv)
{ //init ros nodes, publishers and subsriber
    ros::init(argc, argv, "driver");
    ros::NodeHandle n;
    const std::string camera_name = "photonfocusNIR";
    image_transport::ImageTransport it(n);
    image_transport::Publisher pub_img=it.advertise(camera_name+"/image_raw", 1);
    ros::Publisher pub_info = n.advertise<sensor_msgs::CameraInfo>(camera_name+"/camera_info", 1);
    const std::string camurl = "";
    camera_info_manager::CameraInfoManager caminfo(n, camera_name, camurl);
    sensor_msgs::CameraInfo ci;
    caminfo.loadCameraInfo(camurl);
    ci =caminfo.getCameraInfo();
    //subscribes and binds values to callback arguments with first value being substituted with message from subscribed topic
    image_transport::Subscriber sub= it.subscribe("Camera_publisher", 10, boost::bind(imageCallback, _1, pub_img, pub_info, caminfo, ci));
    ros::spin();
    return 0;
}