#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import sys
import rospy
import rosbag
from message_filters import Subscriber, ApproximateTimeSynchronizer
from sensor_msgs.msg import Imu, PointCloud2, CompressedImage
from geometry_msgs.msg import PoseStamped 

def callback(imu_msg, camera_msg, pose_msg):
    timestamp = imu_msg.header.stamp
    print("Received synchronized messages from IMU, Camera and Pose.")
    bag.write('/imu/data', imu_msg, timestamp)
    # bag.write('/velodyne_points', velodyne_msg, timestamp)
    bag.write('/camera/color/image_raw/compressed', camera_msg, timestamp)
    bag.write('/backpack_3d_robot_pose', pose_msg, timestamp)


if __name__ == '__main__':

    rospy.init_node('sync_and_record_topics')
    args = sys.argv
    id = args[1]
    # Get parameter values
    bag_file = 'bag_file/' + id + '/' + id + '_aligned.bag' 

    imu_topic = rospy.get_param('~imu_topic', '/imu/data')
    # lidar_topic = rospy.get_param('~lidar_topic', '/velodyne_points')
    pose_topic = rospy.get_param('~pose_topic', '/backpack_3d_robot_pose')
    camera_topic = rospy.get_param('~camera_topic', '/camera/color/image_raw/compressed')

    bag = rosbag.Bag(bag_file, 'w')

    imu_sub = Subscriber(imu_topic, Imu)
    # velodyne_sub = Subscriber(lidar_topic, PointCloud2)
    pose_sub = Subscriber(pose_topic, PoseStamped)
    camera_sub = Subscriber(camera_topic, CompressedImage)

    print("Synchronizing ... / save to " + bag_file)
    sync = ApproximateTimeSynchronizer([imu_sub, camera_sub, pose_sub], queue_size=50, slop=0.1)
    sync.registerCallback(callback)

    rospy.spin()
    # bag.close()
