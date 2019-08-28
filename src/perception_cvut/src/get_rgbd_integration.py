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
from trajectory_io import *
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

def pairwise_registration(source, target):

    print("Apply point-to-plane ICP")
    estimate_normals(source, KDTreeSearchParamHybrid(radius = 0.01, max_nn = 20))
    estimate_normals(target, KDTreeSearchParamHybrid(radius = 0.01, max_nn = 20))


    # '''Fast Point Feature Histograms'''
    # radius_feature = voxel_size * 5
    # source_fpfh = compute_fpfh_feature(source,KDTreeSearchParamHybrid(radius = radius_feature, max_nn = 100))
    # target_fpfh = compute_fpfh_feature(target,KDTreeSearchParamHybrid(radius = radius_feature, max_nn = 100))

    icp_coarse = registration_icp(source, target,max_correspondence_distance_coarse, np.identity(4),TransformationEstimationPointToPlane())
    #ransac_coarse=do_ransac_registration(source, target, source_fpfh, target_fpfh )

    icp_fine = registration_icp(source, target, max_correspondence_distance_fine,icp_coarse.transformation,TransformationEstimationPointToPlane())

    transformation_icp = icp_fine.transformation
    information_icp = get_information_matrix_from_point_clouds(source, target, max_correspondence_distance_fine,icp_fine.transformation)

    return transformation_icp, information_icp

def do_ransac_registration(source_down, target_down, source_fpfh, target_fpfh):

    '''RANSAC registration is applied on downsampled point clouds.'''
    #Global registration. This family of algorithms do not require an alignment for initialization.
    #They usually produce less tight alignment results and are used as initialization of the local methods such as ICP.
    #RANSACConvergenceCriteria
    #It defines the maximum number of RANSAC iterations and the maximum number of validation steps.
    #The larger these two numbers are, the more accurate the result is, but also the more time the algorithm takes.
    threshold = 0.003#0.01 * 1.5
    result = registration_ransac_based_on_feature_matching(source_down, target_down, source_fpfh, target_fpfh,threshold,
            TransformationEstimationPointToPoint(False), 4,
            [CorrespondenceCheckerBasedOnEdgeLength(0.9),CorrespondenceCheckerBasedOnDistance(threshold)],
            RANSACConvergenceCriteria(400000, 1000))
    return result

def full_registration(pcds, max_correspondence_distance_coarse,max_correspondence_distance_fine):
    pose_graph = PoseGraph()
    odometry = np.identity(4)
    pose_graph.nodes.append(PoseGraphNode(odometry))
    n_pcds = len(pcds)
    for source_id in range(n_pcds):
        for target_id in range(source_id + 1, n_pcds):
            transformation_icp, information_icp = pairwise_registration(pcds[source_id], pcds[target_id])
            print("Build o3d.registration.PoseGraph")
            if target_id == source_id + 1:  # odometry case
                odometry = np.dot(transformation_icp, odometry)
                pose_graph.nodes.append(PoseGraphNode(np.linalg.inv(odometry)))
                pose_graph.edges.append(PoseGraphEdge(source_id,
                                                   target_id,
                                                   transformation_icp,
                                                   information_icp,
                                                   uncertain=False))
            else:  # loop closure case
                pose_graph.edges.append(PoseGraphEdge(source_id,
                                                   target_id,
                                                   transformation_icp,
                                                   information_icp,
                                                   uncertain=True))
    return pose_graph

def main():
    counter1=0
    counter2=0
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        camera_poses = read_trajectory("3d_rgbd/odometry.log")
        volume = o3d.integration.ScalableTSDFVolume(voxel_length=4.0 / 512.0,sdf_trunc=0.04,color_type=o3d.integration.TSDFVolumeColorType.RGB8)

        for i in range(len(camera_poses)):
            print("Integrate {:d}-th image into the volume.".format(i))
            color = read_image("3d_rgbd/{:05d}.jpg".format(i))
            depth = read_image("3d_rgbd/{:05d}.png".format(i))
            rgbd = create_rgbd_image_from_color_and_depth(color, depth, depth_trunc=4.0, convert_rgb_to_intensity=False)
            volume.integrate(rgbd,PinholeCameraIntrinsic(PinholeCameraIntrinsicParameters.PrimeSenseDefault),np.linalg.inv(camera_poses[i].pose))

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
