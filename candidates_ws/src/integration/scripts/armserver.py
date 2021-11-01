#! /usr/bin/env python3

import roslib
roslib.load_manifest('integration')
import rospy
import actionlib
import random
from integration.msg import armFeedback, armAction, armResult


class armserver:

    _feedback = armFeedback()
    _result = armResult()

    def __init__(self):
        self.server = actionlib.SimpleActionServer('arm_movement', armAction, self.execute(), False)
        self.server.start()

    def execute(self, goal):

        r = rospy.Rate(1)
        success = True
        armResult = 3
        self._feedback = 0
        aux = 0

        while self.aux < 3:
            # Needs goal validation?
            self.server.publish_feedback(self._feedback)
            self._feedback = aux
            if self._feedback == 0:
                print('Calculating FK')
                r.sleep()
                
            elif self._feedback == 1:
                print('Executing arm movement')
                r.sleep()
                self._result = 1
            elif self._feedback == 2:
                print('Executing grip movement')
                r.sleep()
                self._result = 2
            else:
                self._result = 3
            aux = aux+1
        if success:
            self._result = 0
            rospy.loginfo('Succeeded moving arm')
            self.server.set_succeeded(self._result) 
        
        



if __name__ == '__main__':
    rospy.init_node('arm_server')
    server = armserver()
    rospy.spin()