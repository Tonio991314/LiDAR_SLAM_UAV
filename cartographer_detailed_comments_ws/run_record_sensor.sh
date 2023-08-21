source devel_isolated/setup.bash

# $1: sensor
#       l : lidar
#       i : imu
#       c : camera
#       n : none
# $2: mode
#       r : record to $2
#       else : no record
# $3 file_name
#
# Example: ./run_record.sh lic r test.bag -> open lidar, imu, camera and record to test.bag

roslaunch cartographer_ros sensor.launch sensor:=$1 mode:=$2 file_name:=$3
