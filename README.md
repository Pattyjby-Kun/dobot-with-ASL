# Dobot Hand Control
## Detail Project
  project dobot control on respberry pi 
  implement hand tracking to control dobot movement  
## About File
 ```
  dobot.py         | dobot control command
  track.py         | hand tracking mapping sign
  requirement.txt  | packing require library file
 ```
## How to use
 ``` 
  control dobot support only linux and mac os
  1. create python virtual environment 
    : python3 -m venv vnev
  2. activate virtual environment
    : source venv/bin/activate
  3. install library from requirement.txt
    : pip3 install -r requirement.txt
  4. check connected ports and replace port name at 
    : line 14 serial_port = 'replace ports'
      example serial_port = '/dev/ttyUSB0'
  5. test run this control program doboy.py
     and test control dobot movement.
    ** if program has work?
  6. use program track.py for hand control
 ```
## Problem
  hand tracking has many request movement 
  make dobot crash