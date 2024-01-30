#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import sys
import rospy
import rosbag
from message_filters import Subscriber, ApproximateTimeSynchronizer, TimeSynchronizer
from sensor_msgs.msg import Imu, PointCloud2, CompressedImage, Image
from geometry_msgs.msg import PoseStamped 
import os

def callback(rgb_msg, depth_msg, camera_pose_msg):
    timestamp = camera_pose_msg.header.stamp
    print("Received synchronized messages !!!")
    # bag.write('/imu/data', imu_msg, timestamp)
    # bag.write('/velodyne_points', velodyne_msg, timestamp)
    bag.write('/camera/color/image_raw', rgb_msg, timestamp)
    bag.write('/camera/aligned_depth_to_color/image_raw', depth_msg, timestamp)
    bag.write('/camera_pose', camera_pose_msg, timestamp)
    # bag.write('/backpack_3d_robot_pose', robot_pose_msg, timestamp)


if __name__ == '__main__':

    rospy.init_node('sync_and_record_topics')
    args = sys.argv
    id = args[1]
    # Get parameter values
    
    ## check if "/bag_file/id/id/" exists, if not, then make it
    output_directory = 'bag_file/' + id + '/'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    bag_file = os.path.join(output_directory, id + '_sync.bag') 

    # imu_topic = rospy.get_param('~imu_topic', '/imu/data')
    # lidar_topic = rospy.get_param('~lidar_topic', '/velodyne_points')
    # robot_pose_topic = rospy.get_param('~robot_pose_topic', '/backpack_3d_robot_pose')
    camera_pose_topic = rospy.get_param('~camera_pose_topic', '/camera_pose')
    rgb_topic = rospy.get_param('~rgb_topic', '/camera/color/image_raw')
    depth_topic = rospy.get_param('~depth_topic', '/camera/aligned_depth_to_color/image_raw')

    bag = rosbag.Bag(bag_file, 'w')

    # imu_sub = Subscriber(imu_topic, Imu)
    # velodyne_sub = Subscriber(lidar_topic, PointCloud2)
    # robot_pose_sub = Subscriber(robot_pose_topic, PoseStamped)
    camera_pose_sub = Subscriber(camera_pose_topic, PoseStamped)
    rgb_sub = Subscriber(rgb_topic, Image)
    depth_sub = Subscriber(depth_topic, Image)


    print("Synchronizing ... / save to " + bag_file)
    # sync = TimeSynchronizer([rgb_sub, depth_sub, camera_pose_sub, robot_pose_sub], queue_size=30)
    sync = ApproximateTimeSynchronizer([rgb_sub, depth_sub, camera_pose_sub], queue_size=30, slop=0.0008)
    sync.registerCallback(callback)

    rospy.spin()
    # bag.close()
