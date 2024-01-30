source devel/setup.bash

id=$1
mode=$2 

## Topics 
## Need to record in online mode: sensor - lidar, imu
#                                 image - color_image(rgb), aligned_depth(depth) 
#                                 pose - online_camera_pose, online_2d_robot_pose

### sensor
lidar_points_topic="/velodyne_points" ## [online] --> for 3d
lidar_scan_topic="/scan" ## [online] --> for 2d
imu_topic="/imu/data" ## [online]

### image
# color_image_compress_topic="/camera/color/image_raw/compressed"
color_image_topic="/camera/color/image_raw" ## [online]
# depth_image_topic="/camera/depth/image_rect_raw/compressed" 
aligned_depth_image_topic="/camera/aligned_depth_to_color/image_raw" ## [online]

### pose
online_camera_pose="/camera_pose" ## [online]
online_2d_robot_pose="/online_2d_robot_pose" ## [online]
# offline_3d_robot_pose="/backpack_3d_robot_pose" ## [online]
# online_3d_robot_pose="/robot_pose"

## make directory
output_dir="./bag_file/${id}/"
if [ ! -d "$output_dir" ]; then
    echo "makng directory ..."
    mkdir -p "$output_dir"
    echo "directory created"
else
    echo "directory already exists"
fi

## record image
if [ $mode == 'on' ]
then
    rosbag record -O /home/drone/catkin_ws/cartographer_detailed_comments_ws/bag_file/${id}/${id}.bag $lidar_points_topic $lidar_scan_topic $imu_topic $color_image_topic $aligned_depth_image_topic
elif [ $mode == "colmap" ]
then
    rosbag record -O /home/drone/catkin_ws/cartographer_detailed_comments_ws/bag_file/${id}/${id}.bag $color_image_topic
elif [ $mode == "sync" ]
then
    rosrun data_processing record_sync_data.py $id
fi
