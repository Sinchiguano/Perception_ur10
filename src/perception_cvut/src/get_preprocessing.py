#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Cesar Sinchiguano <cesarsinchiguano@hotmail.es>
#
# Distributed under terms of the BSD license.

"""
Everthing done with open3d, pyntcloud, CloudCompare, meshLab and python_pcl binding (wrapper)
--------------------------------------------------------------------------------------------
#Python 2.7 anaconda in a virtual environment working with ros, and extra "tensorflow"
#In order to change the format .obj(CAD model) to .ply(triangle mesh) do the following:
1_open Cloud compare and save a copy as .ply extension
#From .ply (triangle mesh) to .pcd(sample points) run the following code(meshtopc.py),
# meshtopc.py use the a pyntcloud that only run in python3 where i used the method to
# sample point from the mesh data, also use open3D in order to save as .pcd the sample points.
#finally, for processing the data i am working with python_pcl
-----------------------------------------------------------------------------------------
"""

import sys
sys.path.insert(0, '/home/casch/ws_moveit/src/perception_cvut/src/project')
from thesis_class import *


# Returns Downsampled version of a point cloud. The bigger the leaf size the less information retained
def do_voxel_grid_filter(point_cloud, LEAF_SIZE = 0.01):
    voxel_filter = point_cloud.make_voxel_grid_filter()
    voxel_filter.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)
    return voxel_filter.filter()


# Returns only the point cloud information at a specific range of a specific axis
def do_passthrough_filter(point_cloud, name_axis = 'z', min_axis = 0.6, max_axis = 1.1):
    pass_filter = point_cloud.make_passthrough_filter()
    pass_filter.set_filter_field_name(name_axis)
    pass_filter.set_filter_limits(min_axis, max_axis)
    return pass_filter.filter()

# Use RANSAC plane segmentation to separate plane and not plane points
# Returns inliers (plane) and outliers (not plane)
def do_ransac_plane_segmentation(point_cloud, max_distance = 0.01):

    segmenter = point_cloud.make_segmenter()
    segmenter.set_model_type(pcl.SACMODEL_PLANE)
    segmenter.set_method_type(pcl.SAC_RANSAC)
    segmenter.set_distance_threshold(max_distance)

    #obtain inlier indices and model coefficients
    inlier_indices, coefficients = segmenter.segment()

    inliers = point_cloud.extract(inlier_indices, negative = False)
    outliers = point_cloud.extract(inlier_indices, negative = True)

    return inliers, outliers

def main():
    counter1=0
    counter2=0
    counter3=0
    

    voxel_size = 0.002 
    max_correspondence_distance_coarse = voxel_size * 15
    max_correspondence_distance_fine = voxel_size * 1.5
    cloud_='3d_cloud/'
    rgbd_='3d_rgbd/'
    # roi_='3d_rgbd_preprocessing/roi_'
    # table_='3d_rgbd_preprocessing/table_'
    # objects_='3d_rgbd_preprocessing/objects_'

    roi_='3d_cloud_preprocessing/roi_'
    table_='3d_cloud_preprocessing/table_'
    objects_='3d_cloud_preprocessing/objects_'

    flag=True

    rate = rospy.Rate(10) # 10hz
    #rgbd_ = [pcl.load(cloud) for cloud in glob.glob(rgbd_+'*pcd')]
    rgbd_ = [pcl.load(cloud) for cloud in glob.glob(cloud_+'*pcd')]
    while not rospy.is_shutdown():
        counter1+=1

        if flag:
            for i, cloud in enumerate(rgbd_):

                # mask out point cloud in order to get only information in our region of interest, as we don't care about the other parts
                filter = do_passthrough_filter(point_cloud = cloud,name_axis = 'x', min_axis = 0.60, max_axis = 1.0)
                filter = do_passthrough_filter(point_cloud = filter,name_axis = 'y', min_axis = -0.20, max_axis = 0.2)
                pcl.save(filter, roi_+str(i)+'.pcd')
                pcl.save(filter, roi_+str(i)+'.ply')

                # Separate the table from everything else
                table, objects = do_ransac_plane_segmentation(filter, max_distance = 0.01)
                pcl.save(table, table_ +str(i)+'.pcd')
                pcl.save(table, table_ +str(i)+'.ply')

                pcl.save(objects,objects_ +str(i)+'.pcd')
                pcl.save(objects,objects_ +str(i)+'.ply')
            #flag=False

        for i, cloud in enumerate(rgbd_):
            pcd = read_point_cloud(objects_ +str(i)+'.pcd')
            draw_geometries([pcd])

        rate.sleep()

    # When everything done, release the capture
    cv2.destroyAllWindows()

if __name__ == '__main__':
    camObj=camera()
    main()


