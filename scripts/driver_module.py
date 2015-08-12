#!/usr/bin/env python

import rospy
import sys,os
from std_msgs.msg import String
from ros_umirtx_driver.msg import *
from ros_umirtx_driver.srv import *
import connect_module
from functools import partial
import time


def requestcallback(dmod,reqmsg):
	print "Robot request received"
	senddata = []
	fillOutMsg(reqmsg.armreq,senddata)
	
	recvdata = []
	dmod.conn_mod.transmsg(senddata,recvdata)
	
	print "respons: ",recvdata[0]
	respmsg = ArmRequestResponse()
	fillInMsg(recvdata,respmsg.armresp)
	
	return respmsg

def statuscallback(dmod,event):
	print "Posting status"
	senddata = [25, 0,0,0, 0,0,0,0]
	#senddata = [17, 0,0,0, 0,0,0,0]
	reqmsg = ArmRequestRequest()
	fillInMsg(senddata,reqmsg.armreq)
	try:
		respmsg = dmod.reqhand(reqmsg)
		dmod.pub.publish(respmsg.armresp)
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
		time.sleep(10)
	
def fillInMsg(respmsg,msg): #order is wrong TODO: rearrange
	msgarray = list(respmsg)
	msg.status   = msgarray[0]
	msg.shoulder = msgarray[1]
	msg.elbow    = msgarray[2]
	msg.zed      = msgarray[3]
	msg.wrist1   = msgarray[4]
	msg.wrist2   = msgarray[5]
	msg.yaw      = msgarray[6]
	msg.gripper  = msgarray[7]
	
def fillOutMsg(reqmsg,msglst): #order is wrong TODO: rearrange
	while len(msglst) > 0: msglst.pop() #clear list
	msglst.append(reqmsg.status)
	msglst.append(reqmsg.shoulder)
	msglst.append(reqmsg.elbow)
	msglst.append(reqmsg.zed)
	msglst.append(reqmsg.wrist1)
	msglst.append(reqmsg.wrist2)
	msglst.append(reqmsg.yaw)
	msglst.append(reqmsg.gripper)
	
	

class driver_mod:
	
	def __init__(self):
		if(self.setup()!=0):
			return 555
		self.mainFunc()
		
	def setup(self):
		# Define node name and refresh rate
		rospy.init_node('robotdriver', anonymous=True)
		#self.rate = rospy.Rate(1) # 1hz
		
		# Setup connection
		self.conn_mod = connect_module.connect_module(55632)
		if(self.conn_mod.connect()!=0):
			time.sleep(3)
			if(self.conn_mod.connect()!=0):
				time.sleep(5)
				if(self.conn_mod.connect()!=0):
					sys.exit()
		
		# Init publication handler for update
		self.pub = rospy.Publisher('StatusArm', ArmMsg, queue_size=10)
		
		# Create request channel
		self.reqsrv = rospy.Service('request_arm',ArmRequest,partial(requestcallback,self))
		
		# Subscribe to request channel (with handler)
		rospy.wait_for_service('request_arm')
		self.reqhand = rospy.ServiceProxy('request_arm',ArmRequest) #handler
		
		return 0
	
	def mainFunc(self):
		# Request and publish status of robot periodicly
		#rospy.Timer(rospy.Duration(1), partial(statuscallback,self))
		
		# Keeps from finishing program till shutdown signal is send
		rospy.spin()

	def executerequest(self,reqmsg,statmsg):
		print "Executing request"
		recvdata = []
		senddata = list(reqmsg)
		
		if (senddata == 20):
			self.conn_mod.transmsg(senddata,recvdata)
		else:
			self.conn_mod.transmsg(senddata,recvdata)


if __name__ == '__main__':
    try:
        driver_mod()
    except rospy.ROSInterruptException:
        pass
