#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations

import math

pub_ = None

regions_ = {
    'right': 0,
    'fright': 0,
    'front': 0,
    'fleft': 0,
    'left': 0,
}

state_ = 0
state_dict_ = {
    0: 'follow the wall',
    1: 'turn left',
	2: 'turn right',
    3: 'find the wall',
}

def clbk_laser(msg):
	global regions_
	regions_ = {
		'right':  min(min(msg.ranges[0:100]), 5),
		'fright': min(min(msg.ranges[101:287]), 5),
		'front':  min(min(msg.ranges[288:431]), 5),
		'fleft':  min(min(msg.ranges[432:611]), 5),
		'left':   min(min(msg.ranges[612:713]), 5),
    }

	take_action()

def change_state(state):
    global state_, state_dict_
    if state is not state_:
        print 'Wall follower - [%s] - %s' % (state, state_dict_[state])
        state_ = state

def take_action():
	global regions_
	regions = regions_
	msg = Twist()
	linear_x = 0
	angular_z = 0

	state_description = ''


	if regions['front'] > 0.8 and regions['fleft']>0.4 and regions['fright']>0.4:
		state_description = 'case 1 - forward'
		change_state(0)
	elif regions['right'] > regions['left']:
		state_description = 'case 2 - right'
		change_state(2)
	else:
		state_description = 'case 3 - left'
		change_state(1)

	rospy.loginfo(regions)

def turn_left():
	msg = Twist()
	msg.linear.x = 0
	msg.angular.z = 0.8
	return msg
		
def turn_right():
	msg = Twist()
	msg.linear.x = 0
	msg.angular.z = -0.8
	return msg

def follow_the_wall():    
    msg = Twist()
    msg.angular.z = 0
    msg.linear.x = 1
    return msg

def main():
	global pub_
	rospy.init_node('Maze')

	pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	sub = rospy.Subscriber('/base_scan', LaserScan, clbk_laser)

	rate = rospy.Rate(50)
	while not rospy.is_shutdown():
		msg = Twist()
		if state_ == 2:
			msg = turn_right()
		elif state_ == 1:
			msg = turn_left()
		elif state_ == 0:
			msg = follow_the_wall()
			pass
		else:
			rospy.logerr('Unknown state!')
		
		pub_.publish(msg)
		rate.sleep()
	
main()

