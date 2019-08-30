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
# import tf
# import tf2_ros
# from tf.transformations import *

import sys
sys.path.insert(0, '/home/casch/ws_moveit/src/perception_cvut/src/project')
from ur_cam_class import *

name_file='joints_realsense.csv'


def do_csv_file(position,orientation,joints_values):
    global name_file
    x_,y_,z_=position.x,position.y,position.z
    x,y,z,w=orientation.x,orientation.y,orientation.z,orientation.w
    with open(name_file, 'a') as csvfile:# a means append
        filewriter = csv.writer(csvfile, delimiter=',',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(joints_values+[''])

def main():
    r=rospy.Rate(10)

    pose_calibration=list()
    counter=0
    #exit()
    while(not rospy.is_shutdown()):
        #frame=camObj.get_image()
        frame=cv2.imread('test.jpg')
        if frame is None:
            print('no image!!!')
            continue
        try:
            pose_TCP=object_ur10.move_group.get_current_pose().pose
            joints_values=object_ur10.move_group.get_current_joint_values()
            print('pose_TCP.position: \n{}'.format(pose_TCP.position))
            print('pose_TCP.orientation: \n {}'.format(pose_TCP.orientation))
            print ("robot joint values: \n {}".format(joints_values))
            print('counter: {}'.format(counter))
            command=cv2.waitKey(1) & 0xFF
            if command == ord('t'):
            	counter+=1
                print('The current pose was appended:\n{}'.format(pose_TCP))
                do_csv_file(pose_TCP.position,pose_TCP.orientation,[joints_values])
                time.sleep(2)
            print "============ Python movement complete!"
            r.sleep()
        except rospy.ROSInterruptException:
            return
        except KeyboardInterrupt:
            return

        cv2.imshow('frame',frame)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    object_ur10 = UniversalRobot()
    camObj=camera()
    main()
