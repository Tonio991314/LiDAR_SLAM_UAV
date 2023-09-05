source devel/setup.bash


id=$1
mode=$2 

$lidar_topic="/velodyne_points"
$imu_topic="/imu/data"
$color_image_topic="/camera/color/image_raw/compressed"
$depth_image_topic="/camera/depth/image_rect_raw/compressed"
$online_2d_robot_pose="/online_2d_robot_pose"

## make directory
output_dir="./bag_file/$id/"
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
    rosbag record -O /bag_file/$id/${id}.bag $lidar_topic $imu_topic $color_image_topic $depth_image_topic $online_2d_robot_pose
elif [ $mode == "off" ]
then
    rosrun data_processing record_sync_data.py $id
fi
