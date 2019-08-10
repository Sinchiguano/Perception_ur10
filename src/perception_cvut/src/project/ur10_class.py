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

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
import time


def all_close(goal, actual, tolerance):
  """
  Convenience method for testing if a list of values are within a tolerance of their counterparts in another list
  @param: goal       A list of floats, a Pose or a PoseStamped
  @param: actual     A list of floats, a Pose or a PoseStamped
  @param: tolerance  A float
  @returns: bool
  """
  all_equal = True
  if type(goal) is list:
    for index in range(len(goal)):
      if abs(actual[index] - goal[index]) > tolerance:
        return False

  elif type(goal) is geometry_msgs.msg.PoseStamped:
    return all_close(goal.pose, actual.pose, tolerance)

  elif type(goal) is geometry_msgs.msg.Pose:
    return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)

  return True


class UniversalRobot(object):
  """UniversalRobot"""
  def __init__(self):
    super(UniversalRobot, self).__init__()

    ## First initialize `moveit_commander`_ and a `rospy`_ node:
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface', anonymous=True)

    ## Instantiate a `RobotCommander`_ object. Provides information such as the robot's
    ## kinematic model and the robot's current joint states
    robot = moveit_commander.RobotCommander()

    ## Instantiate a `PlanningSceneInterface`_ object.  This provides a remote interface
    ## for getting, setting, and updating the robot's internal understanding of the
    ## surrounding world:
    scene = moveit_commander.PlanningSceneInterface()

    ## Instantiate a `MoveGroupCommander`_ object.  This object is an interface
    ## to a planning group (group of joints). We set the group's name to "panda_arm".
    ## If you are using a different robot, change this value to the name of your robot
    ## arm planning group.
    ## This interface can be used to plan and execute motions:# see more methods in the repository of the MoveGroupCommander
    move_group = moveit_commander.MoveGroupCommander("manipulator")
    #i did it
    #move_group_g = moveit_commander.MoveGroupCommander("endeffector")
    #exit(0)


    ## Create a `DisplayTrajectory`_ ROS publisher which is used to display
    ## trajectories in Rviz:
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory,queue_size=20)


    ## Getting Basic Information
    # We can get the name of the reference frame for this robot:
    planning_frame = move_group.get_planning_frame()
    print "============ Planning frame: %s" % planning_frame

    # We can also print the name of the end-effector link for this group:
    eef_link = move_group.get_end_effector_link()
    print "============ End effector link: %s" % eef_link

    # We can get a list of all the groups in the robot:
    group_names = robot.get_group_names()
    print "============ Available Planning Groups:", robot.get_group_names()

    # Sometimes for debugging it is useful to print the entire state of the
    # robot:
    print "============ Printing robot state"
    print robot.get_current_state()
    print ""
    print "============ Printing robot joint values"
    print move_group.get_current_joint_values()
    print ""
    print "============ Printing robot pose"
    print move_group.get_current_pose()
    print ""
    # print "============ Printing robot pose"
    # print move_group.get_current_pose().pose
    # print ""

    # set the maximum velocity of the joint values
    move_group.set_max_velocity_scaling_factor(0.075)

    minX=0.10
    minY=0.10
    minZ=0.10
    maxX=1.5
    maxY=1.5
    maxZ=2.0
    # Set the workspace for the robot as either
    move_group.set_workspace([minX, minY, minZ, maxX, maxY, maxZ])


    # print "============ Printing robot pose"
    # print move_group.get_current_pose()
    # print ""

    # Misc variables
    self.box_name = ''
    self.robot = robot
    self.scene = scene
    self.move_group = move_group
    #self.move_group_g=move_group_g
    self.display_trajectory_publisher = display_trajectory_publisher
    self.planning_frame = planning_frame
    self.eef_link = eef_link
    self.group_names = group_names

  def go_to_joint_state(self):

    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    move_group = self.move_group

    ## Planning to a Joint Goal
    #Home Position
    joint_goal=[0.543819785118103, -1.6310613791095179, 1.0388636589050293, -0.7879875341998499, 1.6518089771270752, 0.043724071234464645]


    #plan to the new joint space goal and visualize the plan
    move_group.set_joint_value_target(joint_goal)
    move_group.plan()

    # #for safety reasons
    # print "\n============ Enter #1 to execute or any number to skip the plan!"
    # temp=raw_input()
    # control_signal=int(temp)

    # if control_signal==1:
    #Uncomment below line when working with a real robot
    # The go command can be called with joint values, poses, or without any
    # parameters if you have already set the pose or joint target for the group
    move_group.go(wait=True)

    # #When working with the real robot uncomment the following line...
    # move_group.set_joint_value_target(joint_goal)
    # plan = move_group.plan()
    # move_group.execute(plan)

    # Calling ``stop()`` ensures that there is no residual movement
    move_group.stop()

    #del joint_goal[:]

    # For testing:
    current_joints = move_group.get_current_joint_values()
    return all_close(joint_goal, current_joints, 0.01)

  def go_to_pose_goal(self,tmp_pose):
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    move_group = self.move_group

    ## Planning to a Pose Goal
    ## We can plan a motion for this group to a desired pose for the
    ## end-effector:
    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation=tmp_pose.orientation
    pose_goal.position = tmp_pose.position

    move_group.set_pose_target(pose_goal)
    move_group.plan()
    #for safety reasons
    # print "\n============ Enter #1 to execute or any number to skip the plan!"
    # temp=raw_input()
    # control_signal=int(temp)


    #if control_signal==1:
    ## Now, we call the planner to compute the plan and execute it.
    move_group.go(wait=True)

    #When working with the real robot uncomment the following line...
    #it does not work with execute in this control manner
    #move_group.execute(plan)

    # Calling `stop()` ensures that there is no residual movement
    move_group.stop()
    # It is always good to clear your targets after planning with poses.
    # Note: there is no equivalent function for clear_joint_value_targets()
    move_group.clear_pose_targets()

    # For testing:
    # Note that since this section of code will not be included in the tutorials
    # we use the class variable rather than the copied state variable
    current_pose = self.move_group.get_current_pose().pose
    return all_close(pose_goal, current_pose, 0.01)

  def plan_cartesian_path(self, scale=1):
    move_group = self.move_group

    ## Cartesian Paths

    ## You can plan a Cartesian path directly by specifying a list of waypoints
    ## for the end-effector to go through. If executing  interactively in a
    ## Python shell, set scale = 1.0.
    waypoints = []

    wpose = move_group.get_current_pose().pose
    wpose.position.z -= scale * 0.1  # First move up (z)
    wpose.position.y += scale * 0.4  # and sideways (y)
    wpose.position.y -= scale * 0.2
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.x += scale * 0.5  # Second move forward/backwards in (x)
    wpose.position.x -= scale * 0.3
    waypoints.append(copy.deepcopy(wpose))


    wpose.position.x = scale * 0.2  # Third move sideways (y)
    wpose.position.y = scale * 0.2
    wpose.position.z += scale * 0.2
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.x += scale * 0.4  # Fourth move backwards/left side
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.y += scale * 0.3
    waypoints.append(copy.deepcopy(wpose))


    # We want the Cartesian path to be interpolated at a resolution of 1 cm
    # which is why we will specify 0.01 as the eef_step in Cartesian
    # translation.  We will disable the jump threshold by setting it to 0.0,
    # ignoring the check for infeasible jumps in joint space, which is sufficient
    # for this tutorial.
    (plan, fraction) = move_group.compute_cartesian_path(
                                       waypoints,   # waypoints to follow
                                       0.01,        # eef_step
                                       0.0)         # jump_threshold
    #When working with the real robot uncomment the following line...
    #move_group.execute(plan)
    # Note: We are just planning, not asking move_group to actually move the robot yet:
    return plan, fraction

  def display_trajectory(self, plan):

    robot = self.robot
    display_trajectory_publisher = self.display_trajectory_publisher

    ## Displaying a Trajectory
    ## You can ask RViz to visualize a plan (aka trajectory) for you. But the
    ## group.plan() method does this automatically so this is not that useful
    ## here (it just displays the same trajectory again):
    ## A `DisplayTrajectory`_ msg has two primary fields, trajectory_start and trajectory.
    ## We populate the trajectory_start with our current robot state to copy over
    ## any AttachedCollisionObjects and add our plan to the trajectory.
    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan)
    # Publish
    display_trajectory_publisher.publish(display_trajectory);

  def execute_plan(self, plan):
    move_group = self.move_group

    #for safety reasons
    print "\n============ Enter #1 to execute or any number to skip the plan!"
    temp=raw_input()
    control_signal=int(temp)

    if control_signal==1:
        ## Executing a Plan
        ## Use execute if you would like the robot to follow
        ## the plan that has already been computed:
        move_group.execute(plan, wait=True)

        ## **Note:** The robot's current joint state must be within some tolerance of the
        ## first waypoint in the `RobotTrajectory`_ or ``execute()`` will fail
        ############################

  def wait_for_state_update(self, box_is_known=False, box_is_attached=False, timeout=4):
    box_name = self.box_name
    scene = self.scene

    ## Ensuring Collision Updates Are Receieved
    ## If the Python node dies before publishing a collision object update message, the message
    ## could get lost and the box will not appear. To ensure that the updates are
    ## made, we wait until we see the changes reflected in the
    ## ``get_attached_objects()`` and ``get_known_object_names()`` lists.
    ## For the purpose of this tutorial, we call this function after adding,
    ## removing, attaching or detaching an object in the planning scene. We then wait
    ## until the updates have been made or ``timeout`` seconds have passed
    start = rospy.get_time()
    seconds = rospy.get_time()
    while (seconds - start < timeout) and not rospy.is_shutdown():
      # Test if the box is in attached objects
      attached_objects = scene.get_attached_objects([box_name])
      is_attached = len(attached_objects.keys()) > 0

      # Test if the box is in the scene.
      # Note that attaching the box will remove it from known_objects
      is_known = box_name in scene.get_known_object_names()

      # Test if we are in the expected state
      if (box_is_attached == is_attached) and (box_is_known == is_known):
        return True

      # Sleep so that we give other threads time on the processor
      rospy.sleep(0.1)
      seconds = rospy.get_time()

    # If we exited the while loop without returning then we timed out
    return False

  def add_box(self, timeout=4):
    box_name = self.box_name
    scene = self.scene
    eef_link = self.eef_link

    ## Adding Objects to the Planning Scene
    ## First, we will create a box in the planning scene at the location of the left finger:
    box_pose = geometry_msgs.msg.PoseStamped()
    #changed
    box_pose.header.frame_id = "tool0"
    box_pose.pose.orientation.w = 1.0
    box_pose.pose.position.z = 0.07 # slightly above the end effector
    box_name = "box"
    scene.add_box(box_name, box_pose, size=(0.1, 0.1, 0.1))

    ## END_SUB_TUTORIAL
    # Copy local variables back to class variables. In practice, you should use the class
    # variables directly unless you have a good reason not to.
    self.box_name=box_name
    return self.wait_for_state_update(box_is_known=True, timeout=timeout)

  def attach_box(self, timeout=4):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    box_name = self.box_name
    robot = self.robot
    scene = self.scene
    eef_link = self.eef_link
    group_names = self.group_names

    ## BEGIN_SUB_TUTORIAL attach_object
    ## Attaching Objects to the Robot
    ## Next, we will attach the box to the Panda wrist. Manipulating objects requires the
    ## robot be able to touch them without the planning scene reporting the contact as a
    ## collision. By adding link names to the ``touch_links`` array, we are telling the
    ## planning scene to ignore collisions between those links and the box. For the Panda
    ## robot, we set ``grasping_group = 'hand'``. If you are using a different robot,
    ## you should change this value to the name of your end effector group name.
    grasping_group = 'endeffector'
    #grasping_group = 'eef_link
    touch_links = robot.get_link_names(group=grasping_group)
    scene.attach_box(eef_link, box_name, touch_links=touch_links)

    # We wait for the planning scene to update.
    return self.wait_for_state_update(box_is_attached=True, box_is_known=False, timeout=timeout)

  def detach_box(self, timeout=4):
    box_name = self.box_name
    scene = self.scene
    eef_link = self.eef_link

    ## Detaching Objects from the Robot
    ## We can also detach and remove the object from the planning scene:
    scene.remove_attached_object(eef_link, name=box_name)

    # We wait for the planning scene to update.
    return self.wait_for_state_update(box_is_known=True, box_is_attached=False, timeout=timeout)

  def remove_box(self, timeout=4):
    box_name = self.box_name
    scene = self.scene

    ## Removing Objects from the Planning Scene
    ## We can remove the box from the world.
    scene.remove_world_object(box_name)

    # We wait for the planning scene to update.
    return self.wait_for_state_update(box_is_attached=False, box_is_known=False, timeout=timeout)


