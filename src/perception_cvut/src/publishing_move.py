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

def pose_to_tf(br,pose_TCP):

    """input in m and rad"""
    t = geometry_msgs.msg.TransformStamped()
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = 'base_link'
    t.child_frame_id = 'tool0'
    t.transform.translation.x = pose_TCP.position.x
    t.transform.translation.y = pose_TCP.position.y
    t.transform.translation.z = pose_TCP.position.z

    t.transform.rotation.x = pose_TCP.orientation.x
    t.transform.rotation.y = pose_TCP.orientation.y
    t.transform.rotation.z = pose_TCP.orientation.z
    t.transform.rotation.w = pose_TCP.orientation.w
    br.sendTransform(t)


    # """the transform compute from the visp package"""
    # t1 = geometry_msgs.msg.TransformStamped()
    # t1.header.stamp = rospy.Time.now()
    # t1.header.frame_id = 'wrist_3_link'
    # t1.child_frame_id = 'camera_link'
    # t1.transform.translation.x =  -0.381484646554/100
    # t1.transform.translation.y = 1.3657892666/100
    # t1.transform.translation.z = 18.7748810616/100

    # t1.transform.rotation.x = 0.0541712132271
    # t1.transform.rotation.y = -0.00219061966433
    # t1.transform.rotation.z = -0.992874695708
    # t1.transform.rotation.w = 0.106115594832
    # br.sendTransform(t1)


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
            pose_to_tf(br,pose_TCP)
            print "============ Python movement complete!"
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