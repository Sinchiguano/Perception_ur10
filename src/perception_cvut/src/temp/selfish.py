#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Cesar Sinchiguano <cesarsinchiguano@hotmail.es>
#
# Distributed under terms of the MIT license.

"""

"""

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Cesar Sinchiguano <cesarsinchiguano@hotmail.es>
#
# Distributed under terms of the MIT License license.

"""
Finally I got in xyz coordinates according to ROS
"""

import sys
sys.path.insert(0, '/home/casch/ws_moveit/src/perception_cvut/src/project')
from thesis_class import *
from thesis_class import camera
from geometry_msgs.msg import Quaternion

euler_angles_=[0,0,0]
position_=[0.0,0.0,0.0]

##convert a rot and trans matrix to a 4x4 matrix
def data_to_transform(r_matrix,t_position):
    mat =np.hstack((r_matrix,t_position))
    mat=np.vstack((mat,[0.0,0.0,0.0,1.0]))
    return mat


def main():

    counter=0
    tmpNamec='temp2.jpg'

    rate = rospy.Rate(10) # 10hz

    import sys
    print "This is the name of the script: ", sys.argv[0]
    #flag=sys.argv[1]

    while not rospy.is_shutdown():

        counter+=1
        frame=camObj.get_image()

        if frame is None:
            print('no image!!!')
            continue
        print('enter t to take a picture')

        if cv2.waitKey(1) & 0xFF == ord('t'):
            time.sleep(5)
            frame=camObj.get_image()
            cv2.imwrite('temp'+str(counter)+'.jpg', frame)
            print('done')

    
        try:
            cv2.imshow('Target locator',frame)
        except Exception as ex:
            print('-------------------------------------------------')
            continue


    # When everything done, release the capture
    cv2.destroyAllWindows()


if __name__ == '__main__':
    camObj=camera()
    main()

