source devel_isolated/setup.bash

# $1 : sensor
#       l : lidar
#       i : imu
#       c : camera

roslaunch cartographer_ros sensor.launch sensor:=$1

