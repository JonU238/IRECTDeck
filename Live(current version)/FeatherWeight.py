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

FWSettings = {"SF":10, "BW":500, "CR":5, "SyncWord":20, "PreambleLength":8, "Power":5}

sx = SX1262(board.SPI(), clk=board.SCK, mosi=board.MOSI, miso=board.MISO, cs=board.LORA_CS, irq=board.LORA_DIO1, rst=board.LORA_RST, gpio=board.LORA_BUSY)
sx.begin(freq=920.6, bw=500.0, sf=10, cr=5, syncWord=20,
    power=5, currentLimit=60.0, preambleLength=8,
    implicit=False, implicitLen=0xFF,
    crcOn=True, txIq=False, rxIq=False,
    tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

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
