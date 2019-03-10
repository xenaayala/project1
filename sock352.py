import binascii
import socket as syssock
import struct
import sys

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

#flags
SOCK352_SYN = 0x01      
SOCK352_FIN = 0x02          
SOCK352_ACK = 0x04
SOCK352_RESET = 0x08     
SOECK352_HAS_OPT = 0xA0  
#portTx = 0
#portRx = 0

sock352PktHdrData = '!BBBBHHLLQQLL'
max_packsize = bin(64000)        # in bytes
segments = 0

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
	global portTx
	global portRx
	#send port
	portTx=int(UDPportTx)
	#recieving port
	portRx = int(UDPportRx)
	
      
class socket:
    
    def __init__(self):  # fill in your code here
	#create socket
	self.syssock = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)	 
        return
    
    def bind(self,address):
	#bind the socket
	try: 
		self.syssock.bind(address)
	except IOError:
		print ("Binding failed.")
	print("Socket is bound")
	return 

    def connect(self,address):  # fill in your code here 
        return 
    
    def listen(self,backlog):
        return

    def accept(self):
        (clientsocket, address) = (1,1)  # change this to your code 
        return (clientsocket,address)
    
    def close(self):   # fill in your code here 
        return 

    def send(self,buffer):
        bytessent = 0     # fill in your code here 
        return bytesent 

    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here
        return bytesreceived 