g_timestamp_last_move = 0
g_index_last_move = 0

poses=list()


goal_0=geometry_msgs.msg.Pose()
goal_1 = geometry_msgs.msg.Pose()
goal_2 = geometry_msgs.msg.Pose()
goal_3 = geometry_msgs.msg.Pose()
goal_4 = geometry_msgs.msg.Pose()
goal_5 = geometry_msgs.msg.Pose()
goal_6 = geometry_msgs.msg.Pose()



home = goal_0
home.position.x,home.position.y,home.position.z=[0.615913613984735,  0.07210064263944486,  0.621327238895192]
home.orientation.x,home.orientation.y,home.orientation.z,home.orientation.w=[0.8367270065269945,  0.5475591046852049,  0.0020334764183821763,  0.007925174973952662]


goal_1.position.x,goal_1.position.y,goal_1.position.z=[0.5431634459144228,  0.3460516614635293,  0.6174751967102612]
goal_1.orientation.x,goal_1.orientation.y,goal_1.orientation.z,goal_1.orientation.w=[0.8367017529807473,  0.5475980995961437,  0.0021940696979265303,  0.00785391213325322]


goal_2.position.x,goal_2.position.y,goal_2.position.z=[0.6777887837408033,  0.28724752649592133,  0.6197333476680801]
goal_2.orientation.x,goal_2.orientation.y,goal_2.orientation.z,goal_2.orientation.w=[0.8366770329505939,  0.5476363676414185,  0.0021869381929580677,  0.007821040266094063]


