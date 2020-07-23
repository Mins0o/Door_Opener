import serial
from os import listdir
import matplotlib.pyplot as plt
from Classifier import Classifier
from smbus import SMBus
import time
import csv

def chooseDevice():
    """Calling this function will prompt list of files in /dev/ folder with certain prefix
        User can choose device by typing in a number.
        This function will return a serial.Serial object, initialized with the device the user chose.
        """
    devices = [f for f in listdir("/dev/") if ((f[:4]=="ttyS" or f[:4] == "ttyU"))]
    for i in range(len(devices)):
        print(i,end="\t")
        print(devices[i])
    print("Which device are we using?")
    selection=int(input())
    arduino = serial.Serial("/dev/"+devices[selection],9600)
    return arduino

def checkSound(data,clf,targetLabels):
    """This function takes in
     -a list containing information of a "sound snippet"
     -a Classifier class object
     -a list of one-letter target labels
    to understand how the arguments should be given, read the Extractor.py and Classifier.py for more information.
    This function will use the Classifier to classify the input and see if it is one of the targets.

    If the data is classified as one of the target sound, the function will return True and otherwise, it will return False.
    """
    print (clf.predict([data])[0] in targetLabels) 
    return clf.predict([data])[0] in targetLabels 

def openDoor(data,bus,addr):
    """This is the actuation part of the DoorOpener.py
    When this function is called, it will send a signal to the given SMBus(I2C).
    It also asks for data in case the user wants to modify the action. For example, plot the sound data.
    """
    bus.write_byte(addr,0x1)
    time.sleep(2)
    """
    fig=plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(data[-1000:-1])
    plt.show()
    """
    #print(data)

def test(arduino,clf):
    """This function is called in the main function.
    This function keeps searching for serial input from the Arduino of a "sound snippet".
    After receiving the full sound snippet, this function will check if it matches the target sound and actuate accordingly

    User input of the target labels should be in one string containing all the labels the user wants to set as target.
    ex) "y" or "kc"(for label 'k' and label 'c')
    """
    buffer=[]
    addr = 0x8
    bus = SMBus(1)
    # get target label input from user
    targetLabels=[letter for letter in input("What are the target labels?\nTarget labels should be in one string containing all the labels\nex) \"y\" or \"kc\"(for label 'k' and label 'c')\n>>> ")]
    # flush any pre-existing buffers
    while arduino.in_waiting>0:
        arduino.readline()
    rawread=""
    while True:
        if arduino.in_waiting>0:
            # The rawread here is the first line of the incoming data.
            rawread=arduino.readline()
        else: #Because nothing else is being executed until something comes in.
            time.sleep(0.5)
        if(len(rawread)==4): # Checking the start of the "sound snippet" formatting.
            # Until the line has length of 5(a.k.a. end of the "sound snippet" formatting)
            # Every regular lines between len4(start) and len5(end) are len3
            # This is because arduino integer is two bytes and the "\n" follows.
            while len(rawread)<5: # Checking the end of the "sound snippet" formatting.
                while arduino.in_waiting==0:
                    time.sleep(0.2)
                rawread=arduino.readline()
                while len(rawread)<3: # This loop is added to avoid situations where "0x\n" is the value of the first or second byte of the integer.
                    rawread+=arduino.read()
                reading=int.from_bytes(rawread[:2],"big")# First two bytes are the integer sent from Arduino
                buffer.append(reading)
            # After getting the last line(len5), we check with the data and actuate accordingly.
            if(checkSound(buffer,clf,targetLabels)):
                openDoor(buffer,bus,addr)
            # Flush any buffered serial while actuating
            while arduino.in_waiting>0:
                arduino.readline()
            buffer=[]

def recordData(arduino):
    """This function is called in the main function.
    The function first asks for the name of the file the recorded data will be stored. The file will be stored in a subfolder called "data/"
    After that the function continuously takes receives two inputs
     - Sound data: Input by the Arduino through serial port
     - Label : Manually typed in one-lettered label for classification
    and the zipped result is saved as a .tsv file for training or evaluating the Classifier.(Training and evaluating can be done by running Classifier.py)

    To finish recording and save the file, start a new recording but type in two or more characters as label.
    The data will be ignored and the program will terminate after saving the data.
    The data can be loaded in the Classifier.py to train(fit) the model or to evaluate it.
    
    Additional operations can be done after the "Recording..." ends and "Label in one......" is prompted.
     -Not typing in any letter and typing return(enter) will ignored the recorded data.
     -Typing in two or more letters for the label will exit the recording session and save the file.
    """
    buffer=[]
    fileName=input("File name?\nex)trainData\n>>> ")
    if fileName=="":
        fileName="trainData"
    f=open("data/"+fileName+".tsv",'w')
    while arduino.in_waiting>0: # From this part vvvvvvvvvvvvv
        arduino.readline()
    rawread=""
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
                buffer.append(reading) # To this part ^^^^^^^^^ is same as the "test() function"
            label=input("Label in one letter\nAdd another letter to finish recording\nYou can skip by not inputting any letters\n>>> ")
            if len(label)==1:
                for i in range(len(buffer)-2): # It stops at len()-2 to get rid of the last integer (0) and a comma,
                    f.write("{0},".format(buffer[i]))
                f.write(str(buffer[-2])) # Writing the integer without a comma at the end.
                f.write("\t{0}\n".format(label))
            elif len(label)>1:
                f.close()
                break
            while arduino.in_waiting>0:
                arduino.readline()
            buffer=[]
   
if __name__=="__main__":
    """1. User chooses action (record or test)
    2. If record:
        2-1. Name the file.
        2-2. Trigger arduino to send data.
        2-3. Assign label | Ignore recording | Finish Recording
    3. If test:
        3-1. Choose the trained Classifier(as .pkl file).
        3-2. Provide targeted label.
        3-3. Wait for arduino to get triggered on microphone.
        3-4. If the sound was a target sound, this program will send actuation signal to arduino.
    """
    arduino=chooseDevice()
    selection=42
    while not(selection==1 or selection ==0):
        print("0 for data recording, 1 for testing")
        selection=int(input())
    if selection == 1:# if testing,
        # prompt list of trained Classifier(saved as .pkl file)
        itemsList=[f for f in listdir("data/") if f[-4:]==".pkl"]
        for item in range(len(itemsList)):
            print("{0}: {1}".format(item, itemsList[item]))
        lP=int(input("Classifier pickle path?\n"))
        clf=Classifier(loadPath="data/"+itemsList[lP])
        test(arduino,clf)
    else:
        recordData(arduino)

