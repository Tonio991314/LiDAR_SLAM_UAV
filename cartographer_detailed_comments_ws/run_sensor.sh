source devel_isolated/setup.bash

# $1 : sensor
#       l : lidar
#       i : imu
#       c : camera

sensor = $1
roslaunch cartographer_ros sensor.launch sensor:=$sensor

