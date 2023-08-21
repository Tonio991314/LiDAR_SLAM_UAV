#!/usr/bin/env python

import rospy
from sensor_msgs.msg import PointCloud2, CompressedImage, Imu
import message_filters

def callback(camera_sub, imu_msg):
    print("Received synchronized messages from Camera, and IMU.")

if __name__ == '__main__':
    
    print("Starting message sync node...")  
    rospy.init_node('sync_data')

    # lidar_sub = message_filters.Subscriber('/velodyne_points', PointCloud2)
    camera_sub = message_filters.Subscriber('/camera/color/image_raw/compressed', CompressedImage)
    imu_sub = message_filters.Subscriber('/imu/data', Imu)

    sync = message_filters.ApproximateTimeSynchronizer([camera_sub, imu_sub], 2, 1) #queue size
    sync.registerCallback(callback)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
