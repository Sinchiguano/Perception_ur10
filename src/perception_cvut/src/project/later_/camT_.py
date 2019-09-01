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
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
import time



#############CAMERA#################
import sys, time
# numpy and scipy
import numpy as np
import csv
from scipy.ndimage import filters

# OpenCV
import cv2

# Ros libraries
import roslib
import rospy
from cv_bridge import CvBridge, CvBridgeError
# Ros Messages
from sensor_msgs.msg import Image, CameraInfo, PointCloud2
import sensor_msgs.point_cloud2 as pc2
bridge = CvBridge()
import geometry_msgs.msg
from std_msgs.msg import String

#for mesh and pcd
import copy
import time
#from matplotlib import pyplot as plt
import math
from math import pi
from transforms3d.euler import euler2mat, mat2euler
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from pyquaternion import Quaternion
import tf
import tf2_ros
import geometry_msgs.msg
import scipy
from tf.transformations import *
import pcl

#for the 3d data manipulation!!!!!!!!!!!!!
import open3d
from open3d import read_point_cloud, draw_geometries, KDTreeSearchParamHybrid
from open3d import voxel_down_sample, estimate_normals, compute_fpfh_feature
from open3d import registration_ransac_based_on_feature_matching, TransformationEstimationPointToPoint
from open3d import CorrespondenceCheckerBasedOnEdgeLength,RANSACConvergenceCriteria
from open3d import CorrespondenceCheckerBasedOnDistance, statistical_outlier_removal
from open3d import PointCloud, Vector3dVector, write_point_cloud,read_triangle_mesh
from open3d import select_down_sample,create_rgbd_image_from_color_and_depth,read_image
from open3d import read_pinhole_camera_intrinsic,create_point_cloud_from_rgbd_image
from open3d import PoseGraph,set_verbosity_level,GlobalOptimizationOption,VerbosityLevel,TransformationEstimationPointToPlane
from open3d import PoseGraphNode,registration_icp,registration_icp,get_information_matrix_from_point_clouds
from open3d import PoseGraphEdge,global_optimization,GlobalOptimizationLevenbergMarquardt,GlobalOptimizationLevenbergMarquardt
import glob
import matplotlib.pyplot as plt
from open3d import GlobalOptimizationConvergenceCriteria

class camera(object):
    def __init__(self):
        # In ROS, nodes are uniquely named.
        #rospy.init_node('camera_Node', anonymous=True)
        #Real sense camera
        rospy.Subscriber('/camera/color/image_raw', Image, self.callback_rgb)
        rospy.Subscriber('/camera/depth/image_rect_raw', Image, self.callback_depth)
        rospy.Subscriber('/camera/depth/color/points', PointCloud2, self.callback_pointCloud)
        # rospy.Subscriber('/camera/color/camera_info', CameraInfo,self.infoColorCallback)
        # rospy.Subscriber('/camera/depth/image_rect_raw', CameraInfo, self.callback_depth)

        # #Pylon camera
        # rospy.Subscriber('/pylon_camera_node/image_raw', Image, self.callback_rgb)
        # #rospy.Subscriber('/pylon_camera_node/camera_info', Image, self.callback_depth)

        # #Real astra camera
        # rospy.Subscriber('/camera/rgb/image_raw', Image, self.callback_rgb)
        # rospy.Subscriber('/camera/depth/image_raw', Image, self.callback_depth)
        # rospy.Subscriber('/camera/depth/points', PointCloud2, self.callback_pointCloud)
        # # rospy.Subscriber('/camera/rgb/camera_info', CameraInfo,self.infoColorCallback)
        # # rospy.Subscriber('/camera/depth/camera_info', CameraInfo, self.callback_depth)
        self.cv_image1=None
        self.cv_image2=None
        self.pc=None

    def callback_rgb(self,data):
        #global cv_image1
        #### direct conversion to CV2 ####
        try:
          self.cv_image1 = bridge.imgmsg_to_cv2(data, "bgr8")
          #print(type(cv_image1))
        except CvBridgeError as e:
          print(e)

    def callback_depth(self,data):
        #global cv_image2
        try:
            self.cv_image2 = bridge.imgmsg_to_cv2(data, "passthrough")
            #print(type(self.cv_image2))
        except CvBridgeError as e:
            print(e)
            #return None
        #return cv_image
        # cv2.imshow("Depth image. By: Casch!!!", cv_image2)
        # cv2.waitKey(3)

    def callback_pointCloud(self,data):
        #print('data',type(data))
        if data is not None:
            #print('there is something at least!!!')
            pts = list(pc2.read_points(data, skip_nans=False, field_names=("x", "y", "z")))
            #astra camera
            if len(pts) == 307200:
                self.pc = np.array(list(pts)).reshape((480,640,3))
            else:
                self.pc=pts
        else:
            rospy.logerr("No point cloud image, did you initialize Turtlebot(pc=True)")

    def infoDepthCallback(self,msg):
        print('received info from depth camera!!!',msg)
    def infoColorCallback(self,msg):
        rospy.loginfo("received info from color camera!!!%s",msg)

    def get_image(self):
        return self.cv_image1
    def get_depth(self):
        return self.cv_image2
    def get_point_cloud(self):
        return self.pc





