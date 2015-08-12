#client example
import binascii
import socket
import struct
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	client_socket.connect(("127.0.0.1", 55632))
	
except socket.error:
        print >>sys.stderr, 'Could not open socket', sys.exc_info()[0]
	sys.exit()
	
except:
	print >>sys.stderr, 'Unexpected error:', sys.exc_info()[0]
	sys.exit()

out_values = (5,0,0,0,0,0,0,0)
value_lst = []

for x in out_values:
    value_lst.append(socket.htons(x))

packer = struct.Struct('h h h h h h h h')

out_packed_data = packer.pack(*value_lst)

loopit = 5
try:
    client_socket.sendall(out_packed_data)
    print >>sys.stderr, 'packed and send:', out_values
    
    data_in_packed = client_socket.recv(packer.size)
    data_in = packer.unpack(data_in_packed)
    
    print >>sys.stderr, 'received and unpacked:', data_in
        
finally:
    print >> sys.stderr, 'Closing socket'
    client_socket.close()
