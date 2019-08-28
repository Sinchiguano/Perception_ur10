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
cloud_='3d_cloud/'
rgbd_='3d_rgbd/'


def display_objects(cloud1,cloud2):
    pcloud1 = read_point_cloud(cloud1)
    pcloud2 = read_point_cloud(cloud2)
    print("Showing pcloud1 (red) and pcloud2 (gray): ")
    pcloud1.paint_uniform_color([1, 0, 0])
    pcloud2.paint_uniform_color([0.8, 0.8, 0.8])
    #draw_geometries([pcloud1, pcloud2])
    #draw_geometries([pcloud2])

def create_dataset_pointcloud(frame,pc,counter1,tf_cloud):
    global cloud_3d_cloud

    #the following function render a vector in 3d for pcd format in order to use with open3d
    '''With the help of open3d we render pcd'''
    #pc=np.reshape(pc,(np.size(pc[:,:,0]),3))#I took the size of my x coordinates
    #pc=np.nan_to_num(pc)

    #Pass xyz to Open3D.PointCloud and visualize
    pc=np.nan_to_num(pc)
    pcd = PointCloud()
    pcd.points = Vector3dVector(pc)
    # Flip it, otherwise the pointcloud will be upside down
    print("PCD loaded as PCD and PLY, (flip it!!!)")
    #pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    pcd.transform(tf_cloud)


    #we save the pcd in the following formats pcd and ply
    write_point_cloud(cloud_+str(counter1)+'.pcd', pcd)
    write_point_cloud(cloud_+str(counter1)+'.ply', pcd)
    cv2.imwrite(cloud_+str(counter1)+'.jpg', frame)

    source =read_point_cloud(cloud_+str(counter1)+'.ply')
    #draw_geometries([source])

def create_dataset_rgbd(frame,depth,counter2,tf_rgbd):
    global rgbd_
    #we save the pcd in the following formats pcd and ply
    cv2.imwrite(rgbd_+str(counter2)+'.jpg', frame)
    cv2.imwrite(rgbd_+str(counter2)+'.png', depth)


    pinhole_camera_intrinsic = read_pinhole_camera_intrinsic("camera_real.json")
    #print(pinhole_camera_intrinsic.intrinsic_matrix)

    print("Read dataset")
    color_raw = read_image(rgbd_+str(counter2)+'.jpg')
    depth_raw = read_image(rgbd_+str(counter2)+'.png')

    rgbd_image = create_rgbd_image_from_color_and_depth(color_raw, depth_raw)

    #Create point cloud from rgbd imagescloud_='3d_cloud/'
    pcd = create_point_cloud_from_rgbd_image(rgbd_image, pinhole_camera_intrinsic)

    # Flip it, otherwise the pointcloud will be upside down
    #pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    pcd.transform(tf_rgbd)
    #save point cloud
    write_point_cloud(rgbd_+str(counter2)+'.pcd', pcd)
    write_point_cloud(rgbd_+str(counter2)+'.ply', pcd)

    #we read our point cloud data from rgbd in order to see if it is working properlly
    #pcd =read_point_cloud(rgbd_+str(counter2)+'.pcd')
    #draw_geometries([pcd])

def do_csv_file(position,orientation,file):
    with open(file, 'a') as csvfile:# a means append
        filewriter = csv.writer(csvfile, delimiter=',',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        Rq= quaternion_matrix(orientation)
        Rq[0,3],Rq[1,3],Rq[2,3]=position[0],position[1],position[2]
        filewriter.writerow([Rq])
    return Rq

def main():
    counter1=0
    counter2=0
    rate = rospy.Rate(10) # 10hz
    listener = tf.TransformListener()

    while not rospy.is_shutdown():

        # Capture 2D-data
        frame=camObj.get_image()
        # Capture depth data
        depth=camObj.get_depth()

        # Capture 3D-data
        pc=camObj.get_point_cloud()

        if pc is None:
            print('no PointCloud2!!!')
            continue
        if frame is None:
            print('no Frame!!!')
            continue
        if depth is None:
            print('no depth image!!!')
            continue
        print('ready to take frame')
        command=cv2.waitKey(1) & 0xFF

        try:
            (trans,rot) = listener.lookupTransform('/world','/camera_link', rospy.Time(0))
            # Correction of my transform in order to have in openCV convention
            q_corre = tf.transformations.quaternion_from_euler(math.pi/2,-math.pi/2,0)
            q_corre[3]=-q_corre[3]
            q2=quaternion_multiply(rot,q_corre)
            Rq = quaternion_matrix(q2)
            #print('Quaternion in openCV Convention: \n {}'.format(q2))
            #print('Rotation in openCV Convention: \n {}'.format(Rq))

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        if command == ord('p'):
            if not trans==None and not rot==None:
                counter1+=1
                tf_cloud=do_csv_file(trans,q2,'3d_cloud/odom_cam.csv')
                create_dataset_pointcloud(frame,pc,counter1,tf_cloud)
                
        elif command==ord('r'):
            if not trans==None and not rot==None:        #mat=np.vstack((Rq,[0.0,0.0,0.0,1.0]))
                counter2+=1
                tf_rgbd=do_csv_file(trans,q2,'3d_rgbd/odom_cam.csv')
                create_dataset_rgbd(frame,depth,counter2,tf_rgbd)
                
        print('point_cloud2 done: {}'.format(counter1))
        print('rgbd done: {}'.format(counter2))
        #print('tf: world->camera {}'.format(trans,rot))

        cv2.imshow('frame',frame)
    # When everything done, release the capture
    cv2.destroyAllWindows()

if __name__ == '__main__':
    camObj=camera()
    main()
