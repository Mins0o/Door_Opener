# Door_Opener
Sound recognition actuator using Arduino and Raspberry Pi

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
