#!/usr/bin/env python

import rospy
from nav_msgs.msg import OccupancyGrid
import plot_map 


def callback(data):
    rospy.loginfo("width: %d, height: %d", data.info.width, data.info.height)
    # rospy.loginfo("origin: %f, %f", data.info.origin.position.x, data.info.origin.position.y)
    # rospy.loginfo(type(data.data)) # tuple
    # rospy.loginfo("data length: %d", len(data.data))

def draw_map(data):
    plot = plot_map.Plotting(data)
    plot.plot_map()

def map_listener():
    rospy.init_node('map_listener', anonymous=True)
    rospy.Subscriber("/map", OccupancyGrid, draw_map)
    rospy.spin()

if __name__ == '__main__':
    map_listener()
