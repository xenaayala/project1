import binascii
import socket as syssock
import struct
import sys
import random

#set flags
version = 0x1
opt_ptr = 0x0
protocol = 0x0
checksum = 0x0
source_port = 0x0
dest_port = 0x0
window = 0x0
header_len = 40
sentData = ""
sock352PktHdrData = '!BBBBHHLLQQLL'

sendPort = -1
recPort = -1
firstSocket = (0,0)
otherHostAddress = ""
currSeqNum = 0


def init(UDPportTx,UDPportRx):
    global firstSocket, sendPort, recPort
    #create socket
    firstSocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    recPort = int(UDPportRx)
    if(UDPportTx == ''):
        sendPort = recPort
    else:
        sendPort = int(UDPportTx)
    #bind socket
    firstSocket.bind( ('', recPort) )
    
    firstSocket.settimeout(0.2)
 
    return 
    
class socket:
    
    def __init__(self): # fill in your code here
		print("Creating The Socket")
		return
    
    def bind(self,address):   # fill in your code here
		print("binding...")
		return

    def connect(self,address):
        global firstSocket, currSeqNum
        print("Creating a Connection")
        
        currSeqNum = int( random.randint(15, 100) )

        header = self.createHeader(0x01, currSeqNum, 0, 0)
        ackFlag = -1
        
        while(ackFlag != currSeqNum):
            print("Creating new connection...%d bytes sent!" % (firstSocket.sendto(header,
                (address[0], sendPort) ) ) )
            newHeader = self.recPacket()
            ackFlag = newHeader[9]
       
        firstSocket.connect( (address[0], sendPort) )

        currSeqNum += 1
        return

    def accept(self):
        global firstSocket, recPort, currSeqNum
        
        flag = -1
        header2 = ""
        # call  recPacket() until we get a new connection
        while(flag != 0x01):
            header2 = self.recPacket()
            flag = header2[1]
        currSeqNum = header2[8]
        header = self.createHeader(0x04,0,currSeqNum,13)
        firstSocket.sendto(header+"Accepting", otherHostAddress)
        
        currSeqNum += 1
        #Call init for new connection
        clientsocket = socket()
        return (clientsocket,otherHostAddress)
  
    def close(self):
        print("Closing the connection")
        terminal_no = random.randint(7,19)
        header = self.createHeader(0x02, terminal_no, 0, 0)
        ackFlag = -1
 
        while(ackFlag != terminal_no):
            try:
                firstSocket.sendto(header, otherHostAddress)
            except TypeError:
                firstSocket.send(header)
            newHeader = self.recPacket()
            ackFlag = newHeader[9]
 
        firstSocket.close()

        return

    def listen(self,buffer): # fill in your code here 
		print("Listening...")
		return

    def send(self,buffer):
        global firstSocket, header_len, currSeqNum
        #create a new header, a new UDP packet with the header and buffer
        bytesSent = 0
        msglen = len(buffer)
  
        print("Sending...")
        while(msglen > 0):
            # send 255 bytes of the message at a time
            parcel = buffer[:255]
            parcelHeader = self.createHeader(0x03,currSeqNum,0,len(parcel) )
            tempBytesSent = 0
            ackFlag = -1
            while(ackFlag != currSeqNum):
                tempBytesSent = firstSocket.send(parcelHeader+parcel) - header_len
                newHeader = self.recPacket()
                ackFlag = newHeader[9]
            msglen -= 255
            buffer = buffer[255:]
            bytesSent += tempBytesSent
            currSeqNum += 12
        return bytesSent

    def recv(self,bytes_to_receive):
        global firstSocket, sentData, currSeqNum
        
        print("Recieving...")
        sentData = ""
        finalMessage = ""
        while(bytes_to_receive > 0):
            seq_no = -1
            # Check for seq num we need
            while(seq_no != currSeqNum):
                newHeader = self.recPacket()
                seq_no = newHeader[8]
                print("Sequence number %d recieved" % seq_no)
                if(seq_no != currSeqNum):
                    print("Did not recieve sequence number: %d " % currSeqNum)
                # Acknowledge whatever it is we received
                header = self.createHeader(0x04, 0,seq_no,0)
                firstSocket.sendto(header, otherHostAddress)
            #Add message to the buffer
            finalMessage += sentData
            bytes_to_receive -= len(sentData)
            currSeqNum += 1
        print("Recieving complete...")
        return finalMessage
      
    #function to get packets 
    def  recPacket(self):
        global firstSocket, sock352PktHdrData, otherHostAddress, sentData
        
        try:
            (data, senderAddress) =firstSocket.recvfrom(4096)
        except syssock.timeout:
            z = [0,0,0,0,0,0,0,0,0,0,0,0]
            return z
        
        (data_header, data_msg) = (data[:40],data[40:])
        header = struct.unpack(sock352PktHdrData, data_header)
        flag = header[1]

        if(flag == 0x01):
            otherHostAddress = senderAddress
            return header

        elif(flag == 0x02):
            terminalHeader = self.createHeader(0x04,0,header[8],0)
            firstSocket.sendto(terminalHeader, senderAddress)
            return header

        elif(flag == 0x03):
            sentData = data_msg
            return header

        elif(flag == 0x04):
            return header

        elif(flag == 0x08):
            return header

        else:
            header = self.createHeader(0x08,header[8],header[9],0)
            if(firstSocket.sendto(header,senderAddress) > 0):
                print("Sent reset packet!")
            else:
                print("Failed to send reset packet")
            return header
            
    #Create Header structs 
    def  createHeader(self, origFlag, origSeqNo, origAckNo, origPayload):
        global sock352PktHdrData, header_len, version, opt_ptr, protocol
        global checksum, source_port, dest_port, window

        flags = origFlag
        sequence_no = origSeqNo
        ack_no = origAckNo
        payload_len = origPayload
        udpPkt_hdr_data = struct.Struct(sock352PktHdrData)
       
        return udpPkt_hdr_data.pack(version, flags, opt_ptr, protocol,
            header_len, checksum, source_port, dest_port, sequence_no,
            ack_no, window, payload_len)
