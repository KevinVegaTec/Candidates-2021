#!/usr/bin/env python3
# license removed for brevity
import rospy
import time
from geometry_msgs.msg import Pose, Quaternion
from moveit_msgs.msg import Grasp

def arm_movement():
    pub_arm_movement = rospy.Publisher('arm_movement_data', Grasp, queue_size=10)
    grasp = Grasp()
    pub_arm_movement.publish(grasp)
    rospy.loginfo("Arm movement stimuli published.")

def neck_movement():
    pub_neck_movement = rospy.Publisher('neck_movement_data', Quaternion, queue_size=10)
    quat = Quaternion()
    quat.x = 0.0
    quat.y = 0.0
    quat.z = 0.0
    quat.w = 1.0
    pub_neck_movement.publish(quat)
    rospy.loginfo("Neck movement stimuli published.")

def elevator_movement():
    pub_elevator_movement = rospy.Publisher('elevator_movement_data', Pose, queue_size=10)
    p = Pose()
    p.position.x = 0.0
    p.position.y = 0.4
    p.position.z = 0.0
    p.orientation.x = 0.0
    p.orientation.y = 0.0
    p.orientation.z = 0.0
    p.orientation.w = 1.0
    pub_elevator_movement.publish(p)
    rospy.loginfo("Elevator movement stimuli published.")

if __name__ == '__main__':
    try:
        rospy.init_node('mock_mechanical_stimuli', anonymous=True)
        while not rospy.is_shutdown():
            arm_movement()
            neck_movement()
            elevator_movement()
            time.sleep(1)
    except rospy.ROSInterruptException:
        pass