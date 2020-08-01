# Door_Opener
Sound recognition actuator using Arduino and Raspberry Pi.  
This project is a rough prototype and is not intended to follow along.
If you wish to make a similar system and need more details of the project, please contact me: stengine2@gmail.com .

# Motivation
I have a dog in the house and I love having him with me when I go to bed. However, deeper into the night, he wakes me up by skretching the door and whimpering in order to get out of the bedroom.  
I wanted to solve this problem by making a device that will automatically open the door if it detects skretching and/or whimpering.

# Features
- The system is attached to a door and listens to the sound wave around the lower part of the door.
- There are two modes of operation:
  - Recording Mode : User can record sounds and create labeled sound data to train a classifier.
  - Test Mode(Use Mode): The system will listened to sound and open the door according to the sound classification result.
  - There can be multiple labels and user can choose target labels in Test Mode.(eg: setting target labels to whimpering and skretching)
- User can train the classifier and evaluate it.

# System
The system is consisted 2 parts, the processing and IO control, and they can be broken into smaller subsystems.
  ## Processing(Raspberry Pi)
  - Data recording: (DoorOpener.py)
    - This mode can be selected in the interface.
    - 2 recurring inputs: Analog read data from the arduino, user input label (+data file name + serial port selection _ *for once* _)
    - output: A tsv file containing the data and the label
    - In this mode, the program waits for serial input from the arduino and if it receives any valid data(that is, has marked start and end), it asks the user for one-lettered label. After recording datas, when the user exits the program properly, the data will be saved as a .tsv file in the ./data directory.
  - Data fitting: (Classifier.py)
    - input: .tsv data, file name for saving classifier
    - output: .pkl of the trained classifier. This file is used in the Test Mode
  - Actual usage(Test Mode):
    - 

This is an experimental project of mine, intended to learn more about Arduino and Raspberry Pi
In this project, I have learned:
- Basic Linux : directories, devices, configurations etc.
- Git in Linux
- arduino-cli in Linux
- Serial communication : UART and using Tx/Rx pins or USB on both boards
- I2C communication protocol : 
  - The idea of using two wires for multiple devices. 
  - Python SMBus library.
  - Compatibility of I2C between two boards.
- ISR(Interrupt Service Routine) : 
  - Stepper motor cannot work in ISR...Valuable lesson.
  - Using volatile variable to manage states by interrupt.
  - Event handling in Arduino
- Sound Recognition : I am already a bit familiar with the ML concept.
  - Gaussian Process Classification
  - Iris data
  - Extracting Features of sound wave signals
- Stepper motor

Detailed documentation in work...
(Meanwhile, you can read the comments in the code. I tried to provide all of the knowledge how this project operates.)
