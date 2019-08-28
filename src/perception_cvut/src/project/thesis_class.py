#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Cesar Sinchiguano <cesarsinchiguano@hotmail.es>
#
# Distributed under terms of the BSD license.
# initialize cv bridge
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
#from pcl import PointCloud_PointXYZ

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
        rospy.init_node('camera', anonymous=True)
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
                #print()
                # #just for realsense camera
                # points_list = []
                # for data in pc2.read_points(data, skip_nans=False, field_names=("x", "y", "z")):
                #     points_list.append([data[0], data[1], data[2]])
                #
                # pcl_data = pcl.PointCloud_PointXYZ()
                # pcl_data.from_list(points_list)
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
