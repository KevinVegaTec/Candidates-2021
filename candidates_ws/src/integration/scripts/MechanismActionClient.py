#!/usr/bin/env python3

from io import StringIO
from logging import shutdown
from os import truncate
from geometry_msgs import msg
import roslib
from rospy import client
roslib.load_manifest('integration')
import rospy
import actionlib
import random
from std_msgs.msg import String
from std_msgs.msg import UInt16
from integration.msg import armAction, armGoal, neckAction, neckGoal, elevatorAction, elevatorGoal

from geometry_msgs.msg import Pose, Quaternion
from moveit_msgs.msg import Grasp


shutdown = None
global armg
global neckg 
global elevatorg 


def callbacksd(data):
    #rospy.loginfo("SH = %s", data.data)
    shutdown = data.data

def callbackarm(data2):
    global armg 
    armg = data2

def callbackneck(data3):
    global neckg
    neckg = data3

def callbackelevator(data4):
    global elevatorg
    elevatorg = data4

if __name__ == '__main__':
    rospy.init_node('Mechanism_Action_Client', anonymous=True)
    arm_client = actionlib.SimpleActionClient('arm_movement',armAction)
    neck_client = actionlib.SimpleActionClient('neck_movement',neckAction)
    elevator_client = actionlib.SimpleActionClient('elevator_movement',elevatorAction)
    shutdown = 0

    print('Insert an option to make the simulation:')
    print('1 = arm:')
    print('2 = neck')
    print('3 = elevator')
    rospy.Subscriber('arm_movement_data',Grasp,callbackarm)
    rospy.Subscriber('neck_movement_data',Quaternion,callbackneck)
    rospy.Subscriber('elevator_movement_data',Pose,callbackelevator)
    rospy.Subscriber('system_health',UInt16,callbacksd)
    

    option = int(input())
    
    while (option != 0) and (shutdown == 0):
        print ('option = ',option)
        

        if option == 1:
            
            arm_goal  = armGoal()
            
            print(arm_goal)
            #
            arm_goal.grasp.grasp_quality = (random.random()*11)
            print("---------------")
            arm_client.send_goal(arm_goal)
            print ("arm goal sent, waiting for response")
            arm_client.wait_for_result()
            print("Result = ", arm_client.get_result().result)
            
            

        elif option == 2:
            neck_goal = neckGoal()
            neck_client.send_goal(neck_goal)
            print ("neck goal sent, waiting for response")
            neck_client.wait_for_result()
            print("Result = ", neck_client.get_result().result)

        elif option == 3:
            elevator_goal = elevator_goal()
            elevator_client.send_goal(elevator_goal)
            print ("elevator goal sent, waiting for response")
            elevator_client.wait_for_result()
            print("Result = ", neck_client.get_result().result)
        
        option = int(input('Insert an option: '))
    
    if shutdown == 1:
        print("Putting everything in safe positions")