goal_3.position.x,goal_3.position.y,goal_3.position.z= [0.7035537422125395,  0.15545948941081,  0.6214753637348197]
goal_3.orientation.x,goal_3.orientation.y,goal_3.orientation.z,goal_3.orientation.w=[0.7928890857866161,  0.6093131455713582,  0.0018206948021379473,  0.007814943687480098]

# goal_4.position.x,goal_4.position.y,goal_4.position.z=[0.5790982810443824,  0.2805584983724089,  0.6288600393880597]
# goal_4.orientation.x,goal_4.orientation.y,goal_4.orientation.z,goal_4.orientation.w=[0.7164356517168392,  0.6970396839083701,  0.0203875345583521,  0.02097580607793485]

poses.append(home)
poses.append(goal_1)
poses.append(goal_2)
poses.append(goal_3)
#poses.append(goal_4)


# goal_5.position.x,goal_5.position.y,goal_5.position.z=[0.6417158998054968,  0.014154900775432716,  0.6320462367429978]
# goal_5.orientation.x,goal_5.orientation.y,goal_5.orientation.z,goal_5.orientation.w= [0.7192697008221377,  0.6893961430164041,  0.05879839572913152,  0.06266421732550821]
# poses.append(goal_5)
#
# goal_6.position.x,goal_6.position.y,goal_6.position.z=[0.6674803539261742,  0.012621903092877501,  0.4834825855314617]
# goal_6.orientation.x,goal_6.orientation.y,goal_6.orientation.z,goal_6.orientation.w= [0.7192509645358769,  0.6894194283159346,  0.05879273161768367,  0.06262840077530146]
# poses.append(goal_6)

