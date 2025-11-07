import adafruit_gps
import time
import adafruit_sdcard
import board
import busio

uart = busio.UART(board.TX, board.RX, baudrate=38400, timeout=30)
gps = adafruit_gps.GPS(uart, debug=False)
print("GPS INITed")

while True:
    gps.update()
    print("Lat:",gps.latitude,"Lon:",gps.longitude)
    time.sleep(1)