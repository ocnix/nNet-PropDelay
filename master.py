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
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from struct import *


#this function will create the socket, or throw an error if there was an issue creating it
def create_tcp_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        #print ' successfully made socket'
    except socket.error , msg:
        #print 'Error while creating socket, code: '+str(msg[0])+' Message ' + msg[1]
	sys.exit()
    return s

def create_upd_packet():
    try:
    	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#print 'successfully created socket'
    except socket.error, msg:
        print ' error while creating socket : '+msg[1]
	sys.exit()
    return s


#send packet to node
def send_packet(s, port):
        		    
    #create_socket()
    try:   			
	 s.sendto(str(time.clock()),('10.0.0.1', port))#change IP address to the node that is recieving the packet
         #print 'successfully sent packet'
    except socket.error , msg:
         print 'Error sending, please check IP address, internet connection etc....Error: '+msg[1]
       	 sys.exit()

#recieve packet from other node
def recieve_packet(socket, port):
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
  

#===============REGRESSION LEARNING FUNCTION-- touch at your own risk=====================
# ----------- Some notes to make sense of all this: -------
# vars & arrays = what they mean/store
# ALPHA 		= learning rate: this MUST be a SMALL constant!! (0 < ALPHA < 0.05)
# nWeights  	= you need one weight per input variable (one 'Wn' for each 'Xn') PLUS one more for bias/constant (aka Xo)
# m 			= sampling size (how many samples do we want to regress over?)
# maxIters 		= number of times to iterate learning on a particular sample (1500 is usually enough)
# weights 		= vector of weights (first weight is for bias)
# data 			= the data (actual output/Ck is first column, second column is for bias, rest inputs)
# errorVector 	= vector of errors (actual - predicted) for data sample
# hyp			= hypothesis/predicted value by regression 
# -----------------------------------------------------------


def INPUT_REGRESSION():
    ALPHA = float(raw_input('Enter learning rate (alpha): ')) 
    nWeights = 1 + int(raw_input('Enter number of independent variables: ')) 
	# add 1 because you need a weight for the bias (constant)
	# maybe have 2: 1 for error, 1 for previous Ck
    m = int(raw_input('Enter sampling size: '))
    maxIters = int(raw_input('Enter number iterations for gradient descent: '))

    return (ALPHA, nWeights, m, maxIters)

def Regr_magic(tArrive_node1, tArrive_node2, tSent_node1, tSent_node2,ALPHA, nWeights, m, maxIters):
    

    weights = numpy.zeros(shape=(1, nWeights)) #creates a vector of weights
    for i in range(0,nWeights): #making the first weights non zero, have a default prediction for the first packet
	weights[0][i] = random.random()	#

    data = numpy.zeros(shape=(1, nWeights + 1)) # remember: nWeights includes theta0, vector of weights
    data[0,1] = 1 #will get elongated till the sampling size
	# column 0 is actual outputs
	# column 1 is for bias (value is always 1)
    errorVector = numpy.zeros(shape=(1, 1)) #first row second column 

    # ----------- need to code: Wait until you receive 4 data points for PDin and PDout calculation do the following
    # waiting for live data and takes it in
    
    tArrive_node2 = float(tArrive_node2)
    tSent_node1 = float(tSent_node1)
    tArrive_node1 = float(tArrive_node1)
    tSent_node2 = float(tSent_node2)
    stamp_1 = tSent_node1 - tArrive_node1
    stamp_2 = tSent_node2 - tArrive_node2
    Ck = (tArrive_node2 - tSent_node1 - tArrive_node1 + tSent_node2)/2
    dim1, dim2 = data.shape
    data[dim1-1][0] = Ck
    dataShuffled = data # DO NTO DELETE THIS LINE
    #for every iteration we dont want the same order, it is the learning agent

    # --------- SAMPLE DATA TO TEST LINEAR REGRESSION LEARNING --------
    """
    dataShuffled = numpy.ones((10,3))
    for i in range(0,dataShuffled.shape[0]):
        
 	dataShuffled[i][2] = i+1
   	dataShuffled[i][0] = 5 * dataShuffled[i][2]
    dataShuffled[0,:] = [0,1,0]
    errorVector = numpy.zeros(shape=(10,1))
   """

    # ----------------- LEARN PARAMETERS FOR LINEAR REGRESSION ------------
    for k in range(0, maxIters):
	for i in range (0, dataShuffled.shape[0]):
	        hyp = numpy.dot(weights, dataShuffled[i][1:])
	        errorVector[i,0] = hyp - dataShuffled[i,0]
                """
	        if errorVector[i] not 0:
	            print '1'
		else:
		    print '2'
                """
		#if errorVector(i) is not zero, right to cvs 1, else write 0
		#write errorvector to csv

    for i in range(0, weights.shape[1]):
	sum = numpy.dot(errorVector[:,0], dataShuffled[:,i+1])
	weights[0][i] = weights[0][i] - ALPHA / dataShuffled.shape[0] * sum
    numpy.random.shuffle(dataShuffled)
    print weights
	
    # ----------------- STORE DATA AND PREPARE FOR MORE INCOMING DATA ---------------------
    dim1, dim2 = data.shape
    if dim1 < m+1:
        data = numpy.vstack((data, numpy.zeros((1,dim2))))
	data[dim1][1] = 1	# need 1 here for bias/constant
	errorVector = numpy.vstack((errorVector, numpy.zeros((1, 1))))
    elif dim1 >= m+1:
	data = numpy.delete(data,0, axis = 0)
	data = numpy.vstack((data, numpy.zeros((1,dim2))))
	data[dim1][1] = 1	# need 1 here for bias/constant

    data[dim1][2] = Ck	# we're using Ck as x1 (the input variable)
    # you can add more variables to data here

    # ------------------ PLOT LINEAR EQUATION -----------------------------
    #ck_new = left+right*(ck)
    #first column actual ck columns, new ck_values, middle is 1, third old_ck
    #shape function returns number of columns, keep adding points to the column, get dimesions of array, find the last row, take the value of the last 	
    return(weights, stamp_1, stamp_2)