import sys, time
# numpy and scipy
import numpy as np
from scipy.ndimage import filters
# OpenCV
import cv2
# Ros libraries
import roslib
import rospy
from cv_bridge import CvBridge, CvBridgeError
# Ros Messages
from sensor_msgs.msg import Image, CameraInfo, PointCloud2
import sensor_msgs.point_cloud2 as pc2

bridge = CvBridge()
import copy
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String

#for mesh and pcd
import copy
import numpy as np
import time
#from matplotlib import pyplot as plt
import math
from transforms3d.euler import euler2mat, mat2euler
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from pyquaternion import Quaternion
import tf
import tf2_ros
import geometry_msgs.msg
import scipy
from tf.transformations import *
import pcl
# default camera!!!
class camera(object):
    def __init__(self):
        # In ROS, nodes are uniquely named.
        #rospy.init_node('camera', anonymous=True)
        # #Real sense camera
        rospy.Subscriber('/camera/color/image_raw', Image, self.callback_rgb)
        rospy.Subscriber('/camera/aligned_depth_to_color/image_raw', Image, self.callback_depth)
        rospy.Subscriber('/camera/depth/color/points', PointCloud2, self.callback_pointCloud)
        #rospy.Subscriber('/camera/color/camera_info', CameraInfo,self.infoColorCallback)
        #rospy.Subscriber('/camera/depth/image_rect_raw', CameraInfo, self.callback_depth)

        self.cv_image1=None
        self.cv_image2=None
        self.pc=None

    def callback_rgb(self,data):
        #global cv_image1
        #### direct conversion to CV2 ####
        try:
          self.cv_image1 = bridge.imgmsg_to_cv2(data, "bgr8")
          #print(type(cv_image1))
        except CvBridgeError as e:
          print(e)
          #print()

    def callback_depth(self,data):
        #global cv_image2
        try:
            self.cv_image2 = bridge.imgmsg_to_cv2(data, "passthrough")
            #print(type(self.cv_image2))
        except CvBridgeError as e:
            #print()
            print(e)
            #return None
        #return cv_image
        # cv2.imshow("Depth image. By: Casch!!!", cv_image2)
        # cv2.waitKey(3)

    def callback_pointCloud(self,data):
        #print('data',type(data))
        if data is not None:
            #print('there is something at least!!!')
            pts = list(pc2.read_points(data, skip_nans=False, field_names=("x", "y", "z")))
            #print('temp',type(temp))
            #astra camera
            if len(pts) == 307200:
                self.pc = np.array(list(pts)).reshape((480,640,3))
            # else:
            #     #just for realsense camera
            #     points_list = []
            #     for data in pc2.read_points(data, skip_nans=False, field_names=("x", "y", "z")):
            #         points_list.append([data[0], data[1], data[2]])
            #
            #     pcl_data = pcl.PointCloud_PointXYZ()
            #     pcl_data.from_list(points_list)
            #     self.pc=pcl_data
        else:
            rospy.logerr("No point cloud image, did you initialize Turtlebot(pc=True)")

    def infoDepthCallback(self,msg):
        print('received info from depth camera!!!',msg)
    def infoColorCallback(self,msg):
        rospy.loginfo("received info from color camera!!!%s",msg)

    def get_image(self):
        return self.cv_image1
    def get_depth(self):
        return self.cv_image2
    def get_point_cloud(self):
        return self.pc
