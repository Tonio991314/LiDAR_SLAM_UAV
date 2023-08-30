source devel_isolated/setup.bash

type=$1

if [ $type == '2d' ]
then 
    roslaunch cartographer_ros online_2d.launch
elif [ $type == '3d' ]
then
    roslaunch cartographer_ros online_3d.launch
fi