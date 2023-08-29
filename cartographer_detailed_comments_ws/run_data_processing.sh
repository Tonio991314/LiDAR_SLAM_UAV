source devel/setup.bash

bag_file_path=$1
data=$2 # data type to extract, e.g. rgb, imu, lidar


IFS="/"
read -ra bag_file_paths <<< "$bag_file_path"
id="${bag_file_paths[-2]}"


rosrun data_processing extract_data.py --id $id --data "$data"
