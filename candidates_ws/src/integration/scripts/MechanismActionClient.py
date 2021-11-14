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
from geometry_msgs.msg import Pose, Quaternion
from moveit_msgs.msg import Grasp
from integration.msg import armAction, armGoal, neckAction, neckGoal, elevatorAction, elevatorGoal
from subprocess import call



sd = 0
# my tries to get the smituli correctly
armg = armGoal()
neckg = neckGoal()
elevatorg = elevatorGoal()
syshg = UInt16



def callbacksd(data):
    rospy.loginfo("SH = %s", data.data)
    global sd 
    sd = data.data
    if sd == 1:
        call(["rosnode", "kill", "/mock_mechanical_stimuli"])
        
        safepositions()
        rospy.signal_shutdown("something wrong happend")


def callbackarm(data2):
    global armg 
    armg = data2
    arm_goal  = armGoal()
    #rospy.Subscriber("arm_movement_data", Grasp, callbackarm)
    #print(grasp)
    #print ("-----------------------------------")
    #print(arm_goal.grasp)
    arm_goal.grasp = armg

    #
    arm_goal.grasp.grasp_quality = (random.random()*15) # Generates a random number, the service return 0 if the number is between 10 and 11
    print("---------------")
    arm_client.send_goal(arm_goal)
    print ("arm goal sent, waiting for response")
    state = 0
    aux = 0
    while aux == 0:
        try:
            print("Arm Result = ", arm_client.get_result().result)
            aux = 1
        except:
            nstate = arm_client.get_state()

            if (nstate != state):
                
                print("state = ",state)
                print("nstate = ",nstate)
                state = nstate

    #arm_client.wait_for_result()

    #print("Arm Result = ", arm_client.get_result().result)
    

def callbackneck(data3):
    global neckg
    neckg = data3
    neck_goal = neckGoal()
    neck_goal.posture = neckg
    neck_client.send_goal(neck_goal)
    print ("neck goal sent, waiting for response")
    neck_client.wait_for_result()
    print("Neck Result = ", neck_client.get_result().result)

def callbackelevator(data4):
    global elevatorg
    elevatorg = data4
    elevator_goal = elevatorGoal()
    elevator_goal.pose = elevatorg
    elevator_client.send_goal(elevator_goal)
    print ("elevator goal sent, waiting for response")
    elevator_client.wait_for_result()
    print("Elevator Result = ", elevator_client.get_result().result)

def safepositions():

    print("Putting the arm in a safe position")
    arm_goal  = armGoal()
    arm_goal.grasp.grasp_quality = 0
    arm_client.send_goal(arm_goal)
    print ("arm safe psoition goal sent, waiting for response")
    arm_client.wait_for_result()
    result = arm_client.get_result()
    print("Arm Result = ", result)
    if result.result == 0:
        print("The arm was successfuly move to his safe position")
    else:
        print("The arm failed to move to his safe position ")
    
    print("Putting the neck in a safe position")
    neck_goal  = neckGoal()
    neck_goal.posture.x = 0.1
    neck_goal.posture.y = 1.2
    neck_goal.posture.z = 2.3
    neck_goal.posture.w = 3.4
    neck_client.send_goal(neck_goal)
    print ("neck safe psoition goal sent, waiting for response")
    neck_client.wait_for_result()
    result = neck_client.get_result()
    print("neck Result = ", result)
    if result.result == 0:
        print("The neck was successfuly move to his safe position")
    else:
        print("The neck failed to move to his safe position ")

    print("Putting the elevator in a safe position")
    elevator_goal  = elevatorGoal()
    elevator_goal.pose.position.x = 0.1
    elevator_goal.pose.position.y = 1.2
    elevator_goal.pose.position.z = 2.3
    elevator_goal.pose.orientation.x = 3.4
    elevator_client.send_goal(elevator_goal)
    print ("elevator safe psoition goal sent, waiting for response")
    elevator_client.wait_for_result()
    result = elevator_client.get_result()
    print("elevator Result = ", result)
    if result.result == 0:
        print("The elevator was successfuly move to his safe position")
    else:
        print("The elevator failed to move to his safe position ")

    




    
if __name__ == '__main__':
    rospy.init_node('Mechanism_Action_Client', anonymous=True)
    arm_client = actionlib.SimpleActionClient('arm_movement',armAction)
    neck_client = actionlib.SimpleActionClient('neck_movement',neckAction)
    elevator_client = actionlib.SimpleActionClient('elevator_movement',elevatorAction)
    # creating the node and the 3 clients
    shutdown = 0
    print ("Waiting for servers...")
    arm_client.wait_for_server()
    print("Arm server ready")
    neck_client.wait_for_server()
    print("Neck server ready")
    elevator_client.wait_for_server()
    print("Elevator server ready")

    print('Insert an option to make the simulation:')
    print('1 = arm:')
    print('2 = neck')
    print('3 = elevator')
    rospy.Subscriber('arm_movement_data',Grasp,callbackarm)
    rospy.Subscriber('neck_movement_data',Quaternion,callbackneck)
    rospy.Subscriber('elevator_movement_data',Pose,callbackelevator)
    rospy.Subscriber('system_health',UInt16,callbacksd)
    # subscribing the node to the topics
    print(".................",sd)


    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("program interrupted before completion")