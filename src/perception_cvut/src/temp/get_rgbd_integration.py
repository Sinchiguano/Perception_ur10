#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Cesar Sinchiguano <cesarsinchiguano@hotmail.es>
#
# Distributed under terms of the BSD license.

import sys
sys.path.insert(0, '/home/casch/ws_moveit/src/perception_cvut/src/project')
from thesis_class import *
import open3d as o3d
#from trajectory_io import *
import numpy as np



voxel_size = 0.002
max_correspondence_distance_coarse = voxel_size * 15
max_correspondence_distance_fine = voxel_size * 1.5
cloud_='3d_cloud/'
rgbd_='3d_rgbd/'


def load_point_clouds(voxel_size=0.0):
    pcds = []

    for i in range(1,5):
        #pcd = read_point_cloud("TestData/ICP/cloud_bin_%d.pcd" % i)
        pcd = read_point_cloud("3d_rgbd/%d.ply" % i)
        #pcd = read_point_cloud("3d_cloud/%d.ply" % i)
        pcd_down = voxel_down_sample(pcd, voxel_size=voxel_size)
        pcds.append(pcd_down)

    return pcds
#,[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

def main():
    pcds=list()
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        #camera_poses = read_trajectory("3d_rgbd/odometry.log")
        volume = o3d.integration.ScalableTSDFVolume(voxel_length=4.0 / 512.0,sdf_trunc=0.04,color_type=o3d.integration.TSDFVolumeColorType.RGB8)

        for i in range(1,5):
            pcd = read_point_cloud("3d_rgbd/%d.ply" % i)
            pcd_down = voxel_down_sample(pcd, voxel_size=0.002)
            pcds.append(pcd_down)

        pinhole_camera_intrinsic = read_pinhole_camera_intrinsic("camera_real.json")

        for i in pcds:
            volume.integrate(i,pinhole_camera_intrinsic,np.array([[1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]]))

        print("Extract a triangle mesh from the volume and visualize it.")
        mesh = volume.extract_triangle_mesh()
        mesh.compute_vertex_normals()
        o3d.visualization.draw_geometries([mesh])

        #cv2.imshow('frame',frame)
    # When everything done, release the capture
    #cv2.destroyAllWindows()

if __name__ == '__main__':
    camObj=camera()
    main()
