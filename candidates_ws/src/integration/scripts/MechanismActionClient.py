#!/usr/bin/env python3

from geometry_msgs import msg
import roslib
roslib.load_manifest('integration')
import rospy
import actionlib
import random
from integration.msg import armAction, armGoal, neckAction, neckGoal, elevatorAction, elevatorGoal
mechani

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

if __name__ == '__main__':
    rospy.init_node('Mechanism_Action_Client')
    arm_client = actionlib.SimpleActionClient('arm_movement')
    neck_client = actionlib.SimpleActionClient('neck_movement')
    elevator_client = actionlib.SimpleActionClient('elevator_movement')

    print('Insert an option:')
    print('1 = arm:')
    print('2 = neck')
    print('3 = elevator')
    option = input()
    
    while (option != 0):
        

        if option == 1:
            arm_goal = armGoal()
            arm_goal = rospy.Subscriber('arm_movement',armAction,callback)

        elif option == 2:
            neck_goal = neckGoal()
            neck_goal = rospy.Subscriber('neck_movement', neckAction, callback)
        
        elif option == 3:
            elevator_goal = elevatorGoal()
            elevator_goal = rospy.Subscriber('elevator_movement', elevatorAction, callback)
        option = input('Insert an option: ')
