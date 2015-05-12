#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import connect_module
from functools import partial


def requestcallback(dmod,rosdata):
	print "Robot request received"
	senddata = rosdata
	recvdata = []
	dmod.conn_mod.transmsg(rosdata,recvdata)
	# TODO implement

def statuscallback(dmod,event):
	print "Posting status"
	# TODO communicate with driver
	
	senddata = [25, 0,0,0, 0,0,0,0]
	#data = [17, 0,0,0, 0,0,0,0]
	recvdata = []
	dmod.conn_mod.transmsg(senddata,recvdata)
	dmod.pub.publish(recvdata)
	


class driver_mod:
	
	def __init__(self):
		self.zero = 0
		
		self.setup()
		self.mainFunc()
		
	def setup(self):
		# define node name and refresh rate
		rospy.init_node('robotdriver', anonymous=True)
		#self.rate = rospy.Rate(1) # 1hz
		
		# setup connection
		self.conn_mod = connect_module.connect_module(55632)
		self.conn_mod.connect()
		
		# init publication handler for update
		self.pub = rospy.Publisher('StatusArm', String, queue_size=10)
	
	def mainFunc(self):
		# subscribe to request channel
		rospy.Subscriber("ActionArm", String, partial(requestcallback,self))
		
		# publish status of robot periodicly
		rospy.Timer(rospy.Duration(1), partial(statuscallback,self))
		# start status loop
		#while not rospy.is_shutdown():
		#	statuscallback(pub)
		#	rate.sleep()
		
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
