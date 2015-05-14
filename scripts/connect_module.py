#!/usr/bin/env python

import rospy
import binascii
import socket
import struct
import sys

class connect_module:
	""" Connection module to communicate with UMIRTX robot server """
	
	def __init__(self,port = 55632):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.packer = struct.Struct('h h h h h h h h')
		self.connected = False
		self.port = port
		
	def connect(self,port=0):
		if port == 0:
			port = self.port 
		
		try:
			self.client_socket.connect(("127.0.0.1", port))
			self.connected = True
		
		except socket.error:
			print >>sys.stderr, 'Could not open socket', sys.exc_info()[0]
			return 1;
			
		except:
			print >>sys.stderr, 'Unexpected error:', sys.exc_info()[0]
			return 2;
		
		return 0
		
	def close(self):
		print 'Closing socket'
		self.client_socket.close()
		self.connected = False
		
		
		
	def transmsg(self,requestarray,statusarray):
		try:
			self.send(requestarray)
			self.recv(statusarray)
		except:
			print >>sys.stderr, "Error occured while communicating", sys.exc_info()[0]
			
		
	def send(self,msgarray):
		if self.connected != True:
			self.connect()
		
		value_lst = []
		for x in msgarray:
			value_lst.append(socket.htons(x))
		out_packed_data = self.packer.pack(*value_lst)

		try:
			print "Sending"
			self.client_socket.sendall(out_packed_data)
			print 'packed and send:', msgarray
		
		except:
			print >>sys.stderr, 'Unexpected error:', sys.exc_info()[0]
			return 2;
		
	
	def recv(self,msgarray):
		if self.connected != True:
			self.connect()
		
		try:
			print "Receiving"
			data_in_packed = self.client_socket.recv(self.packer.size)
		except:
			print >>sys.stderr, 'Unexpected error:', sys.exc_info()[0]
			self.close()
			return 1
		
		data_in = self.packer.unpack(data_in_packed)
		while len(msgarray) > 0: msgarray.pop()
		for x in data_in:
			msgarray.append(socket.ntohs(x))
		print 'received and unpacked:', msgarray
		return msgarray
		
		
		
	def initserconn(self,recvdata):
		print 'Initialising serial connection'
		senddata = [5, 0,0,0, 0,0,0,0]
		while len(recvdata) > 0: recvdata.pop() #clear list
		dmod.conn_mod.transmsg(senddata,recvdata)
		
	def resetserconn(self,recvdata):
		print 'Resetting serial connection'
		senddata = [9, 0,0,0, 0,0,0,0]
		while len(recvdata) > 0: recvdata.pop() #clear list
		dmod.conn_mod.transmsg(senddata,recvdata)
		
	def closeserconn(self,recvdata):
		print "Closing serial connection"
		senddata = [4, 0,0,0, 0,0,0,0]
		while len(recvdata) > 0: recvdata.pop() #clear list
		dmod.conn_mod.transmsg(senddata,recvdata)
		
	def defineorigin(self,recvdata):
		print "Setting current position as origin"
		senddata = [8, 0,0,0, 0,0,0,0]
		while len(recvdata) > 0: recvdata.pop() #clear list
		dmod.conn_mod.transmsg(senddata,recvdata)
		
		
		
		
		
if __name__ == '__main__':
    try:
        conn_mod = connect_module()
        conn_mod.connect()
        
        recvmsg = []
        conn_mod.send((25,0,0,0, 0,0,0,0))
        conn_mod.recv(recvmsg)
        
    except rospy.ROSInterruptException:
        pass

		
