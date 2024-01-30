import rosbag
from sensor_msgs.msg import Image

bag_file_path = '/home/drone/catkin_ws/cartographer_detailed_comments_ws/bag_file/ver1_test_data/ver1_test_data_sync.bag'
depth_topic = '/camera/aligned_depth_to_color/image_raw'
color_topic = '/camera/color/image_raw'

with rosbag.Bag(bag_file_path, 'r') as bag:
    depth_msgs = bag.read_messages(topics=[depth_topic])
    color_msgs = bag.read_messages(topics=[color_topic])

    depth_msg = next(depth_msgs, None)
    color_msg = next(color_msgs, None)

    while depth_msg and color_msg:
        depth_time = depth_msg[1].header.stamp
        color_time = color_msg[1].header.stamp

        if depth_time == color_time:
            # Now you have a matching pair of messages!
            # Process or store them as required.
            # For example:
            
            print("Matching timestamp: " + str(depth_time))

            depth_msg = next(depth_msgs, None)
            color_msg = next(color_msgs, None)
        
        elif depth_time < color_time:
            depth_msg = next(depth_msgs, None)
        else:
            color_msg = next(color_msgs, None)
