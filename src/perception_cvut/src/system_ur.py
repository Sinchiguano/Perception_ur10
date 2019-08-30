#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Cesar Sinchiguano <cesarsinchiguano@hotmail.es>
#
# Distributed under terms of the BSD license.

import sys
sys.path.insert(0, '/home/casch/ws_moveit/src/perception_cvut/src/project')
# from thesis_class import *
# from ur10_class import *
from ur_cam_class import *


cloud_='3d_cloud/'
rgbd_='3d_rgbd/'


model_path='CAD_model/'
scene_path='SCENE_model/'

tmp='output_pipeline/'
name_file=tmp+'transform_data.csv'

def do_pointcloud(frame,pc,counter,tf_cloud):
    global scene_path

    #Pass xyz to Open3D.PointCloud and visualize
    pc=np.nan_to_num(pc)
    pcd = PointCloud()
    pcd.points = Vector3dVector(pc)
    # Flip it, otherwise the pointcloud will be upside down
    print("PCD loaded as PCD and PLY, (flip it!!!)")

    pcd.transform(tf_cloud)

    #we save the pcd in the following formats pcd and ply
    write_point_cloud(scene_path+str(counter)+'.pcd', pcd)
    #write_point_cloud(scene_path+str(counter)+'.ply', pcd)
    #cv2.imwrite(scene_path+str(counter)+'.jpg', frame)

    return pcl.load(scene_path+str(counter)+'.pcd')

def do_dataset(source,target):
    '''Preprocessing step'''
    #print("Downsample the point cloud and get features with FPFH")
    source_down, source_fpfh = do_preprocessing_pcd(source, 0.005)#in mm
    tmp_source=np.asarray(source_down.points)

    #print("Downsample the point cloud and get features with FPFH")
    target_down, target_fpfh = do_preprocessing_pcd(target, 0.005)#good tunning
    tmp_target=np.asarray(target_down.points)

    return source, target, source_down, target_down, source_fpfh, target_fpfh

def do_preprocessing_pcd(pcd, voxel_size):
    '''Downsample the point cloud'''
    pcd_down = voxel_down_sample(pcd, voxel_size)

    '''Estimate normals'''
    radius_normal = voxel_size * 6
    estimate_normals(pcd_down, KDTreeSearchParamHybrid(radius = radius_normal, max_nn = 30))

    '''Fast Point Feature Histograms'''
    radius_feature = voxel_size * 6
    pcd_fpfh = compute_fpfh_feature(pcd_down,KDTreeSearchParamHybrid(radius = radius_feature, max_nn = 100))

    return pcd_down, pcd_fpfh

def do_ransac_registration(source_down, target_down, source_fpfh, target_fpfh):

    '''RANSAC registration is applied on downsampled point clouds.'''
    threshold = 0.003
    result = registration_ransac_based_on_feature_matching(source_down, target_down, source_fpfh, target_fpfh,threshold,
            TransformationEstimationPointToPoint(False), 4,
            [CorrespondenceCheckerBasedOnEdgeLength(0.9),CorrespondenceCheckerBasedOnDistance(threshold)],
            RANSACConvergenceCriteria(400000, 1000))
    return result

def do_icp_registration(source, target, transformation):


    '''Point-to-plane ICP registration is applied on original points'''
    estimate_normals(source, KDTreeSearchParamHybrid(radius = 0.006, max_nn = 20))
    estimate_normals(target, KDTreeSearchParamHybrid(radius = 0.006, max_nn = 20))
    threshold = 0.005
    result = registration_icp(source, target, threshold,transformation,TransformationEstimationPointToPlane())
    return result

def do_drawing_registration(source, target, transformation):

    source_tmp= copy.deepcopy(source)
    target_tmp = copy.deepcopy(target)
    source_tmp.paint_uniform_color([1, 0.706, 0])
    target_tmp.paint_uniform_color([0, 0.651, 0.929])

    source_tmp.transform(transformation)
    draw_geometries([source_tmp, target_tmp])

def do_passthrough_filter(point_cloud, name_axis = 'z', min_axis = 0.6, max_axis = 1.1):
    pass_filter = point_cloud.make_passthrough_filter()
    pass_filter.set_filter_field_name(name_axis)
    pass_filter.set_filter_limits(min_axis, max_axis)
    return pass_filter.filter()

def do_ransac_plane_segmentation(point_cloud, max_distance = 0.01):

    segmenter = point_cloud.make_segmenter()
    segmenter.set_model_type(pcl.SACMODEL_PLANE)
    segmenter.set_method_type(pcl.SAC_RANSAC)
    segmenter.set_distance_threshold(max_distance)
    inlier_indices, coefficients = segmenter.segment()

    inliers = point_cloud.extract(inlier_indices, negative = False)
    outliers = point_cloud.extract(inlier_indices, negative = True)
    return inliers, outliers

def do_publishing_pose(br,transformation):
    pose_translation=list(transformation[:-1,3])
    pose_quaternion = tf.transformations.quaternion_from_matrix(transformation)
    print('pose_translation {}'.format(pose_translation))
    print('pose_quaternion {}'.format(pose_quaternion))

    """input in m and rad"""
    t = geometry_msgs.msg.TransformStamped()
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = 'world'
    t.child_frame_id = 'pose_object'
    t.transform.translation.x = pose_translation[0]#-0.06
    t.transform.translation.y = pose_translation[1]#-0.05
    t.transform.translation.z = pose_translation[2]#+0.05
    t.transform.rotation.w = pose_quaternion[3]
    t.transform.rotation.x = pose_quaternion[0]
    t.transform.rotation.y = pose_quaternion[1]
    t.transform.rotation.z = pose_quaternion[2]
    br.sendTransform(t)

