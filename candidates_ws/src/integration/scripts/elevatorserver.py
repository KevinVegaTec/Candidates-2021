#! /usr/bin/env python3

import roslib
roslib.load_manifest('integration')
import rospy
import actionlib
import random
from integration.msg import elevatorFeedback, elevatorAction, elevatorResult


class elevatorserver:

    _feedback = elevatorFeedback()
    _result = elevatorResult()

    def __init__(self):
        self.server = actionlib.SimpleActionServer('elevator_movement', elevatorAction, self.execute(), False)
        self.server.start()

    def execute(self, goal):

        r = rospy.Rate(1)
        success = True
        self._result = 3
        self._feedback = 0

        aux = 0
        while aux < 2:
            # Needs goal validation ?
            self.server.publish_feedback(self._feedback)
            self._feedback = aux
            if self._feedback == 0:
                print('Calculating FK')
                r.sleep()
                
            elif self._feedback == 1:
                print('Executing elevator movement')
                r.sleep()
                self._result = 1
    
            else:
                self._result = 2
            aux = aux + 1

        if success:
            self._result = 0
            rospy.loginfo('Succeeded moving elevator')
            self.server.set_succeeded(self._result) 
        
        



if __name__ == '__main__':
    rospy.init_node('elevator_server')
    server = elevatorserver()
    rospy.spin()