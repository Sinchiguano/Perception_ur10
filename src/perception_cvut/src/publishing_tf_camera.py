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



def pose_to_tf(br,pose_TCP):

    # """input in m and rad"""
    # t = geometry_msgs.msg.TransformStamped()
    # t.header.stamp = rospy.Time.now()
    # t.header.frame_id = 'world'
    # t.child_frame_id = 'calibration_target'
    # t.transform.translation.x = 0.50
    # t.transform.translation.y = 0
    # t.transform.translation.z = 0

    # t.transform.rotation.x = 0
    # t.transform.rotation.y = 0
    # t.transform.rotation.z = 0
    # t.transform.rotation.w = 1
    # br.sendTransform(t)

    # t2 = geometry_msgs.msg.TransformStamped()
    # t2.header.stamp = rospy.Time.now()
    # t2.header.frame_id = "camera_link_2"
    # t2.child_frame_id = "camera_link"
    # t2.transform.translation.x = 0
    # t2.transform.translation.y = 0
    # t2.transform.translation.z = 0
    # #orientation according to openCV
    # #q3 = tf.transformations.quaternion_from_euler(euler_angles_[0],euler_angles_[1],euler_angles_[2])
    # #orientation of camera link. which is parallel to world frame
    # q2 = tf.transformations.quaternion_from_euler(-math.pi/2,math.pi/2,0)
    # #correction of camera frame according to openCV orientation
    # #q4=quaternion_multiply(q3,q2)#rotation,origin
    # t2.transform.rotation.x = q2[0]
    # t2.transform.rotation.y = q2[1]
    # t2.transform.rotation.z = q2[2]
    # t2.transform.rotation.w = q2[3]
    # br.sendTransform(t2)

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

    while(not rospy.is_shutdown()):
        try:
            pose_TCP=object_ur10.move_group.get_current_pose().pose
            pose_to_tf(br,pose_TCP)
            print "============ Publishing new tf of the camera link!"
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
