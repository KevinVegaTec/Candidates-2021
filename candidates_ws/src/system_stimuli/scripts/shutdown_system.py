#!/usr/bin/env python3
# license removed for brevity
import rospy
import time
from std_msgs.msg import UInt16
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('system_health',UInt16, queue_size = 5)
    rospy.init_node('mock_shutdown_system',anonymous=True)
    rate = rospy.Rate(1)
    option = 0
    while not rospy.is_shutdown() and option == 0:
        rospy.loginfo(0)
        pub.publish(0)
        rate.sleep()
        #option = int(input())


if __name__ == '__main__':
    try:
        talker()
        rospy.init_node('mock_shutdown_system', anonymous=True)
        pub = rospy.Publisher('system_health', UInt16, queue_size=10)
        pub.publish(1)
        rospy.loginfo("System error published.")
    except rospy.ROSInterruptException:
        pass