#include <ros/ros.h>
#include <image_transport/image_transport.h> 
#include <cv_bridge/cv_bridge.h> 
#include <sstream>
#include <camera_info_manager/camera_info_manager.h>

camera_info_manager::CameraInfoManager caminfo(n, camera_name, camurl);

void imageCallback(const sensor_msgs::ImageConstPtr& msg, image_transport::Publisher pub_img, ros::Publisher pub_info)
{ //use camera_info_manager to create header for camera_info topic
    sensor_msgs::CameraInfo ci;
    ci.header.stamp = ros::Time::now(); 
    ci =caminfo.getCameraInfo(); 
    // publish camera_info and image_raw with camera_info_manager and image_transport 
    pub_img.publish(msg);
    pub_info.publish(ci);
}

int main(int argc, char **argv)
{ //init ros nodes, publishers and subsriber
    ros::init(argc, argv, "driver");
    ros::NodeHandle n;
    string camera_name = "camera";
    image_transport::ImageTransport it(n);
    image_transport::Publisher pub_img it.advertise(camera_name+"/image_raw", 1);
    ros::Publisher pub_info = n.advertise<sensor_msgs::CameraInfo>(camera_name+"/camera_info", 1);
    const string camurl = "";
    
    //subscribes and binds values to callback arguments with first value being substituted with message from subscribed topic
    image_transport::Subscriber sub= it.subscribe("Camera_publisher", 10, boost::bind(imageCallback, _1, image_transport::Publisher pub_img, ros::Publisher pub_info));
    ros::spin();
    return 0;
}