#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Cesar Sinchiguano <cesarsinchiguano@hotmail.es>
#
# Distributed under terms of the MIT license.

"""

"""

import sys
sys.path.insert(0, '/home/casch/ws_moveit/src/perception_cvut/src/project')
from ur10_class import *
import tf
import tf2_ros
from tf.transformations import *

poses=list()


goal_0=geometry_msgs.msg.Pose()
goal_1 = geometry_msgs.msg.Pose()
goal_2 = geometry_msgs.msg.Pose()
goal_3 = geometry_msgs.msg.Pose()
goal_4 = geometry_msgs.msg.Pose()
goal_5 = geometry_msgs.msg.Pose()
goal_6 = geometry_msgs.msg.Pose()
#
# pose_goal=list()
# for i in range(7):

import csv

with open('pose_ur10.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=' ')
    line_count = 0
    for row in csv_file:
    # for row in csv_reader:
    #     if line_count == 0:
    #         print(f'Column names are {", ".join(row)}')
    #         line_count += 1
    #     else:
    #         print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
    #         line_count += 1
    # print(f'Processed {line_count} lines.')
