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

#The order matters
from thesis_class import *
import glob


import numpy as np
import cv2
import cv2.aruco as aruco
import glob


#path_images='images_camera/'

path_images='image_smartek/'

calibration_data = np.load('image_smartek/calibration.npy',allow_pickle=True)
mtx = calibration_data[0]
dist = calibration_data[1]
rvecs = calibration_data[2][1]
tvecs = calibration_data[3][1]

print(mtx)
print(dist)
exit(0)

def main():
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # # prepare object points for a 8x6 chess board
    # objp = np.zeros((7*9,3), np.float32)
    # objp[:,:2] = np.mgrid[0:7,0:9].T.reshape(-1,2)

    #Vertical configuration
    x,y=np.meshgrid(range(8),range(9))#col row vertical
    objp=np.hstack((y.reshape(72,1)*0.01,x.reshape(72,1)*0.01,np.zeros((72,1)))).astype(np.float32)

    # #####################################################################
    # # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # # checkerboard of size (7 x 6) is used
    # objp = np.zeros((6*7,3), np.float32)
    # objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)


    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob(path_images+'/*.jpg')
    print(images[0])

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        #ret, corners = cv2.findChessboardCorners(gray, (7,9),None)
        ret, corners = cv2.findChessboardCorners(gray, (8,9),None)

        # #######################################################
        # # find the chess board (calibration pattern) corners
        # ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

        print('cesar sinc') 
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)
            #print(corners2)
            #exit(0)

            # Draw and display the corners
            #img = cv2.drawChessboardCorners(img, (7,9), corners2,ret)
            img = cv2.drawChessboardCorners(img, (8,9), corners2,ret)

            # ###############################
            # # Draw and display the corners
            # img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)

            cv2.imshow('img',img)
            cv2.waitKey(500)

    cv2.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    np.save('image_smartek/calibration', [mtx, dist, rvecs, tvecs])


    calibration_data = np.load('image_smartek/calibration.npy',allow_pickle=True)
    mtx = calibration_data[0]
    dist = calibration_data[1]
    rvecs = calibration_data[2][1]
    tvecs = calibration_data[3][1]

    print(mtx)
    print(dist)
    print(rvecs)
    print(tvecs)

if __name__ == '__main__':
    #camObj=camera()
    main()
    
