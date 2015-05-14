#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from ros_umirtx_driver.msg import *
from ros_umirtx_driver.srv import *
import sys, os
import time

def fillInMsg(respmsg,msg):
	msgarray = list(respmsg)
	msg.status   = msgarray[0]
	msg.zed      = msgarray[1]
	msg.shoulder = msgarray[2]
	msg.elbow    = msgarray[3]
	msg.yaw      = msgarray[4]
	msg.wrist1   = msgarray[5]
	msg.wrist2   = msgarray[6]
	msg.gripper  = msgarray[7]
	
def fillOutMsg(reqmsg,msglst):
	while len(msglst) > 0: msglst.pop() #clear list
	msglst.append(reqmsg.status)
	msglst.append(reqmsg.zed)
	msglst.append(reqmsg.shoulder)
	msglst.append(reqmsg.elbow)
	msglst.append(reqmsg.yaw)
	msglst.append(reqmsg.wrist1)
	msglst.append(reqmsg.wrist2)
	msglst.append(reqmsg.gripper)

class dummyprog:
	
	def __init__(self):
		self.setup()
		self.mainFunc()
		
	def setup(self):
		# define node name and refresh rate
		rospy.init_node('dummyprog', anonymous=True)
		#self.rate = rospy.Rate(1) # 1hz
		
		# init publication handler for update
		rospy.wait_for_service('request_arm')
		self.reqhand = rospy.ServiceProxy('request_arm',ArmRequest) #handler
		
	def mainFunc(self):
		print "Dummy program started"
		self.init()
		input("Press Enter to continue...")
		motcoord = (-500,-300,300,200,200,-200,600)
		self.moveMotTo(motcoord)
		
	def pubArray(self,msgtup):
		msg = ArmMsg()
		fillInMsg(msgtup,msg)
		
		resp = self.reqhand(msg)
		
		print "response: ", resp.armresp.status
		return resp
		
		
	def init(self):
		print "Connecting with arm"
		self.initSer()
		time.sleep(1)
		print "Initialising arm"
		self.initArm()
		
	def initSer(self):
		senddata = [5, 0,0,0, 0,0,0,0] #5 = init serial connection
		self.pubArray(senddata)
		
	def initArm(self):
		senddata = [6, 0,0,0, 0,0,0,0] #6 = init arm motors
		self.pubArray(senddata)
		
	def moveMotTo(self,motcoord):
		sendarray = (20+motcoord)
		self.pubArray(senddata)
		
	def testConn(self):
		self.pubArray((25,0,0,0, 0,0,0,0))
		
	def getUserInput(self):
		loopTest = 0
		while (loopTest==0):
			uistr = input("Give command: ")
			if(len(uistr)!=0):
				pos = uistr.find(' ')
				if(pos==-1):
					comm = uistr
					var  = ""
				else:
					comm = uistr[0:pos-1]
					var  = uistr[pos+1:]
				loopTest = self.execUsInput(comm,var)
				
	def execUsInput(self,comm,var):
		
		if   (comm=="test"):
			print "Testing connection"
			self.testConn()
			
		elif (comm=="mov1"):
			print "Moving to position 1"
			motcoord = (-500,-300,300,200,200,-200,600)
			self.moveMotTo(motcoord)
			
		elif (comm=="mov2"):
			print "Moving to position 2"
			motcoord = (-500,-300,300,200,200,-200,600)
			self.moveMotTo(motcoord)
			
		elif (comm=="mov"):
			print "Moving to position"
			motcoord = (-500,-300,300,200,200,-200,600)
			self.moveMotTo(motcoord)
			
		else:
			print "No command found for input"
		


if __name__ == '__main__':
    try:
        dummy = dummyprog()
        
    except rospy.ROSInterruptException:
        pass



