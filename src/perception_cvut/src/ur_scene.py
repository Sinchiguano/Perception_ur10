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

import sys
sys.path.insert(0, '/home/casch/ws_moveit/src/perception_cvut/src/project')
#from ur_cam_class import *
from urT_class import *


def main():
    r=rospy.Rate(10)
    object_ur10.scene.is_diff = True
    
    #it does not work like that
    # object_ur10.add_gripper()
    # object_ur10.attach_gripper()

    while(True):

        try:
            
            object_ur10.add_box()
            time.sleep(0.01)
            
            object_ur10.attach_box()
            time.sleep(0.01)
            object_ur10.detach_box()
            time.sleep(0.01)
            
            object_ur10.remove_box()
            time.sleep(0.01)

            print "============ Python scene!"
        except rospy.ROSInterruptException:
            return
        except KeyboardInterrupt:
            return
        r.sleep()

if __name__ == '__main__':
    object_ur10 = UniversalRobot()
    main()