# ============ Home position!
# pose_TCP.position:
# x: 0.72015383355
# y: 0.094471510805
# z: 0.906768096989
# pose_TCP.orientation:
#  x: -0.991071723421
# y: 0.0307909114419
# z: -0.126173927763
# w: 0.0301479478545
# robot joint values:
#  [-0.10107690492738897, -1.4395411650287073, 0.9641895294189453, 0.22433340549468994, 1.5416154861450195, 0.07725817710161209]


def main():
    counter1=0

    pose_TCP=object_ur10.move_group.get_current_pose().pose
    joints_values=object_ur10.move_group.get_current_joint_values()
    print('pose_TCP.position: \n{}'.format(pose_TCP.position))
    print('pose_TCP.orientation: \n {}'.format(pose_TCP.orientation))
    print ("robot joint values: \n {}".format(joints_values))
    transformation= quaternion_matrix([pose_TCP.orientation.x,
                                            pose_TCP.orientation.y,
                                            pose_TCP.orientation.z,
                                            pose_TCP.orientation.w])

    transformation[0,3]=pose_TCP.position.x
    transformation[1,3]=pose_TCP.position.y
    transformation[2,3]=pose_TCP.position.z

    rate = rospy.Rate(10) # 10hz
    br = tf2_ros.TransformBroadcaster()
    listener = tf.TransformListener()

    #camera-home position from where the point cloud is taken. (It can change it does not matter)
    object_ur10.go_to_joint_state([0.018217895179986954,  -1.7413442770587366,  1.7994475364685059,  -0.47932321230043584,  1.5953648090362549,  -0.018981281911031544] )
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
        print('>>> Ready to take scene data!!!')
        #print('   >>>>  press {} to take a scene image...'.format(str(t)))
        #Enter to process a depth image and generate the 6D pose estimation
        command=cv2.waitKey(1) & 0xFF
        #print('>>> Ready to take scene data!!!')
        if command == ord('t'):
            try:
                (trans,rot) = listener.lookupTransform('/world','/camera_link', rospy.Time(0))
                # Correction of my transform in order to have in openCV convention
                q_corre = tf.transformations.quaternion_from_euler(math.pi/2,-math.pi/2,0)
                q_corre[3]=-q_corre[3]
                q2=quaternion_multiply(rot,q_corre)
                #PACKAGING THE TF FOR EACH SCENE TAKEN BY THE CAMERA
                Rq = quaternion_matrix(q2)
                Rq[0,3],Rq[1,3],Rq[2,3]=trans[0],trans[1],trans[2]
                tf_cloud=Rq
                #print('Quaternion in openCV Convention: \n {}'.format(q2))
                #print('Rotation in openCV Convention: \n {}'.format(Rq))

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                print('error in the listening transform')
                continue
            counter1+=1
            """Get a scene cloud in the world coordinate system"""
            pcd=do_pointcloud(frame,pc,counter1,tf_cloud)
            #in order to not modify the original point cloud...
            cloud=copy.deepcopy(pcd)

            # Thresholding the point cloud in order to get rid of undesirable points.
            filter = do_passthrough_filter(point_cloud = cloud,name_axis = 'x', min_axis = 0.50, max_axis = 1.50)
            filter = do_passthrough_filter(point_cloud = filter,name_axis = 'y', min_axis = -0.60, max_axis = 0.60)
            pcl.save(filter,scene_path +'filter_'+str(counter1)+'.pcd' )
            #pcl.save(filter,scene_path +'filter_'+str(counter1)+'.ply' )
            print('filter done!')

            # Segmentation process in order to separate the objecscene_path+'objects_'+str(counter1)+'.pcd't from table
            table, objects = do_ransac_plane_segmentation(filter, max_distance = 0.01)
            pcl.save(objects,scene_path +'objects_'+str(counter1)+'.pcd' )
            pcl.save(objects,scene_path +'objects_'+str(counter1)+'.ply' )
            print('segmentation done!')

            #The target cloud is a scene image, it is already mapped into the world coordinate system (T: Worldobject_robot -> Camera)
            target=read_point_cloud(scene_path+'objects_'+str(counter1)+'.pcd')

            #Template to match with the image taken from scene
            source=read_point_cloud(model_path+'template'+'.ply')

            #DOWNSAMPLE AND COMPUTE FAST POINT FEATURE HISTOGRAM-->PREPROCESSING STEP: DATA MANIPULATION OF THE POINT CLOUD
            source, target, source_down, target_down, source_fpfh, target_fpfh=do_dataset(source,target)
            #draw_geometries([source_down,target_down])

            #RANSAC REGISTRATION-->>global registration
            ransac_output=do_ransac_registration(source_down, target_down, source_fpfh, target_fpfh )

            #ICP REGISTRATION -->>local registration, point to plane approach
            icp_output = do_icp_registration(source_down, target_down,ransac_output.transformation)
            transformation=icp_output.transformation
            do_publishing_pose(br,icp_output.transformation)
            #do_drawing_registration(source, target, ransac_output.transformation)
            #do_drawing_registration(source, target, icp_output.transformation)
        do_publishing_pose(br,transformation)
        cv2.imshow('frame',frame)
        #rate.sleep()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    object_ur10 = UniversalRobot()
    camObj=camera()
    main()


 