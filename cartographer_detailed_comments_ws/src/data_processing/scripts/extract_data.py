#!/usr/bin/env python

import rosbag
import os
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import PoseStamped
from cv_bridge import CvBridge
import cv2
import argparse
import numpy as np
import logging
import sys
import csv

extract_topics = {"rgb_comp": "/camera/color/image_raw/compressed",
                  "rgb": "/camera/color/image_raw",
                  "rgb_align_depth": "/camera/aligned_depth_to_color/image_raw",
                  "depth": "/camera/depth/image_rect_raw/compressedDepth",
                  "imu": "/imu/data",
                  "lidar": "/velodyne_points",
                  "3d_pose": "/backpack_3d_robot_pose",
                  }

def extract_images(bag_file, type, topic_name, output_directory):
    bridge = CvBridge()
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with rosbag.Bag(bag_file, 'r') as bag:
        for topic, msg, t in bag.read_messages(topics=topic_name):

            stamp = msg.header.stamp
            timestamp = "{}.{}".format(stamp.secs, stamp.nsecs)

            if type == "rgb_comp":
                arr = np.fromstring(msg.data, np.uint8)
                image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            elif type == "rgb":   
                image = bridge.imgmsg_to_cv2(msg, "bgr8")
            elif type == "rgb_align_depth":
                bridge = CvBridge()
                depth_image = bridge.imgmsg_to_cv2(msg, desired_encoding="16UC1")
                depth_values = np.array(depth_image, dtype=np.float32) # Access the depth values (in millimeters)
                temp = depth_values.flatten()/1000
                temp[temp >= 10] = 0
                result = np.any(temp >= 10)

                # To show depth image
                # reshaped_depth_array = temp.reshape(480, 640)
                # depth_image = np.array(reshaped_depth_array, dtype=np.float32)
                # depth_image /= depth_image.max()  # Normalize depth values for visualization
                # depth_image = 255 * depth_image  # Scale to 8-bit range
                # depth_image = depth_image.astype(np.uint8)
                # cv2.imshow("Depth Image", depth_image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                
            # filename = os.path.join(output_directory, "image_" + timestamp + ".jpg")
            # print(image.shape)
            # cv2.imwrite(filename, image)
            # logging.info(image.shape)
            # logging.info("Saving {}".format(filename))

def extract_pose_data(bag_file, topic_name, output_directory):
    
    fieldnames = ['timestamp', 'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw']
    with rosbag.Bag(bag_file, 'r') as bag:
        for topic, msg, t in bag.read_messages(topics=topic_name):
            stamp = msg.header.stamp
            timestamp = "{}.{}".format(stamp.secs, stamp.nsecs)

            ## make directory for each timestamp
            output_directory_timestamp = os.path.join(output_directory, timestamp)
            if not os.path.exists(output_directory_timestamp):
                os.makedirs(output_directory_timestamp)

            ## write pose data to csv file
            filename = os.path.join(output_directory_timestamp, timestamp + ".csv")
            with open(filename, mode='w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'tx': msg.pose.position.x, 'ty': msg.pose.position.y, 'tz': msg.pose.position.z, 
                                'qx': msg.pose.orientation.x, 'qy': msg.pose.orientation.y, 'qz': msg.pose.orientation.z, 'qw': msg.pose.orientation.w})

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--id")
    parser.add_argument("--type", default="rgb")
    args = parser.parse_args()

    bag_file_path = os.path.expanduser("~/catkin_ws/cartographer_detailed_comments_ws/bag_file/") + args.id + "/" + args.id + ".bag"
    topic_to_extract = extract_topics[args.type]
    output_folder = os.path.expanduser("~/catkin_ws/cartographer_detailed_comments_ws/bag_file/") + args.id + "/" + args.type
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    if args.type == "pose":
        extract_pose_data(bag_file_path, topic_to_extract, output_folder)
    else:   
        extract_images(bag_file_path, args.type, topic_to_extract, output_folder)



    