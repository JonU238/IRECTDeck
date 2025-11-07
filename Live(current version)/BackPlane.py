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
import binascii


LoraSettings = {"SF":12, "BW":125, "CR":8, "SyncWord":0x14, "PreambleLength":8, "Power":5}


sx = SX1262(board.SPI(), clk=board.SCK, mosi=board.MOSI, miso=board.MISO, cs=board.LORA_CS, irq=board.LORA_DIO1, rst=board.LORA_RST, gpio=board.LORA_BUSY)
sx.begin(freq=906.9, bw=125.0, sf=12, cr=8, syncWord=0x14,
    power=5, currentLimit=60.0, preambleLength=8,
    implicit=False, implicitLen=0xFF,
    crcOn=True, txIq=False, rxIq=False,
    tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)


def msg2port(msg):
    if len(msg) >= 2:
        return msg[0] | msg[1]<<8
    else:
        return None

portmapping = {
    12005: ('Radio', 'fffhBB'), # lat, long, alt, sat cnt, fix status, fix quality
    11020: ("Power", 'hhhhhh'), # mV,
    13020: ("Sensor", 'hhhhhhhh'), # press, temp, ax, ay, az (mm/s^2), gx, gy, gz (milliradians/s)
}

while True:
    try:
        msg = sx.recv(0,True,5000)
        msg = msg[0]
        if msg is None:
            continue

        if len(msg) == 0:
            print("No MSG")
            continue

        port = msg2port(msg)
        if port is None:
            print("short msg", binascii.hexlify(msg).decode())
            continue

        if not port in portmapping:
            print("Data: ", binascii.hexlify(msg).decode())
            continue

        port_name, s = portmapping[port]
        print("Port", port, port_name)

        rest = msg[2:]
        if struct.calcsize(s) != len(rest):
            print("Wrong Fmt: ", binascii.hexlify(msg).decode())

        t = struct.unpack(s, rest)
        print(t)
    except Exception as e:
        print("error", e)
