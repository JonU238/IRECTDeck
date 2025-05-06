import time
import sys
import board
import busio
import digitalio
import struct
from sx1262 import SX1262
import TDInput
import adafruit_sdcard
import adafruit_gps
import storage
import os

#Mode = "Tx"
#Mode = "Rx"
spi = board.SPI()
FWSettings = {"SF":10, "BW":500, "CR":5, "SyncWord":20, "PreambleLength":8, "Power":5}
TestSettings = {"SF":10, "BW":500, "CR":5, "SyncWord":20, "PreambleLength":8, "Power":5}




def SetLoraSettings():
  freq = TDInput.TDInput("Frequency(850-930):")
  bw = TDInput.TDInput("Bandwidth(7,10,15,20,31,41,62,125,250,500):")
  sf = TDInput.TDInput("Spreading Factor(6-12):")
  cr = TDInput.TDInput("Coding Rate(5-8):")
  syncWord = TDInput.TDInput("Sync Word(0xXX):")
  power = TDInput.TDInput("Power(0-20):")
  preambleLength = TDInput.TDInput("Preamble Length(int):")

#Main setting of what the device is doing

Mode = TDInput.TDInput("Input mode (0=Tx, 1=Rx, 2=RxScan, 3=Feather weight):")
if Mode =="0":
   Mode = "Tx"
if Mode == "1":
    Mode = "Rx"
if Mode == "2":
    Mode = "RxScan"
if Mode == "3":
    Mode = "FeatherWeight"
if Mode == "4":
  Mode = "RangeTest3D"
    

if Mode=="Tx" or Mode == "Rx" or Mode == "RxScan" or Mode == "FeatherWeight" or Mode == "RangeTest3D":
  sx = SX1262(board.SPI(), clk=board.SCK, mosi=board.MOSI, miso=board.MISO, cs=board.LORA_CS, irq=board.LORA_DIO1, rst=board.LORA_RST, gpio=board.LORA_BUSY)
  sx.begin(freq=920.6, bw=500.0, sf=10, cr=5, syncWord=20,
        power=5, currentLimit=60.0, preambleLength=8,
        implicit=False, implicitLen=0xFF,
        crcOn=True, txIq=False, rxIq=False,
        tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

if Mode is "Tx":
    for i in range(10):
        print(sx.send(b'Hello World!'))
        time.sleep(2)


if Mode is "RxScan":
  for i in range(1):
    for i in range(5,9):
      sx.setCodingRate(i)
      for k in range(0x00, 0x100):
        sx.setSyncWord(k)
        print("starting RX. CR: "+str(i)+" SyncWord: " + str(k))
        msg = sx.recv(0,True,2000)
        print(msg)
        print("ending RX")

if Mode is "Rx":
  while True:
    msg = sx.recv(0,True,2000)
    print(list(msg[0]))

if Mode is "FeatherWeight":
  sx.setFrequency(float(TDInput.TDInput("Frequency(850-930):")))
  sx.setBandwidth(FWSettings["BW"])
  sx.setSpreadingFactor(FWSettings["SF"])
  sx.setCodingRate(FWSettings["CR"])
  sx.setSyncWord(FWSettings["SyncWord"])
  sx.setPreambleLength(FWSettings["PreambleLength"])
  sx.setOutputPower(FWSettings["Power"])
  while True:
    msg = sx.recv(0,True,2000)
    msg = msg[0]
    print("*")
    try:
      if msg:
        lat = struct.unpack("i", msg[13:13+4])[0]
        lon = struct.unpack("i", msg[17:17+4])[0]
        alt = struct.unpack("i", msg[21:21+4])[0]
        lat = lat*0.0000001
        lon = lon*0.0000001
        alt = alt*0.001
        print("Lat: ",lat,"deg")
        print("Lon: ",lon,"deg")
        print("Alt: ",alt,"m")
    except:
      print("Decode error")

      
if Mode is "RangeTest3D":
    uart = busio.UART(board.TX, board.RX, baudrate=38400, timeout=30)
    gps = adafruit_gps.GPS(uart, debug=False)
    sdcard = adafruit_sdcard.SDCard(board.SPI(),digitalio.DigitalInOut(board.SDCARD_CS))
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs,"/sd")

    while(True):
      print("Entered the while loop")
      time.sleep(3)
      logfile = open("/sd/LogFile.txt",'w')
      gps.update()
      print("updated")
      print(gps.timestamp_utc.tm_hour,gps.timestamp_utc.tm_min,gps.timestamp_utc.tm_sec,gps.latitude,gps.longitude)
      #print(sx.getRSSIInstant())
      logfile.write(gps.timestamp_utc.tm_hour,gps.timestamp_utc.tm_min,gps.timestamp_utc.tm_sec,gps.latitude,gps.longitude)
      logfile.close()