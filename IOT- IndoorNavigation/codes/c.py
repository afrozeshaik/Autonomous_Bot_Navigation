# client.py  
import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

#host = "192.168.0.102"                          

port = input()

# connection to hostname on the port.
s.connect(("10.42.0.112", port))  
print s.recv(1024)                             

instr='urrr'                                     
s.send(instr)
for i in instr:
	print s.recv(1024)

s.close()