# g_timestamp_last_move = 0
# g_index_last_move = 0
#
# poses=list()
#
#
# goal_0=geometry_msgs.msg.Pose()
# goal_1 = geometry_msgs.msg.Pose()
# goal_2 = geometry_msgs.msg.Pose()
# goal_3 = geometry_msgs.msg.Pose()
# goal_4 = geometry_msgs.msg.Pose()
# goal_5 = geometry_msgs.msg.Pose()
# goal_6 = geometry_msgs.msg.Pose()
# goal_7 = geometry_msgs.msg.Pose()
# goal_8 = geometry_msgs.msg.Pose()
# goal_9 = geometry_msgs.msg.Pose()
#
#
# home = goal_0
# home.position.x,home.position.y,home.position.z= [0.6044897497971731,  0.2611879818362852,  0.5973805032611594]
# home.orientation.x,home.orientation.y,home.orientation.z,home.orientation.w=[0.7136097533836827,  0.7002567082360588,  0.01392144931313463,  0.014417201361588824]
#
#
# goal_1.position.x,goal_1.position.y,goal_1.position.z= [0.6792170687038906,  0.2595806102601011,  0.6004240152169116]
# goal_1.orientation.x,goal_1.orientation.y,goal_1.orientation.z,goal_1.orientation.w= [0.7137240438370314,  0.7001395499445111,  0.013934957389277303,  0.014436648328879434]
#
#
# goal_2.position.x,goal_2.position.y,goal_2.position.z=[0.7300653931760371,  0.258636102036575,  0.6024867866803]
# goal_2.orientation.x,goal_2.orientation.y,goal_2.orientation.z,goal_2.orientation.w=[0.7136432029536898,  0.7002228892704451,  0.013914804386057023,  0.014410497515580047]
#
#
# goal_3.position.x,goal_3.position.y,goal_3.position.z= [0.7035537422125395,  0.15545948941081,  0.6214753637348197]
# goal_3.orientation.x,goal_3.orientation.y,goal_3.orientation.z,goal_3.orientation.w=[0.7928890857866161,  0.6093131455713582,  0.0018206948021379473,  0.007814943687480098]
#
# goal_4.position.x,goal_4.position.y,goal_4.position.z=[0.7288303826582216,  0.18682625560701704,  0.6025412818627581]
# goal_4.orientation.x,goal_4.orientation.y,goal_4.orientation.z,goal_4.orientation.w=[0.71375435762414,  0.7001099601135318,  0.013979280196329043,  0.014329705076260793]
#
# goal_5.position.x,goal_5.position.y,goal_5.position.z=[0.6767072279760193,  0.18782601094693227,  0.6003188598945391]
# goal_5.orientation.x,goal_5.orientation.y,goal_5.orientation.z,goal_5.orientation.w= [0.7137013273247063,  0.7001685843065901,  0.013873822129271239,  0.014208658789036311]
#
#
# goal_6.position.x,goal_6.position.y,goal_6.position.z=[0.6755934847070446,  0.1308157557420405,  0.6003676886876154]
# goal_6.orientation.x,goal_6.orientation.y,goal_6.orientation.z,goal_6.orientation.w= [0.7137591297052486,  0.7001061742770575,  0.0139653493400223,  0.014290504517334367]
#
# goal_7.position.x,goal_7.position.y,goal_7.position.z= [0.6207439707612881,  0.13164862449093792,  0.598265138984852]
# goal_7.orientation.x,goal_7.orientation.y,goal_7.orientation.z,goal_7.orientation.w= [0.71375108394431,  0.7001134267654829,  0.013977021486629444,  0.014325596021725277]
#
# goal_8.position.x,goal_8.position.y,goal_8.position.z=  [0.5568401162361492,  0.13293034872029502,  0.5956477647060543]
# goal_8.orientation.x,goal_8.orientation.y,goal_8.orientation.z,goal_8.orientation.w= [0.7137194188717318,  0.7001472443196016,  0.013946052695757967,  0.014280581615348802]
#
#
# goal_9.position.x,goal_9.position.y,goal_9.position.z=   [0.5576243412091563,  0.17938184053692052,  0.5957389333994288]
# goal_9.orientation.x,goal_9.orientation.y,goal_9.orientation.z,goal_9.orientation.w= [0.7137293998692598,  0.7001305777887191,  0.014088824004738721,  0.014457622407030768]
#
#
# poses.append(home)
# poses.append(goal_1)
# poses.append(goal_2)
# poses.append(goal_3)
# poses.append(goal_4)
# poses.append(goal_5)
# poses.append(goal_6)
# poses.append(goal_7)
# poses.append(goal_8)
# poses.append(goal_9)
