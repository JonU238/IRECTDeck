import time
import sys
import board
import busio
import digitalio
import struct
from sx1262 import SX1262
import TDInput


sx = SX1262(board.SPI(), clk=board.SCK, mosi=board.MOSI, miso=board.MISO, cs=board.LORA_CS, irq=board.LORA_DIO1, rst=board.LORA_RST, gpio=board.LORA_BUSY)
sx.begin(freq=920.6, bw=500.0, sf=10, cr=5, syncWord=20,
    power=5, currentLimit=60.0, preambleLength=8,
    implicit=False, implicitLen=0xFF,
    crcOn=True, txIq=False, rxIq=False,
    tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

def BasicTX():
    while(True):
        sx.send(TDInput.TDInput("To send in ascii"))
