source devel/setup.bash


mode=$1
id=$2
 
# IFS="/"
# read -ra bag_file_paths <<< "$bag_file_path"
# id="${bag_file_paths[-2]}"


#!/bin/bash
# conda activate base
# !! DON'T ACTIVATE ANY ENV, IT WILL CAUSE ERROR !!

rosbag reindex "./bag_file/$id/${id}_sync.bag"

if [ $mode == 'meta' ]
then 
    rosrun data_processing extract_data.py --id $id
elif [ $mode == 'colmap' ]
then 
    rosrun data_processing extract_data.py --id $id --colmap true
elif [ $mode == 'video' ]
then 
    rosrun data_processing rosbag2video.py --id $id
fi