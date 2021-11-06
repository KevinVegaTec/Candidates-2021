#!/usr/bin/env python3

from io import StringIO
from os import truncate
from geometry_msgs import msg
import roslib
roslib.load_manifest('integration')
import rospy
import actionlib
import random
from std_msgs.msg import String
from std_msgs.msg import UInt16
from integration.msg import armAction, armGoal, neckAction, neckGoal, elevatorAction, elevatorGoal

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

if __name__ == '__main__':
    rospy.init_node('Mechanism_Action_Client', anonymous=True)
    arm_client = actionlib.SimpleActionClient('arm_movement',armAction)
    neck_client = actionlib.SimpleActionClient('neck_movement',neckAction)
    elevator_client = actionlib.SimpleActionClient('elevator_movement',elevatorAction)
    


    print('Insert an option to make the simulation:')
    print('1 = arm:')
    print('2 = neck')
    print('3 = elevator')
    print('4 = system_healt')
    option = int(input())
    
    while (option != 0):
        print ('option = ',option)
        

        if option == 1:
            arm_goal = armGoal()
            arm_goal = rospy.Subscriber('arm_movement',armAction,callback)

        elif option == 2:
            neck_goal = neckGoal()
            neck_goal = rospy.Subscriber('neck_movement', neckAction, callback)
        
        elif option == 4:
            rospy.Subscriber('system_health',UInt16, callback)
            rospy.spin()
            
        
        elif option == 3:
            elevator_goal = elevatorGoal()
            elevator_goal = rospy.Subscriber('elevator_movement', elevatorAction, callback)
        option = int(input('Insert an option: '))
        

