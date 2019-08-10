#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Cesar Sinchiguano <cesarsinchiguano@hotmail.es>
#
# Distributed under terms of the MIT license.

"""
source: https://github.com/Sinchiguano/repo_project/tree/master/src/thesis_pkg/yumi_main/scripts/source_files
"""
import sys
sys.path.insert(0, '/home/casch/ws_moveit/src/perception_cvut/src/project')
from thesis_class import *
import glob


path_images='images_camera/'


def create_dataset_images(frame,counter):
    global path_images
    #we save the pcd in the following formats pcd and ply
    tmp=path_images+'img'+str(counter)
    cv2.imwrite(tmp+'.jpg', frame)

def main():
    counter1=0
    counter2=0

    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        counter1+=1

        # Capture 2D-data
        frame=camObj.get_image()
        aux= copy.deepcopy(frame)

        if frame is None:
            print('no Frame!!!')
            continue

        cv2.imshow('frame',frame)
        print('ready!!!')
        command=cv2.waitKey(3) & 0xFF
        if command == ord('p'):
            #time.sleep(1)
            counter2+=1
            create_dataset_images(aux,counter2)
            continue

        try:
            # 2D image points
            # To handle the corners array more easily, we can reshape it as follows
            ret, corners = cv2.findChessboardCorners(frame, (7,9))#coulmn and rows
            corners=corners.reshape(-1,2)#undefied number of rows
            cv2.drawChessboardCorners(frame, (7,9), corners, ret)

        except Exception as ex:
            print('\nStatus of findChessboardCorners: {}'.format(ret))
            print('Please, locate well the calibration target!!!')
            print(ex)
            print('-------------------------------------------------')
            continue





    # When everything done, release the capture
    cv2.destroyAllWindows()

if __name__ == '__main__':
    camObj=camera()
    main()
