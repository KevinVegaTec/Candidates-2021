#!/usr/bin/env python3

from __future__ import print_function

from integration.srv import FK_service, FK_serviceResponse
import rospy

def handle_FK(req):
    print("If the value is less than 10 is accepted, otherwise is not accepted", req.input)
    if req.input <= 10:
        print(req.input, "OK")
        i = 1
    else:
        print(req.input, "NOK")
        i = 0
    return FK_serviceResponse(i)

def FK_server():
    rospy.init_node("FK_server")
    s = rospy.Service("FK_service",FK_service,handle_FK)
    print ("FK server ready")
    rospy.spin()

if __name__ == "__main__":
    FK_server()