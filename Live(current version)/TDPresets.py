import board
import digitalio
import adafruit_sdcard
import storage
import os




sdcard = adafruit_sdcard.SDCard(board.SPI(),digitalio.DigitalInOut(board.SDCARD_CS))
vfs = storage.VfsFat(sdcard)
storage.mount(vfs,"/sd")
print(os.listdir("/sd"))