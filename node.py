#Osama Mahmoud
#--------------------------------------------------------------------------------------------
#You must run this under root(ie su or sudo)
#FYI, this will work perfectly on LINUX machines, certain it will work on UNIX like machines, 
#BSD(mac) should not have an issue running this, if so you will need some modification, 
#as for windows.....lulz
#--------------------------------------------------------------------------------------------
import socket 
import time
import sys
import numpy
import random
from collections import deque
from struct import *


#this function will create the socket, or throw an error if there was an issue creating it
def create_tcp_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        print ' successfully made socket'
    except socket.error , msg:
        print 'Error while creating socket, code: '+str(msg[0])+' Message ' + msg[1]
	sys.exit()
    return s

def create_upd_packet():
    try:
    	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'successfully created socket'
    except socket.error, msg:
        print ' error while creating socket : '+msg[1]
	sys.exit()
    return s


#send packet to node
def send_packet(s, port):
        		    
    #create_socket()
    #clock = str(time.clock())
    try:   			
	 s.sendto(str(time.clock),('10.0.0.2', port))#change IP address to the node that is recieving the packet
         print 'successfully sent packet'
    except socket.error , msg:
         print 'Error sending, please check IP address, internet connection etc....Error: '+msg[1]
       	 sys.exit()

#recieve packet from other node
def recieve_packet(socket, port):
    #create_socket()
    socket.bind(("", port))
    (data, addr) = socket.recvfrom(1024)
    while True:
        while socket.recvfrom(1024):
            recv = time.clock()
            print data, recv
            return (float(data), float(recv))
         

#this function will analyze and organize the packets via the headers by unpacking 
#this method is very heavy on networks, especially wifi, it may give a  buffer issue, make sure its a wired connection,
#if still doesn't work i set up a backup method 
def sort_packets(socket, port):
    ack_list=[] #this list will store contents of the packet header
    #socket.bind(("", port))
    packet = socket.recvfrom(1024) #recieve max 1024 bits, change if you need 
    
    header = packet[0:20] #get the header from the packet: tuple ---> string 
    ip__h = unpack('!BBHHHBBH4s4s',header)
    
    #------Can be used or not, but it is here------#
    version_h = ip__h[0]
    version_h = version_h >> 4
    ihl = version_h&0xF
   
    iph_len = ihl*4

    ttl = ip__h[5]
    proto = ip__h[6]
    s_addr = socket.inet_ntoa(ip__h[8])
    d_addr = socket.inet_ntoa(ip__h[9])
    #----------------------------------------------#
    #----TCP header info---------------------------#
    tcp__h = packet[ip_len:ip_len+20]  
    tcph = unpack('!HHLLBBHHH', tcp__h)
    
    #more info if needed
    source_p = tcph[0]
    dest_port = tcph[1]
    sque = tcph[2]
    ack = tcph[3]
    doff_r = tcph[4]
    tcph_len = doff_r >> 4
    
    ack_list.append(ack)
    
    h_s = iph_len+tcph_len*4
    data_s = len(packet)-h_s
   
    ack_list = [int(x) for x in ack_list]
    ack_list.sort()
    print data_s


def start_sending():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, msg:
        print msg[1]
        sys.exit()

    while True:
        s.sendto(str(time.clock()),('10.0.0.2',5002))


def main():
	
    port1 = 5001 #sending port
    port2 = 5002 #recieving port
    port3 = 5003 #extra port for sending, may not need
    #global s	
    #create = create_socket()
    #create = create_upd_packet()
    #send_packet(create, port1)
    while True:
        create = create_upd_packet()
        recieve_packet(create, port2)
        #start_sending()       
    
    
    
    
    
if __name__ == "__main__":
    main()	    
