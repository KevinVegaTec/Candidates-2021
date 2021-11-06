#! /usr/bin/env python3

import roslib
roslib.load_manifest('integration')
import rospy
import actionlib
import random
from integration.msg import neckFeedback, neckAction, neckResult


class neckserver:

    _feedback = neckFeedback()
    _result = neckResult()

    def __init__(self):
        self.server = actionlib.SimpleActionServer('neck_movement', neckAction, self.execute, False)
        self.server.start()

    def execute(self, goal):
        print(goal)
        r = rospy.Rate(1)
        success = True
        self._result = 3
        self._feedback.state = 0

        aux = 0
        while aux < 2:
            # Needs goal validation , a valid pose
            self.server.publish_feedback(self._feedback)
            self._feedback.state = aux
            if self._feedback.state == 0:
                print('First') # Simulating first state
                r.sleep()
                
            elif self._feedback.state == 1:
                print('Second') #Simulating second state
                r.sleep()
                self._result = 1
    
            else:
                self._result = 2 # Unknow error
            aux = aux + 1

        if success:
            self._result = 0
            rospy.loginfo('Succeeded moving neck') #succees
            self.server.set_succeeded(self._result) 
        
        



if __name__ == '__main__':
    rospy.init_node('neck_server')
    server = neckserver()
    rospy.spin()