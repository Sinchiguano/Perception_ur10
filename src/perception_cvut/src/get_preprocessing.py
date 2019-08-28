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


def display_objects(cloud1,cloud2):
    pcloud1 = read_point_cloud(cloud1)
    pcloud2 = read_point_cloud(cloud2)
    print("Showing pcloud1 (red) and pcloud2 (gray): ")
    pcloud1.paint_uniform_color([1, 0, 0])
    pcloud2.paint_uniform_color([0.8, 0.8, 0.8])

    #draw_geometries([pcloud1, pcloud2])
    draw_geometries([pcloud2])


def main():
    counter1=0
    counter2=0
    counter3=0
    

    voxel_size = 0.002    voxel_size = 0.002
    max_correspondence_distance_coarse = voxel_size * 15
    max_correspondence_distance_fine = voxel_size * 1.5
    cloud_='3d_cloud/'
    rgbd_='3d_rgbd/'
    max_correspondence_distance_coarse = voxel_size * 15
    max_correspondence_distance_fine = voxel_size * 1.5

    cloud_='3d_cloud/'
    rgbd_='3d_rgbd/'

    roi_=path_cloud+'roi_name'
    table_=path_cloud+'table_name'
    objects_=path_cloud+'objects_name'

    flag=True

    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        counter1+=1

        #rgbd_ = [pcl.load(rgbd) for rgbd in glob.glob(pc_path+'*pcd')]

        rgbd_ = [pcl.load(rgbd) for rgbd in glob.glob(rgbd_path+'*pcd')]

        if flag:
            for i, cloud in enumerate(rgbd_):

                # mask out point cloud in order to get only information in our region of interest, as we don't care about the other parts
                filter = do_passthrough_filter(point_cloud = cloud,name_axis = 'x', min_axis = -0.5, max_axis = 1.5)
                filter = do_passthrough_filter(point_cloud = filter,name_axis = 'y', min_axis = -0.5, max_axis = 0.2)
                pcl.save(filter, roi_name+str(i)+'.pcd')


                # Separate the table from everything else
                table, objects = do_ransac_plane_segmentation(filter, max_distance = 0.01)
                pcl.save(table, table_name +str(i)+'.pcd')
                pcl.save(objects,objects_name +str(i)+'.pcd')
            flag=False

        for i, cloud in enumerate(rgbd_):
            # Display the table and the object
            pcd = read_point_cloud(objects_name +str(i)+'.pcd')
            write_point_cloud(objects_name +str(i)+'.ply', pcd)
            draw_geometries([pcd])

        print('------------------')
        print('counter:',counter1)

    # When everything done, release the capture
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #camObj=camera()
    main()


