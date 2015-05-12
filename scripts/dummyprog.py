#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import sys, os
import time

if __name__ == '__main__':
    try:
        dummy = dummyprog()
        
    except rospy.ROSInterruptException:
        pass



class dummyprog:
	
	def __init__(self):
		self.setup()
		self.mainFunc()
		
	def setup(self):
		# define node name and refresh rate
		rospy.init_node('dummyprog', anonymous=True)
		#self.rate = rospy.Rate(1) # 1hz
		
		# init publication handler for update
		self.pubact = rospy.Publisher('ActionArm', String, queue_size=10)
		
	
	def mainFunc(self):
		print "Dummy program started"
		
		self.init()
		
	def init(self):
		print "Connecting with arm"
		self.initser()
		time.sleep(1)
		print "Initialising arm"
		self.initarm()
		input("Press Enter to continue...")
		motcoord = (0,0,0,0,0,0,0)
		self.moveMotTo(motcoord)
		
	def initser(self):
		senddata = [5, 0,0,0, 0,0,0,0] #5 = init serial connection
		self.pubact.publish(senddata)
		
	def initarm(self):
		senddata = [6, 0,0,0, 0,0,0,0] #6 = init arm motors
		self.pubact.publish(senddata)
		
	def moveMotTo(self,motcoord)
		sendarray = (20+motcoord)
		self.pubact.publish(senddata)
