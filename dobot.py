#! /usr/bin/python3
from pydobot import Dobot
import serial.tools.list_ports
X_LIMITS = (0, 250)  
Y_LIMITS = (0, 250)  
Z_LIMITS = (-10, 150)  

def connect():
    print('connect')
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
     print(port)

    serial_port = '/dev/ttyUSB0'
    global dobot 
    dobot = Dobot(port=serial_port,verbose=True)
    print(dir(dobot))
    enable=True
    disable=False
    dobot.suck(disable)
    
    # Go HOME
    dobot.move_to(200, -20, 30, 0)
    return dobot, enable, disable

def is_within_limits(x, y, z):
    """ตรวจสอบว่าพิกัด (x, y, z) อยู่ภายในขอบเขตที่กำหนดหรือไม่"""
    return X_LIMITS[0] <= x <= X_LIMITS[1] and Y_LIMITS[0] <= y <= Y_LIMITS[1] and Z_LIMITS[0] <= z <= Z_LIMITS[1]
    
def GoLeft():
    (x, y, z, r, j1, j2, j3, j4) = dobot.pose()
    y+=20
    if is_within_limits(x, y, z):
        dobot.move_to(x, y, z, r)
        dobot.wait(1000)
        print("Right")
    else:
        dobot.move_to(200, -20, 30, 0)
        
    
def GoRight():
    (x, y, z, r, j1, j2, j3, j4) = dobot.pose()
    y-=20
    if is_within_limits(x, y, z):
        dobot.move_to(x, y, z, r)
        dobot.wait(1000)
        print("Right")
    else:
        dobot.move_to(200, -20, 30, 0)

def GoUp():
    (x, y, z, r, j1, j2, j3, j4) = dobot.pose()
    z+=20
    if is_within_limits(x, y, z):
        dobot.move_to(x, y, z, r)
        dobot.wait(1000)
        print("Up")
    else:
        dobot.move_to(200, -20, 30, 0)
    
def GoDown():
    (x, y, z, r, j1, j2, j3, j4) = dobot.pose()
    z-=20
    if is_within_limits(x, y, z):
        dobot.move_to(x, y, z, r)
        dobot.wait(1000)
        print("Down")
    else:
        dobot.move_to(200, -20, 30, 0)

if __name__ == '__main__':
    # Connect Dobot
    dobot, enable, disable = connect()
    (x, y, z, r, j1, j2, j3, j4) = dobot.pose()
    print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
    try:
        while True:
            try:
                move = int(input(f"""1. Home\n2. Left \n3. Right \n4. Up \n5. Down \nEnter Command: """))
                match move:
                    case 1:
                        dobot.move_to(200, -20, 30, 0)
                    case 2:
                        GoLeft()
                    case 3:
                        GoRight()
                    case 4:
                        GoUp()
                    case 5:
                        GoDown()
                    case _:
                        print('nah')
            except ValueError as excp:
                print(f"Value Error {excp}")
    except KeyboardInterrupt as excp:
        print(f"User Exit {excp}")