def Graphing():
   
    def data_gen(t=0)
    cnt = 0
    while cnt < 1000 #data file
    cnt += 1
    t +=0.1
    yield t, numpy.sin(2*numpy.pi*t) * numpy.exp(-t/10.)

    def init():
	ax.set_ylim(-1.1, 1.1)
	ax.set_xlim(0,10)
	del xdata[:]
	del ydata[:]
	line.set_data(xdata, ydata)
	return line
 
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.grid()
    xdata, ydata = [], []

    def run(data):
        t,y = data
        xdata.append(t)
        ydata.append(y)
        xmin, xmax = ax.get_xlim()
        if t >= xmax:
	    ax.set_xlim(xmin, 2*xmax)
        line.set_data(xdata, ydata)
	
	return line
    ani = animation.FuncAnimation(fig,run,data_gen,blit=False,interval=10,repeat=False, init_func=init)
plt.show()
def write(d1,d2,d3):
    with open('text.txt','a') as ww:
	ww.write('%     %.6f    %.6f\n'%(d1,d2,d3))
	ww.flush()
	ww.close()

def main():
    Graphing()
    port1 = 5001 #sending port
    port2 = 5002 #recieving port
    port3 = 5003 #extra port for sending, may not need
    #global s	
    #create = create_socket()
    #create = create_upd_packet()
   

    a,n,m,i = INPUT_REGRESSION()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)





    s.bind(("", 5002))
    (data, addr) = s.recvfrom(1024)
    while s.recvfrom(1024):
	create = create_upd_packet()
	send_packet(create, port2)
	#print data, time.clock()
    	d_1, d_2, d_3 = Regr_magic(data, float(data)+.005, time.clock(), time.clock()+.004, a,n,m,i)
	write(d_1, d_2, d_3)
    while True:
    	create = create_upd_packet()
    	send_packet(create, port2)
	recieve_packet(create, port3)
    recieve_packet(create, 5002)
    sort_packets(create, port2)
    a,n,m,i = INPUT_REGRESSION()
    recc_1, recc_2 = recieve_packet(create, port2)
	
    #TESTING    
    set_1 = time.clock()
    set_2 = time.clock()+.0005   
    while True:

        Regr_magic(recc_1, recc_2, set_1, set_2,a,n,m,i)
if __name__ == "__main__":
    main()	    
