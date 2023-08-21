#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import sys
import rospy
import rosbag
from message_filters import Subscriber, ApproximateTimeSynchronizer
from sensor_msgs.msg import Imu, PointCloud2, CompressedImage

def callback(imu_msg, camera_msg):
    timestamp = imu_msg.header.stamp
    print("Received synchronized messages from IMU, Velodyne, and Camera.")
    bag.write('/imu/data', imu_msg, timestamp)
    # bag.write('/velodyne_points', velodyne_msg, timestamp)
    bag.write('/camera/color/image_raw/compressed', camera_msg, timestamp)

if __name__ == '__main__':
    rospy.init_node('sync_and_record_topics')
    args = sys.argv

    # Get parameter values
    bag_file = 'bag_file/' + args[1] + '.bag'
    imu_topic = rospy.get_param('~imu_topic', '/imu/data')
    lidar_topic = rospy.get_param('~lidar_topic', '/velodyne_points')
    camera_topic = rospy.get_param('~camera_topic', '/camera/color/image_raw/compressed')

    bag = rosbag.Bag(bag_file, 'w')

    imu_sub = Subscriber(imu_topic, Imu)
    velodyne_sub = Subscriber(lidar_topic, PointCloud2)
    camera_sub = Subscriber(camera_topic, CompressedImage)

    print("Synchronizing ... / save to " + bag_file)
    sync = ApproximateTimeSynchronizer([imu_sub, camera_sub], queue_size=10, slop=0.1)
    sync.registerCallback(callback)

    rospy.spin()
    bag.close()
