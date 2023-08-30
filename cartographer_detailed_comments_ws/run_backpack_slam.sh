source devel_isolated/setup.bash

type=$1 # 2D or 3D
mode=$2
bag_file_path=$3

IFS="/"
read -ra bag_file_paths <<< "$bag_file_path"
id="${bag_file_paths[-2]}"
bag_file="${bag_file_paths[-1]}"


######### main #########
if [ $type == '3d' ]
then
    if [ $mode == 'off' ]
    then 
        roslaunch cartographer_ros offline_3d.launch id:=$id bag_filenames:=$bag_file
    elif [ $mode == 'on' ]
    then 
        roslaunch cartographer_ros demo_backpack_online_3d.launch id:=$id bag_filename:=$bag_file
    fi
elif [ $type == '2d' ]
then
    if [ $mode == 'off' ]
    then 
        roslaunch cartographer_ros offline_2d.launch id:=$id bag_filenames:=$bag_file
    # elif [ $mode == 'on' ]
    # then 
    #     roslaunch cartographer_ros demo_backpack_online_2d.launch id:=$id bag_filename:=$bag_file
    fi
fi