#!/usr/bin/env python

import rosbag
import os
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2
import argparse
import numpy as np
import logging


extract_topics = {"rgb": "/camera/color/image_raw/compressed",
                  "depth": "/camera/depth/image_rect_raw/compressedDepth",
                  "imu": "/imu/data",
                  "lidar": "/velodyne_points",
                  }

def extract_images(bag_file, topic_name, output_directory):
    bridge = CvBridge()
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with rosbag.Bag(bag_file, 'r') as bag:
        for topic, msg, t in bag.read_messages(topics=topic_name):

            stamp = msg.header.stamp
            timestamp = "{}.{}".format(stamp.secs, stamp.nsecs)

            arr = np.fromstring(msg.data, np.uint8)
            image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            filename = os.path.join(output_directory, "image_" + timestamp + ".jpg")

            cv2.imwrite(filename, image)

            logging.info("Saving {}".format(filename))


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--id")
    parser.add_argument("--data", default="rgb")
    args = parser.parse_args()

    bag_file_path = os.path.expanduser("~/catkin_ws/cartographer_detailed_comments_ws/bag_file/") + args.id + "/" + args.id + ".bag"
    topic_to_extract = extract_topics[args.data]
    output_folder = os.path.expanduser("~/catkin_ws/cartographer_detailed_comments_ws/bag_file/") + args.id + "/" + args.data
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if args.data == "rgb":
        extract_images(bag_file_path, topic_to_extract, output_folder)



    