#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Cesar Sinchiguano <cesarsinchiguano@hotmail.es>
#
# Distributed under terms of the MIT license.

"""

"""
import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import sys
sys.path.insert(0, '/home/casch/ws_moveit/src/perception_cvut/src/project')
from thesis_class import *
from thesis_class import camera
from geometry_msgs.msg import Quaternion
#aruco setup
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)


def print_information(rvec,tvec,rmatrix):


    # print("\n\nThe aruco_marker frame in -->> camera_link frame:")
    # print("===R:")
    # print(rmatrix)
    # print("===t:")
    # print(tvec.reshape(1,3))

    print("\n\nThe camera_link frame in -->>aruco_marker frame:")
    print("=== R:")
    print(rmatrix.T)
    print("=== t:")
    print(-np.dot(rmatrix.T, tvec.reshape(3,1)))
    print('\n\n-----------------------------------------------------')

def publish_transforms(br,mat,t,ids):

    t2 = geometry_msgs.msg.TransformStamped()
    t2.header.stamp = rospy.Time.now()
    t2.header.frame_id = "camera_link"
    t2.child_frame_id = "aruco_link"+ids
    t2.transform.translation.x = 1.0*t[0]
    t2.transform.translation.y = 1.0*t[1]
    t2.transform.translation.z = 1.0*t[2]
    #orientation according to openCV
    q3 = tf.transformations.quaternion_from_matrix(mat)
    t2.transform.rotation.x = q3[0]
    t2.transform.rotation.y = q3[1]
    t2.transform.rotation.z = q3[2]
    t2.transform.rotation.w = q3[3]
    br.sendTransform(t2)


def data_to_transform(r_matrix,t_position):
    t_position

    mat =np.hstack((r_matrix,t_position))
    mat=np.vstack((mat,[0.0,0.0,0.0,1.0]))
    return mat

def main():

    rate = rospy.Rate(10) # 10hz
    counter=0
    br = tf2_ros.TransformBroadcaster()

    # Intrinsic parameters for the real sense camera
    list_matrix=[605.639808, 0.000000, 299.642146, 0.000000, 605.730544, 253.182947, 0.000000, 0.000000, 1.000000]
    cameraMatrix_ar=np.asarray(list_matrix).reshape(3,3)
    distCoef=[0.100646, -0.217538, 0.000350, -0.004858, 0.000000]
    distCoef_ar=np.asarray(distCoef).reshape(len(distCoef),1)

    while not rospy.is_shutdown():
        counter+=1
        frame=camObj.get_image()

        if frame is None:
            print('no image!!!')
            continue
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite('temp'+str(counter)+'.jpg', frame)
            break

        #Post processing for aruco detector
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        # font for displaying text (below)
        font = cv2.FONT_HERSHEY_SIMPLEX

        try:
            # check if the ids list is not empty
            # if no check is added the code will crash
            if np.all(ids != None):
                # estimate pose of each marker and return the values rvet and tvec-different from camera coefficients
                rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, 0.055, cameraMatrix_ar,distCoef_ar)
                #(rvec-tvec).any() # get rid of that nasty numpy value array error
                print('----------------------')
                #print('rvec \n{}'.format(rvec))
                print('tvec \n{}'.format(tvec))
                print('----------------------')

                for i in range(0, ids.size):
                    # draw axis for the aruco markers
                    aruco.drawAxis(frame, cameraMatrix_ar, distCoef_ar, rvec[i], tvec[i], 0.1)

                # draw a square around the markers
                aruco.drawDetectedMarkers(frame, corners)

                # code to show ids of the marker found
                for i in range(len(ids)):
                    c = corners[i][0]#this is one retrieve the corner of the first marker
                    x=int(c[:, 0].mean()+25.0)
                    y=int(c[:, 1].mean()+0.0)
                    cv2.putText(frame, "Id: " + str(ids[i]),(x,y), font, 1, (0,255,0),2,cv2.LINE_AA)

                    # print information about rotation and translation for the camera and world frame
                    rmatrix = cv2.Rodrigues(rvec[i])[0]
                    #print_information(rvec[i],tvec[i],rmatrix)

                    # get transform matrix from rotation and translation of the camera frame relative to the world frame
                    #mat=data_to_transform(rmatrix.T,-np.dot(rmatrix.T, tvec[i].reshape(3,1)))
                    mat=data_to_transform(rmatrix,tvec[i].reshape(3,1))


                    # publish transform for the following coordinate frames: target, camera and world
                    publish_transforms(br,mat,tvec[i].reshape(3,1),str(ids[i]))

                    del mat
                    rate.sleep()


        except Exception as ex:
            print('Please, point into the aruco markers!!!')
            print(ex)
            continue
        cv2.imshow('Target locator',frame)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    camObj=camera()
    main()



# print('corners[i] \n{}'.format(corners[i]))
# print('corners[i][0] \n{}'.format(corners[i][0]))
# print('type(corners[i][0]) \n{}'.format(type(corners[i][0])))

#help
# fig = plt.figure()
# nx = 4
# ny = 3
# for i in range(1, nx*ny+1):
#     ax = fig.add_subplot(ny,nx, i)
#     img = aruco.drawMarker(aruco_dict,i, 700)
#     plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
#     ax.axis("off")

# plt.savefig("markers.pdf")
# plt.show()
#
# frame = cv2.imread("testphoto.png")
# #Post processing
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
# parameters =  aruco.DetectorParameters_create()
# corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
# frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
# plt.figure()
# plt.imshow(frame)
# plt.show()
#
# #Results
# plt.figure()
# plt.imshow(frame_markers)
# for i in range(len(ids)):
#     c = corners[i][0]
#     plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "o", label = "id={0}".format(ids[i]))
# plt.legend()
# plt.show()



# for i in range(0, ids.size):
#     strg += str(ids[i][0])+','
# print('corners shape: {}'.format(corners[0].shape))
# print('corners type: {}'.format(type(corners)))
# print('corners[0]: {}'.format(corners[0]))
# print('ids len: {}'.format(len(ids)))
# print('ids type: {}'.format(type(ids)))
# print('ids: {}'.format(ids))
