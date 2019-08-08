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
import tf
import tf2_ros
from tf.transformations import *

import sys
sys.path.insert(0, '/home/casch/ws_moveit/src/perception_cvut/src/project')
from ur10_class import *
import csv

name_file='pose_ur10.csv'

def do_csv_file(position,orientation):
    global name_file
    x_,y_,z_=position.x,position.y,position.z
    x,y,z,w=orientation.x,orientation.y,orientation.z,orientation.w
    with open(name_file, 'a') as csvfile:# a means append
        filewriter = csv.writer(csvfile, delimiter=',',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([['position:'],[x_,y_,z_]]+[['orientation:'],[x,y,z,w]])
def main():
    r=rospy.Rate(10)

    pose_calibration=list()
    while(not rospy.is_shutdown()):
        frame=camObj.get_image()
        if frame is None:
            print('no image!!!')
            continue
        try:
            pose_TCP=object_ur10.move_group.get_current_pose().pose
            print('pose_TCP.position: \n{}'.format(pose_TCP.position))
            print('pose_TCP.orientation: \n {}'.format(pose_TCP.orientation))
            command=cv2.waitKey(1) & 0xFF
            if command == ord('t'):
                print('The current pose was appended:\n{}'.format(pose_TCP))
                do_csv_file(pose_TCP.position,pose_TCP.orientation)
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

#filewriter.writerow(computation_time+aux_rmse+min_rmse+aux_fitness+max_fitness)
# #pose_calibration.append(np.ravel([pose_TCP.position.x, pose_TCP.position.y ,pose_TCP.position.z]))
# pose_calibration.append([pose_TCP.position.x, pose_TCP.position.y ,pose_TCP.position.z])
# pose_calibration.append([pose_TCP.orientation.x, pose_TCP.orientation.y,pose_TCP.orientation.z,pose_TCP.orientation.w])
# print('pose_calibration:\n{}'.format(pose_calibration))
