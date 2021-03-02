#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <image_transport/image_transport.h> 
#include <camera_info_manager/camera_info_manager.h>
#include <string>

image_transport::ImageTransport* img_transport;
camera_info_manager::CameraInfoManager *cam_info_manager; 
image_transport::CameraPublisher img_pub; 

auto imageCallback(const sensor_msgs::ImageConstPtr& msg) -> void{
    auto cam_info = cam_info_manager->getCameraInfo(); 
    cam_info.header = msg->header; 
    img_pub.publish(*msg, cam_info); 
}

int main(int argc, char **argv)
{ //init ros nodes, publishers and subsriber
    ros::init(argc, argv, "cppdriver");
    ros::NodeHandle nh;
    ros::NodeHandle private_nh("~");

    const std::string cname = "photonfocusNIR";
    const std::string url = "package://camera_calibration_nodes/configs/photonfocusNIR.yaml";

    img_transport = new image_transport::ImageTransport(nh);
    cam_info_manager = new camera_info_manager::CameraInfoManager(nh, cname, url);
    img_pub = img_transport->advertiseCamera("image_raw", 1);
    //subscribes and binds values to callback arguments with first value being substituted with message from subscribed topic
    auto img_sub = nh.subscribe("Camera_publisher", 1, imageCallback);
    ros::spin();

    delete img_transport; 
    delete cam_info_manager;
    return 0;
}