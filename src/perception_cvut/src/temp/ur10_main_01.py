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

def main():
    global home
    r=rospy.Rate(10)
    #Task space
    ###########
    print "============ Press `Enter` to start from --> Home position..."
    raw_input()
    object_ur10.go_to_pose_goal(home)
    time.sleep(3)

    while(not rospy.is_shutdown()):
        try:
            # #Joint space
            # ############
            # print "============ Press `Enter` to start Joint Space movement..."
            # raw_input()
            # object_ur10.go_to_joint_state()
            #
            # #Task space
            # ###########
            # print "============ Press `Enter` to start Task Space movement..."
            # raw_input()
            # object_ur10.go_to_pose_goal(home)
            #
            #
            # #Cartesian path
            # ###############
            # print "============ Press `Enter` to start Cartisian Control movement..."
            # raw_input()
            # cartesian_plan, fraction = object_ur10.plan_cartesian_path()
            # object_ur10.execute_plan(cartesian_plan)

            move(object_ur10)
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
