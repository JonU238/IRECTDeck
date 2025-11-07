from sx1262 import SX1262
import struct
import adafruit_sdcard
import storage
import board
import busio
import digitalio
import adafruit_gps
import time
import TDInput
import LoraCalc

class fakeGPS:
    timestamp_utc = 0
    latitude = 0.0
    longitude = 0.0
    has_fix = True
    def update(self):
         return True
    


mode = int(TDInput.TDInput("GS-N = 0, FS-N = 1, Individule TX = 2"))
useGPS = bool(int(TDInput.TDInput("Use GPS? (0/1)")))

def _format_datetime(datetime):
    date_part = f"{datetime.tm_mon:02}/{datetime.tm_mday:02}/{datetime.tm_year}"
    time_part = f"{datetime.tm_hour:02}:{datetime.tm_min:02}:{datetime.tm_sec:02}"
    return f"{date_part} {time_part}"

if useGPS:
    uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=30)
    gps = adafruit_gps.GPS(uart, debug=False)
    print("GPS INITed")
else:
     gps = fakeGPS()

sdcard = adafruit_sdcard.SDCard(board.SPI(),digitalio.DigitalInOut(board.SDCARD_CS))
vfs = storage.VfsFat(sdcard)
storage.mount(vfs,"/sd")
print("Storage INITED")


if useGPS:
    has_Time = False
    while not has_Time:
        gps.update()
        if gps.has_fix:
            StartTimeReal = gps.timestamp_utc
            StartTime = time.monotonic()
            has_Time = True
    print("Time Aquired")
else:
     StartTimeReal = 0
     StartTime = time.monotonic()


with open("/sd/test.txt", "a") as f:
    if(useGPS):
        f.write("Test begining, Mode:"+str(mode)+" @"+_format_datetime(StartTimeReal)+" UTC, CPU TIME:"+str(time.monotonic)+"\n")
    else:
        f.write("Test begining, Mode:"+str(mode)+" @"+str(StartTimeReal)+" UTC, CPU TIME:"+str(time.monotonic)+"\n")
    f.close()


sx = SX1262(board.SPI(), clk=board.SCK, mosi=board.MOSI, miso=board.MISO, cs=board.LORA_CS, irq=board.LORA_DIO1, rst=board.LORA_RST, gpio=board.LORA_BUSY)
sx.begin(freq=920.6, bw=500.0, sf=10, cr=5, syncWord=20,
    power=22, currentLimit=60.0, preambleLength=8,
    implicit=False, implicitLen=0xFF,
    crcOn=True, txIq=False, rxIq=False,
    tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

print("Radio begun")

SF = list(range(5,13))#Spreading factor
CR = list(range(5,9)) #Codingrate
BW = [62,125,250,500] #bandwidth KHZ
puff = ['','Puff is puffy and the puff puffs puffing puff puffs who even puffs dude!']

if mode == 0:
    with open("/sd/3Drangetest.txt", "a") as f:
                    f.write("Time,SF,CR,BW,Lat,Lon,Packet Length,SNR,RSSI\n")
                    f.close()
    while True:
        #negoteation
        sx.setBandwidth(62)
        sx.setSpreadingFactor(12)
        sx.setCodingRate(8)
        print("Listening for negoteation")
        packetN = sx.recv(0,True,6000)
        #Setting the test perams
        if packetN[0]:
            packetN = packetN[0]
            print(packetN)
            SF = struct.unpack('h',packetN[0:2])[0]
            #print(SF)
            CR = struct.unpack('h',packetN[2:4])[0]
            #print(CR)
            BW = struct.unpack('h',packetN[4:6])[0]
            #print(BW)
            sx.setBandwidth(BW)
            sx.setSpreadingFactor(SF)
            sx.setCodingRate(CR)
            #rxing da packet
            print("Listening for test SF,CR,BW",str(SF),str(CR),str(BW))
            packetT = sx.recv(0,True,6000)
            if packetT[0]:
                packetT=packetT[0]
                lat = struct.unpack('f',packetT[0:4])[0]
                lon = struct.unpack('f',packetT[4:8])[0]
                length = len(packetT)
                print("Packet Recived Len:",length)
                with open("/sd/3Drangetest.txt", "a") as f:
                    f.write(str(time.monotonic()-StartTime)+","+str(SF)+','+str(CR)+','+str(BW)+','+str(lat)+','+str(lon)+','+str(length)+','+str(sx.getSNR())+','+str(sx.getRSSI())+"\n")
            else:
                print("No Packet Heard")

if mode == 1:
    for i in SF:
        for j in CR:
            for k in BW:
                for l in puff:
                    print("TX-ing settings: SF,CR,BW,Long:"+str(i)+','+str(j)+','+str(k)+","+str(bool(l)))
                    sx.setBandwidth(62)
                    sx.setSpreadingFactor(12)
                    sx.setCodingRate(8)
                    sx.send(struct.pack('h',i)+struct.pack('h',j)+struct.pack('h',k))
                    time.sleep(0.5)
                    gps.update()
                    sx.setBandwidth(k)
                    sx.setSpreadingFactor(i)
                    sx.setCodingRate(j)
                    sx.send(struct.pack('f',gps.latitude)+struct.pack('f',gps.longitude)+l)
if mode == 2:
    print("Custome TX: ")
    BW = int(TDInput.TDInput("BW:"))
    SF = int(TDInput.TDInput("SF:"))
    CR = int(TDInput.TDInput("CR:"))
    PL = int(TDInput.TDInput("PacketLen(8-255): "))
    sx.setBandwidth(62)
    sx.setSpreadingFactor(12)
    sx.setCodingRate(8)
    sx.send(struct.pack('h',SF)+struct.pack('h',CR)+struct.pack('h',BW))
    time.sleep(0.1)
    gps.update()
    sx.setBandwidth(BW)
    sx.setSpreadingFactor(SF)
    sx.setCodingRate(CR)
    sx.send(struct.pack('f',gps.latitude)+struct.pack('f',gps.longitude))
