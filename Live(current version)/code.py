import gc
print(gc.mem_free())
import TDInput
print(gc.mem_free())

#Main setting of what the device is doing

Mode = TDInput.TDInput("Input mode (0=Tx, 1=Rx, 2=RxScan, 3=Feather weight, 4=3D Range Test, 5=DisentanglementTest), 6=RangeTest, 7=JustGPS:")
if Mode =="0":
   Mode = "Tx"
if Mode == "1":
    Mode = "Rx"
if Mode == "2":
    Mode = "RxScan"
if Mode == "3":
    import FeatherWeight
    FeatherWeight.GPS_Decode()
if Mode == "4":
  Mode = "RangeTest3D"
if Mode == "5":
  Mode = "BackPlane"
  import BackPlane
if Mode == "6":
   import RangeTest
if Mode == "7":
   import justGPS
   

'''
if Mode is "Rx":
  while True:
    msg = sx.recv(0,True,2000)
    print(list(msg[0]))

if Mode is "Tx":
    import TDTX
    TDTX.BasicTX()


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


'''
