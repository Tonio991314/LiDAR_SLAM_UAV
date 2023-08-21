source devel/setup.bash

bag_name=$1
rosrun sync_data sync_data.py $bag_name
