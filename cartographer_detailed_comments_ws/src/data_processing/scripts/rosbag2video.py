#!/usr/bin/env python

import rosbag
import cv2
import argparse
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import os

def extract_images_to_video(bag_id):
    bag_file_dir = "/home/drone/catkin_ws/cartographer_detailed_comments_ws/bag_file"
    # bag_path = os.path.join(bag_file_dir, bag_id, bag_id + "_sync.bag") ## sync
    bag_path = os.path.join(bag_file_dir, bag_id, bag_id + ".bag") ## not sync
    video_path = os.path.join(bag_file_dir, bag_id, bag_id, "output_video.mp4")

    topic_name = "/camera/color/image_raw"

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = None

    # Initialize the cv bridge
    bridge = CvBridge()

    with rosbag.Bag(bag_path, 'r') as bag:
        for topic, msg, t in bag.read_messages(topics=[topic_name]):
            # Convert ROS Image message to OpenCV image
            cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # If the video writer has not been initialized, do it now
            if video_writer is None:
                h, w = cv_image.shape[:2]
                video_writer = cv2.VideoWriter(video_path, fourcc, 30, (w, h))
            
            video_writer.write(cv_image)

    if video_writer is not None:
        video_writer.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag file and convert to a video.")
    parser.add_argument("--id", type=str, help="ID of the bag file (e.g., 231022_1)")

    args = parser.parse_args()
    extract_images_to_video(args.id)
