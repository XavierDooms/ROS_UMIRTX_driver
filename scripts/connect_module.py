#!/usr/bin/env python

import rospy
import binascii
import socket
import struct
import sys

def get_bit(byteval,idx):
    return ((byteval&(1<<idx))!=0);

class connect_module:
	""" Connection module to communicate with UMIRTX robot server """
	
	def __init__(self,port = 55632):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		self.packer = struct.Struct('H H H H H H H H')
		#self.packer = struct.Struct('h h h h h h h h')
		#self.unpacker = struct.Struct('h h h h h h h h')
		
		self.connected = False
		#self.ipadress = "127.0.0.1"
		self.ipadress = "192.168.56.1"
		self.port = port
		
	def connect(self,port=0):
		if port == 0:
			port = self.port 
		
		try:
			self.client_socket.connect((self.ipadress, port))
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
			val_out_masked = x & 0xffff
			val_out_conv = socket.htons(val_out_masked)
			#if x<0:
			#	val_out_conv2 = val_out_conv | ~0xffff #2??? TODO: check
			value_lst.append(val_out_conv)
			
		out_packed_data = self.packer.pack(*value_lst)
		print "Sending: ",out_packed_data

		try:
			print "Sending"
			self.client_socket.sendall(out_packed_data)
			print 'packed and send:', msgarray
		
		except:
			print >>sys.stderr, 'Unexpected error:', sys.exc_info()[0]
			return 2;
		
	
	def recv(self,msgarray):
		#if self.connected != True:
		#	self.connect()
		
		try:
			print "Receiving"
			data_in_packed = self.client_socket.recv(self.packer.size)
		except:
			print >>sys.stderr, 'Unexpected error:', sys.exc_info()[0]
			self.close()
			return 1
		print "Received"
		
		
		try:
			data_in = self.packer.unpack(data_in_packed)
			print "Unpacked: ",data_in
			data_in_conv = []
			for x in data_in:
				val_in_conv = socket.ntohs(x)
				if (val_in_conv > 32768):
					val_in_conv2 = val_in_conv | ~0xffff
				else:
					val_in_conv2 = val_in_conv
				#if (x != 0):
				#    print >>sys.stderr, x, ": ",format(x,"#018b")
				#    print >>sys.stderr, val_in_conv , ": ",format(val_in_conv ,"#018b")
				#    print >>sys.stderr, val_in_conv2 , ": ",format(val_in_conv2 ,"#018b")                
				data_in_conv.append(val_in_conv2)
		except:
			print >>sys.stderr, 'Unexpected error:', sys.exc_info()[0]
			self.close()
			return 1
			
		#print >>sys.stderr, 'received and unpacked:', data_in_conv
		return data_in_conv
		
		
		
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

		
