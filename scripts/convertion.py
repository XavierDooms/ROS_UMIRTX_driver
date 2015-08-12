#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from ros_umirtx_driver.msg import *
from ros_umirtx_driver.srv import *
import sys, os
import time


class RobParam:
	
	def __init__(self, name):
		self.zed      = -120
		self.shoulder = 0
		self.elbow    = 0
		self.wrist1   = 0
		self.wrist2   = 0
		self.yaw      = 0
		self.gripper  = 100
		
	def setRob(self,shoulder,elbow,zed,wrist1,wrist2,yaw,gripper):
                self.shoulder = shoulder
                self.elbow    = elbow
                self.zed      = zed
                self.wrist1   = wrist1
                self.wrist2   = wrist2
                self.yaw      = yaw
                self.gripper  = gripper

	def setReal(self,x,y,z,yaw,pitch,roll):	
                param = self.xyzypr2rob(x,y,z,yaw,pitch,roll)
                self.shoulder = param(1)
                self.elbow    = param(2)
                self.zed      = param(3)
                self.wrist1   = param(4)
                self.wrist2   = param(5)
                self.yaw      = param(6)
                
	def getRob(self):
                return [self.shoulder,self.elbow,self.zed,self.wrist1,self.wrist2,self.yaw,self.gripper]
                
	#def getReal(self,):

        def sendRob(self):

                
def xyzypr2rob(xtip,ytip,ztip,yawd,pitchd,rolld):
        lgrip  = 177
        yaw    = math.radians(yawd)
        pitch  = math.radians(pitchd)
        roll   = math.radians(rolld)

        xgrip  = lgrip*math.cos(pitchr)*math.cos(yawr)
        ygrip  = lgrip*math.cos(pitchr)*math.sin(yawr)
        zgrip  = lgrip*math.sin(pitchr)
        
        xwrist = xtip - xgrip
        ywrist = ytip - ygrip
        zwrist = ztip - zgrip

        radius = math.hypot(xwrist,ywrist)
        thetax = math.atan(ywrist,xwrist)
        thetay = math.acos(radius/(2*253.5))
        
        theta2 = thetax + thetay
        theta3 = 2*thetay
        theta4 = yaw-thetax

        #x2     = 253.5*math.cos(theta2)
        #y2     = 253.5*math.sin(theta2)

        robsho = -14.6113*theta2*(180/math.pi)
        robelb =  29.2227*theta3*(180/math.pi)
        robyaw =  9.73994*theta4*(180/math.pi)
        robwr1 =  13.4862*(pitchd+rolld)
        robwr2 =  13.4862*(pitchd-rolld)
        robzed =  3.74953*(915-zwrist)
        
        return  [robsho,robelb,robzed,robwr1,robwr2,robyaw]
