#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Cesar Sinchiguano <cesarsinchiguano@hotmail.es>
#
# Distributed under terms of the MIT license.

"""
Inspired by MoveIt tutorial
"""
#from ur10_class_01 import *

import sys
sys.path.insert(0, '/home/casch/ws_moveit/src/perception_cvut/src/project')
from ur10_class import *
import tf
import tf2_ros
from tf.transformations import *




def move(object_robot):
    import time
    global g_index_last_move
    global g_timestamp_last_move
    global poses

    if (time.time() - g_timestamp_last_move) < 5:
        return

    g_index_last_move = (g_index_last_move + 1) % len(poses)

    object_robot.go_to_pose_goal(poses[g_index_last_move])

    print('g_index_last_move {}'.format(g_index_last_move))

    g_timestamp_last_move = time.time()

def main():
    global home

    br = tf2_ros.TransformBroadcaster()
    r=rospy.Rate(10)

    #Task space
    ##########
    print "============ Press `Enter` to go to --> Home position..."
    raw_input()
    object_ur10.go_to_pose_goal(home)
    #time.sleep(3)
    print "============ Press `Enter` to start start sample poses..."
    raw_input()

    while(not rospy.is_shutdown()):
        try:
            move(object_ur10)
            pose_TCP=object_ur10.move_group.get_current_pose().pose
            print "============ Python movement is completed!"
            r.sleep()
        except rospy.ROSInterruptException:
            return
        except KeyboardInterrupt:
            return

if __name__ == '__main__':
    print ""
    print "----------------------------------------------------------"
    print "Welcome to the MoveIt MoveGroup Python Interface"
    print "----------------------------------------------------------"
    print "Press Ctrl-D to exit at any time"
    print ""
    print "============ Press `Enter` to begin the moveit_commander ..."
    raw_input()
    #create an object in order to get acces to my UniversalRobot
    object_ur10 = UniversalRobot()
    main()


# print(pose_TCP)
# print(pose_TCP.position)
# print(pose_TCP.position.x)
# print(type(pose_TCP.position))
# print(pose_TCP.orientation)
# print(pose_TCP.orientation.w)
# print(type(pose_TCP))



# t = geometry_msgs.msg.TransformStamped()
# t.header.stamp = rospy.Time.now()
# t.header.frame_id = 'tool0'
# t.child_frame_id = 'camera_link'
# t.transform.translation.x = 0.10
# t.transform.translation.y = 0.15
# t.transform.translation.z = 0.30
#
# q2 = tf.transformations.quaternion_from_euler(math.pi,0,0)
# t.transform.rotation.x = q2[0]
# t.transform.rotation.y = q2[1]
# t.transform.rotation.z = q2[2]
# t.transform.rotation.w = q2[3]
# br.sendTransform(t)
