import serial
from os import listdir
from os.path import isfile, join

devices = [f for f in listdir(mypath) if ((f[:4]=="ttyA" or f[:4] == "ttyU")and isfile(join(mypath, f)))]

for i in range(len(devices)):
    print(i+"\n")
    print(devices[i])

print("Which device are we using?")

selection=int(readline())

arduino = serial.Serial(diveces[selection],9600)

while True:
    soundIn=arduino.readline()
    print(soundIn)
