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
import pandas as pd
import rospy

extract_topics = {"rgb_comp": "/camera/color/image_raw/compressed",
                  "rgb": "/camera/color/image_raw",
                  "depth": "/camera/aligned_depth_to_color/image_raw",
                  "imu": "/imu/data",
                  "lidar": "/velodyne_points",
                  "3d_pose": "/backpack_3d_robot_pose",
                  "camera_pose": "/camera_pose", 
                  "image": ["/camera/color/image_raw", "/camera/aligned_depth_to_color/image_raw"]
                  }

def extract_rgb_images(bag_file, topic_names, output_directory):
    print("====== [INFO] Extracting images from {}... ======".format(bag_file))
    rgb_topic = topic_names
    bridge = CvBridge()
    
    ## make output directory
    rgb_output_directory = os.path.join(output_directory, "rgb")
    if not os.path.exists(rgb_output_directory):
        os.makedirs(rgb_output_directory)
    
    ## save csv file and image
    with rosbag.Bag(bag_file, 'r') as bag:
        color_msgs = bag.read_messages(topics=[rgb_topic])
        color_msg = next(color_msgs, None)

        while color_msg:
            color_time = color_msg[1].header.stamp
            if color_time:
                timestamp = "{}.{}".format(color_time.secs, color_time.nsecs)    
                rgb_data = bridge.imgmsg_to_cv2(color_msg[1], "bgr8")

                ## save rgb image
                filename = os.path.join(rgb_output_directory, timestamp + ".png")
                cv2.imwrite(filename, rgb_data)

                ## print progress print percentage of num / total
                print("[INFO] progress: {}/{}".format(color_msg[1].header.seq, bag.get_message_count(rgb_topic)))

                color_msg = next(color_msgs, None)

def extract_both_images(bag_file, topic_names, output_directory):
    print("====== [INFO] Extracting images from {}... ======".format(bag_file))
    rgb_topic = topic_names[0]
    depth_topic = topic_names[1]
    bridge = CvBridge()
    
    ## make output directory
    rgb_output_directory = os.path.join(output_directory, "rgb")
    if not os.path.exists(rgb_output_directory):
        os.makedirs(rgb_output_directory)
        
    depth_output_directory = os.path.join(output_directory, "depth")
    if not os.path.exists(depth_output_directory):
        os.makedirs(depth_output_directory)

    # image_output_directory = os.path.join(output_directory, "image_info")
    # if not os.path.exists(image_output_directory):
    #     os.makedirs(image_output_directory)
    
    ## save csv file and image
    with rosbag.Bag(bag_file, 'r') as bag:
        depth_msgs = bag.read_messages(topics=[depth_topic])
        color_msgs = bag.read_messages(topics=[rgb_topic])

        depth_msg = next(depth_msgs, None)
        color_msg = next(color_msgs, None)

        while depth_msg and color_msg:
            depth_time = depth_msg[1].header.stamp
            color_time = color_msg[1].header.stamp
            if depth_time == color_time:
                timestamp = "{}.{}".format(depth_time.secs, depth_time.nsecs)
            
                
                rgb_data = bridge.imgmsg_to_cv2(color_msg[1], "bgr8")
                depth_data = bridge.imgmsg_to_cv2(depth_msg[1], desired_encoding="16UC1")
                depth_data = np.array(depth_data, dtype=np.float32)
                depth_data = depth_data.flatten()/1000
                depth_data[depth_data > 5] = 0
                depth_data = depth_data.reshape(720, 1280) # 720, 1280 / 480, 848 

                # print("depth_data.shape: ", depth_data.shape)
                ## save info
                # csv_file = os.path.join(image_output_directory, timestamp + ".csv")
                # with open(csv_file, 'w') as file:
                #     writer = csv.writer(file)
                #     writer.writerow(["u", "v", "r", "g", "b", "depth"])

                #     for u in range(rgb_data.shape[0]):
                #         for v in range(rgb_data.shape[1]):
                #             b, g, r = rgb_data[u, v]
                #             depth = depth_data[u, v]
                #             writer.writerow([u, v, r, g, b, depth])

                # cv2.imshow(depth_data)
                ## save rgb image
                filename = os.path.join(rgb_output_directory, timestamp + ".png")
                cv2.imwrite(filename, rgb_data)
                
                ## save depth image in shape (640, 480, 1) and it's value is in meter
                filename = os.path.join(depth_output_directory, timestamp + ".exr")
                cv2.imwrite(filename, depth_data)
                
                
                ## print progress print percentage of num / total
                print("[INFO] progress: {}/{}".format(depth_msg[1].header.seq, bag.get_message_count(depth_topic)))
                
                depth_msg = next(depth_msgs, None)
                color_msg = next(color_msgs, None)
                
            elif depth_time < color_time:
                depth_msg = next(depth_msgs, None)
            else:
                color_msg = next(color_msgs, None)
                
def extract_pose_data(bag_file, topic_name, output_directory):
    print("====== [INFO] Extracting pose from {}... ======".format(bag_file))
    fieldnames = ['timestamp', 'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw']

    with rosbag.Bag(bag_file, 'r') as bag:
        for topic, msg, t in bag.read_messages(topics=topic_name):
            stamp = msg.header.stamp
            timestamp = "{}.{}".format(stamp.secs, stamp.nsecs)
    
            ## make directory for each timestamp
            camera_pose_output_directory = os.path.join(output_directory, "camera_pose")
            if not os.path.exists(camera_pose_output_directory):
                os.makedirs(camera_pose_output_directory)

            ## write pose data to csv file
            filename_data = os.path.join(camera_pose_output_directory, timestamp + ".csv")
            
            ## print progress print percentage of num / total. seq from "1" to total
            print("[INFO] progress: {}/{}".format(msg.header.seq, bag.get_message_count(topic_name)))
            
            with open(filename_data, mode='w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                data = {'timestamp': timestamp,
                        'tx': msg.pose.position.x,
                        'ty': msg.pose.position.y, 
                        'tz': msg.pose.position.z, 
                        'qx': msg.pose.orientation.x, 
                        'qy': msg.pose.orientation.y, 
                        'qz': msg.pose.orientation.z, 
                        'qw': msg.pose.orientation.w }
                writer.writerow(data)
                
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--id")
    parser.add_argument("--colmap", type=bool, default=False)
    args = parser.parse_args()

    bag_file_dir = "/home/drone/catkin_ws/cartographer_detailed_comments_ws/bag_file"
    output_folder = os.path.expanduser(bag_file_dir) + "/" + args.id + "/" + args.id + "/"
    
    if args.colmap == True:
        print("===colmap===")
        bag_file_path = os.path.expanduser(bag_file_dir) + "/" + args.id + "/" + args.id + ".bag"
        extract_rgb_images(bag_file_path, extract_topics["rgb"], output_folder)
    else:
        print("===meta===")
        sync_bag_file_path = os.path.expanduser(bag_file_dir) + "/" + args.id + "/" + args.id + "_sync.bag"
        extract_pose_data(sync_bag_file_path, extract_topics["camera_pose"], output_folder)
        extract_both_images(sync_bag_file_path, extract_topics["image"], output_folder)


