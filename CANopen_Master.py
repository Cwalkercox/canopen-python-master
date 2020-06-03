import canopen
import os
import can
import time
import signal
import logging
from threading import Thread, Lock
import time
import otherfuncs
import opcuainit
from opcua import Server
from random import randint
import datetime
import netifaces as ni2
import numpy as np

# logging.basicConfig(level=logging.DEBUG)
# logger=logging.getLogger(__name__)
canLock=Lock()
opcLock=Lock()

url = "opc.tcp://169.254.247.12:4840" #this URL changes from CM to CM. Grab it from ifconfig->eth0
server = Server()
server.set_endpoint(url)
name = "OPCUA_Simulation_Server"
addspace= server.register_namespace(name)
opcnode=server.get_objects_node()

################################Create OPCUA  Data Model Structure
global opcdevNames
global opcdevTypes
global opcProcessVariables
global opcHARTPrimaryValues
[opcdevNames, opcdevTypes, opcProcessVariables, opcHARTPrimaryValues]=opcuainit.configOPCUAdatamodel(server, addspace, opcnode)
######################################

server.start()
print("Server started at {}".format(url))

global NumDemoIO #number of I/O modules to account for for the demo.
NumDemoIO=8 
global ProcessValue #This is the sensor reading values that is retrieved from slave.
ProcessValue=[0 for i in range(NumDemoIO)]
global actuatorValue #This is the actuator value that is sent to the slave
actuatorValue=[0 for i in range(NumDemoIO)]
global HARTPrimaryValue
HARTPrimaryValue=[0 for i in range(NumDemoIO)]
global current_nodes
current_nodes=[]


class Thread1set:  
    def __init__(self):
        self._running = True

    def terminate(self):  
        self._running = False  

    def run(self):
        while self._running:
            try:
                canLock.acquire()
                print('thread 1 is using the can bus')
                otherfuncs.initCAN() #init CAN bus
                network=otherfuncs.initCANopen() #create canopen network
                #otherfuncs.addmasternode(network) #adds local master node
                #search network for all connected nodes
                global previous_nodes
                global current_nodes
                previous_nodes=current_nodes
                current_nodes=otherfuncs.findactivenodes(network, NumDemoIO) #scans all active nodes

                print(current_nodes)
                otherfuncs.disconnectCANopen(network)
                otherfuncs.deinitCAN() #don't set CANinuse here because we're about to use the can bus again
                print('Scanning Function Complete')
                compare=(sum(previous_nodes)==sum(current_nodes))
                if (len(current_nodes)>0 and compare==False):#if there are new nodes present
                    can0=otherfuncs.initCAN() #no harm is setting CANinuse again here
                    network=otherfuncs.initCANopen()
                    global deviceType
                    deviceType=["N/A" for i in range(NumDemoIO)]
                    global deviceName
                    deviceName=["N/A" for i in range(NumDemoIO)]
                    
                    for x in current_nodes: #loop through nodes and get device information
                        node = network.add_node(x, '/home/pi/canopen-rpi/examples/NXP_CiA401.eds')
                        #node.sdo.RESPONSE_TIMEOUT=0.3
                        deviceType[x-1]=node.sdo[0x1000].raw #0x1000 is device Type
                        deviceName[x-1]=node.sdo[0x1009].raw #0x1009 is device Name
                        ###############End of for loop that receives slave device info
                    print(deviceType)
                    print(deviceName)                    
                    otherfuncs.disconnectCANopen(network)
                    otherfuncs.deinitCAN()
                     #print('thread 1 is done using the can bus')
                    #########################OPCUA code goes here
                    opcLock.acquire()
                    for y in current_nodes:
                        opcdevNames[y-1].set_value(deviceName[y-1]) #set the value to the opcua client
                        opcdevTypes[y-1].set_value(deviceType[y-1]) #set the value to the opcua client
                        print('OPC objects created')
                
                    opcLock.release()
                ################################ END of OPCUA code    
                canLock.release()
                    
                    #print('thread1 released the lock')
            except:
                print('thread1 exited due to error')
        
            time.sleep(7) #Execute this thread every x seconds
##############################


############Initialize Thread2
class Thread2set:  
    def __init__(self):
        self._running = True
    def terminate(self):  
        self._running = False  
    def run(self):
        while self._running:
            canLock.acquire()
            opcLock.acquire()
            print('Thread2 has the locks')
#             try:
        #print('thread2 entered')
            if (len(current_nodes)>0):
                otherfuncs.initCAN() #init CAN bus
                network=otherfuncs.initCANopen() #create canopen network
                global ProcessValue
                global actuatorValue
                global HARTPrimaryValue
                Iiter=0 #to iterate through AI or DI nodes
                Oiter=0 #to iterate through AO or DO nodes
                for x in current_nodes:
                    if (deviceType[x-1]=="AI" or deviceType[x-1]=="DI"):
                        node = network.add_node(x, '/home/pi/canopen-rpi/examples/NXP_CiA401.eds')
                        #node.sdo.RESPONSE_TIMEOUT=0.3
                        ProcessValue[x-1]=node.sdo[0x6401][1].phys
                        #sensorReading=node.sdo['Read Sensor Data']['AnalogInput'].phys
                        HARTPrimaryValue[x-1]=node.sdo[0x6401][2].phys
                        
                        opcProcessVariables[x-1].set_value(ProcessValue[x-1]) #set the value to the opcua client
                        opcHARTPrimaryValues[x-1].set_value(HARTPrimaryValue[x-1]) #set the value to the opcua client
                        #Insert HART data output here
                        print('AI/DI process data written')
                        Iiter=Iiter+1
                    elif (deviceType[x-1]=="AO" or deviceType[x-1]=="DO"):
                        node = network.add_node(x, '/home/pi/canopen-rpi/examples/NXP_CiA401.eds')
                        #node.sdo.RESPONSE_TIMEOUT=0.3
                        node.sdo[0x6401][1].write(actuatorValue[x-1],'raw')
                        #Insert HART data output here
                        opcProcessVariables[x-1].set_value(actuatorValue[x-1]) #set the value to the opcua client
                        print('AO/DO process data written')
                        Oiter=Oiter+1
                        
                otherfuncs.disconnectCANopen(network)
                otherfuncs.deinitCAN()
                        
                        #print('thread2 is done using the can bus')
#             except:
#                 print('thread 2 exited due to error')
            
            canLock.release()
            opcLock.release()
            print('Thread2 released the locks')
            time.sleep(0.01)
##############################

############Initialize Thread3
class Thread3set:  
    def __init__(self):
        self._running = True
    def terminate(self):  
        self._running = False  
    def run(self):
        while self._running:
#            try:
            if (len(current_nodes)>0):
                itercount=[0 for i in range(NumDemoIO)]
                for x in itercount:
                    actuatorValue[x]=2.5 * ProcessValue[x]
                        
                
                print('actuator values written')
#            except:
#                print('thread 3 exited due to error')
    
            time.sleep(0.5)
            #Remaining NXT code Thread Code goes here


threader1 = Thread1set()
threader2 = Thread2set()
threader3 = Thread3set()
#Create Thread
Thread1 = Thread(target=threader1.run)
Thread2 = Thread(target=threader2.run)
Thread3 = Thread(target=threader3.run)
#Start Thread 
Thread1.start()
Thread2.start()
Thread3.start()
