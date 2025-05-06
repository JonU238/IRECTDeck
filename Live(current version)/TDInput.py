import time
import sys
import board
import busio
import digitalio
import keypad

i2c = busio.I2C(board.SCL, board.SDA)
keyboard = 0x55
#print(dir(board))
TBUP = digitalio.DigitalInOut(board.TRACKBALL_UP)
TBDOWN = digitalio.DigitalInOut(board.TRACKBALL_DOWN)
TBCLICK = digitalio.DigitalInOut(board.TRACKBALL_CLICK)

def TDInput(prompt = "Input: "):
  print(prompt)
  userIn = ""
  while not i2c.try_lock():
    pass

  r = bytearray(1)
  while (r != b'\r'):
      i2c.readfrom_into(keyboard, r)
      if r != b'\x00' and r != b'\r':
          if r == b'\x08':
              userIn = userIn[:-2]
              print("\b ", end="\b")
          print(r.decode(), end="")
          userIn = userIn + r.decode()
      time.sleep(0.05)
  i2c.unlock()
  print("")
  return userIn

def TBTEST():
    while True:
        print("UP: ",TBUP.value, "DOWN: ", TBDOWN.value, "CLICK: ", TBCLICK.value)
        time.sleep(0.1)

def TBSelect(options = ["1","2","3"]):
    userPick = 0
    while TBCLICK.value:
        if not TBUP.value:
            print("\r\033[K", end="")
            print("UP", end="")
            userPick = userPick + 1
            print(options[userPick % len(options)], end="")
        if TBDOWN.value:
            print("\r\033[K", end="")
            print(TBDOWN.value, end="")
            userPick = userPick - 1
            print(options[userPick % len(options)], end="")
        time.sleep(0.1)
    return options[userPick%len(options)]