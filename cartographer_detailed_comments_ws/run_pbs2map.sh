source devel_isolated/setup.bash

# bag_file_path=$1
# pose_graph_path=$2

# IFS="/"
# read -ra bag_file_paths <<< "$bag_file_path"
# read -ra pose_graph_paths <<< "$pose_graph_path"

# id="${bag_file_paths[-2]}"
# bag_file="${bag_file_paths[-1]}"
# pose_graph_file="${pose_graph_paths[-1]}"

id=$1
bag_file_path="/home/drone/catkin_ws/cartographer_detailed_comments_ws/bag_file/$id/$id.bag"
pose_graph_path="/home/drone/catkin_ws/cartographer_detailed_comments_ws/bag_file/$id/$id.bag.pbstream"

######### make directory #########
folder_path="/home/drone/catkin_ws/cartographer_detailed_comments_ws/bag_file/$id/map"
if [ ! -d "$folder_path" ]; then
    echo "makng directory ..."
    mkdir -p "$folder_path"
    echo "directory created"
else
    echo "directory already exists"
fi

######### main #########
roslaunch cartographer_ros pbs2map.launch id:=$id bag_filenames:=$bag_file_path pose_graph_filename:=$pose_graph_path

