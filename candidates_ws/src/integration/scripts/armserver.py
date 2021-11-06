#! /usr/bin/env python3

#from candidates_ws.src.integration.scripts.FK_service import FK_service
from logging import fatal
import roslib
roslib.load_manifest('integration')
import rospy
import actionlib
import random
from integration.msg import armFeedback, armAction, armResult
from integration.srv import *


class armserver:

    _feedback = armFeedback()
    _result = armResult()

    def __init__(self):
        self.server = actionlib.SimpleActionServer('arm_movement', armAction, self.execute, False)
        self.server.start()

    def execute(self, goal):
        print("The goal is = ", goal.grasp.grasp_quality)
        r = rospy.Rate(1)
        success = True
        armResult = 3
        self._feedback.state = 0
        aux = 0

        while self._feedback.state < 3:
            # Needs goal validation?
            self.server.publish_feedback(self._feedback)
            self._feedback.state = aux
            if self._feedback.state == 0:
                print('Calculating FK')
                try:
                    fks = rospy.ServiceProxy('FK_service',FK_service)
                    print(fks())
                    if fks(goal.grasp.grasp_quality).res == 1:
                        print("FK Success")
                    else:
                        print("FK failed")
                        success = False
                        break

                except rospy.ServiceException as e:
                    print("FK Service call falied: %s" %e)
                r.sleep()
                
            elif self._feedback.state == 1 and success:
                print('Executing arm movement')
                r.sleep()
                self._result = 1
            elif self._feedback.state == 2 and success:
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
        else:
            rospy.loginfo('failed moving arm')
            self.server.set_aborted(result=self._result) 
        
        



if __name__ == '__main__':
    rospy.init_node('arm_server')
    server = armserver()
    rospy.spin()