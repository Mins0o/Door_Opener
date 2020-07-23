import serial
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
from Classifier import Classifier
from smbus import SMBus
import time
import csv


def chooseDevice():
    devices = [f for f in listdir("/dev/") if ((f[:4]=="ttyA" or f[:4] == "ttyU" or f[:4] =="ttyS"))]
    for i in range(len(devices)):
        print(i,end="\t")
        print(devices[i])
    print("Which device are we using?")
    selection=int(input())
    arduino = serial.Serial("/dev/"+devices[selection],9600)
    return arduino

def checkSound(data,clf,targetLabels):
    print (clf.predict([data])[0] in targetLabels) 
    return clf.predict([data])[0] in targetLabels 

def openDoor(data,bus,addr):
    bus.write_byte(addr,0x1)
    time.sleep(2)
    fig=plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(data[-1000:-1])
    plt.show()
    #print(data)

def test(arduino,clf):
    buffer=[]
    addr = 0x8
    print("Setting up SMBus")
    bus = SMBus(1)
    print("SMBus setup complete")
    targetLabels=[letter for letter in input("What are the target labels?\n")]
    while arduino.in_waiting>0:
        arduino.readline()
    rawread=""
    while True:
        if arduino.in_waiting>0:
            rawread=arduino.readline()
        else:
            time.sleep(0.5)
        if(len(rawread)==4):
            while len(rawread)<5:
                while arduino.in_waiting==0:
                    time.sleep(0.2)
                rawread=arduino.readline()
                while len(rawread)<3:
                    rawread+=arduino.read()
                reading=int.from_bytes(rawread[:2],"big")
                buffer.append(reading)
            if(checkSound(buffer,clf,targetLabels)):
                openDoor(buffer,bus,addr)
            while arduino.in_waiting>0:
                arduino.readline()
            buffer=[]

def recordData(arduino):
    buffer=[]
    arduino.readline()
    arduino.readline()
    fileName=input("File name?\nex)trainData\n")
    if fileName=="":
        fileName="trainData"
    f=open("data/"+fileName+".tsv",'w')
    while True:
        if arduino.in_waiting>0:
            rawread=arduino.readline()
        else:
            time.sleep(0.5)
        if(len(rawread)==4):
            print("Recording...")
            while len(rawread)<5:
                while arduino.in_waiting==0:
                    time.sleep(0.5)
                rawread=arduino.readline()
                while len(rawread)<3:
                    rawread+=arduino.read()
                reading=int.from_bytes(rawread[:2],"big")
                buffer.append(reading)
            label=input("Label in one letter\tAdd another letter to finish recording\nYou can skip by not inputting any letters\n")
            if len(label)==1:
                for i in range(len(buffer)-2):
                    f.write("{0},".format(buffer[i]))
                f.write(str(buffer[-2]))
                f.write("\t{0}\n".format(label))
            elif len(label)>1:
                f.close()
                break
            while arduino.in_waiting>0:
                arduino.readline()
            buffer=[]
   
if __name__=="__main__":
    arduino=chooseDevice()
    selection=42
    while not(selection==1 or selection ==0):
        print("0 for data recording, 1 for testing")
        selection=int(input())
    if selection == 1:
        itemsList=listdir("data/")
        for item in range(len(itemsList)):
            print("{0}: {1}".format(item, itemsList[item]))
        lP=int(input("Classifier pickle path?\n"))
        clf=Classifier(loadPath="data/"+itemsList[lP])
        test(arduino,clf)
    else:
        recordData(arduino)

