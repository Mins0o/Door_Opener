import serial
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import asyncio
import time

fig=plt.figure()
ax = fig.add_subplot(1,1,1)
buffer=[]

def chooseDevice():
    devices = [f for f in listdir("/dev/") if ((f[:4]=="ttyA" or f[:4] == "ttyU"))]
    for i in range(len(devices)):
        print(i,end="\t")
        print(devices[i])
    print("Which device are we using?")
    selection=int(input())
    arduino = serial.Serial("/dev/"+devices[selection],9600)
    return arduino

def addData(i):
    
    while arduino.in_waiting>0:
        rawread=arduino.readline()
        
        while(len(rawread)<3):
            rawread+=arduino.read()
        reading=int.from_bytes(rawread[:2],"big")
        buffer.append(reading)
    ax.clear()
    ax.plot(buffer[-1000:])

def checkSound(data):
    return len(data)>0

def openDoor(data):
    ax.clear()
    ax.plot(data[-1000:-1])
    plt.show()
    print(data)
    
if __name__=="__main__":
    arduino=chooseDevice()
    arduino.readline()
    arduino.readline()
    while True:
        buffer=[]
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
        if(checkSound(buffer)):
            openDoor(buffer)
    #ani=animation.FuncAnimation(fig,addData,fargs=(),interval=5)
    #plt.show()
            
    """
    while True:
        buffer=buffer[-20:]
        while arduino.in_waiting>0:
            rawread=arduino.readline()
            while(len(rawread)<3):
                rawread+=arduino.read()
            reading=int.from_bytes(rawread[:2],"big")
            print(reading)
            buffer.append(reading)
        if(len(buffer)>0):
            print(buffer)"""
        
        
"""
            buffer+=arduino.readline()
            #plot(buffer)
        buffer=[]
        time.sleep(1)
"""
"""
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# Initialize communication with TMP102
tmp102.init()

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    temp_c = round(tmp102.read_temp(), 2)

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(temp_c)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()"""
