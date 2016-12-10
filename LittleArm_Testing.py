#This program has a complete set of commands for most behaviors
#an improvement to the software would be for the arduino to wait until completion of the execution of the command before sending a ready signal

#from Tkinter import *
#import tkMessageBox
import time
import serial
import serial.tools.list_ports

#+++++++++++++Global Variables+++++++++++++++++++++

ser = serial.Serial('COM3', 9600)
defaultPos = {'base': '108', 'shoulder':'154','elbow':'32','gripper':'5','speed':'4'}
currentPos = {}

#++++++++++++++++Functions+++++++++++++++++++++++
def getPos(part):
    global currentPos
    global defaultPos
    if currentPos.has_key(part):
        position = currentPos[part]
        print "Getting position for "+part+" from current"
    else:
        position = defaultPos[part]
        print "Getting position for "+part+" from default"
    return position


def sendCommand(base = False, shoulder = False, elbow = False, gripper = False, speed = False, wait = 0):
    # Function to send command to arduino
    args = locals().keys()
    global currentPos
    # If the param wasn't passed, grab the value from either default or current
    if not base:
        base = getPos('base')
    if not shoulder:
        shoulder = getPos('shoulder')
    if not elbow:
        elbow = getPos('elbow')
    if not gripper:
        gripper = getPos('gripper')
    if not speed:
        speed = getPos('speed')
    
    ser.flushInput()
    ser.flushOutput()
    currentPos = {'base': base, 'shoulder': shoulder, 'elbow': elbow, 'gripper': gripper, 'speed': speed}
    print currentPos
    command = currentPos['base']+','+currentPos['shoulder']+','+currentPos['elbow']+','+currentPos['gripper']+','+currentPos['speed']+'\n'
    ser.write(command)
    
    if wait != '0':
        time.sleep(int(wait))
        return

    #wait until a repsonse if found from the arduino
    OK = 'no'
    while (OK != 'd'):
        OK = ser.read(1)

def clap (claps = 3):
    for index in range(int(claps)):
        # Close gripper
        sendCommand(gripper='5', speed='4') 
        # Open gripper
        sendCommand(gripper='70')
        time.sleep(.25)
    # Leave gripper open after clapping
    sendCommand(gripper='5') 

def goHome():
    sendCommand (base = '108', shoulder = '154', elbow = '30', gripper = '5', speed = '4')
    
def salute():
    goHome()
    sendCommand(base = '175', shoulder = '40', elbow = '5', gripper = '50', speed = '11')
    sendCommand(base = '6', shoulder = '123', gripper = '69')
    goHome()
    sendCommand(shoulder = '123', elbow = '5', gripper = '5')

def shoulderDown():
    sendCommand(shoulder = '15', elbow = '0')

def fistBump():
    sendCommand (base = '180', shoulder = '55', elbow = '30', gripper = '70', speed = '5', wait = '2')
    sendCommand (elbow = '130', shoulder = '154', speed = '4', wait = '1')
    sendCommand (elbow = '55', wait = '0')
    sendCommand (gripper = '5')

    goHome()
    salute()
    shoulderDown()
    fistBump()
    clap()

