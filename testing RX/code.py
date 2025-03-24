import time
import board
import busio
import digitalio
from sx1262 import SX1262

print(dir(board))

#Mode = "Tx"
Mode = "Rx"
spi = board.SPI()

print(spi)

time.sleep(2)

sx = SX1262(board.SPI(), clk=board.SCK, mosi=board.MOSI, miso=board.MISO, cs=board.LORA_CS, irq=board.LORA_DIO1, rst=board.LORA_RST, gpio=board.LORA_BUSY)

# LoRa
sx.begin(freq=915, bw=125.0, sf=11, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)


print("Holy shit pls yes")
time.sleep(5)

#if Mode is "Tx":
#    for i in range(10):
 #       print(sx.send(b'Hello world'))
  #      time.sleep(2)
#
 #   print("Should have sent?")
while(True):
    print("starting RX")
    print(sx.recv(0,True,5000))
    print("ending RX")