import canopen
import os
import can
import time
import signal
import socketcan
import logging
from threading import Thread
import time


def initCAN():
    CANon=1
    ###########Initialize CAN communication and set up CANopen Network
    #os.system('sudo ip link set can0 up type can bitrate 1000000   dbitrate 8000000 restart-ms 1000 berr-reporting on fd on')
    os.system('sudo ip link set can0 up type can bitrate 1000000')
    #os.system('sudo ifconfig can0 txqueuelen 65536')
    os.system('sudo ifconfig can0 txqueuelen 100000')
    can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')# socketcan_native
    #print('Initialized can0')
    return can0, CANon

def deinitCAN():
    CANon=0
    os.system('sudo ifconfig can0 down')
    #print('Closed can0')
    return CANon
    
def initCANopen():
    network = canopen.Network()
    network.connect(channel='can0', bustype='socketcan')
    return network

def findactivenodes(network):
    network.scanner.search()
    time.sleep(0.05)
    for node_id in network.scanner.nodes:
        print("Found node %d!" % node_id)
        #print(network.scanner.nodes)
    return network.scanner.nodes

def disconnectCANopen(network):
    network.disconnect()
    #os.system('sudo ifconfig can0 down')
    #print('Closed can0')
    print('Network disconnected')
    
def addmasternode(network):
#     node = network.add_node(7, '/home/pi/canopen-rpi/examples/NXP_CiA401.eds')
    local_node = canopen.LocalNode(1, '/home/pi/canopen-rpi/examples/NXP_CiA401.eds')
    network.add_node(local_node)
    
#     node.nmt.__init__(7)
#     local_node.nmt.__init__(7,1)
    
#     node.nmt.state = 'OPERATIONAL'