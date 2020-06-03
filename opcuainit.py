import os
import time
import logging
from threading import Thread
import time
import numpy as np

def configOPCUAdatamodel(server, addspace, opcnode):
    ###Add 8 OPCUA Objects, 1 for each I/O Module
    Obj1 = opcnode.add_object(addspace, "I/O Module 1") #Adds a new OPCUA object for every I/O module
    Obj2 = opcnode.add_object(addspace, "I/O Module 2") #Adds a new OPCUA object for every I/O module
    Obj3 = opcnode.add_object(addspace, "I/O Module 3") #Adds a new OPCUA object for every I/O module
    Obj4 = opcnode.add_object(addspace, "I/O Module 4") #Adds a new OPCUA object for every I/O module
    Obj5 = opcnode.add_object(addspace, "I/O Module 5") #Adds a new OPCUA object for every I/O module
    Obj6 = opcnode.add_object(addspace, "I/O Module 6") #Adds a new OPCUA object for every I/O module
    Obj7 = opcnode.add_object(addspace, "I/O Module 7") #Adds a new OPCUA object for every I/O module
    Obj8 = opcnode.add_object(addspace, "I/O Module 8") #Adds a new OPCUA object for every I/O module

    ########Add OPCUA Variables for each Object
    opcdevNameVar1 = Obj1.add_variable(addspace,"Device Name","N/A") #this gives that object a new variable
    opcdevNameVar2 = Obj2.add_variable(addspace,"Device Name","N/A") #this gives that object a new variable
    opcdevNameVar3 = Obj3.add_variable(addspace,"Device Name","N/A") #this gives that object a new variable
    opcdevNameVar4 = Obj4.add_variable(addspace,"Device Name","N/A") #this gives that object a new variable
    opcdevNameVar5 = Obj5.add_variable(addspace,"Device Name","N/A") #this gives that object a new variable
    opcdevNameVar6 = Obj6.add_variable(addspace,"Device Name","N/A") #this gives that object a new variable
    opcdevNameVar7 = Obj7.add_variable(addspace,"Device Name","N/A") #this gives that object a new variable
    opcdevNameVar8 = Obj8.add_variable(addspace,"Device Name","N/A") #this gives that object a new variable
    opcdevNames=[opcdevNameVar1, opcdevNameVar2, opcdevNameVar3, opcdevNameVar4, opcdevNameVar5, opcdevNameVar6, opcdevNameVar7, opcdevNameVar8]

    opcdevTypeVar1 = Obj1.add_variable(addspace,"Device Type","N/A") #this gives that object another variable
    opcdevTypeVar2 = Obj2.add_variable(addspace,"Device Type","N/A") #this gives that object another variable
    opcdevTypeVar3 = Obj3.add_variable(addspace,"Device Type","N/A") #this gives that object another variable
    opcdevTypeVar4 = Obj4.add_variable(addspace,"Device Type","N/A") #this gives that object another variable
    opcdevTypeVar5 = Obj5.add_variable(addspace,"Device Type","N/A") #this gives that object another variable
    opcdevTypeVar6 = Obj6.add_variable(addspace,"Device Type","N/A") #this gives that object another variable
    opcdevTypeVar7 = Obj7.add_variable(addspace,"Device Type","N/A") #this gives that object another variable
    opcdevTypeVar8 = Obj8.add_variable(addspace,"Device Type","N/A") #this gives that object another variable
    opcdevTypes=[opcdevTypeVar1, opcdevTypeVar2, opcdevTypeVar3, opcdevTypeVar4, opcdevTypeVar5, opcdevTypeVar6, opcdevTypeVar7, opcdevTypeVar8]

    opcProcessVar1 = Obj1.add_variable(addspace,"Process Value", 0) #this gives that object another variable for process values
    opcProcessVar2 = Obj2.add_variable(addspace,"Process Value", 0) #this gives that object another variable for process values
    opcProcessVar3 = Obj3.add_variable(addspace,"Process Value", 0) #this gives that object another variable for process values
    opcProcessVar4 = Obj4.add_variable(addspace,"Process Value", 0) #this gives that object another variable for process values
    opcProcessVar5 = Obj5.add_variable(addspace,"Process Value", 0) #this gives that object another variable for process values
    opcProcessVar6 = Obj6.add_variable(addspace,"Process Value", 0) #this gives that object another variable for process values
    opcProcessVar7 = Obj7.add_variable(addspace,"Process Value", 0) #this gives that object another variable for process values
    opcProcessVar8 = Obj8.add_variable(addspace,"Process Value", 0) #this gives that object another variable for process values
    opcProcessVariables=[opcProcessVar1, opcProcessVar2, opcProcessVar3, opcProcessVar4, opcProcessVar5, opcProcessVar6, opcProcessVar7, opcProcessVar8]
    
    opcHARTPrimaryValue1 = Obj1.add_variable(addspace,"HART Primary Value", 0) #this gives that object another variable for HART PV values
    opcHARTPrimaryValue2 = Obj2.add_variable(addspace,"HART Primary Value", 0) #this gives that object another variable for HART PV values
    opcHARTPrimaryValue3 = Obj3.add_variable(addspace,"HART Primary Value", 0) #this gives that object another variable for HART PV values
    opcHARTPrimaryValue4 = Obj4.add_variable(addspace,"HART Primary Value", 0) #this gives that object another variable for HART PV values
    opcHARTPrimaryValue5 = Obj5.add_variable(addspace,"HART Primary Value", 0) #this gives that object another variable for HART PV values
    opcHARTPrimaryValue6 = Obj6.add_variable(addspace,"HART Primary Value", 0) #this gives that object another variable for HART PV values
    opcHARTPrimaryValue7 = Obj7.add_variable(addspace,"HART Primary Value", 0) #this gives that object another variable for HART PV values
    opcHARTPrimaryValue8 = Obj8.add_variable(addspace,"HART Primary Value", 0) #this gives that object another variable for HART PV values
    opcHARTPrimaryValues=[opcHARTPrimaryValue1, opcHARTPrimaryValue2, opcHARTPrimaryValue3, opcHARTPrimaryValue4, opcHARTPrimaryValue5, opcHARTPrimaryValue6, opcHARTPrimaryValue7, opcHARTPrimaryValue8]
    

    #set all variables to be writable
    varIndexarr = np.arange(len(opcdevNames))
    for i in varIndexarr:
        opcdevNames[i].set_writable()
        opcdevTypes[i].set_writable()
        opcProcessVariables[i].set_writable()
        opcHARTPrimaryValues[i].set_writable()
    
    return opcdevNames, opcdevTypes, opcProcessVariables, opcHARTPrimaryValues
    ##########################
