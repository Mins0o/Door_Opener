import serial
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import time
import csv


def chooseDevice():
    devices = [f for f in listdir("/dev/") if ((f[:4]=="ttyA" or f[:4] == "ttyU"))]
    for i in range(len(devices)):
        print(i,end="\t")
        print(devices[i])
    print("Which device are we using?")
    selection=int(input())
    arduino = serial.Serial("/dev/"+devices[selection],9600)
    return arduino

def checkSound(data,clf):
    return len(data)>0

def openDoor(data):
    fig=plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(data[-1000:-1])
    plt.show()
    #print(data)

def test(arduino,clf):
    buffer=[]
    arduino.readline()
    arduino.readline()
    while True:
        if arduino.in_waiting>0:
            rawread=arduino.readline()
        else:
            time.sleep(0.5)
        if(len(rawread)==4):
            while len(rawread)<5:
                while arduino.in_waiting==0:
                    time.sleep(0.5)
                rawread=arduino.readline()
                while len(rawread)<3:
                    rawread+=arduino.read()
                reading=int.from_bytes(rawread[:2],"big")
                buffer.append(reading)
            if(checkSound(buffer,clf)):
                openDoor(buffer)
            buffer=[]

def recordData(arduino):
    buffer=[]
    arduino.readline()
    arduino.readline()
    fileName=input("File name?")
    if fileName=="":
        fileName="trainData.tsv"
    f=open("./"+fileName,'w')
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
            print("Is this the target sound?")
            label=input()
            if label.lower()=="n" or label.lower()=="y":
                for i in range(len(buffer)-2):
                    f.write("{0},".format(buffer[i]))
                f.write(str(buffer[-2]))
                f.write("\t{0}\n".format(label))
            print("Stop recording?")
            hault=input()
            if not(hault=="" or hault=="n"):
                f.close()
                break
            buffer=[]
   
if __name__=="__main__":
    arduino=chooseDevice()
    selection=42
    clf=[]#Classifier(loadPath="")
    while not(selection==1 or selection ==0):
        print("0 for data recording, 1 for testing")
        selection=int(input())
    if selection == 1:
        test(arduino,clf)
    else:
        recordData(arduino)

