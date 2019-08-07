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
from ur10_class_01 import *
import tf
import tf2_ros
from tf.transformations import *

def move(object_robot):
    import time
    global g_index_last_move
    global g_timestamp_last_move
    global poses

    if (time.time() - g_timestamp_last_move) < 2:
        return

    g_index_last_move = (g_index_last_move + 1) % len(poses)

    object_robot.go_to_pose_goal(poses[g_index_last_move])

    print('g_index_last_move {}'.format(g_index_last_move))

    g_timestamp_last_move = time.time()

def pose_to_tf(br,pose_TCP):

    """input in m and rad"""
    t = geometry_msgs.msg.TransformStamped()
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = 'world'
    t.child_frame_id = 'tool0'
    t.transform.translation.x = pose_TCP.position.x
    t.transform.translation.y = pose_TCP.position.y
    t.transform.translation.z = pose_TCP.position.z

    t.transform.rotation.x = pose_TCP.orientation.x
    t.transform.rotation.y = pose_TCP.orientation.y
    t.transform.rotation.z = pose_TCP.orientation.z
    t.transform.rotation.w = pose_TCP.orientation.w
    br.sendTransform(t)

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


def main():
    global home

    br = tf2_ros.TransformBroadcaster()
    r=rospy.Rate(10)

    #Task space
    ###########
    # print "============ Press `Enter` to start from --> Home position..."
    # raw_input()
    # object_ur10.go_to_pose_goal(home)
    # time.sleep(3)

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
    # print ""
    # print "----------------------------------------------------------"
    # print "Welcome to the MoveIt MoveGroup Python Interface"
    # print "----------------------------------------------------------"
    # print "Press Ctrl-D to exit at any time"
    # print ""
    # print "============ Press `Enter` to begin the moveit_commander ..."
    # raw_input()
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
