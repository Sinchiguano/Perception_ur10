#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Cesar Sinchiguano <cesarsinchiguano@hotmail.es>
#
# Distributed under terms of the MIT license.

"""
Inspired by MoveIt tutorial
"""
#from ur10_class_01 import *

import sys
sys.path.insert(0, '/home/casch/ws_moveit/src/perception_cvut/src/project')
#from ur10_class import *
from ur_cam_class import *
import time 

temp_flag=False
def main():
    #rospy.init_node('tcp_tf', anonymous=True)
    listener = tf.TransformListener()
    r=rospy.Rate(10)

    time.sleep(2)
    #i should give some time after i create the tf listener otherwise it's not going to work.
    (trans,rot) = listener.lookupTransform('/world','/pose_object', rospy.Time(0))
    previous_trans=trans
    previous_rot=rot

    #pose_goal = geometry_msgs.msg.Pose()
    temp_flag=False
    while(not rospy.is_shutdown()):
        try:
            print("flag:{}".format(temp_flag))
            (trans,rot) = listener.lookupTransform('/world','/pose_object', rospy.Time(0))
            roll_, pitch_, yaw_=tf.transformations.euler_from_quaternion(rot)
            #print('trans and rot: \n {} \n {}'.format(trans,rot))

            if not trans==None and not rot==None and not previous_trans==trans and not previous_rot==rot:
                # home position for the gasping action 
                object_ur10.go_to_joint_state([0.007624588906764984,  -1.2646663824664515,  1.7031769752502441,  -0.44650203386415654,  1.5900388956069946,  -0.0073769728290002945])                    
                ee_link=object_ur10.move_group.get_current_pose().pose
                print('pose_ee_link.position: \n{}'.format(ee_link.position))
                print('pose_ee_link.orientation: \n {}'.format(ee_link.orientation))
                q_home = [ee_link.orientation.x,ee_link.orientation.y,ee_link.orientation.z,ee_link.orientation.w]
                q_corr = quaternion_from_euler(0, 0, yaw_)
                q_goal = quaternion_multiply(q_corr, q_home)
                q_goal/=np.linalg.norm(q_goal)

                pose_goal = geometry_msgs.msg.Pose()
                pose_goal.position.x= trans[0]
                pose_goal.position.y= trans[1]
                pose_goal.position.z= trans[2]+0.01
                pose_goal.orientation.x = q_goal[0]
                pose_goal.orientation.y = q_goal[1]
                pose_goal.orientation.z = q_goal[2]
                pose_goal.orientation.w = q_goal[3]

                previous_trans=trans
                previous_rot==rot
                print('pose_goal {}'.format(pose_goal))
                temp_flag=True
        except rospy.ROSInterruptException:
            return
        except KeyboardInterrupt:
            return
        #print('pose_goal {}'.format(pose_goal))
        if temp_flag:
            # pose goal of the object to be lift
            object_ur10.go_to_pose_goal(pose_goal)
            time.sleep(2)

            # home position for the object
            pose_goal.position.x= 0.0
            pose_goal.position.y= 0.0
            pose_goal.position.z= 0.07
            object_ur10.go_to_pose_goal(pose_goal)
            time.sleep(2)


            object_ur10.go_to_joint_state([0.599541962146759,  -1.2912901083575647,  1.41935396194458,  -0.22077924409975225,  1.773498296737671,  -0.06576806703676397])
            time.sleep(2)
            
            # home position for camera
            object_ur10.go_to_joint_state([0.018217895179986954,  -1.7413442770587366,  1.7994475364685059,  -0.47932321230043584,  1.5953648090362549,  -0.018981281911031544] )
            time.sleep(2)
            temp_flag=False

        r.sleep()

if __name__ == '__main__':
    object_ur10 = UniversalRobot()
    main()






