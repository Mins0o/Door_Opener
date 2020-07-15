import serial
from os import listdir
from os.path import isfile, join

devices = [f for f in listdir("/dev/") if ((f[:4]=="ttyA" or f[:4] == "ttyU"))]

for i in range(len(devices)):
    print(i,end="\t")
    print(devices[i])

print("Which device are we using?")

selection=int(input())

arduino = serial.Serial("/dev/"+devices[selection],9600)

while True:
    soundIn=ord(arduino.read())
    print(soundIn)
