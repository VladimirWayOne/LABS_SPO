#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from turtlesim.msg import Color
from turtlesim.srv import SetPen
from turtlesim.srv import TeleportAbsolute

x = 0
y = 0
z = 0
yaw = 0

def teleport(x,y,angle):
	rospy.wait_for_service('turtle1/teleport_absolute')
	turtle1_teleport = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
	pen_color(255, 255, 255)
	turtle1_teleport(x, y, angle)
	pen_color(204, 153, 255)

def next_num():
    pen_color(255, 255, 255)
    rotate(78.69006753, False)
    move(1, 1.022, 1)
    rotate(78.69006753, True)
    pen_color(204, 153, 255)

def pen_color(r, g, b):
    rospy.wait_for_service('turtle1/set_pen')
    turtle1_set_pen = rospy.ServiceProxy('turtle1/set_pen', SetPen)
    turtle1_set_pen(r, g, b, 2, 0)


def rotate(angle, clockwise):
    global yaw
    yaw0 = yaw
    PI = 3.1415926535897
    vel_msg = Twist()
    ang_speed = 60 * 2 * PI / 360
    rel_ang = angle * 2 * PI / 360
    if (clockwise):
        vel_msg.angular.z = -abs(ang_speed)
    else:
        vel_msg.angular.z = abs(ang_speed)

    angle_moved = 0
    loop_rate = rospy.Rate(120)
    cmd_vel_topic = 'turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
    while True:
        velocity_publisher.publish(vel_msg)
        loop_rate.sleep()
        angle_moved = abs(yaw - yaw0)
        if not (angle_moved < rel_ang):
            break
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)


def callPoseback(pose_message):
    global x
    global y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta


def move(speed, distance, is_forward):
    velocity_message = Twist()
    global x, y
    x0 = x
    y0 = y

    if (is_forward):
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)

    distance_moved = 0.0
    loop_rate = rospy.Rate(10)
    cmd_vel_topic = 'turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    while True:
        # rospy.loginfo('Turtle moves forward')
        velocity_publisher.publish(velocity_message)

        loop_rate.sleep()

        distance_moved = abs(0.4 * math.sqrt(((x - x0) ** 2) + ((y - y0) ** 2)))
        # print distance_moved
        if not (distance_moved < distance):
            #  rospy.loginfo('reached')
            break
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)


def square(side):
    move(1, side, True)
    rotate(90, True)
    move(1, side, True)
    rotate(90, True)
    move(1, side, True)
    rotate(90, True)
    move(1, side, True)
    
def two():
    move(1, 0.5, 1)
    rotate(90, True)
    move(1, 0.5, 1)
    rotate(90, True)
    move(1, 0.5, 1)
    rotate(90, False)
    move(1, 0.5, 1)
    rotate(90, False)
    move(1, 0.5, 1)

def four():
	rotate(90, True)
	move(1, 0.5, 1)
	rotate(90, False)
	move(1, 0.5, 1)
	rotate(90, False)
	move(1, 0.5, 1)
	move(2, 1, False)
	rotate(90, True)

def seven():
	move(1, 0.5, 1)
	rotate(116.56505, True)
	move(1,1.118034,1)
	rotate(153.434395, True)
	pen_color(255,255,255)
	move(1, 0.5, 1)
	rotate(90, True)
	pen_color(204, 153, 255)
	move(1, 0.5, 1)
	rotate(90, True)
	pen_color(255,255,255)
	move(1, 0.5, 1)
	rotate(90, False)

def three():
	move(1, 0.5, 1)
	rotate(90, True)
	move(1, 0.5, 1)
	rotate(90, True)
	move(1, 0.5, 1)
	move(1, 0.5, False)
	rotate(90, False)
	move(1, 0.5, 1)
	rotate(90, True)
	move(1, 0.5, 1)
	move(1, 0.5, False) 
	rotate(180, False)

def zero():
	move(1, 0.5, 1)
	rotate(90, True)
	move(2, 1, 1)
	rotate(90, True)
	move(1, 0.5, 1)
	rotate(90, True)
	move(2, 1, 1)
	rotate(90, True)
	rotate(63.4349488, True)
	pen_color(255,255,255)
	move(1, 1.118033989,1)
	rotate(63.4349488, False)
	
	
    
    

if __name__ == '__main__':
    try:

        rospy.init_node('Turtlesim_number', anonymous=True)
        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        position_topic = 'turtle1/pose'
        pose_subscriber = rospy.Subscriber(position_topic, Pose, callPoseback)
        time.sleep(1)  

	teleport(0.2, 5, 0)
        pen_color(204, 153, 255)

        two()
	next_num()
	four()
	next_num()
	four()
	next_num()
	seven()
	next_num()
	three()
	next_num()
	zero()
	next_num()

    except rospy.ROSInterruptException:
        rospy.loginfo('node terminated')
